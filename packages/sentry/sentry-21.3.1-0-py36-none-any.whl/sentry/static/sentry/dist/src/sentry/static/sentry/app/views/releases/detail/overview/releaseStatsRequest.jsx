import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import meanBy from 'lodash/meanBy';
import omitBy from 'lodash/omitBy';
import pick from 'lodash/pick';
import { fetchTotalCount } from 'app/actionCreators/events';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t, tct } from 'app/locale';
import { defined } from 'app/utils';
import { getExactDuration } from 'app/utils/formatters';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { displayCrashFreePercent, roundDuration } from '../../utils';
import { YAxis } from './chart/releaseChartControls';
import { fillChartDataFromSessionsResponse, fillCrashFreeChartDataFromSessionsReponse, getInterval, getReleaseEventView, getTotalsFromSessionsResponse, initCrashFreeChartData, initOtherCrashFreeChartData, initOtherSessionDurationChartData, initOtherSessionsBreakdownChartData, initSessionDurationChartData, initSessionsBreakdownChartData, } from './chart/utils';
var omitIgnoredProps = function (props) {
    return omitBy(props, function (_, key) {
        return ['api', 'version', 'orgId', 'projectSlug', 'location', 'children'].includes(key);
    });
};
var ReleaseStatsRequest = /** @class */ (function (_super) {
    __extends(ReleaseStatsRequest, _super);
    function ReleaseStatsRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            reloading: false,
            errored: false,
            data: null,
        };
        _this.unmounting = false;
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var data, _a, yAxis, hasHealthData, hasDiscover, hasPerformance, error_1;
            var _b, _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        data = null;
                        _a = this.props, yAxis = _a.yAxis, hasHealthData = _a.hasHealthData, hasDiscover = _a.hasDiscover, hasPerformance = _a.hasPerformance;
                        if (!hasHealthData && !hasDiscover && !hasPerformance) {
                            return [2 /*return*/];
                        }
                        this.setState(function (state) { return ({
                            reloading: state.data !== null,
                            errored: false,
                        }); });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 12, , 13]);
                        if (!(yAxis === YAxis.SESSIONS)) return [3 /*break*/, 3];
                        return [4 /*yield*/, this.fetchSessions()];
                    case 2:
                        data = _d.sent();
                        _d.label = 3;
                    case 3:
                        if (!(yAxis === YAxis.USERS)) return [3 /*break*/, 5];
                        return [4 /*yield*/, this.fetchUsers()];
                    case 4:
                        data = _d.sent();
                        _d.label = 5;
                    case 5:
                        if (!(yAxis === YAxis.CRASH_FREE)) return [3 /*break*/, 7];
                        return [4 /*yield*/, this.fetchCrashFree()];
                    case 6:
                        data = _d.sent();
                        _d.label = 7;
                    case 7:
                        if (!(yAxis === YAxis.SESSION_DURATION)) return [3 /*break*/, 9];
                        return [4 /*yield*/, this.fetchSessionDuration()];
                    case 8:
                        data = _d.sent();
                        _d.label = 9;
                    case 9:
                        if (!(yAxis === YAxis.EVENTS ||
                            yAxis === YAxis.FAILED_TRANSACTIONS ||
                            yAxis === YAxis.COUNT_DURATION ||
                            yAxis === YAxis.COUNT_VITAL)) return [3 /*break*/, 11];
                        return [4 /*yield*/, this.fetchEventData()];
                    case 10:
                        // this is used to get total counts for chart footer summary
                        data = _d.sent();
                        _d.label = 11;
                    case 11: return [3 /*break*/, 13];
                    case 12:
                        error_1 = _d.sent();
                        addErrorMessage((_c = (_b = error_1.responseJSON) === null || _b === void 0 ? void 0 : _b.detail) !== null && _c !== void 0 ? _c : t('Error loading chart data'));
                        this.setState({
                            errored: true,
                            data: null,
                        });
                        return [3 /*break*/, 13];
                    case 13:
                        if (!defined(data) && !this.state.errored) {
                            // this should not happen
                            this.setState({
                                errored: true,
                                data: null,
                            });
                        }
                        if (this.unmounting) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            reloading: false,
                            data: data,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ReleaseStatsRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ReleaseStatsRequest.prototype.componentDidUpdate = function (prevProps) {
        if (isEqual(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    };
    ReleaseStatsRequest.prototype.componentWillUnmount = function () {
        this.unmounting = true;
    };
    Object.defineProperty(ReleaseStatsRequest.prototype, "path", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/sessions/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ReleaseStatsRequest.prototype, "baseQueryParams", {
        get: function () {
            var _a = this.props, version = _a.version, location = _a.location, selection = _a.selection, defaultStatsPeriod = _a.defaultStatsPeriod;
            return __assign({ query: stringifyQueryObject(new QueryResults(["release:\"" + version + "\""])), interval: getInterval(selection.datetime) }, getParams(pick(location.query, Object.values(URL_PARAM)), {
                defaultStatsPeriod: defaultStatsPeriod,
            }));
        },
        enumerable: false,
        configurable: true
    });
    ReleaseStatsRequest.prototype.fetchSessions = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, version, _b, releaseResponse, otherReleasesResponse, totalSessions, chartData, otherChartData;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.path, {
                                    query: __assign(__assign({}, this.baseQueryParams), { field: 'sum(session)', groupBy: 'session.status' }),
                                }),
                                api.requestPromise(this.path, {
                                    query: __assign(__assign({}, this.baseQueryParams), { field: 'sum(session)', groupBy: 'session.status', query: stringifyQueryObject(new QueryResults(["!release:\"" + version + "\""])) }),
                                }),
                            ])];
                    case 1:
                        _b = __read.apply(void 0, [_c.sent(), 2]), releaseResponse = _b[0], otherReleasesResponse = _b[1];
                        totalSessions = getTotalsFromSessionsResponse({
                            response: releaseResponse,
                            field: 'sum(session)',
                        });
                        chartData = fillChartDataFromSessionsResponse({
                            response: releaseResponse,
                            field: 'sum(session)',
                            groupBy: 'session.status',
                            chartData: initSessionsBreakdownChartData(),
                        });
                        otherChartData = fillChartDataFromSessionsResponse({
                            response: otherReleasesResponse,
                            field: 'sum(session)',
                            groupBy: 'session.status',
                            chartData: initOtherSessionsBreakdownChartData(),
                        });
                        return [2 /*return*/, {
                                chartData: __spreadArray(__spreadArray([], __read(Object.values(chartData))), __read(Object.values(otherChartData))),
                                chartSummary: totalSessions.toLocaleString(),
                            }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.fetchUsers = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, version, _b, releaseResponse, otherReleasesResponse, totalUsers, chartData, otherChartData;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.path, {
                                    query: __assign(__assign({}, this.baseQueryParams), { field: 'count_unique(user)', groupBy: 'session.status' }),
                                }),
                                api.requestPromise(this.path, {
                                    query: __assign(__assign({}, this.baseQueryParams), { field: 'count_unique(user)', groupBy: 'session.status', query: stringifyQueryObject(new QueryResults(["!release:\"" + version + "\""])) }),
                                }),
                            ])];
                    case 1:
                        _b = __read.apply(void 0, [_c.sent(), 2]), releaseResponse = _b[0], otherReleasesResponse = _b[1];
                        totalUsers = getTotalsFromSessionsResponse({
                            response: releaseResponse,
                            field: 'count_unique(user)',
                        });
                        chartData = fillChartDataFromSessionsResponse({
                            response: releaseResponse,
                            field: 'count_unique(user)',
                            groupBy: 'session.status',
                            chartData: initSessionsBreakdownChartData(),
                        });
                        otherChartData = fillChartDataFromSessionsResponse({
                            response: otherReleasesResponse,
                            field: 'count_unique(user)',
                            groupBy: 'session.status',
                            chartData: initOtherSessionsBreakdownChartData(),
                        });
                        return [2 /*return*/, {
                                chartData: __spreadArray(__spreadArray([], __read(Object.values(chartData))), __read(Object.values(otherChartData))),
                                chartSummary: totalUsers.toLocaleString(),
                            }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.fetchCrashFree = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, version, _b, releaseResponse, otherReleasesResponse, chartData, otherChartData, summary;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.path, {
                                    query: __assign(__assign({}, this.baseQueryParams), { field: ['sum(session)', 'count_unique(user)'], groupBy: 'session.status' }),
                                }),
                                api.requestPromise(this.path, {
                                    query: __assign(__assign({}, this.baseQueryParams), { field: ['sum(session)', 'count_unique(user)'], groupBy: 'session.status', query: stringifyQueryObject(new QueryResults(["!release:\"" + version + "\""])) }),
                                }),
                            ])];
                    case 1:
                        _b = __read.apply(void 0, [_c.sent(), 2]), releaseResponse = _b[0], otherReleasesResponse = _b[1];
                        chartData = fillCrashFreeChartDataFromSessionsReponse({
                            response: releaseResponse,
                            field: 'sum(session)',
                            entity: 'sessions',
                            chartData: initCrashFreeChartData(),
                        });
                        chartData = fillCrashFreeChartDataFromSessionsReponse({
                            response: releaseResponse,
                            field: 'count_unique(user)',
                            entity: 'users',
                            chartData: chartData,
                        });
                        otherChartData = fillCrashFreeChartDataFromSessionsReponse({
                            response: otherReleasesResponse,
                            field: 'sum(session)',
                            entity: 'sessions',
                            chartData: initOtherCrashFreeChartData(),
                        });
                        otherChartData = fillCrashFreeChartDataFromSessionsReponse({
                            response: otherReleasesResponse,
                            field: 'count_unique(user)',
                            entity: 'users',
                            chartData: otherChartData,
                        });
                        summary = tct('[usersPercent] users, [sessionsPercent] sessions', {
                            usersPercent: displayCrashFreePercent(meanBy(chartData.users.data.filter(function (item) { return defined(item.value); }), 'value')),
                            sessionsPercent: displayCrashFreePercent(meanBy(chartData.sessions.data.filter(function (item) { return defined(item.value); }), 'value')),
                        });
                        return [2 /*return*/, {
                                chartData: __spreadArray(__spreadArray([], __read(Object.values(chartData))), __read(Object.values(otherChartData))),
                                chartSummary: summary,
                            }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.fetchSessionDuration = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, version, _b, releaseResponse, otherReleasesResponse, totalMedianDuration, chartData, otherChartData;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, version = _a.version;
                        return [4 /*yield*/, Promise.all([
                                api.requestPromise(this.path, {
                                    query: __assign(__assign({}, this.baseQueryParams), { field: 'p50(session.duration)' }),
                                }),
                                api.requestPromise(this.path, {
                                    query: __assign(__assign({}, this.baseQueryParams), { field: 'p50(session.duration)', query: stringifyQueryObject(new QueryResults(["!release:\"" + version + "\""])) }),
                                }),
                            ])];
                    case 1:
                        _b = __read.apply(void 0, [_c.sent(), 2]), releaseResponse = _b[0], otherReleasesResponse = _b[1];
                        totalMedianDuration = getTotalsFromSessionsResponse({
                            response: releaseResponse,
                            field: 'p50(session.duration)',
                        });
                        chartData = fillChartDataFromSessionsResponse({
                            response: releaseResponse,
                            field: 'p50(session.duration)',
                            groupBy: null,
                            chartData: initSessionDurationChartData(),
                            valueFormatter: function (duration) { return roundDuration(duration ? duration / 1000 : 0); },
                        });
                        otherChartData = fillChartDataFromSessionsResponse({
                            response: otherReleasesResponse,
                            field: 'p50(session.duration)',
                            groupBy: null,
                            chartData: initOtherSessionDurationChartData(),
                            valueFormatter: function (duration) { return roundDuration(duration ? duration / 1000 : 0); },
                        });
                        return [2 /*return*/, {
                                chartData: __spreadArray(__spreadArray([], __read(Object.values(chartData))), __read(Object.values(otherChartData))),
                                chartSummary: getExactDuration(roundDuration(totalMedianDuration ? totalMedianDuration / 1000 : 0)),
                            }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.fetchEventData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, location, yAxis, eventType, vitalType, selection, version, eventView, payload, eventsCountResponse, chartSummary;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, location = _a.location, yAxis = _a.yAxis, eventType = _a.eventType, vitalType = _a.vitalType, selection = _a.selection, version = _a.version;
                        eventView = getReleaseEventView(selection, version, yAxis, eventType, vitalType, organization, true);
                        payload = eventView.getEventsAPIPayload(location);
                        return [4 /*yield*/, fetchTotalCount(api, organization.slug, payload)];
                    case 1:
                        eventsCountResponse = _b.sent();
                        chartSummary = eventsCountResponse.toLocaleString();
                        return [2 /*return*/, { chartData: [], chartSummary: chartSummary }];
                }
            });
        });
    };
    ReleaseStatsRequest.prototype.render = function () {
        var _a, _b;
        var children = this.props.children;
        var _c = this.state, data = _c.data, reloading = _c.reloading, errored = _c.errored;
        var loading = data === null;
        return children({
            loading: loading,
            reloading: reloading,
            errored: errored,
            chartData: (_a = data === null || data === void 0 ? void 0 : data.chartData) !== null && _a !== void 0 ? _a : [],
            chartSummary: (_b = data === null || data === void 0 ? void 0 : data.chartSummary) !== null && _b !== void 0 ? _b : '',
        });
    };
    return ReleaseStatsRequest;
}(React.Component));
export default ReleaseStatsRequest;
//# sourceMappingURL=releaseStatsRequest.jsx.map
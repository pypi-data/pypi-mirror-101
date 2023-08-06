import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import React from 'react';
import isEqual from 'lodash/isEqual';
import omit from 'lodash/omit';
import pick from 'lodash/pick';
import moment from 'moment';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { getDiffInMinutes, ONE_WEEK, TWENTY_FOUR_HOURS, TWO_WEEKS, } from 'app/components/charts/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t } from 'app/locale';
import { HealthStatsPeriodOption, } from 'app/types';
import { defined, percent } from 'app/utils';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import withApi from 'app/utils/withApi';
import { DisplayOption } from '../list/utils';
import { getCrashFreePercent } from '.';
function omitIgnoredProps(props) {
    return omit(props, [
        'api',
        'organization',
        'children',
        'selection.datetime.utc',
        'location',
    ]);
}
function getInterval(datetimeObj) {
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes >= TWO_WEEKS) {
        return '1d';
    }
    if (diffInMinutes >= ONE_WEEK) {
        return '6h';
    }
    if (diffInMinutes > TWENTY_FOUR_HOURS) {
        return '4h';
    }
    // TODO(sessions): sub-hour session resolution is still not possible
    return '1h';
}
function reduceTimeSeriesGroups(acc, group, field) {
    var _a;
    (_a = group.series[field]) === null || _a === void 0 ? void 0 : _a.forEach(function (value, index) { var _a; return (acc[index] = ((_a = acc[index]) !== null && _a !== void 0 ? _a : 0) + value); });
    return acc;
}
var ReleaseHealthRequest = /** @class */ (function (_super) {
    __extends(ReleaseHealthRequest, _super);
    function ReleaseHealthRequest() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            errored: false,
            statusCountByReleaseInPeriod: null,
            totalCountByReleaseIn24h: null,
            totalCountByProjectIn24h: null,
            statusCountByProjectInPeriod: null,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, healthStatsPeriod, promises, _b, statusCountByReleaseInPeriod, totalCountByReleaseIn24h, totalCountByProjectIn24h, statusCountByProjectInPeriod, error_1;
            var _c, _d;
            return __generator(this, function (_e) {
                switch (_e.label) {
                    case 0:
                        _a = this.props, api = _a.api, healthStatsPeriod = _a.healthStatsPeriod;
                        api.clear();
                        this.setState({
                            loading: true,
                            errored: false,
                            statusCountByReleaseInPeriod: null,
                            totalCountByReleaseIn24h: null,
                            totalCountByProjectIn24h: null,
                        });
                        promises = [
                            this.fetchStatusCountByReleaseInPeriod(),
                            this.fetchTotalCountByReleaseIn24h(),
                            this.fetchTotalCountByProjectIn24h(),
                        ];
                        if (healthStatsPeriod === HealthStatsPeriodOption.AUTO) {
                            promises.push(this.fetchStatusCountByProjectInPeriod());
                        }
                        _e.label = 1;
                    case 1:
                        _e.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, Promise.all(promises)];
                    case 2:
                        _b = __read.apply(void 0, [_e.sent(), 4]), statusCountByReleaseInPeriod = _b[0], totalCountByReleaseIn24h = _b[1], totalCountByProjectIn24h = _b[2], statusCountByProjectInPeriod = _b[3];
                        this.setState({
                            loading: false,
                            statusCountByReleaseInPeriod: statusCountByReleaseInPeriod,
                            totalCountByReleaseIn24h: totalCountByReleaseIn24h,
                            totalCountByProjectIn24h: totalCountByProjectIn24h,
                            statusCountByProjectInPeriod: statusCountByProjectInPeriod,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _e.sent();
                        addErrorMessage((_d = (_c = error_1.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) !== null && _d !== void 0 ? _d : t('Error loading health data'));
                        this.setState({
                            loading: false,
                            errored: true,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.getHealthData = function () {
            // TODO(sessions): investigate if this needs to be optimized to lower O(n) complexity
            return {
                getCrashCount: _this.getCrashCount,
                getCrashFreeRate: _this.getCrashFreeRate,
                get24hCountByRelease: _this.get24hCountByRelease,
                get24hCountByProject: _this.get24hCountByProject,
                getTimeSeries: _this.getTimeSeries,
                getAdoption: _this.getAdoption,
            };
        };
        _this.getCrashCount = function (version, project, display) {
            var _a;
            var statusCountByReleaseInPeriod = _this.state.statusCountByReleaseInPeriod;
            var field = _this.displayToField(display);
            return (_a = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.find(function (_a) {
                var by = _a.by;
                return by.release === version &&
                    by.project === project &&
                    by['session.status'] === 'crashed';
            })) === null || _a === void 0 ? void 0 : _a.totals[field];
        };
        _this.getCrashFreeRate = function (version, project, display) {
            var _a;
            var statusCountByReleaseInPeriod = _this.state.statusCountByReleaseInPeriod;
            var field = _this.displayToField(display);
            var totalCount = (_a = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.filter(function (_a) {
                var by = _a.by;
                return by.release === version && by.project === project;
            })) === null || _a === void 0 ? void 0 : _a.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
            var crashedCount = _this.getCrashCount(version, project, display);
            return !defined(totalCount) || totalCount === 0
                ? null
                : getCrashFreePercent(100 - percent(crashedCount !== null && crashedCount !== void 0 ? crashedCount : 0, totalCount !== null && totalCount !== void 0 ? totalCount : 0));
        };
        _this.get24hCountByRelease = function (version, project, display) {
            var _a;
            var totalCountByReleaseIn24h = _this.state.totalCountByReleaseIn24h;
            var field = _this.displayToField(display);
            return (_a = totalCountByReleaseIn24h === null || totalCountByReleaseIn24h === void 0 ? void 0 : totalCountByReleaseIn24h.groups.filter(function (_a) {
                var by = _a.by;
                return by.release === version && by.project === project;
            })) === null || _a === void 0 ? void 0 : _a.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
        };
        _this.get24hCountByProject = function (project, display) {
            var _a;
            var totalCountByProjectIn24h = _this.state.totalCountByProjectIn24h;
            var field = _this.displayToField(display);
            return (_a = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.groups.filter(function (_a) {
                var by = _a.by;
                return by.project === project;
            })) === null || _a === void 0 ? void 0 : _a.reduce(function (acc, group) { return acc + group.totals[field]; }, 0);
        };
        _this.getTimeSeries = function (version, project, display) {
            var healthStatsPeriod = _this.props.healthStatsPeriod;
            if (healthStatsPeriod === HealthStatsPeriodOption.AUTO) {
                return _this.getPeriodTimeSeries(version, project, display);
            }
            return _this.get24hTimeSeries(version, project, display);
        };
        _this.get24hTimeSeries = function (version, project, display) {
            var _a, _b, _c;
            var _d = _this.state, totalCountByReleaseIn24h = _d.totalCountByReleaseIn24h, totalCountByProjectIn24h = _d.totalCountByProjectIn24h;
            var field = _this.displayToField(display);
            var intervals = (_a = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.intervals) !== null && _a !== void 0 ? _a : [];
            var projectData = (_b = totalCountByProjectIn24h === null || totalCountByProjectIn24h === void 0 ? void 0 : totalCountByProjectIn24h.groups.find(function (_a) {
                var by = _a.by;
                return by.project === project;
            })) === null || _b === void 0 ? void 0 : _b.series[field];
            var releaseData = (_c = totalCountByReleaseIn24h === null || totalCountByReleaseIn24h === void 0 ? void 0 : totalCountByReleaseIn24h.groups.find(function (_a) {
                var by = _a.by;
                return by.project === project && by.release === version;
            })) === null || _c === void 0 ? void 0 : _c.series[field];
            return [
                {
                    seriesName: t('This Release'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map(function (interval, index) {
                        var _a;
                        return ({
                            name: moment(interval).valueOf(),
                            value: (_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                },
                {
                    seriesName: t('Total Project'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map(function (interval, index) {
                        var _a;
                        return ({
                            name: moment(interval).valueOf(),
                            value: (_a = projectData === null || projectData === void 0 ? void 0 : projectData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                    z: 0,
                },
            ];
        };
        _this.getPeriodTimeSeries = function (version, project, display) {
            var _a, _b, _c;
            var _d = _this.state, statusCountByReleaseInPeriod = _d.statusCountByReleaseInPeriod, statusCountByProjectInPeriod = _d.statusCountByProjectInPeriod;
            var field = _this.displayToField(display);
            var intervals = (_a = statusCountByProjectInPeriod === null || statusCountByProjectInPeriod === void 0 ? void 0 : statusCountByProjectInPeriod.intervals) !== null && _a !== void 0 ? _a : [];
            var projectData = (_b = statusCountByProjectInPeriod === null || statusCountByProjectInPeriod === void 0 ? void 0 : statusCountByProjectInPeriod.groups.filter(function (_a) {
                var by = _a.by;
                return by.project === project;
            })) === null || _b === void 0 ? void 0 : _b.reduce(function (acc, group) { return reduceTimeSeriesGroups(acc, group, field); }, []);
            var releaseData = (_c = statusCountByReleaseInPeriod === null || statusCountByReleaseInPeriod === void 0 ? void 0 : statusCountByReleaseInPeriod.groups.filter(function (_a) {
                var by = _a.by;
                return by.project === project && by.release === version;
            })) === null || _c === void 0 ? void 0 : _c.reduce(function (acc, group) { return reduceTimeSeriesGroups(acc, group, field); }, []);
            return [
                {
                    seriesName: t('This Release'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map(function (interval, index) {
                        var _a;
                        return ({
                            name: moment(interval).valueOf(),
                            value: (_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                },
                {
                    seriesName: t('Total Project'),
                    data: intervals === null || intervals === void 0 ? void 0 : intervals.map(function (interval, index) {
                        var _a;
                        return ({
                            name: moment(interval).valueOf(),
                            value: (_a = projectData === null || projectData === void 0 ? void 0 : projectData[index]) !== null && _a !== void 0 ? _a : 0,
                        });
                    }),
                    z: 0,
                },
            ];
        };
        _this.getAdoption = function (version, project, display) {
            var get24hCountByRelease = _this.get24hCountByRelease(version, project, display);
            var get24hCountByProject = _this.get24hCountByProject(project, display);
            return defined(get24hCountByRelease) && defined(get24hCountByProject)
                ? percent(get24hCountByRelease, get24hCountByProject)
                : undefined;
        };
        return _this;
    }
    ReleaseHealthRequest.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ReleaseHealthRequest.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.releasesReloading) {
            return;
        }
        if (isEqual(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    };
    Object.defineProperty(ReleaseHealthRequest.prototype, "path", {
        get: function () {
            var organization = this.props.organization;
            return "/organizations/" + organization.slug + "/sessions/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ReleaseHealthRequest.prototype, "baseQueryParams", {
        get: function () {
            var _a = this.props, location = _a.location, selection = _a.selection, defaultStatsPeriod = _a.defaultStatsPeriod, releases = _a.releases;
            return __assign({ query: stringifyQueryObject(new QueryResults(releases.reduce(function (acc, release, index, allReleases) {
                    acc.push("release:\"" + release + "\"");
                    if (index < allReleases.length - 1) {
                        acc.push('OR');
                    }
                    return acc;
                }, []))), interval: getInterval(selection.datetime) }, getParams(pick(location.query, Object.values(URL_PARAM)), {
                defaultStatsPeriod: defaultStatsPeriod,
            }));
        },
        enumerable: false,
        configurable: true
    });
    /**
     * Used to calculate crash free rate, count histogram (This Release series), and crash count
     */
    ReleaseHealthRequest.prototype.fetchStatusCountByReleaseInPeriod = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, display, response;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, display = _a.display;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: __assign(__assign({}, this.baseQueryParams), { field: __spreadArray([], __read(new Set(__spreadArray(__spreadArray([], __read(display.map(function (d) { return _this.displayToField(d); }))), ['sum(session)'])))), groupBy: ['project', 'release', 'session.status'] }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    /**
     * Used to calculate count histogram (Total Project series)
     */
    ReleaseHealthRequest.prototype.fetchStatusCountByProjectInPeriod = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, display, response;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, display = _a.display;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: __assign(__assign({}, this.baseQueryParams), { query: undefined, field: __spreadArray([], __read(new Set(__spreadArray(__spreadArray([], __read(display.map(function (d) { return _this.displayToField(d); }))), ['sum(session)'])))), groupBy: ['project', 'session.status'] }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    /**
     * Used to calculate adoption, and count histogram (This Release series)
     */
    ReleaseHealthRequest.prototype.fetchTotalCountByReleaseIn24h = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, display, response;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, display = _a.display;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: __assign(__assign({}, this.baseQueryParams), { field: display.map(function (d) { return _this.displayToField(d); }), groupBy: ['project', 'release'], interval: '1h', statsPeriod: '24h' }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    /**
     * Used to calculate adoption, and count histogram (Total Project series)
     */
    ReleaseHealthRequest.prototype.fetchTotalCountByProjectIn24h = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, display, response;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, display = _a.display;
                        return [4 /*yield*/, api.requestPromise(this.path, {
                                query: __assign(__assign({}, this.baseQueryParams), { query: undefined, field: display.map(function (d) { return _this.displayToField(d); }), groupBy: ['project'], interval: '1h', statsPeriod: '24h' }),
                            })];
                    case 1:
                        response = _b.sent();
                        return [2 /*return*/, response];
                }
            });
        });
    };
    ReleaseHealthRequest.prototype.displayToField = function (display) {
        switch (display) {
            case DisplayOption.USERS:
                return 'count_unique(user)';
            case DisplayOption.SESSIONS:
            default:
                return 'sum(session)';
        }
    };
    ReleaseHealthRequest.prototype.render = function () {
        var _a = this.state, loading = _a.loading, errored = _a.errored;
        var children = this.props.children;
        return children({
            isHealthLoading: loading,
            errored: errored,
            getHealthData: this.getHealthData(),
        });
    };
    return ReleaseHealthRequest;
}(React.Component));
export default withApi(ReleaseHealthRequest);
//# sourceMappingURL=releaseHealthRequest.jsx.map
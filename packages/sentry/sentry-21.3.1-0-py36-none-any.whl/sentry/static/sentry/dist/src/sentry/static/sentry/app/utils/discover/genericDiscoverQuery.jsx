import { __assign, __awaiter, __extends, __generator, __read } from "tslib";
import React from 'react';
import { t } from 'app/locale';
import { isAPIPayloadSimilar, } from 'app/utils/discover/eventView';
/**
 * Generic component for discover queries
 */
var GenericDiscoverQuery = /** @class */ (function (_super) {
    __extends(GenericDiscoverQuery, _super);
    function GenericDiscoverQuery() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            tableFetchID: undefined,
            error: null,
            tableData: null,
            pageLinks: null,
        };
        _this._shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.getPayload(_this.props);
            var otherAPIPayload = _this.getPayload(prevProps);
            return (!isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload) ||
                prevProps.limit !== _this.props.limit ||
                prevProps.route !== _this.props.route ||
                prevProps.cursor !== _this.props.cursor);
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, beforeFetch, afterFetch, eventView, orgSlug, route, limit, cursor, setError, noPagination, referrer, url, tableFetchID, apiPayload, _b, data, jqXHR_1, tableData_1, err_1, error;
            var _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, api = _a.api, beforeFetch = _a.beforeFetch, afterFetch = _a.afterFetch, eventView = _a.eventView, orgSlug = _a.orgSlug, route = _a.route, limit = _a.limit, cursor = _a.cursor, setError = _a.setError, noPagination = _a.noPagination, referrer = _a.referrer;
                        if (!eventView.isValid()) {
                            return [2 /*return*/];
                        }
                        url = "/organizations/" + orgSlug + "/" + route + "/";
                        tableFetchID = Symbol("tableFetchID");
                        apiPayload = this.getPayload(this.props);
                        this.setState({ isLoading: true, tableFetchID: tableFetchID });
                        setError === null || setError === void 0 ? void 0 : setError(undefined);
                        if (limit) {
                            apiPayload.per_page = limit;
                        }
                        if (noPagination) {
                            apiPayload.noPagination = noPagination;
                        }
                        if (cursor) {
                            apiPayload.cursor = cursor;
                        }
                        if (referrer) {
                            apiPayload.referrer = referrer;
                        }
                        beforeFetch === null || beforeFetch === void 0 ? void 0 : beforeFetch(api);
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, doDiscoverQuery(api, url, apiPayload)];
                    case 2:
                        _b = __read.apply(void 0, [_d.sent(), 3]), data = _b[0], jqXHR_1 = _b[2];
                        if (this.state.tableFetchID !== tableFetchID) {
                            // invariant: a different request was initiated after this request
                            return [2 /*return*/];
                        }
                        tableData_1 = afterFetch ? afterFetch(data, this.props) : data;
                        this.setState(function (prevState) {
                            var _a;
                            return ({
                                isLoading: false,
                                tableFetchID: undefined,
                                error: null,
                                pageLinks: (_a = jqXHR_1 === null || jqXHR_1 === void 0 ? void 0 : jqXHR_1.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : prevState.pageLinks,
                                tableData: tableData_1,
                            });
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _d.sent();
                        error = ((_c = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) || t('An unknown error occurred.');
                        this.setState({
                            isLoading: false,
                            tableFetchID: undefined,
                            error: error,
                            tableData: null,
                        });
                        if (setError) {
                            setError(error);
                        }
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    GenericDiscoverQuery.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GenericDiscoverQuery.prototype.componentDidUpdate = function (prevProps) {
        // Reload data if we aren't already loading,
        var refetchCondition = !this.state.isLoading && this._shouldRefetchData(prevProps);
        // or if we've moved from an invalid view state to a valid one,
        var eventViewValidation = prevProps.eventView.isValid() === false && this.props.eventView.isValid();
        var shouldRefetchExternal = this.props.shouldRefetchData
            ? this.props.shouldRefetchData(prevProps, this.props)
            : false;
        if (refetchCondition || eventViewValidation || shouldRefetchExternal) {
            this.fetchData();
        }
    };
    GenericDiscoverQuery.prototype.getPayload = function (props) {
        if (this.props.getRequestPayload) {
            return this.props.getRequestPayload(props);
        }
        return props.eventView.getEventsAPIPayload(props.location);
    };
    GenericDiscoverQuery.prototype.render = function () {
        var _a = this.state, isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData, pageLinks = _a.pageLinks;
        var childrenProps = {
            isLoading: isLoading,
            error: error,
            tableData: tableData,
            pageLinks: pageLinks,
        };
        var children = this.props.children; // Explicitly setting type due to issues with generics and React's children
        return children === null || children === void 0 ? void 0 : children(childrenProps);
    };
    return GenericDiscoverQuery;
}(React.Component));
export function doDiscoverQuery(api, url, params) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, api.requestPromise(url, {
                    method: 'GET',
                    includeAllArgs: true,
                    query: __assign({}, params),
                })];
        });
    });
}
export default GenericDiscoverQuery;
//# sourceMappingURL=genericDiscoverQuery.jsx.map
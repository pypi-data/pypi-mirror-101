import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import moment from 'moment';
import { fetchOrgMembers } from 'app/actionCreators/members';
import Feature from 'app/components/acl/feature';
import { t } from 'app/locale';
import { getUtcDateString } from 'app/utils/dates';
import withApi from 'app/utils/withApi';
import { fetchAlertRule, fetchIncidentsForRule } from '../../utils';
import DetailsBody from './body';
import { ALERT_RULE_DETAILS_DEFAULT_PERIOD, TIME_OPTIONS, TIME_WINDOWS } from './constants';
import DetailsHeader from './header';
var AlertRuleDetails = /** @class */ (function (_super) {
    __extends(AlertRuleDetails, _super);
    function AlertRuleDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { isLoading: false, hasError: false };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, orgId, ruleId, timePeriod, start, end, rulePromise, incidentsPromise, _err_1;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({ isLoading: true, hasError: false });
                        _a = this.props.params, orgId = _a.orgId, ruleId = _a.ruleId;
                        timePeriod = this.getTimePeriod();
                        start = timePeriod.start, end = timePeriod.end;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        rulePromise = fetchAlertRule(orgId, ruleId).then(function (rule) {
                            return _this.setState({ rule: rule });
                        });
                        incidentsPromise = fetchIncidentsForRule(orgId, ruleId, start, end).then(function (incidents) { return _this.setState({ incidents: incidents }); });
                        return [4 /*yield*/, Promise.all([rulePromise, incidentsPromise])];
                    case 2:
                        _b.sent();
                        this.setState({ isLoading: false, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _b.sent();
                        this.setState({ isLoading: false, hasError: true });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleTimePeriodChange = function (value) { return __awaiter(_this, void 0, void 0, function () {
            var location;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        location = this.props.location;
                        return [4 /*yield*/, browserHistory.push({
                                pathname: location.pathname,
                                query: {
                                    period: value,
                                },
                            })];
                    case 1:
                        _a.sent();
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AlertRuleDetails.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, params = _a.params;
        fetchOrgMembers(api, params.orgId);
        this.fetchData();
    };
    AlertRuleDetails.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.location.search !== this.props.location.search ||
            prevProps.params.orgId !== this.props.params.orgId ||
            prevProps.params.ruleId !== this.props.params.ruleId) {
            this.fetchData();
        }
    };
    AlertRuleDetails.prototype.getTimePeriod = function () {
        var _a, _b;
        var location = this.props.location;
        var timePeriod = (_a = location.query.period) !== null && _a !== void 0 ? _a : ALERT_RULE_DETAILS_DEFAULT_PERIOD;
        if (location.query.start && location.query.end) {
            return {
                start: location.query.start,
                end: location.query.end,
                period: timePeriod,
                label: t('Custom time'),
                custom: true,
            };
        }
        var timeOption = (_b = TIME_OPTIONS.find(function (item) { return item.value === timePeriod; })) !== null && _b !== void 0 ? _b : TIME_OPTIONS[1];
        var start = getUtcDateString(moment(moment.utc().diff(TIME_WINDOWS[timeOption.value])));
        var end = getUtcDateString(moment.utc());
        return {
            start: start,
            end: end,
            label: timeOption.label,
            period: timePeriod,
        };
    };
    AlertRuleDetails.prototype.render = function () {
        var _a = this.state, rule = _a.rule, incidents = _a.incidents, hasError = _a.hasError;
        var _b = this.props, params = _b.params, organization = _b.organization;
        var timePeriod = this.getTimePeriod();
        return (<React.Fragment>
        <Feature organization={organization} features={['alert-details-redesign']}>
          <DetailsHeader hasIncidentRuleDetailsError={hasError} params={params} rule={rule}/>
          <DetailsBody {...this.props} rule={rule} incidents={incidents} timePeriod={timePeriod} handleTimePeriodChange={this.handleTimePeriodChange}/>
        </Feature>
      </React.Fragment>);
    };
    return AlertRuleDetails;
}(React.Component));
export default withApi(AlertRuleDetails);
//# sourceMappingURL=index.jsx.map
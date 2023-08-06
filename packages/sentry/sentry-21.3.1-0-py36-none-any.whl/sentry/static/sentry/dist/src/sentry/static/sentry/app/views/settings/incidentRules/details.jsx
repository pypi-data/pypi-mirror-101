import { __assign, __extends } from "tslib";
import React from 'react';
import withTeams from 'app/utils/withTeams';
import AsyncView from 'app/views/asyncView';
import RuleForm from 'app/views/settings/incidentRules/ruleForm';
var IncidentRulesDetails = /** @class */ (function (_super) {
    __extends(IncidentRulesDetails, _super);
    function IncidentRulesDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function () {
            var router = _this.props.router;
            var orgId = _this.props.params.orgId;
            router.push("/organizations/" + orgId + "/alerts/rules/");
        };
        return _this;
    }
    IncidentRulesDetails.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { actions: new Map() });
    };
    IncidentRulesDetails.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, ruleId = _a.ruleId;
        return [['rule', "/organizations/" + orgId + "/alert-rules/" + ruleId + "/"]];
    };
    IncidentRulesDetails.prototype.onRequestSuccess = function (_a) {
        var stateKey = _a.stateKey, data = _a.data;
        if (stateKey === 'rule' && data.name) {
            this.props.onChangeTitle(data.name);
        }
    };
    IncidentRulesDetails.prototype.renderBody = function () {
        var teams = this.props.teams;
        var ruleId = this.props.params.ruleId;
        var rule = this.state.rule;
        var userTeamIds = new Set(teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        }).map(function (_a) {
            var id = _a.id;
            return id;
        }));
        return (<RuleForm {...this.props} ruleId={ruleId} rule={rule} onSubmitSuccess={this.handleSubmitSuccess} userTeamIds={userTeamIds}/>);
    };
    return IncidentRulesDetails;
}(AsyncView));
export default withTeams(IncidentRulesDetails);
//# sourceMappingURL=details.jsx.map
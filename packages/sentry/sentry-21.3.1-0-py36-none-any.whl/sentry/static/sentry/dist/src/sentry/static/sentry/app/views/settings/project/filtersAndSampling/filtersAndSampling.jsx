import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import React from 'react';
import partition from 'lodash/partition';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import Alert from 'app/components/alert';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import { DynamicSamplingConditionOperator, DynamicSamplingRuleType, } from 'app/types/dynamicSampling';
import withProject from 'app/utils/withProject';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import PermissionAlert from 'app/views/settings/organization/permissionAlert';
import ErrorRuleModal from './modals/errorRuleModal';
import TransactionRuleModal from './modals/transactionRuleModal';
import { modalCss } from './modals/utils';
import RulesPanel from './rulesPanel';
import { DYNAMIC_SAMPLING_DOC_LINK } from './utils';
var FiltersAndSampling = /** @class */ (function (_super) {
    __extends(FiltersAndSampling, _super);
    function FiltersAndSampling() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.successfullySubmitted = function (projectDetails, successMessage) {
            _this.setState({ projectDetails: projectDetails });
            if (successMessage) {
                addSuccessMessage(successMessage);
            }
        };
        _this.handleOpenErrorRule = function (rule) { return function () {
            var _a = _this.props, organization = _a.organization, project = _a.project;
            var _b = _this.state, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            return openModal(function (modalProps) { return (<ErrorRuleModal {...modalProps} api={_this.api} organization={organization} project={project} rule={rule} errorRules={errorRules} transactionRules={transactionRules} onSubmitSuccess={_this.successfullySubmitted}/>); }, {
                modalCss: modalCss,
            });
        }; };
        _this.handleOpenTransactionRule = function (rule) { return function () {
            var _a = _this.props, organization = _a.organization, project = _a.project;
            var _b = _this.state, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            return openModal(function (modalProps) { return (<TransactionRuleModal {...modalProps} api={_this.api} organization={organization} project={project} rule={rule} errorRules={errorRules} transactionRules={transactionRules} onSubmitSuccess={_this.successfullySubmitted}/>); }, {
                modalCss: modalCss,
            });
        }; };
        _this.handleAddRule = function (type) { return function () {
            if (type === 'errorRules') {
                _this.handleOpenErrorRule()();
                return;
            }
            _this.handleOpenTransactionRule()();
        }; };
        _this.handleEditRule = function (rule) { return function () {
            if (rule.type === DynamicSamplingRuleType.ERROR) {
                _this.handleOpenErrorRule(rule)();
                return;
            }
            _this.handleOpenTransactionRule(rule)();
        }; };
        _this.handleDeleteRule = function (rule) { return function () {
            var _a = _this.state, errorRules = _a.errorRules, transactionRules = _a.transactionRules;
            var newErrorRules = rule.type === DynamicSamplingRuleType.ERROR
                ? errorRules.filter(function (errorRule) { return errorRule.id !== rule.id; })
                : errorRules;
            var newTransactionRules = rule.type !== DynamicSamplingRuleType.ERROR
                ? transactionRules.filter(function (transactionRule) { return transactionRule.id !== rule.id; })
                : transactionRules;
            var newRules = __spreadArray(__spreadArray([], __read(newErrorRules)), __read(newTransactionRules));
            _this.submitRules(newRules, t('Successfully deleted dynamic sampling rule'), t('An error occurred while deleting dynamic sampling rule'));
        }; };
        _this.handleUpdateRules = function (rules) {
            var _a;
            if (!rules.length) {
                return;
            }
            var _b = _this.state, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            if (((_a = rules[0]) === null || _a === void 0 ? void 0 : _a.type) === DynamicSamplingRuleType.ERROR) {
                _this.submitRules(__spreadArray(__spreadArray([], __read(rules)), __read(transactionRules)));
                return;
            }
            _this.submitRules(__spreadArray(__spreadArray([], __read(errorRules)), __read(rules)));
        };
        return _this;
    }
    FiltersAndSampling.prototype.getTitle = function () {
        return t('Filters & Sampling');
    };
    FiltersAndSampling.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { errorRules: [], transactionRules: [], projectDetails: null });
    };
    FiltersAndSampling.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [['projectDetails', "/projects/" + organization.slug + "/" + project.slug + "/"]];
    };
    FiltersAndSampling.prototype.componentDidMount = function () {
        this.getRules();
    };
    FiltersAndSampling.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.projectDetails !== this.state.projectDetails) {
            this.getRules();
            return;
        }
    };
    FiltersAndSampling.prototype.getRules = function () {
        var _a;
        var projectDetails = this.state.projectDetails;
        if (!projectDetails) {
            return;
        }
        var dynamicSampling = projectDetails.dynamicSampling;
        var rules = (_a = dynamicSampling === null || dynamicSampling === void 0 ? void 0 : dynamicSampling.rules) !== null && _a !== void 0 ? _a : [];
        var _b = __read(partition(rules, function (rule) { return rule.type === DynamicSamplingRuleType.ERROR; }), 2), errorRules = _b[0], transactionRules = _b[1];
        this.setState({ errorRules: errorRules, transactionRules: transactionRules });
    };
    FiltersAndSampling.prototype.submitRules = function (newRules, successMessage, errorMessage) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, organization, project, projectDetails, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, project = _a.project;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/", { method: 'PUT', data: { dynamicSampling: { rules: newRules } } })];
                    case 2:
                        projectDetails = _b.sent();
                        this.successfullySubmitted(projectDetails, successMessage);
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.getRules();
                        if (errorMessage) {
                            addErrorMessage(errorMessage);
                        }
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    FiltersAndSampling.prototype.renderBody = function () {
        var _a = this.state, errorRules = _a.errorRules, transactionRules = _a.transactionRules;
        var hasAccess = this.props.hasAccess;
        var disabled = !hasAccess;
        var hasNotSupportedConditionOperator = __spreadArray(__spreadArray([], __read(errorRules)), __read(transactionRules)).some(function (rule) { return rule.condition.op !== DynamicSamplingConditionOperator.AND; });
        if (hasNotSupportedConditionOperator) {
            return (<Alert type="error">
          {t('A condition operator has been found that is not yet supported.')}
        </Alert>);
        }
        return (<React.Fragment>
        <SettingsPageHeader title={this.getTitle()}/>
        <PermissionAlert />
        <TextBlock>
          {tct('Manage the inbound data you want to store. To change the sampling rate or rate limits, [link:update your SDK configuration]. The rules added below will apply on top of your SDK configuration.', {
                link: <ExternalLink href={DYNAMIC_SAMPLING_DOC_LINK}/>,
            })}
        </TextBlock>
        <RulesPanel rules={errorRules} disabled={disabled} onAddRule={this.handleAddRule('errorRules')} onEditRule={this.handleEditRule} onDeleteRule={this.handleDeleteRule} onUpdateRules={this.handleUpdateRules} isErrorPanel/>
        <TextBlock>
          {t('The transaction order is limited. Traces must occur first and individual transactions must occur last. Any individual transaction rules before a trace rule will be disregarded. ')}
        </TextBlock>
        <RulesPanel rules={transactionRules} disabled={disabled} onAddRule={this.handleAddRule('transactionRules')} onEditRule={this.handleEditRule} onDeleteRule={this.handleDeleteRule} onUpdateRules={this.handleUpdateRules}/>
      </React.Fragment>);
    };
    return FiltersAndSampling;
}(AsyncView));
export default withProject(FiltersAndSampling);
//# sourceMappingURL=filtersAndSampling.jsx.map
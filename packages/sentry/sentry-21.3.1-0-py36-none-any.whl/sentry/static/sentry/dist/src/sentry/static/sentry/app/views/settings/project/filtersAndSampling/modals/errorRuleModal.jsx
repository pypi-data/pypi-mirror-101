import { __assign, __extends, __read, __spreadArray } from "tslib";
import isEqual from 'lodash/isEqual';
import { t } from 'app/locale';
import { DynamicSamplingConditionOperator, DynamicSamplingInnerName, DynamicSamplingRuleType, } from 'app/types/dynamicSampling';
import Form from './form';
import { Transaction } from './utils';
var ErrorRuleModal = /** @class */ (function (_super) {
    __extends(ErrorRuleModal, _super);
    function ErrorRuleModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function () {
            var _a = _this.state, sampleRate = _a.sampleRate, conditions = _a.conditions, transaction = _a.transaction;
            if (!sampleRate) {
                return;
            }
            var _b = _this.props, rule = _b.rule, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            var newRule = {
                // All new/updated rules must have id equal to 0
                id: 0,
                type: DynamicSamplingRuleType.ERROR,
                condition: {
                    op: DynamicSamplingConditionOperator.AND,
                    inner: transaction === Transaction.ALL ? [] : conditions.map(_this.getNewCondition),
                },
                sampleRate: sampleRate / 100,
            };
            var newRules = rule
                ? __spreadArray(__spreadArray([], __read(errorRules.map(function (errorRule) {
                    return isEqual(errorRule, rule) ? newRule : errorRule;
                }))), __read(transactionRules)) : __spreadArray(__spreadArray(__spreadArray([], __read(errorRules)), [newRule]), __read(transactionRules));
            var currentRuleIndex = newRules.findIndex(function (newR) { return newR === newRule; });
            _this.submitRules(newRules, currentRuleIndex);
        };
        return _this;
    }
    ErrorRuleModal.prototype.getDefaultState = function () {
        return __assign({}, _super.prototype.getDefaultState.call(this));
    };
    ErrorRuleModal.prototype.getModalTitle = function () {
        var rule = this.props.rule;
        if (rule) {
            return t('Edit a custom rule for errors');
        }
        return t('Add a custom rule for errors');
    };
    ErrorRuleModal.prototype.geTransactionFieldDescription = function () {
        return {
            label: t('Error'),
            // help: t('This is a description'), TODO(PRISCILA): Add correct description
        };
    };
    ErrorRuleModal.prototype.getCategoryOptions = function () {
        return [
            [DynamicSamplingInnerName.EVENT_RELEASE, t('Releases')],
            [DynamicSamplingInnerName.EVENT_ENVIRONMENT, t('Environments')],
            [DynamicSamplingInnerName.EVENT_USER_ID, t('User Id')],
            [DynamicSamplingInnerName.EVENT_USER_SEGMENT, t('User Segment')],
            [DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS, t('Browser Extensions')],
            [DynamicSamplingInnerName.EVENT_LOCALHOST, t('Localhost')],
            [DynamicSamplingInnerName.EVENT_LEGACY_BROWSER, t('Legacy Browsers')],
            [DynamicSamplingInnerName.EVENT_WEB_CRAWLERS, t('Web Crawlers')],
        ];
    };
    return ErrorRuleModal;
}(Form));
export default ErrorRuleModal;
//# sourceMappingURL=errorRuleModal.jsx.map
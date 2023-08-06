import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import partition from 'lodash/partition';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import ExternalLink from 'app/components/links/externalLink';
import Tooltip from 'app/components/tooltip';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { DynamicSamplingConditionOperator, DynamicSamplingInnerName, DynamicSamplingRuleType, } from 'app/types/dynamicSampling';
import Field from 'app/views/settings/components/forms/field';
import { DYNAMIC_SAMPLING_DOC_LINK } from '../utils';
import Form from './form';
import { Transaction } from './utils';
var TransactionRuleModal = /** @class */ (function (_super) {
    __extends(TransactionRuleModal, _super);
    function TransactionRuleModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDeleteCondition = function (index) { return function () {
            var newConditions = __spreadArray([], __read(_this.state.conditions));
            newConditions.splice(index, 1);
            if (!newConditions.length) {
                _this.setState({
                    conditions: newConditions,
                    transaction: Transaction.ALL,
                    isTracingDisabled: false,
                });
                return;
            }
            _this.setState({ conditions: newConditions });
        }; };
        _this.handleSubmit = function () {
            var _a = _this.state, tracing = _a.tracing, sampleRate = _a.sampleRate, conditions = _a.conditions, transaction = _a.transaction;
            if (!sampleRate) {
                return;
            }
            var _b = _this.props, rule = _b.rule, errorRules = _b.errorRules, transactionRules = _b.transactionRules;
            var newRule = {
                // All new/updated rules must have id equal to 0
                id: 0,
                type: tracing ? DynamicSamplingRuleType.TRACE : DynamicSamplingRuleType.TRANSACTION,
                condition: {
                    op: DynamicSamplingConditionOperator.AND,
                    inner: transaction === Transaction.ALL ? [] : conditions.map(_this.getNewCondition),
                },
                sampleRate: sampleRate / 100,
            };
            var newTransactionRules = rule
                ? transactionRules.map(function (transactionRule) {
                    return isEqual(transactionRule, rule) ? newRule : transactionRule;
                })
                : __spreadArray(__spreadArray([], __read(transactionRules)), [newRule]);
            var _c = __read(partition(newTransactionRules, function (transactionRule) { return transactionRule.type === DynamicSamplingRuleType.TRACE; }), 2), transactionTraceRules = _c[0], individualTransactionRules = _c[1];
            var newRules = __spreadArray(__spreadArray(__spreadArray([], __read(errorRules)), __read(transactionTraceRules)), __read(individualTransactionRules));
            var currentRuleIndex = newRules.findIndex(function (newR) { return newR === newRule; });
            _this.submitRules(newRules, currentRuleIndex);
        };
        return _this;
    }
    TransactionRuleModal.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (prevState.transaction !== this.state.transaction) {
            this.setIsTracingDisabled(this.state.transaction !== Transaction.ALL);
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    TransactionRuleModal.prototype.setIsTracingDisabled = function (isTracingDisabled) {
        this.setState({ isTracingDisabled: isTracingDisabled });
    };
    TransactionRuleModal.prototype.getDefaultState = function () {
        var rule = this.props.rule;
        if (rule) {
            var condition = rule.condition;
            var inner = condition.inner;
            return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { tracing: rule.type === DynamicSamplingRuleType.TRACE, isTracingDisabled: !!inner.length });
        }
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { tracing: true });
    };
    TransactionRuleModal.prototype.getModalTitle = function () {
        var rule = this.props.rule;
        if (rule) {
            return t('Edit a custom rule for transactions');
        }
        return t('Add a custom rule for transactions');
    };
    TransactionRuleModal.prototype.geTransactionFieldDescription = function () {
        return {
            label: t('Transaction'),
            // help: t('This is a description'),  TODO(Priscila): Add correct descriptions
        };
    };
    TransactionRuleModal.prototype.getCategoryOptions = function () {
        var tracing = this.state.tracing;
        if (tracing) {
            return [
                [DynamicSamplingInnerName.TRACE_RELEASE, t('Releases')],
                [DynamicSamplingInnerName.TRACE_ENVIRONMENT, t('Environments')],
                [DynamicSamplingInnerName.TRACE_USER_ID, t('User Id')],
                [DynamicSamplingInnerName.TRACE_USER_SEGMENT, t('User Segment')],
            ];
        }
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
    TransactionRuleModal.prototype.getExtraFields = function () {
        var _this = this;
        var theme = this.props.theme;
        var _a = this.state, tracing = _a.tracing, isTracingDisabled = _a.isTracingDisabled;
        return (<Field label={t('Tracing')} 
        // help={t('this is a description')} // TODO(Priscila): Add correct descriptions
        inline={false} flexibleControlStateSize stacked showHelpInTooltip>
        <Tooltip title={t('This field can only be edited if there are no match conditions')} disabled={!isTracingDisabled} popperStyle={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n            @media (min-width: ", ") {\n              max-width: 370px;\n            }\n          "], ["\n            @media (min-width: ", ") {\n              max-width: 370px;\n            }\n          "])), theme.breakpoints[0])}>
          <TracingWrapper onClick={isTracingDisabled ? undefined : function () { return _this.handleChange('tracing', !tracing); }}>
            <StyledCheckboxFancy isChecked={tracing} isDisabled={isTracingDisabled}/>
            {tct('Include all related transactions by trace ID. This can span across multiple projects. All related errors will remain. [link:Learn more about tracing].', {
                link: (<ExternalLink href={DYNAMIC_SAMPLING_DOC_LINK} onClick={function (event) { return event.stopPropagation(); }}/>),
            })}
          </TracingWrapper>
        </Tooltip>
      </Field>);
    };
    return TransactionRuleModal;
}(Form));
export default withTheme(TransactionRuleModal);
var TracingWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  cursor: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  cursor: ", ";\n"])), space(1), function (p) { return (p.onClick ? 'pointer' : 'not-allowed'); });
var StyledCheckboxFancy = styled(CheckboxFancy)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=transactionRuleModal.jsx.map
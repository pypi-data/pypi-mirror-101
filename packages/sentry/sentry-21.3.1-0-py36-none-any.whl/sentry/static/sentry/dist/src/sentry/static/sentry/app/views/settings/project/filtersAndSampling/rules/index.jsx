import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { PanelTable } from 'app/components/panels';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import { DynamicSamplingRuleType } from 'app/types/dynamicSampling';
import DraggableList from './draggableList';
import Rule from './rule';
import { layout } from './utils';
var Rules = /** @class */ (function (_super) {
    __extends(Rules, _super);
    function Rules() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { rules: [] };
        _this.handleUpdateRules = function (_a) {
            var activeIndex = _a.activeIndex, overIndex = _a.overIndex, ruleIds = _a.reorderedItems;
            var rules = _this.state.rules;
            var reorderedRules = ruleIds
                .map(function (ruleId) { return rules.find(function (rule) { return String(rule.id) === ruleId; }); })
                .filter(function (rule) { return !!rule; });
            var activeRuleType = rules[activeIndex].type;
            var overRuleType = rules[overIndex].type;
            if (activeRuleType === DynamicSamplingRuleType.TRACE &&
                overRuleType === DynamicSamplingRuleType.TRANSACTION) {
                addErrorMessage(t('Transaction traces rules cannot be under individual transactions rules'));
                return;
            }
            if (activeRuleType === DynamicSamplingRuleType.TRANSACTION &&
                overRuleType === DynamicSamplingRuleType.TRACE) {
                addErrorMessage(t('Individual transactions rules cannot be above transaction traces rules'));
                return;
            }
            _this.setState({ rules: reorderedRules });
        };
        return _this;
    }
    Rules.prototype.componentDidMount = function () {
        this.getRules();
    };
    Rules.prototype.componentDidUpdate = function (prevProps) {
        if (!isEqual(prevProps.rules, this.props.rules)) {
            this.getRules();
            return;
        }
        if (!isEqual(this.props.rules, this.state.rules)) {
            this.handleUpdateRulesParent();
        }
    };
    Rules.prototype.getRules = function () {
        this.setState({ rules: this.props.rules });
    };
    Rules.prototype.handleUpdateRulesParent = function () {
        var onUpdateRules = this.props.onUpdateRules;
        var rules = this.state.rules;
        onUpdateRules(rules);
    };
    Rules.prototype.render = function () {
        var _a = this.props, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, disabled = _a.disabled, emptyMessage = _a.emptyMessage;
        var rules = this.state.rules;
        return (<StyledPanelTable headers={['', t('Type'), t('Conditions'), t('Rate'), '']} isEmpty={!rules.length} emptyMessage={emptyMessage}>
        <DraggableList disabled={disabled} items={rules.map(function (rule) { return String(rule.id); })} onUpdateItems={this.handleUpdateRules} wrapperStyle={function (_a) {
                var isDragging = _a.isDragging, isSorting = _a.isSorting, index = _a.index;
                if (isDragging) {
                    return {
                        cursor: 'grabbing',
                    };
                }
                if (isSorting) {
                    return {};
                }
                return {
                    transform: 'none',
                    transformOrigin: '0',
                    '--box-shadow': 'none',
                    '--box-shadow-picked-up': 'none',
                    overflow: 'visible',
                    position: 'relative',
                    zIndex: rules.length - index,
                    cursor: 'default',
                };
            }} renderItem={function (_a) {
                var value = _a.value, listeners = _a.listeners, attributes = _a.attributes, dragging = _a.dragging, sorting = _a.sorting;
                var currentRule = rules.find(function (rule) { return String(rule.id) === value; });
                if (!currentRule) {
                    return null;
                }
                return (<Rule rule={currentRule} onEditRule={onEditRule(currentRule)} onDeleteRule={onDeleteRule(currentRule)} disabled={disabled} listeners={listeners} grabAttributes={attributes} dragging={dragging} sorting={sorting}/>);
            }}/>
      </StyledPanelTable>);
    };
    return Rules;
}(React.PureComponent));
export default Rules;
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow: visible;\n  margin-bottom: 0;\n  border: none;\n  border-bottom-right-radius: 0;\n  border-bottom-left-radius: 0;\n  ", "\n  > * {\n    ", ";\n    :not(:last-child) {\n      border-bottom: 1px solid ", ";\n    }\n    :nth-child(n + 6) {\n      ", "\n    }\n  }\n"], ["\n  overflow: visible;\n  margin-bottom: 0;\n  border: none;\n  border-bottom-right-radius: 0;\n  border-bottom-left-radius: 0;\n  ", "\n  > * {\n    ", ";\n    :not(:last-child) {\n      border-bottom: 1px solid ", ";\n    }\n    :nth-child(n + 6) {\n      ",
    "\n    }\n  }\n"])), function (p) { return layout(p.theme); }, overflowEllipsis, function (p) { return p.theme.border; }, function (p) {
    return !p.isEmpty
        ? "\n              display: grid;\n              grid-column: 1/-1;\n              padding: 0;\n            "
        : "\n              display: block;\n              grid-column: 1/-1;\n            ";
});
var templateObject_1;
//# sourceMappingURL=index.jsx.map
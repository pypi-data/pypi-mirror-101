import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import { IconGrabbable } from 'app/icons/iconGrabbable';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { layout } from '../utils';
import Actions from './actions';
import Conditions from './conditions';
import SampleRate from './sampleRate';
import Type from './type';
var Rule = /** @class */ (function (_super) {
    __extends(Rule, _super);
    function Rule() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isMenuActionsOpen: false,
        };
        _this.handleChangeMenuAction = function () {
            _this.setState(function (state) { return ({
                isMenuActionsOpen: !state.isMenuActionsOpen,
            }); });
        };
        return _this;
    }
    Rule.prototype.componentDidMount = function () {
        this.checkMenuActionsVisibility();
    };
    Rule.prototype.componentDidUpdate = function () {
        this.checkMenuActionsVisibility();
    };
    Rule.prototype.checkMenuActionsVisibility = function () {
        var _a = this.props, dragging = _a.dragging, sorting = _a.sorting;
        var isMenuActionsOpen = this.state.isMenuActionsOpen;
        if ((dragging || sorting) && isMenuActionsOpen) {
            this.setState({ isMenuActionsOpen: false });
        }
    };
    Rule.prototype.render = function () {
        var _a = this.props, rule = _a.rule, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, disabled = _a.disabled, listeners = _a.listeners, grabAttributes = _a.grabAttributes;
        var type = rule.type, condition = rule.condition, sampleRate = rule.sampleRate;
        var isMenuActionsOpen = this.state.isMenuActionsOpen;
        return (<Columns>
        <GrabColumn>
          <Tooltip title={disabled
                ? t('You do not have permission to reorder dynamic sampling rules.')
                : undefined}>
            <IconGrabbableWrapper {...listeners} disabled={disabled} {...grabAttributes}>
              <IconGrabbable />
            </IconGrabbableWrapper>
          </Tooltip>
        </GrabColumn>
        <Column>
          <Type type={type}/>
        </Column>
        <Column>
          <Conditions condition={condition}/>
        </Column>
        <CenteredColumn>
          <SampleRate sampleRate={sampleRate}/>
        </CenteredColumn>
        <Column>
          <Actions onEditRule={onEditRule} onDeleteRule={onDeleteRule} disabled={disabled} onOpenMenuActions={this.handleChangeMenuAction} isMenuActionsOpen={isMenuActionsOpen}/>
        </Column>
      </Columns>);
    };
    return Rule;
}(React.Component));
export default Rule;
var Columns = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  ", "\n  > * {\n    overflow: visible;\n    :nth-child(5n) {\n      justify-content: flex-end;\n    }\n  }\n"], ["\n  display: grid;\n  align-items: center;\n  ", "\n  > * {\n    overflow: visible;\n    :nth-child(5n) {\n      justify-content: flex-end;\n    }\n  }\n"])), function (p) { return layout(p.theme); });
var Column = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  cursor: default;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  cursor: default;\n"])), space(2));
var GrabColumn = styled(Column)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  cursor: inherit;\n  [role='button'] {\n    cursor: grab;\n  }\n"], ["\n  cursor: inherit;\n  [role='button'] {\n    cursor: grab;\n  }\n"])));
var CenteredColumn = styled(Column)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  text-align: center;\n  justify-content: center;\n"], ["\n  text-align: center;\n  justify-content: center;\n"])));
var IconGrabbableWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n  outline: none;\n"], ["\n  ",
    ";\n  outline: none;\n"])), function (p) {
    return p.disabled &&
        "\n    color: " + p.theme.disabled + ";\n    cursor: not-allowed;\n  ";
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map
import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import GroupingActions from 'app/actions/groupingActions';
import Checkbox from 'app/components/checkbox';
import EventOrGroupHeader from 'app/components/eventOrGroupHeader';
import { IconChevron } from 'app/icons';
import GroupingStore from 'app/stores/groupingStore';
import space from 'app/styles/space';
var MergedItem = /** @class */ (function (_super) {
    __extends(MergedItem, _super);
    function MergedItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            collapsed: false,
            checked: false,
            busy: false,
        };
        _this.listener = GroupingStore.listen(function (data) { return _this.onGroupChange(data); }, undefined);
        _this.onGroupChange = function (_a) {
            var unmergeState = _a.unmergeState;
            if (!unmergeState) {
                return;
            }
            var fingerprint = _this.props.fingerprint;
            var stateForId = unmergeState.has(fingerprint)
                ? unmergeState.get(fingerprint)
                : undefined;
            if (!stateForId) {
                return;
            }
            Object.keys(stateForId).forEach(function (key) {
                if (stateForId[key] === _this.state[key]) {
                    return;
                }
                _this.setState(function (prevState) {
                    var _a;
                    return (__assign(__assign({}, prevState), (_a = {}, _a[key] = stateForId[key], _a)));
                });
            });
        };
        _this.handleToggleEvents = function () {
            var fingerprint = _this.props.fingerprint;
            GroupingActions.toggleCollapseFingerprint(fingerprint);
        };
        _this.handleToggle = function () {
            var _a = _this.props, disabled = _a.disabled, fingerprint = _a.fingerprint, event = _a.event;
            if (disabled || _this.state.busy) {
                return;
            }
            // clicking anywhere in the row will toggle the checkbox
            GroupingActions.toggleUnmerge([fingerprint, event.id]);
        };
        return _this;
    }
    MergedItem.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.listener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    // Disable default behavior of toggling checkbox
    MergedItem.prototype.handleLabelClick = function (event) {
        event.preventDefault();
    };
    MergedItem.prototype.handleCheckClick = function () {
        // noop because of react warning about being a controlled input without `onChange`
        // we handle change via row click
    };
    MergedItem.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, event = _a.event, fingerprint = _a.fingerprint, organization = _a.organization;
        var _b = this.state, collapsed = _b.collapsed, busy = _b.busy, checked = _b.checked;
        var checkboxDisabled = disabled || busy;
        // `event` can be null if last event w/ fingerprint is not within retention period
        return (<MergedGroup busy={busy}>
        <Controls expanded={!collapsed}>
          <ActionWrapper onClick={this.handleToggle}>
            <Checkbox id={fingerprint} value={fingerprint} checked={checked} disabled={checkboxDisabled} onChange={this.handleCheckClick}/>

            <Fingerprint onClick={this.handleLabelClick} htmlFor={fingerprint}>
              {fingerprint}
            </Fingerprint>
          </ActionWrapper>

          <div>
            <Collapse onClick={this.handleToggleEvents}>
              <IconChevron direction={collapsed ? 'down' : 'up'} size="xs"/>
            </Collapse>
          </div>
        </Controls>

        {!collapsed && (<MergedEventList className="event-list">
            {event && (<EventDetails className="event-details">
                <EventOrGroupHeader data={event} organization={organization} hideIcons hideLevel/>
              </EventDetails>)}
          </MergedEventList>)}
      </MergedGroup>);
    };
    return MergedItem;
}(React.Component));
var MergedGroup = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return p.busy && 'opacity: 0.2'; });
var ActionWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  gap: ", ";\n\n  /* Can't use styled components for this because of broad selector */\n  input[type='checkbox'] {\n    margin: 0;\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  align-items: center;\n  gap: ", ";\n\n  /* Can't use styled components for this because of broad selector */\n  input[type='checkbox'] {\n    margin: 0;\n  }\n"])), space(1));
var Controls = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  border-top: 1px solid ", ";\n  background-color: ", ";\n  padding: ", " ", ";\n  ", ";\n\n  ", " {\n    &:first-child & {\n      border-top: none;\n    }\n    &:last-child & {\n      border-top: none;\n      border-bottom: 1px solid ", ";\n    }\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n  border-top: 1px solid ", ";\n  background-color: ", ";\n  padding: ", " ", ";\n  ", ";\n\n  ", " {\n    &:first-child & {\n      border-top: none;\n    }\n    &:last-child & {\n      border-top: none;\n      border-bottom: 1px solid ", ";\n    }\n  }\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.gray100; }, space(0.5), space(1), function (p) { return p.expanded && "border-bottom: 1px solid " + p.theme.innerBorder; }, MergedGroup, function (p) { return p.theme.innerBorder; });
var Fingerprint = styled('label')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-family: ", ";\n\n  ", " & {\n    font-weight: 400;\n    margin: 0;\n  }\n"], ["\n  font-family: ", ";\n\n  " /* sc-selector */, " & {\n    font-weight: 400;\n    margin: 0;\n  }\n"])), function (p) { return p.theme.text.familyMono; }, /* sc-selector */ Controls);
var Collapse = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  cursor: pointer;\n"], ["\n  cursor: pointer;\n"])));
var MergedEventList = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  overflow: hidden;\n  border: none;\n"], ["\n  overflow: hidden;\n  border: none;\n"])));
var EventDetails = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n\n  .event-list & {\n    padding: ", ";\n  }\n"], ["\n  display: flex;\n  justify-content: space-between;\n\n  .event-list & {\n    padding: ", ";\n  }\n"])), space(1));
export default MergedItem;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=mergedItem.jsx.map
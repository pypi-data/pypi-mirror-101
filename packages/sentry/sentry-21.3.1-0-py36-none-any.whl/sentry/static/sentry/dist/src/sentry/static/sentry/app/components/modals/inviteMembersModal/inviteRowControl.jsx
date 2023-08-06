import { __assign, __extends, __read, __spreadArray } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
import Button from 'app/components/button';
import SelectControl from 'app/components/forms/selectControl';
import RoleSelectControl from 'app/components/roleSelectControl';
import { IconClose } from 'app/icons/iconClose';
import { t } from 'app/locale';
import renderEmailValue from './renderEmailValue';
function ValueComponent(props, inviteStatus) {
    return renderEmailValue(inviteStatus[props.data.value], props);
}
function mapToOptions(values) {
    return values.map(function (value) { return ({ value: value, label: value }); });
}
var InviteRowControl = /** @class */ (function (_super) {
    __extends(InviteRowControl, _super);
    function InviteRowControl() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = { inputValue: '' };
        _this.handleInputChange = function (inputValue) {
            _this.setState({ inputValue: inputValue });
        };
        _this.handleKeyDown = function (event) {
            var _a = _this.props, onChangeEmails = _a.onChangeEmails, emails = _a.emails;
            var inputValue = _this.state.inputValue;
            switch (event.key) {
                case 'Enter':
                case 'Tab':
                case ',':
                case ' ':
                    onChangeEmails(__spreadArray(__spreadArray([], __read(mapToOptions(emails))), [{ label: inputValue, value: inputValue }]));
                    _this.setState({ inputValue: '' });
                    event.preventDefault();
                    break;
                default:
                // do nothing.
            }
        };
        return _this;
    }
    InviteRowControl.prototype.render = function () {
        var _a = this.props, className = _a.className, disabled = _a.disabled, emails = _a.emails, role = _a.role, teams = _a.teams, roleOptions = _a.roleOptions, roleDisabledUnallowed = _a.roleDisabledUnallowed, teamOptions = _a.teamOptions, inviteStatus = _a.inviteStatus, onRemove = _a.onRemove, onChangeEmails = _a.onChangeEmails, onChangeRole = _a.onChangeRole, onChangeTeams = _a.onChangeTeams, disableRemove = _a.disableRemove, theme = _a.theme;
        return (<div className={className}>
        <SelectControl data-test-id="select-emails" disabled={disabled} placeholder={t('Enter one or more emails')} inputValue={this.state.inputValue} value={emails} components={{
                MultiValue: function (props) {
                    return ValueComponent(props, inviteStatus);
                },
                DropdownIndicator: function () { return null; },
            }} options={mapToOptions(emails)} onBlur={function (e) {
                return e.target.value &&
                    onChangeEmails(__spreadArray(__spreadArray([], __read(mapToOptions(emails))), [
                        { label: e.target.value, value: e.target.value },
                    ]));
            }} styles={getStyles(theme, inviteStatus)} onInputChange={this.handleInputChange} onKeyDown={this.handleKeyDown} onBlurResetsInput={false} onCloseResetsInput={false} onChange={onChangeEmails} multiple creatable clearable menuIsOpen={false}/>
        <RoleSelectControl data-test-id="select-role" disabled={disabled} value={role} roles={roleOptions} disableUnallowed={roleDisabledUnallowed} onChange={onChangeRole}/>
        <SelectControl data-test-id="select-teams" disabled={disabled} placeholder={t('Add to teams\u2026')} value={teams} options={teamOptions.map(function (_a) {
                var slug = _a.slug;
                return ({
                    value: slug,
                    label: "#" + slug,
                });
            })} onChange={onChangeTeams} multiple clearable/>
        <Button borderless icon={<IconClose />} size="zero" onClick={onRemove} disabled={disableRemove}/>
      </div>);
    };
    return InviteRowControl;
}(React.Component));
/**
 * The email select control has custom selected item states as items
 * show their delivery status after the form is submitted.
 */
function getStyles(theme, inviteStatus) {
    return {
        multiValue: function (provided, _a) {
            var data = _a.data;
            var status = inviteStatus[data.value];
            return __assign(__assign({}, provided), ((status === null || status === void 0 ? void 0 : status.error)
                ? {
                    color: theme.red300,
                    border: "1px solid " + theme.red300,
                    backgroundColor: theme.red100,
                }
                : {}));
        },
        multiValueLabel: function (provided, _a) {
            var data = _a.data;
            var status = inviteStatus[data.value];
            return __assign(__assign(__assign({}, provided), { pointerEvents: 'all' }), ((status === null || status === void 0 ? void 0 : status.error) ? { color: theme.red300 } : {}));
        },
        multiValueRemove: function (provided, _a) {
            var data = _a.data;
            var status = inviteStatus[data.value];
            return __assign(__assign({}, provided), ((status === null || status === void 0 ? void 0 : status.error)
                ? {
                    borderLeft: "1px solid " + theme.red300,
                    ':hover': { backgroundColor: theme.red100, color: theme.red300 },
                }
                : {}));
        },
    };
}
export default withTheme(InviteRowControl);
//# sourceMappingURL=inviteRowControl.jsx.map
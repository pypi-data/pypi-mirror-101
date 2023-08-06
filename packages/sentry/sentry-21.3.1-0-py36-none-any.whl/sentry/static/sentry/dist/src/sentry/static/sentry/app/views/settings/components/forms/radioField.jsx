import { __extends, __rest } from "tslib";
import React from 'react';
import RadioGroup from 'app/views/settings/components/forms/controls/radioGroup';
import InputField from 'app/views/settings/components/forms/inputField';
var RadioField = /** @class */ (function (_super) {
    __extends(RadioField, _super);
    function RadioField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onChange = function (id, onChange, onBlur, e) {
            onChange(id, e);
            onBlur(id, e);
        };
        return _this;
    }
    RadioField.prototype.render = function () {
        var _this = this;
        return (<InputField {...this.props} field={function (_a) {
                var onChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, disabled = _a.disabled, orientInline = _a.orientInline, props = __rest(_a, ["onChange", "onBlur", "value", "disabled", "orientInline"]);
                return (<RadioGroup choices={props.choices} disabled={disabled} orientInline={orientInline} value={value === '' ? null : value} label={props.label} onChange={function (id, e) { return _this.onChange(id, onChange, onBlur, e); }}/>);
            }}/>);
    };
    return RadioField;
}(React.Component));
export default RadioField;
//# sourceMappingURL=radioField.jsx.map
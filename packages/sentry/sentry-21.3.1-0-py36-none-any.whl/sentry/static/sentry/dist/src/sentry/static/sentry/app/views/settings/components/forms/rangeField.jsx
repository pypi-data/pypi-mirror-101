import { __assign, __rest } from "tslib";
import React from 'react';
import RangeSlider from 'app/views/settings/components/forms/controls/rangeSlider';
import InputField from 'app/views/settings/components/forms/inputField';
function onChange(fieldOnChange, value, e) {
    fieldOnChange(value, e);
}
function defaultFormatMessageValue(value, props) {
    return (typeof props.formatLabel === 'function' && props.formatLabel(value)) || value;
}
export default function RangeField(_a) {
    var _b = _a.formatMessageValue, formatMessageValue = _b === void 0 ? defaultFormatMessageValue : _b, disabled = _a.disabled, otherProps = __rest(_a, ["formatMessageValue", "disabled"]);
    var resolvedDisabled = typeof disabled === 'function' ? disabled(otherProps) : disabled;
    var props = __assign(__assign({}, otherProps), { disabled: resolvedDisabled, formatMessageValue: formatMessageValue });
    return (<InputField {...props} field={function (_a) {
            var fieldOnChange = _a.onChange, onBlur = _a.onBlur, value = _a.value, fieldProps = __rest(_a, ["onChange", "onBlur", "value"]);
            return (<RangeSlider {...fieldProps} value={value} onBlur={onBlur} onChange={function (val, event) { return onChange(fieldOnChange, val, event); }}/>);
        }}/>);
}
//# sourceMappingURL=rangeField.jsx.map
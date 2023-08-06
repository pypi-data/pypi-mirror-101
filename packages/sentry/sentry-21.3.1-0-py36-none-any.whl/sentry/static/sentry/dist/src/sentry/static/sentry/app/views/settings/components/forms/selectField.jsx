import { __extends, __rest } from "tslib";
import React from 'react';
import SelectControl from 'app/components/forms/selectControl';
import InputField from 'app/views/settings/components/forms/inputField';
function getChoices(props) {
    var choices = props.choices;
    if (typeof choices === 'function') {
        return choices(props);
    }
    if (choices === undefined) {
        return [];
    }
    return choices;
}
/**
 * Required to type guard for OptionsType<T> which is a readonly Array
 */
function isArray(maybe) {
    return Array.isArray(maybe);
}
var SelectField = /** @class */ (function (_super) {
    __extends(SelectField, _super);
    function SelectField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChange = function (onBlur, onChange, optionObj) {
            var value = undefined;
            // If optionObj is empty, then it probably means that the field was "cleared"
            if (!optionObj) {
                value = optionObj;
            }
            else if (_this.props.multiple && isArray(optionObj)) {
                // List of optionObjs
                value = optionObj.map(function (_a) {
                    var val = _a.value;
                    return val;
                });
            }
            else if (!isArray(optionObj)) {
                value = optionObj.value;
            }
            onChange === null || onChange === void 0 ? void 0 : onChange(value, {});
            onBlur === null || onBlur === void 0 ? void 0 : onBlur(value, {});
        };
        return _this;
    }
    SelectField.prototype.render = function () {
        var _this = this;
        var _a = this.props, multiple = _a.multiple, allowClear = _a.allowClear, small = _a.small, otherProps = __rest(_a, ["multiple", "allowClear", "small"]);
        return (<InputField {...otherProps} alignRight={small} field={function (_a) {
                var onChange = _a.onChange, onBlur = _a.onBlur, _required = _a.required, props = __rest(_a, ["onChange", "onBlur", "required"]);
                return (<SelectControl {...props} clearable={allowClear} multiple={multiple} onChange={_this.handleChange.bind(_this, onBlur, onChange)}/>);
            }}/>);
    };
    SelectField.defaultProps = {
        allowClear: false,
        allowEmpty: false,
        placeholder: '--',
        escapeMarkup: true,
        multiple: false,
        small: false,
        formatMessageValue: function (value, props) {
            return (getChoices(props).find(function (choice) { return choice[0] === value; }) || [null, value])[1];
        },
    };
    return SelectField;
}(React.Component));
export default SelectField;
//# sourceMappingURL=selectField.jsx.map
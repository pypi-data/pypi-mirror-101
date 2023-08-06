import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { StyledForm } from 'app/components/forms/form';
import SelectControl from 'app/components/forms/selectControl';
import SelectField from 'app/components/forms/selectField';
import { defined } from 'app/utils';
import convertFromSelect2Choices from 'app/utils/convertFromSelect2Choices';
/**
 * This is a <SelectField> that allows the user to create new options if one does't exist.
 *
 * This is used in some integrations
 */
var SelectCreatableField = /** @class */ (function (_super) {
    __extends(SelectCreatableField, _super);
    function SelectCreatableField(props, context) {
        var _this = _super.call(this, props, context) || this;
        // We only want to parse options once because react-select relies
        // on `options` mutation when you create a new option
        //
        // Otherwise you will not get the created option in the dropdown menu
        _this.options = _this.getOptions(props);
        return _this;
    }
    SelectCreatableField.prototype.UNSAFE_componentWillReceiveProps = function (nextProps, nextContext) {
        var newError = this.getError(nextProps, nextContext);
        if (newError !== this.state.error) {
            this.setState({ error: newError });
        }
        if (this.props.value !== nextProps.value || defined(nextContext.form)) {
            var newValue = this.getValue(nextProps, nextContext);
            // This is the only thing that is different from parent, we compare newValue against coerved value in state
            // To remain compatible with react-select, we need to store the option object that
            // includes `value` and `label`, but when we submit the format, we need to coerce it
            // to just return `value`. Also when field changes, it propagates the coerced value up
            var coercedValue = this.coerceValue(this.state.value);
            // newValue can be empty string because of `getValue`, while coerceValue needs to return null (to differentiate
            // empty string from cleared item). We could use `!=` to compare, but lets be a bit more explicit with strict equality
            //
            // This can happen when this is apart of a field, and it re-renders onChange for a different field,
            // there will be a mismatch between this component's state.value and `this.getValue` result above
            if (newValue !== coercedValue &&
                !!newValue !== !!coercedValue &&
                newValue !== this.state.value) {
                this.setValue(newValue);
            }
        }
    };
    SelectCreatableField.prototype.getOptions = function (props) {
        return convertFromSelect2Choices(props.choices) || props.options;
    };
    SelectCreatableField.prototype.getField = function () {
        var _a = this.props, deprecatedSelectControl = _a.deprecatedSelectControl, placeholder = _a.placeholder, disabled = _a.disabled, required = _a.required, clearable = _a.clearable, name = _a.name;
        return (<StyledSelectControl deprecatedSelectControl={deprecatedSelectControl} creatable id={this.getId()} options={this.options} placeholder={placeholder} disabled={disabled} required={required} value={this.state.value} onChange={this.onChange} clearable={clearable} multiple={this.isMultiple()} name={name}/>);
    };
    return SelectCreatableField;
}(SelectField));
export default SelectCreatableField;
// This is because we are removing `control-group` class name which provides margin-bottom
var StyledSelectControl = styled(SelectControl)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", " &, .form-stacked & {\n    .control-group & {\n      margin-bottom: 0;\n    }\n\n    margin-bottom: 15px;\n  }\n"], ["\n  ", " &, .form-stacked & {\n    .control-group & {\n      margin-bottom: 0;\n    }\n\n    margin-bottom: 15px;\n  }\n"])), StyledForm);
var templateObject_1;
//# sourceMappingURL=selectCreatableField.jsx.map
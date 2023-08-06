import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import BooleanField from './booleanField';
import ChoiceMapperField from './choiceMapperField';
import EmailField from './emailField';
import FieldSeparator from './fieldSeparator';
import HiddenField from './hiddenField';
import InputField from './inputField';
import NumberField from './numberField';
import ProjectMapperField from './projectMapperField';
import RadioField from './radioField';
import RangeField from './rangeField';
import RichListField from './richListField';
import SelectField from './selectField';
import SentryProjectSelectorField from './sentryProjectSelectorField';
import TableField from './tableField';
import TextareaField from './textareaField';
import TextField from './textField';
var FieldFromConfig = /** @class */ (function (_super) {
    __extends(FieldFromConfig, _super);
    function FieldFromConfig() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FieldFromConfig.prototype.render = function () {
        var _a = this.props, field = _a.field, otherProps = __rest(_a, ["field"]);
        var props = __assign(__assign({}, otherProps), field);
        switch (field.type) {
            case 'separator':
                return <FieldSeparator />;
            case 'secret':
                return <InputField {...props} type="password"/>;
            case 'range':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <RangeField {...props}/>;
            case 'bool':
            case 'boolean':
                return <BooleanField {...props}/>;
            case 'email':
                return <EmailField {...props}/>;
            case 'hidden':
                return <HiddenField {...props}/>;
            case 'string':
            case 'text':
            case 'url':
                if (props.multiline) {
                    return <TextareaField {...props}/>;
                }
                return <TextField {...props}/>;
            case 'number':
                return <NumberField {...props}/>;
            case 'textarea':
                return <TextareaField {...props}/>;
            case 'choice':
            case 'select':
            case 'array':
                return <SelectField {...props}/>;
            case 'choice_mapper':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <ChoiceMapperField {...props}/>;
            case 'radio':
                var choices = props.choices;
                if (!Array.isArray(choices)) {
                    throw new Error('Invalid `choices` type. Use an array of options');
                }
                return <RadioField {...props} choices={choices}/>;
            case 'rich_list':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <RichListField {...props}/>;
            case 'table':
                // TODO(ts) The switch on field.type is not resolving
                // the Field union for this component. The union might be 'too big'.
                return <TableField {...props}/>;
            case 'project_mapper':
                return <ProjectMapperField {...props}/>;
            case 'sentry_project_selector':
                return <SentryProjectSelectorField {...props}/>;
            case 'custom':
                return field.Component(props);
            default:
                return null;
        }
    };
    return FieldFromConfig;
}(React.Component));
export default FieldFromConfig;
//# sourceMappingURL=fieldFromConfig.jsx.map
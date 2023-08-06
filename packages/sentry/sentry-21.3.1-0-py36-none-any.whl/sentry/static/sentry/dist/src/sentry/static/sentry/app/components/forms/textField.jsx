import { __extends } from "tslib";
import InputField from 'app/components/forms/inputField';
var TextField = /** @class */ (function (_super) {
    __extends(TextField, _super);
    function TextField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TextField.prototype.getAttributes = function () {
        return {
            spellCheck: this.props.spellCheck,
        };
    };
    TextField.prototype.getType = function () {
        return 'text';
    };
    return TextField;
}(InputField));
export default TextField;
//# sourceMappingURL=textField.jsx.map
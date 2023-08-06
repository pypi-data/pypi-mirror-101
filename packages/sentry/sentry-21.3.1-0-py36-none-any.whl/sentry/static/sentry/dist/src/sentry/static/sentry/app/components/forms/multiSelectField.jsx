import { __extends } from "tslib";
import SelectField from 'app/components/forms/selectField';
var MultiSelectField = /** @class */ (function (_super) {
    __extends(MultiSelectField, _super);
    function MultiSelectField() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MultiSelectField.prototype.isMultiple = function () {
        return true;
    };
    return MultiSelectField;
}(SelectField));
export default MultiSelectField;
//# sourceMappingURL=multiSelectField.jsx.map
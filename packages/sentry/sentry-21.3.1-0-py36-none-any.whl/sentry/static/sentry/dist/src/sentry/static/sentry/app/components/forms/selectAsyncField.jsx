import { __assign, __extends } from "tslib";
import React from 'react';
import SelectAsyncControl from './selectAsyncControl';
import SelectField from './selectField';
var SelectAsyncField = /** @class */ (function (_super) {
    __extends(SelectAsyncField, _super);
    function SelectAsyncField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.onResults = function (data) {
            var name = _this.props.name;
            var results = data && data[name];
            return (results && results.map(function (_a) {
                var id = _a.id, text = _a.text;
                return ({ value: id, label: text });
            })) || [];
        };
        _this.onQuery = function (query) {
            // Used by legacy integrations
            return ({ autocomplete_query: query, autocomplete_field: _this.props.name });
        };
        return _this;
    }
    SelectAsyncField.prototype.getField = function () {
        // Callers should be able to override all props except onChange
        // FormField calls props.onChange via `setValue`
        return (<SelectAsyncControl id={this.getId()} onResults={this.onResults} onQuery={this.onQuery} {...this.props} value={this.state.value} onChange={this.onChange}/>);
    };
    SelectAsyncField.defaultProps = __assign(__assign({}, SelectField.defaultProps), { placeholder: 'Start typing to search for an issue' });
    return SelectAsyncField;
}(SelectField));
export default SelectAsyncField;
//# sourceMappingURL=selectAsyncField.jsx.map
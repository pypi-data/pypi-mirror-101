import { __assign, __awaiter, __extends, __generator, __rest } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { loadSearchMap } from 'app/actionCreators/formSearch';
import FormSearchStore from 'app/stores/formSearchStore';
import { createFuzzySearch } from 'app/utils/createFuzzySearch';
import replaceRouterParams from 'app/utils/replaceRouterParams';
var FormSource = /** @class */ (function (_super) {
    __extends(FormSource, _super);
    function FormSource() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            fuzzy: null,
        };
        return _this;
    }
    FormSource.prototype.componentDidMount = function () {
        this.createSearch(this.props.searchMap);
    };
    FormSource.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.searchMap !== prevProps.searchMap) {
            this.createSearch(this.props.searchMap);
        }
    };
    FormSource.prototype.createSearch = function (searchMap) {
        return __awaiter(this, void 0, void 0, function () {
            var _a;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.setState;
                        _b = {};
                        return [4 /*yield*/, createFuzzySearch(searchMap || [], __assign(__assign({}, this.props.searchOptions), { keys: ['title', 'description'] }))];
                    case 1:
                        _a.apply(this, [(_b.fuzzy = _c.sent(),
                                _b)]);
                        return [2 /*return*/];
                }
            });
        });
    };
    FormSource.prototype.render = function () {
        var _a = this.props, searchMap = _a.searchMap, query = _a.query, params = _a.params, children = _a.children;
        var results = [];
        if (this.state.fuzzy) {
            var rawResults = this.state.fuzzy.search(query);
            results = rawResults.map(function (value) {
                var item = value.item, rest = __rest(value, ["item"]);
                return __assign({ item: __assign(__assign({}, item), { sourceType: 'field', resultType: 'field', to: replaceRouterParams(item.route, params) + "#" + encodeURIComponent(item.field.name) }) }, rest);
            });
        }
        return children({
            isLoading: searchMap === null,
            results: results,
        });
    };
    FormSource.defaultProps = {
        searchOptions: {},
    };
    return FormSource;
}(React.Component));
var FormSourceContainer = withRouter(createReactClass({
    displayName: 'FormSourceContainer',
    mixins: [Reflux.connect(FormSearchStore, 'searchMap')],
    componentDidMount: function () {
        // Loads form fields
        loadSearchMap();
    },
    render: function () {
        return <FormSource searchMap={this.state.searchMap} {...this.props}/>;
    },
}));
export default FormSourceContainer;
//# sourceMappingURL=formSource.jsx.map
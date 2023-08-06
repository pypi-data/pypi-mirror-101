import { __assign, __awaiter, __extends, __generator, __rest } from "tslib";
import React from 'react';
import { openHelpSearchModal, openSudo } from 'app/actionCreators/modal';
import Access from 'app/components/acl/access';
import { toggleLocaleDebug } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import { createFuzzySearch } from 'app/utils/createFuzzySearch';
var ACTIONS = [
    {
        title: 'Open Sudo Modal',
        description: 'Open Sudo Modal to re-identify yourself.',
        requiresSuperuser: false,
        action: function () {
            return openSudo({
                sudo: true,
            });
        },
    },
    {
        title: 'Open Superuser Modal',
        description: 'Open Superuser Modal to re-identify yourself.',
        requiresSuperuser: true,
        action: function () {
            return openSudo({
                superuser: true,
            });
        },
    },
    {
        title: 'Toggle dark mode',
        description: 'Toggle dark mode (superuser only atm)',
        requiresSuperuser: true,
        action: function () {
            return ConfigStore.set('theme', ConfigStore.get('theme') === 'dark' ? 'light' : 'dark');
        },
    },
    {
        title: 'Toggle Translation Markers',
        description: 'Toggles translation markers on or off in the application',
        requiresSuperuser: true,
        action: function () {
            toggleLocaleDebug();
            window.location.reload();
        },
    },
    {
        title: 'Search Documentation and FAQ',
        description: 'Open the Documentation and FAQ search modal.',
        requiresSuperuser: false,
        action: function () {
            openHelpSearchModal();
        },
    },
];
/**
 * This source is a hardcoded list of action creators and/or routes maybe
 */
var CommandSource = /** @class */ (function (_super) {
    __extends(CommandSource, _super);
    function CommandSource() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            fuzzy: null,
        };
        return _this;
    }
    CommandSource.prototype.componentDidMount = function () {
        this.createSearch(ACTIONS);
    };
    CommandSource.prototype.createSearch = function (searchMap) {
        return __awaiter(this, void 0, void 0, function () {
            var options, _a;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        options = __assign(__assign({}, this.props.searchOptions), { keys: ['title', 'description'] });
                        _a = this.setState;
                        _b = {};
                        return [4 /*yield*/, createFuzzySearch(searchMap || [], options)];
                    case 1:
                        _a.apply(this, [(_b.fuzzy = _c.sent(),
                                _b)]);
                        return [2 /*return*/];
                }
            });
        });
    };
    CommandSource.prototype.render = function () {
        var _a = this.props, searchMap = _a.searchMap, query = _a.query, isSuperuser = _a.isSuperuser, children = _a.children;
        var results = [];
        if (this.state.fuzzy) {
            var rawResults = this.state.fuzzy.search(query);
            results = rawResults
                .filter(function (_a) {
                var item = _a.item;
                return !item.requiresSuperuser || isSuperuser;
            })
                .map(function (value) {
                var item = value.item, rest = __rest(value, ["item"]);
                return __assign({ item: __assign(__assign({}, item), { sourceType: 'command', resultType: 'command' }) }, rest);
            });
        }
        return children({
            isLoading: searchMap === null,
            results: results,
        });
    };
    CommandSource.defaultProps = {
        searchMap: [],
        searchOptions: {},
    };
    return CommandSource;
}(React.Component));
var CommandSourceWithFeature = function (props) { return (<Access isSuperuser>
    {function (_a) {
    var hasSuperuser = _a.hasSuperuser;
    return <CommandSource {...props} isSuperuser={hasSuperuser}/>;
}}
  </Access>); };
export default CommandSourceWithFeature;
export { CommandSource };
//# sourceMappingURL=commandSource.jsx.map
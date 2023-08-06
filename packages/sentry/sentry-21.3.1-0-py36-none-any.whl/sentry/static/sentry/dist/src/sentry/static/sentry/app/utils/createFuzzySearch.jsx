import { __assign, __awaiter, __generator } from "tslib";
import { DEFAULT_FUSE_OPTIONS } from 'app/constants';
export function loadFuzzySearch() {
    return import(/* webpackChunkName: "Fuse" */ 'fuse.js');
}
export function createFuzzySearch(objects, options) {
    return __awaiter(this, void 0, void 0, function () {
        var Fuse, opts;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!options.keys) {
                        throw new Error('You need to define `options.keys`');
                    }
                    return [4 /*yield*/, loadFuzzySearch()];
                case 1:
                    Fuse = (_a.sent()).default;
                    opts = __assign(__assign({}, DEFAULT_FUSE_OPTIONS), options);
                    return [2 /*return*/, new Fuse(objects, opts)];
            }
        });
    });
}
//# sourceMappingURL=createFuzzySearch.jsx.map
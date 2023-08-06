import { __awaiter, __generator } from "tslib";
export function getPreloadedDataPromise(name, slug, fallback, isInitialFetch) {
    return __awaiter(this, void 0, void 0, function () {
        var data, result, _1;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 6, , 7]);
                    data = window.__sentry_preload;
                    if (!(!isInitialFetch ||
                        !data ||
                        !data.orgSlug ||
                        data.orgSlug.toLowerCase() !== slug.toLowerCase() ||
                        !data[name] ||
                        !data[name].then)) return [3 /*break*/, 2];
                    return [4 /*yield*/, fallback()];
                case 1: return [2 /*return*/, _a.sent()];
                case 2: return [4 /*yield*/, data[name].catch(fallback)];
                case 3:
                    result = _a.sent();
                    if (!!result) return [3 /*break*/, 5];
                    return [4 /*yield*/, fallback()];
                case 4: return [2 /*return*/, _a.sent()];
                case 5: return [3 /*break*/, 7];
                case 6:
                    _1 = _a.sent();
                    return [3 /*break*/, 7];
                case 7: return [4 /*yield*/, fallback()];
                case 8: return [2 /*return*/, _a.sent()];
            }
        });
    });
}
//# sourceMappingURL=getPreloadedData.js.map
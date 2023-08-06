import { __awaiter, __generator } from "tslib";
import SdkUpdatesActions from 'app/actions/sdkUpdatesActions';
/**
 * Load SDK Updates for a specific organization
 */
export function loadSdkUpdates(api, orgSlug) {
    return __awaiter(this, void 0, void 0, function () {
        var updates;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/sdk-updates/")];
                case 1:
                    updates = _a.sent();
                    SdkUpdatesActions.load(orgSlug, updates);
                    return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=sdkUpdates.jsx.map
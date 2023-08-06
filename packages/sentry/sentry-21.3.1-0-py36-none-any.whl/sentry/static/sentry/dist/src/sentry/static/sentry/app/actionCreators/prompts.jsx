import { __assign, __awaiter, __generator } from "tslib";
/**
 * Update the status of a prompt
 */
export function promptsUpdate(api, params) {
    return api.requestPromise('/prompts-activity/', {
        method: 'PUT',
        data: {
            organization_id: params.organizationId,
            project_id: params.projectId,
            feature: params.feature,
            status: params.status,
        },
    });
}
/**
 * Get the status of a prompt
 */
export function promptsCheck(api, params) {
    return __awaiter(this, void 0, void 0, function () {
        var query, response, data;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    query = __assign({ feature: params.feature, organization_id: params.organizationId }, (params.projectId === undefined ? {} : { project_id: params.projectId }));
                    return [4 /*yield*/, api.requestPromise('/prompts-activity/', {
                            query: query,
                        })];
                case 1:
                    response = _a.sent();
                    data = response === null || response === void 0 ? void 0 : response.data;
                    if (!data) {
                        return [2 /*return*/, null];
                    }
                    return [2 /*return*/, {
                            dismissedTime: data.dismissed_ts,
                            snoozedTime: data.snoozed_ts,
                        }];
            }
        });
    });
}
//# sourceMappingURL=prompts.jsx.map
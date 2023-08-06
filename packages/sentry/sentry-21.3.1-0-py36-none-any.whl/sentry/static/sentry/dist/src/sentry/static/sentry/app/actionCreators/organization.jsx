import { __awaiter, __generator, __read } from "tslib";
import * as Sentry from '@sentry/react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { setActiveOrganization } from 'app/actionCreators/organizations';
import GlobalSelectionActions from 'app/actions/globalSelectionActions';
import OrganizationActions from 'app/actions/organizationActions';
import ProjectActions from 'app/actions/projectActions';
import TeamActions from 'app/actions/teamActions';
import { Client } from 'app/api';
import ProjectsStore from 'app/stores/projectsStore';
import TeamStore from 'app/stores/teamStore';
import { getPreloadedDataPromise } from 'app/utils/getPreloadedData';
function fetchOrg(api, slug, detailed, isInitialFetch) {
    return __awaiter(this, void 0, void 0, function () {
        var org;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, getPreloadedDataPromise('organization', slug, function () {
                        // This data should get preloaded in static/sentry/index.ejs
                        // If this url changes make sure to update the preload
                        return api.requestPromise("/organizations/" + slug + "/", {
                            query: { detailed: detailed ? 1 : 0 },
                        });
                    }, isInitialFetch)];
                case 1:
                    org = _a.sent();
                    if (!org) {
                        throw new Error('retrieved organization is falsey');
                    }
                    OrganizationActions.update(org, { replace: true });
                    setActiveOrganization(org);
                    return [2 /*return*/, org];
            }
        });
    });
}
function fetchProjectsAndTeams(slug, isInitialFetch) {
    return __awaiter(this, void 0, void 0, function () {
        var uncancelableApi, _a, projects, teams, err_1;
        return __generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    uncancelableApi = new Client();
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, Promise.all([
                            getPreloadedDataPromise('projects', slug, function () {
                                // This data should get preloaded in static/sentry/index.ejs
                                // If this url changes make sure to update the preload
                                return uncancelableApi.requestPromise("/organizations/" + slug + "/projects/", {
                                    query: {
                                        all_projects: 1,
                                        collapse: 'latestDeploys',
                                    },
                                });
                            }, isInitialFetch),
                            getPreloadedDataPromise('teams', slug, 
                            // This data should get preloaded in static/sentry/index.ejs
                            // If this url changes make sure to update the preload
                            function () { return uncancelableApi.requestPromise("/organizations/" + slug + "/teams/"); }, isInitialFetch),
                        ])];
                case 2:
                    _a = __read.apply(void 0, [_b.sent(), 2]), projects = _a[0], teams = _a[1];
                    return [2 /*return*/, [projects, teams]];
                case 3:
                    err_1 = _b.sent();
                    // It's possible these requests fail with a 403 if the user has a role with insufficient access
                    // to projects and teams, but *can* access org details (e.g. billing).
                    // An example of this is in org settings.
                    //
                    // Ignore 403s and bubble up other API errors
                    if (err_1.status !== 403) {
                        throw err_1;
                    }
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/, [[], []]];
            }
        });
    });
}
/**
 * Fetches an organization's details with an option for the detailed representation
 * with teams and projects
 *
 * @param api A reference to the api client
 * @param slug The organization slug
 * @param detailed Whether or not the detailed org details should be retrieved
 * @param silent Should we silently update the organization (do not clear the
 *               current organization in the store)
 */
export function fetchOrganizationDetails(api, slug, detailed, silent, isInitialFetch) {
    var _a, _b, _c, _d, _e;
    return __awaiter(this, void 0, void 0, function () {
        var promises, _f, org, projectsAndTeams, _g, projects, teams, err_2, errMessage;
        return __generator(this, function (_h) {
            switch (_h.label) {
                case 0:
                    if (!silent) {
                        OrganizationActions.fetchOrg();
                        ProjectActions.reset();
                        GlobalSelectionActions.reset();
                    }
                    _h.label = 1;
                case 1:
                    _h.trys.push([1, 3, , 4]);
                    promises = [fetchOrg(api, slug, detailed, isInitialFetch)];
                    if (!detailed) {
                        promises.push(fetchProjectsAndTeams(slug, isInitialFetch));
                    }
                    return [4 /*yield*/, Promise.all(promises)];
                case 2:
                    _f = __read.apply(void 0, [_h.sent(), 2]), org = _f[0], projectsAndTeams = _f[1];
                    if (!detailed) {
                        _g = __read(projectsAndTeams, 2), projects = _g[0], teams = _g[1];
                        ProjectActions.loadProjects(projects);
                        TeamActions.loadTeams(teams);
                    }
                    if (org && detailed) {
                        // TODO(davidenwang): Change these to actions after organization.projects
                        // and organization.teams no longer exists. Currently if they were changed
                        // to actions it would cause OrganizationContext to rerender many times
                        TeamStore.loadInitialData(org.teams);
                        ProjectsStore.loadInitialData(org.projects);
                    }
                    return [3 /*break*/, 4];
                case 3:
                    err_2 = _h.sent();
                    if (!err_2) {
                        return [2 /*return*/];
                    }
                    OrganizationActions.fetchOrgError(err_2);
                    if (err_2.status === 403 || err_2.status === 401) {
                        errMessage = typeof ((_a = err_2.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === 'string'
                            ? (_b = err_2.responseJSON) === null || _b === void 0 ? void 0 : _b.detail
                            : typeof ((_d = (_c = err_2.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.message) === 'string'
                                ? (_e = err_2.responseJSON) === null || _e === void 0 ? void 0 : _e.detail.message
                                : null;
                        if (errMessage) {
                            addErrorMessage(errMessage);
                        }
                        return [2 /*return*/];
                    }
                    Sentry.captureException(err_2);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
//# sourceMappingURL=organization.jsx.map
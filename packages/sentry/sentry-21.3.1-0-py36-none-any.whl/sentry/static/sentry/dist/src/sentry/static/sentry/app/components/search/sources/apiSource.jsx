import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import * as Sentry from '@sentry/react';
import debounce from 'lodash/debounce';
import flatten from 'lodash/flatten';
import { Client } from 'app/api';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import { createFuzzySearch } from 'app/utils/createFuzzySearch';
import { singleLineRenderer as markedSingleLine } from 'app/utils/marked';
import withLatestContext from 'app/utils/withLatestContext';
import { documentIntegrationList } from 'app/views/organizationIntegrations/constants';
// event ids must have string length of 32
var shouldSearchEventIds = function (query) {
    return typeof query === 'string' && query.length === 32;
};
// STRING-HEXVAL
var shouldSearchShortIds = function (query) { return /[\w\d]+-[\w\d]+/.test(query); };
// Helper functions to create result objects
function createOrganizationResults(organizationsPromise) {
    return __awaiter(this, void 0, void 0, function () {
        var organizations;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, organizationsPromise];
                case 1:
                    organizations = (_a.sent()) || [];
                    return [2 /*return*/, flatten(organizations.map(function (org) { return [
                            {
                                title: t('%s Dashboard', org.slug),
                                description: t('Organization Dashboard'),
                                model: org,
                                sourceType: 'organization',
                                resultType: 'route',
                                to: "/" + org.slug + "/",
                            },
                            {
                                title: t('%s Settings', org.slug),
                                description: t('Organization Settings'),
                                model: org,
                                sourceType: 'organization',
                                resultType: 'settings',
                                to: "/settings/" + org.slug + "/",
                            },
                        ]; }))];
            }
        });
    });
}
function createProjectResults(projectsPromise, orgId, orgFeatures) {
    return __awaiter(this, void 0, void 0, function () {
        var projects;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, projectsPromise];
                case 1:
                    projects = (_a.sent()) || [];
                    return [2 /*return*/, flatten(projects.map(function (project) {
                            var projectResults = [
                                {
                                    title: t('%s Settings', project.slug),
                                    description: t('Project Settings'),
                                    model: project,
                                    sourceType: 'project',
                                    resultType: 'settings',
                                    to: "/settings/" + orgId + "/projects/" + project.slug + "/",
                                },
                            ];
                            if (orgFeatures === null || orgFeatures === void 0 ? void 0 : orgFeatures.includes('project-detail')) {
                                projectResults.unshift({
                                    title: t('%s Dashboard', project.slug),
                                    description: t('Project Details'),
                                    model: project,
                                    sourceType: 'project',
                                    resultType: 'route',
                                    to: "/organizations/" + orgId + "/projects/" + project.slug + "/?project=" + project.id,
                                });
                            }
                            return projectResults;
                        }))];
            }
        });
    });
}
function createTeamResults(teamsPromise, orgId) {
    return __awaiter(this, void 0, void 0, function () {
        var teams;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, teamsPromise];
                case 1:
                    teams = (_a.sent()) || [];
                    return [2 /*return*/, teams.map(function (team) { return ({
                            title: "#" + team.slug,
                            description: 'Team Settings',
                            model: team,
                            sourceType: 'team',
                            resultType: 'settings',
                            to: "/settings/" + orgId + "/teams/" + team.slug + "/",
                        }); })];
            }
        });
    });
}
function createMemberResults(membersPromise, orgId) {
    return __awaiter(this, void 0, void 0, function () {
        var members;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, membersPromise];
                case 1:
                    members = (_a.sent()) || [];
                    return [2 /*return*/, members.map(function (member) { return ({
                            title: member.name,
                            description: member.email,
                            model: member,
                            sourceType: 'member',
                            resultType: 'settings',
                            to: "/settings/" + orgId + "/members/" + member.id + "/",
                        }); })];
            }
        });
    });
}
function createPluginResults(pluginsPromise, orgId) {
    return __awaiter(this, void 0, void 0, function () {
        var plugins;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, pluginsPromise];
                case 1:
                    plugins = (_a.sent()) || [];
                    return [2 /*return*/, plugins
                            .filter(function (plugin) {
                            //show a plugin if it is not hidden (aka legacy) or if we have projects with it configured
                            return !plugin.isHidden || !!plugin.projectList.length;
                        })
                            .map(function (plugin) {
                            var _a;
                            return ({
                                title: plugin.isHidden ? plugin.name + " (Legacy)" : plugin.name,
                                description: (<span dangerouslySetInnerHTML={{
                                        __html: markedSingleLine((_a = plugin.description) !== null && _a !== void 0 ? _a : ''),
                                    }}/>),
                                model: plugin,
                                sourceType: 'plugin',
                                resultType: 'integration',
                                to: "/settings/" + orgId + "/plugins/" + plugin.id + "/",
                            });
                        })];
            }
        });
    });
}
function createIntegrationResults(integrationsPromise, orgId) {
    return __awaiter(this, void 0, void 0, function () {
        var providers;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, integrationsPromise];
                case 1:
                    providers = ((_a.sent()) || {}).providers;
                    return [2 /*return*/, ((providers &&
                            providers.map(function (provider) { return ({
                                title: provider.name,
                                description: (<span dangerouslySetInnerHTML={{
                                        __html: markedSingleLine(provider.metadata.description),
                                    }}/>),
                                model: provider,
                                sourceType: 'integration',
                                resultType: 'integration',
                                to: "/settings/" + orgId + "/integrations/" + provider.slug + "/",
                            }); })) ||
                            [])];
            }
        });
    });
}
function createSentryAppResults(sentryAppPromise, orgId) {
    return __awaiter(this, void 0, void 0, function () {
        var sentryApps;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, sentryAppPromise];
                case 1:
                    sentryApps = (_a.sent()) || [];
                    return [2 /*return*/, sentryApps.map(function (sentryApp) { return ({
                            title: sentryApp.name,
                            description: (<span dangerouslySetInnerHTML={{
                                    __html: markedSingleLine(sentryApp.overview || ''),
                                }}/>),
                            model: sentryApp,
                            sourceType: 'sentryApp',
                            resultType: 'integration',
                            to: "/settings/" + orgId + "/sentry-apps/" + sentryApp.slug + "/",
                        }); })];
            }
        });
    });
}
//Not really async but we need to return a promise
function creatDocIntegrationResults(orgId) {
    return __awaiter(this, void 0, void 0, function () {
        return __generator(this, function (_a) {
            return [2 /*return*/, documentIntegrationList.map(function (integration) { return ({
                    title: integration.name,
                    description: (<span dangerouslySetInnerHTML={{
                            __html: markedSingleLine(integration.description),
                        }}/>),
                    model: integration,
                    sourceType: 'docIntegration',
                    resultType: 'integration',
                    to: "/settings/" + orgId + "/document-integrations/" + integration.slug + "/",
                }); })];
        });
    });
}
function createShortIdLookupResult(shortIdLookupPromise) {
    return __awaiter(this, void 0, void 0, function () {
        var shortIdLookup, issue;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, shortIdLookupPromise];
                case 1:
                    shortIdLookup = _a.sent();
                    if (!shortIdLookup) {
                        return [2 /*return*/, null];
                    }
                    issue = shortIdLookup && shortIdLookup.group;
                    return [2 /*return*/, {
                            item: {
                                title: "" + ((issue && issue.metadata && issue.metadata.type) || shortIdLookup.shortId),
                                description: "" + ((issue && issue.metadata && issue.metadata.value) || t('Issue')),
                                model: shortIdLookup.group,
                                sourceType: 'issue',
                                resultType: 'issue',
                                to: "/" + shortIdLookup.organizationSlug + "/" + shortIdLookup.projectSlug + "/issues/" + shortIdLookup.groupId + "/",
                            },
                            score: 1,
                        }];
            }
        });
    });
}
function createEventIdLookupResult(eventIdLookupPromise) {
    return __awaiter(this, void 0, void 0, function () {
        var eventIdLookup, event;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, eventIdLookupPromise];
                case 1:
                    eventIdLookup = _a.sent();
                    if (!eventIdLookup) {
                        return [2 /*return*/, null];
                    }
                    event = eventIdLookup && eventIdLookup.event;
                    return [2 /*return*/, {
                            item: {
                                title: "" + ((event && event.metadata && event.metadata.type) || t('Event')),
                                description: "" + (event && event.metadata && event.metadata.value),
                                sourceType: 'event',
                                resultType: 'event',
                                to: "/" + eventIdLookup.organizationSlug + "/" + eventIdLookup.projectSlug + "/issues/" + eventIdLookup.groupId + "/events/" + eventIdLookup.eventId + "/",
                            },
                            score: 1,
                        }];
            }
        });
    });
}
var ApiSource = /** @class */ (function (_super) {
    __extends(ApiSource, _super);
    function ApiSource() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
            searchResults: null,
            directResults: null,
            fuzzy: null,
        };
        _this.api = new Client();
        // Debounced method to handle querying all API endpoints (when necessary)
        _this.doSearch = debounce(function (query) { return __awaiter(_this, void 0, void 0, function () {
            var _a, params, organization, orgId, searchUrls, directUrls, searchRequests, directRequests;
            var _this = this;
            return __generator(this, function (_b) {
                _a = this.props, params = _a.params, organization = _a.organization;
                orgId = (params && params.orgId) || (organization && organization.slug);
                searchUrls = ['/organizations/'];
                directUrls = [];
                // Only run these queries when we have an org in context
                if (orgId) {
                    searchUrls = __spreadArray(__spreadArray([], __read(searchUrls)), [
                        "/organizations/" + orgId + "/projects/",
                        "/organizations/" + orgId + "/teams/",
                        "/organizations/" + orgId + "/members/",
                        "/organizations/" + orgId + "/plugins/configs/",
                        "/organizations/" + orgId + "/config/integrations/",
                        '/sentry-apps/?status=published',
                    ]);
                    directUrls = [
                        shouldSearchShortIds(query) ? "/organizations/" + orgId + "/shortids/" + query + "/" : null,
                        shouldSearchEventIds(query) ? "/organizations/" + orgId + "/eventids/" + query + "/" : null,
                    ];
                }
                searchRequests = searchUrls.map(function (url) {
                    return _this.api
                        .requestPromise(url, {
                        query: {
                            query: query,
                        },
                    })
                        .then(function (resp) { return resp; }, function (err) {
                        _this.handleRequestError(err, { orgId: orgId, url: url });
                        return null;
                    });
                });
                directRequests = directUrls.map(function (url) {
                    if (!url) {
                        return Promise.resolve(null);
                    }
                    return _this.api.requestPromise(url).then(function (resp) { return resp; }, function (err) {
                        // No need to log 404 errors
                        if (err && err.status === 404) {
                            return null;
                        }
                        _this.handleRequestError(err, { orgId: orgId, url: url });
                        return null;
                    });
                });
                this.handleSearchRequest(searchRequests, directRequests);
                return [2 /*return*/];
            });
        }); }, 150);
        _this.handleRequestError = function (err, _a) {
            var url = _a.url, orgId = _a.orgId;
            Sentry.withScope(function (scope) {
                scope.setExtra('url', url.replace("/organizations/" + orgId + "/", '/organizations/:orgId/'));
                Sentry.captureException(new Error("API Source Failed: " + (err && err.responseJSON && err.responseJSON.detail)));
            });
        };
        return _this;
    }
    ApiSource.prototype.componentDidMount = function () {
        if (typeof this.props.query !== 'undefined') {
            this.doSearch(this.props.query);
        }
    };
    ApiSource.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        // Limit the number of times we perform API queries by only attempting API queries
        // using first two characters, otherwise perform in-memory search.
        //
        // Otherwise it'd be constant :spinning_loading_wheel:
        if ((nextProps.query.length <= 2 &&
            nextProps.query.substr(0, 2) !== this.props.query.substr(0, 2)) ||
            // Also trigger a search if next query value satisfies an eventid/shortid query
            shouldSearchShortIds(nextProps.query) ||
            shouldSearchEventIds(nextProps.query)) {
            this.setState({ loading: true });
            this.doSearch(nextProps.query);
        }
    };
    // Handles a list of search request promises, and then updates state with response objects
    ApiSource.prototype.handleSearchRequest = function (searchRequests, directRequests) {
        return __awaiter(this, void 0, void 0, function () {
            var searchOptions, _a, organizations, projects, teams, members, plugins, integrations, sentryApps, _b, shortIdLookup, eventIdLookup, _c, searchResults, directResults, fuzzy, _d;
            var _e;
            return __generator(this, function (_f) {
                switch (_f.label) {
                    case 0:
                        searchOptions = this.props.searchOptions;
                        _a = __read(searchRequests, 7), organizations = _a[0], projects = _a[1], teams = _a[2], members = _a[3], plugins = _a[4], integrations = _a[5], sentryApps = _a[6];
                        _b = __read(directRequests, 2), shortIdLookup = _b[0], eventIdLookup = _b[1];
                        return [4 /*yield*/, Promise.all([
                                this.getSearchableResults([
                                    organizations,
                                    projects,
                                    teams,
                                    members,
                                    plugins,
                                    integrations,
                                    sentryApps,
                                ]),
                                this.getDirectResults([shortIdLookup, eventIdLookup]),
                            ])];
                    case 1:
                        _c = __read.apply(void 0, [_f.sent(), 2]), searchResults = _c[0], directResults = _c[1];
                        fuzzy = createFuzzySearch(searchResults, __assign(__assign({}, searchOptions), { keys: ['title', 'description'] }));
                        _d = this.setState;
                        _e = {
                            loading: false
                        };
                        return [4 /*yield*/, fuzzy];
                    case 2:
                        _d.apply(this, [(_e.fuzzy = _f.sent(),
                                _e.directResults = directResults,
                                _e)]);
                        return [2 /*return*/];
                }
            });
        });
    };
    // Process API requests that create result objects that should be searchable
    ApiSource.prototype.getSearchableResults = function (requests) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, params, organization, orgId, _b, organizations, projects, teams, members, plugins, integrations, sentryApps, searchResults, _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _a = this.props, params = _a.params, organization = _a.organization;
                        orgId = (params && params.orgId) || (organization && organization.slug);
                        _b = __read(requests, 7), organizations = _b[0], projects = _b[1], teams = _b[2], members = _b[3], plugins = _b[4], integrations = _b[5], sentryApps = _b[6];
                        _c = flatten;
                        return [4 /*yield*/, Promise.all([
                                createOrganizationResults(organizations),
                                createProjectResults(projects, orgId, organization === null || organization === void 0 ? void 0 : organization.features),
                                createTeamResults(teams, orgId),
                                createMemberResults(members, orgId),
                                createIntegrationResults(integrations, orgId),
                                createPluginResults(plugins, orgId),
                                createSentryAppResults(sentryApps, orgId),
                                creatDocIntegrationResults(orgId),
                            ])];
                    case 1:
                        searchResults = _c.apply(void 0, [_d.sent()]);
                        return [2 /*return*/, searchResults];
                }
            });
        });
    };
    // Create result objects from API requests that do not require fuzzy search
    // i.e. these responses only return 1 object or they should always be displayed regardless of query input
    ApiSource.prototype.getDirectResults = function (requests) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, shortIdLookup, eventIdLookup, directResults;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = __read(requests, 2), shortIdLookup = _a[0], eventIdLookup = _a[1];
                        return [4 /*yield*/, Promise.all([
                                createShortIdLookupResult(shortIdLookup),
                                createEventIdLookupResult(eventIdLookup),
                            ])];
                    case 1:
                        directResults = (_b.sent()).filter(defined);
                        if (!directResults.length) {
                            return [2 /*return*/, []];
                        }
                        return [2 /*return*/, directResults];
                }
            });
        });
    };
    ApiSource.prototype.render = function () {
        var _a = this.props, children = _a.children, query = _a.query;
        var _b = this.state, fuzzy = _b.fuzzy, directResults = _b.directResults;
        var results = [];
        if (fuzzy) {
            results = fuzzy.search(query);
        }
        return children({
            isLoading: this.state.loading,
            results: flatten([results, directResults].filter(defined)) || [],
        });
    };
    ApiSource.defaultProps = {
        searchOptions: {},
    };
    return ApiSource;
}(React.Component));
export { ApiSource };
export default withLatestContext(withRouter(ApiSource));
//# sourceMappingURL=apiSource.jsx.map
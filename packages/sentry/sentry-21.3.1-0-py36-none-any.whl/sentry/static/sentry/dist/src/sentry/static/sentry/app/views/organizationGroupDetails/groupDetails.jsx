import { __assign, __awaiter, __extends, __generator, __read } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import * as ReactRouter from 'react-router';
import * as Sentry from '@sentry/react';
import PropTypes from 'prop-types';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import MissingProjectMembership from 'app/components/projects/missingProjectMembership';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import GroupStore from 'app/stores/groupStore';
import { PageContent } from 'app/styles/organization';
import { callIfFunction } from 'app/utils/callIfFunction';
import { getMessage, getTitle } from 'app/utils/events';
import Projects from 'app/utils/projects';
import recreateRoute from 'app/utils/recreateRoute';
import withApi from 'app/utils/withApi';
import { ERROR_TYPES } from './constants';
import GroupHeader, { TAB } from './header';
import { fetchGroupEvent, getGroupReprocessingStatus, markEventSeen, ReprocessingStatus, } from './utils';
var GroupDetails = /** @class */ (function (_super) {
    __extends(GroupDetails, _super);
    function GroupDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.initialState;
        _this.remountComponent = function () {
            _this.setState(_this.initialState);
            _this.fetchData();
        };
        _this.refetchGroup = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, loadingGroup, loading, loadingEvent, group, api, updatedGroup, reprocessingNewRoute, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.state, loadingGroup = _a.loadingGroup, loading = _a.loading, loadingEvent = _a.loadingEvent, group = _a.group;
                        if ((group === null || group === void 0 ? void 0 : group.status) !== ReprocessingStatus.REPROCESSING ||
                            loadingGroup ||
                            loading ||
                            loadingEvent) {
                            return [2 /*return*/];
                        }
                        api = this.props.api;
                        this.setState({ loadingGroup: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(this.groupDetailsEndpoint, {
                                query: this.getGroupQuery(),
                            })];
                    case 2:
                        updatedGroup = _b.sent();
                        reprocessingNewRoute = this.getReprocessingNewRoute(updatedGroup);
                        if (reprocessingNewRoute) {
                            ReactRouter.browserHistory.push(reprocessingNewRoute);
                            return [2 /*return*/];
                        }
                        this.setState({ group: updatedGroup, loadingGroup: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.handleRequestError(error_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.listener = GroupStore.listen(function (itemIds) { return _this.onGroupChange(itemIds); }, undefined);
        _this.interval = undefined;
        return _this;
    }
    GroupDetails.prototype.getChildContext = function () {
        return {
            group: this.state.group,
            location: this.props.location,
        };
    };
    GroupDetails.prototype.componentDidMount = function () {
        this.fetchData();
        this.updateReprocessingProgress();
    };
    GroupDetails.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a, _b;
        if (prevProps.isGlobalSelectionReady !== this.props.isGlobalSelectionReady ||
            prevProps.location.pathname !== this.props.location.pathname) {
            this.fetchData();
        }
        if ((!this.canLoadEventEarly(prevProps) && !(prevState === null || prevState === void 0 ? void 0 : prevState.group) && this.state.group) ||
            (((_a = prevProps.params) === null || _a === void 0 ? void 0 : _a.eventId) !== ((_b = this.props.params) === null || _b === void 0 ? void 0 : _b.eventId) && this.state.group)) {
            this.getEvent(this.state.group);
        }
    };
    GroupDetails.prototype.componentWillUnmount = function () {
        GroupStore.reset();
        callIfFunction(this.listener);
        if (this.interval) {
            clearInterval(this.interval);
        }
    };
    Object.defineProperty(GroupDetails.prototype, "initialState", {
        get: function () {
            return {
                group: null,
                loading: true,
                loadingEvent: true,
                loadingGroup: true,
                error: false,
                eventError: false,
                errorType: null,
                project: null,
            };
        },
        enumerable: false,
        configurable: true
    });
    GroupDetails.prototype.canLoadEventEarly = function (props) {
        return !props.params.eventId || ['oldest', 'latest'].includes(props.params.eventId);
    };
    Object.defineProperty(GroupDetails.prototype, "groupDetailsEndpoint", {
        get: function () {
            return "/issues/" + this.props.params.groupId + "/";
        },
        enumerable: false,
        configurable: true
    });
    GroupDetails.prototype.getEvent = function (group) {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            var _b, params, environments, api, orgSlug, groupId, eventId, projectId, event_1, err_1;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        if (group) {
                            this.setState({ loadingEvent: true, eventError: false });
                        }
                        _b = this.props, params = _b.params, environments = _b.environments, api = _b.api;
                        orgSlug = params.orgId;
                        groupId = params.groupId;
                        eventId = (params === null || params === void 0 ? void 0 : params.eventId) || 'latest';
                        projectId = (_a = group === null || group === void 0 ? void 0 : group.project) === null || _a === void 0 ? void 0 : _a.slug;
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchGroupEvent(api, orgSlug, groupId, eventId, environments, projectId)];
                    case 2:
                        event_1 = _c.sent();
                        this.setState({ event: event_1, loading: false, eventError: false, loadingEvent: false });
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        // This is an expected error, capture to Sentry so that it is not considered as an unhandled error
                        Sentry.captureException(err_1);
                        this.setState({ eventError: true, loading: false, loadingEvent: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    GroupDetails.prototype.getCurrentRouteInfo = function (group) {
        var _a = this.props, routes = _a.routes, organization = _a.organization;
        var event = this.state.event;
        // All the routes under /organizations/:orgId/issues/:groupId have a defined props
        var _b = routes[routes.length - 1].props, currentTab = _b.currentTab, isEventRoute = _b.isEventRoute;
        var baseUrl = isEventRoute && event
            ? "/organizations/" + organization.slug + "/issues/" + group.id + "/events/" + event.id + "/"
            : "/organizations/" + organization.slug + "/issues/" + group.id + "/";
        return { currentTab: currentTab, baseUrl: baseUrl };
    };
    GroupDetails.prototype.updateReprocessingProgress = function () {
        var hasReprocessingV2Feature = this.hasReprocessingV2Feature();
        if (!hasReprocessingV2Feature) {
            return;
        }
        this.interval = setInterval(this.refetchGroup, 30000);
    };
    GroupDetails.prototype.hasReprocessingV2Feature = function () {
        var _a;
        var organization = this.props.organization;
        return (_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('reprocessing-v2');
    };
    GroupDetails.prototype.getReprocessingNewRoute = function (data) {
        var _a = this.props, routes = _a.routes, location = _a.location, params = _a.params;
        var groupId = params.groupId;
        var nextGroupId = data.id;
        var hasReprocessingV2Feature = this.hasReprocessingV2Feature();
        var reprocessingStatus = getGroupReprocessingStatus(data);
        var _b = this.getCurrentRouteInfo(data), currentTab = _b.currentTab, baseUrl = _b.baseUrl;
        if (groupId !== nextGroupId) {
            if (hasReprocessingV2Feature) {
                // Redirects to the Activities tab
                if (reprocessingStatus === ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
                    currentTab !== TAB.ACTIVITY) {
                    return {
                        pathname: "" + baseUrl + TAB.ACTIVITY + "/",
                        query: __assign(__assign({}, params), { groupId: nextGroupId }),
                    };
                }
            }
            return recreateRoute('', {
                routes: routes,
                location: location,
                params: __assign(__assign({}, params), { groupId: nextGroupId }),
            });
        }
        if (hasReprocessingV2Feature) {
            if (reprocessingStatus === ReprocessingStatus.REPROCESSING &&
                currentTab !== TAB.DETAILS) {
                return {
                    pathname: baseUrl,
                    query: params,
                };
            }
            if (reprocessingStatus === ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
                currentTab !== TAB.ACTIVITY &&
                currentTab !== TAB.USER_FEEDBACK) {
                return {
                    pathname: "" + baseUrl + TAB.ACTIVITY + "/",
                    query: params,
                };
            }
        }
        return undefined;
    };
    GroupDetails.prototype.getGroupQuery = function () {
        var _a;
        var _b = this.props, environments = _b.environments, organization = _b.organization;
        // Note, we do not want to include the environment key at all if there are no environments
        var query = __assign({}, (environments ? { environment: environments } : {}));
        if ((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('inbox')) {
            query.expand = 'inbox';
        }
        return query;
    };
    GroupDetails.prototype.getFetchDataRequestErrorType = function (status) {
        if (!status) {
            return null;
        }
        if (status === 404) {
            return ERROR_TYPES.GROUP_NOT_FOUND;
        }
        if (status === 403) {
            return ERROR_TYPES.MISSING_MEMBERSHIP;
        }
        return null;
    };
    GroupDetails.prototype.handleRequestError = function (error) {
        Sentry.captureException(error);
        var errorType = this.getFetchDataRequestErrorType(error === null || error === void 0 ? void 0 : error.status);
        this.setState({
            loadingGroup: false,
            loading: false,
            error: true,
            errorType: errorType,
        });
    };
    GroupDetails.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, isGlobalSelectionReady, params, eventPromise, groupPromise, _b, data, reprocessingNewRoute, project, locationWithProject, error_2;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, isGlobalSelectionReady = _a.isGlobalSelectionReady, params = _a.params;
                        // Need to wait for global selection store to be ready before making request
                        if (!isGlobalSelectionReady) {
                            return [2 /*return*/];
                        }
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 4, , 5]);
                        eventPromise = this.canLoadEventEarly(this.props)
                            ? this.getEvent()
                            : undefined;
                        return [4 /*yield*/, api.requestPromise(this.groupDetailsEndpoint, {
                                query: this.getGroupQuery(),
                            })];
                    case 2:
                        groupPromise = _c.sent();
                        return [4 /*yield*/, Promise.all([groupPromise, eventPromise])];
                    case 3:
                        _b = __read.apply(void 0, [_c.sent(), 1]), data = _b[0];
                        reprocessingNewRoute = this.getReprocessingNewRoute(data);
                        if (reprocessingNewRoute) {
                            ReactRouter.browserHistory.push(reprocessingNewRoute);
                            return [2 /*return*/];
                        }
                        project = data.project;
                        markEventSeen(api, params.orgId, project.slug, params.groupId);
                        if (!project) {
                            Sentry.withScope(function () {
                                Sentry.captureException(new Error('Project not found'));
                            });
                        }
                        else {
                            locationWithProject = __assign({}, this.props.location);
                            if (locationWithProject.query.project === undefined &&
                                locationWithProject.query._allp === undefined) {
                                //We use _allp as a temporary measure to know they came from the issue list page with no project selected (all projects included in filter).
                                //If it is not defined, we add the locked project id to the URL (this is because if someone navigates directly to an issue on single-project priveleges, then goes back - they were getting assigned to the first project).
                                //If it is defined, we do not so that our back button will bring us to the issue list page with no project selected instead of the locked project.
                                locationWithProject.query.project = project.id;
                            }
                            delete locationWithProject.query._allp; //We delete _allp from the URL to keep the hack a bit cleaner, but this is not an ideal solution and will ultimately be replaced with something smarter.
                            ReactRouter.browserHistory.replace(locationWithProject);
                        }
                        this.setState({ project: project, loadingGroup: false });
                        GroupStore.loadInitialData([data]);
                        return [3 /*break*/, 5];
                    case 4:
                        error_2 = _c.sent();
                        this.handleRequestError(error_2);
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        });
    };
    GroupDetails.prototype.onGroupChange = function (itemIds) {
        var id = this.props.params.groupId;
        if (itemIds.has(id)) {
            var group = GroupStore.get(id);
            if (group) {
                // TODO(ts) This needs a better approach. issueActions is splicing attributes onto
                // group objects to cheat here.
                if (group.stale) {
                    this.fetchData();
                    return;
                }
                this.setState({
                    group: group,
                });
            }
        }
    };
    GroupDetails.prototype.getTitle = function () {
        var organization = this.props.organization;
        var group = this.state.group;
        var defaultTitle = 'Sentry';
        if (!group) {
            return defaultTitle;
        }
        var title = getTitle(group, organization).title;
        var message = getMessage(group);
        var project = group.project;
        var eventDetails = organization.slug + " - " + project.slug;
        if (title && message) {
            return title + ": " + message + " - " + eventDetails;
        }
        return (title || message || defaultTitle) + " - " + eventDetails;
    };
    GroupDetails.prototype.renderError = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, location = _c.location;
        var projects = (_a = organization.projects) !== null && _a !== void 0 ? _a : [];
        var projectId = location.query.project;
        var projectSlug = (_b = projects.find(function (proj) { return proj.id === projectId; })) === null || _b === void 0 ? void 0 : _b.slug;
        switch (this.state.errorType) {
            case ERROR_TYPES.GROUP_NOT_FOUND:
                return (<LoadingError message={t('The issue you were looking for was not found.')}/>);
            case ERROR_TYPES.MISSING_MEMBERSHIP:
                return (<MissingProjectMembership organization={this.props.organization} projectSlug={projectSlug}/>);
            default:
                return <LoadingError onRetry={this.remountComponent}/>;
        }
    };
    GroupDetails.prototype.renderContent = function (project, group) {
        var _this = this;
        var _a = this.props, children = _a.children, environments = _a.environments;
        var _b = this.state, loadingEvent = _b.loadingEvent, eventError = _b.eventError, event = _b.event;
        var _c = this.getCurrentRouteInfo(group), currentTab = _c.currentTab, baseUrl = _c.baseUrl;
        var groupReprocessingStatus = getGroupReprocessingStatus(group);
        var childProps = {
            environments: environments,
            group: group,
            project: project,
        };
        if (currentTab === TAB.DETAILS) {
            childProps = __assign(__assign({}, childProps), { event: event,
                loadingEvent: loadingEvent,
                eventError: eventError,
                groupReprocessingStatus: groupReprocessingStatus, onRetry: function () { return _this.remountComponent(); } });
        }
        if (currentTab === TAB.TAGS) {
            childProps = __assign(__assign({}, childProps), { event: event, baseUrl: baseUrl });
        }
        return (<React.Fragment>
        <GroupHeader groupReprocessingStatus={groupReprocessingStatus} project={project} event={event} group={group} currentTab={currentTab} baseUrl={baseUrl}/>
        {React.isValidElement(children)
                ? React.cloneElement(children, childProps)
                : children}
      </React.Fragment>);
    };
    GroupDetails.prototype.renderPageContent = function () {
        var _this = this;
        var _a;
        var _b = this.state, isError = _b.error, group = _b.group, project = _b.project, loading = _b.loading;
        var isLoading = loading || (!group && !isError);
        if (isLoading) {
            return <LoadingIndicator />;
        }
        if (isError) {
            return this.renderError();
        }
        var organization = this.props.organization;
        return (<Projects orgId={organization.slug} slugs={[(_a = project === null || project === void 0 ? void 0 : project.slug) !== null && _a !== void 0 ? _a : '']} data-test-id="group-projects-container">
        {function (_a) {
                var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
                return initiallyLoaded ? (fetchError ? (<LoadingError message={t('Error loading the specified project')}/>) : (_this.renderContent(projects[0], group) // TODO(ts): Update renderContent function to deal with empty group
                )) : (<LoadingIndicator />);
            }}
      </Projects>);
    };
    GroupDetails.prototype.render = function () {
        var project = this.state.project;
        return (<DocumentTitle title={this.getTitle()}>
        <GlobalSelectionHeader skipLoadLastUsed forceProject={project} showDateSelector={false} shouldForceProject lockedMessageSubject={t('issue')} showIssueStreamLink showProjectSettingsLink>
          <PageContent>{this.renderPageContent()}</PageContent>
        </GlobalSelectionHeader>
      </DocumentTitle>);
    };
    GroupDetails.childContextTypes = {
        group: SentryTypes.Group,
        location: PropTypes.object,
    };
    return GroupDetails;
}(React.Component));
export default withApi(Sentry.withProfiler(GroupDetails));
//# sourceMappingURL=groupDetails.jsx.map
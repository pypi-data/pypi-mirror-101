import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import isEqual from 'lodash/isEqual';
import { fetchSentryAppComponents } from 'app/actionCreators/sentryAppComponents';
import ErrorBoundary from 'app/components/errorBoundary';
import GroupEventDetailsLoadingError from 'app/components/errors/groupEventDetailsLoadingError';
import EventEntries from 'app/components/events/eventEntries';
import { withMeta } from 'app/components/events/meta/metaProxy';
import GroupSidebar from 'app/components/group/sidebar';
import LoadingIndicator from 'app/components/loadingIndicator';
import MutedBox from 'app/components/mutedBox';
import ReprocessedBox from 'app/components/reprocessedBox';
import ResolutionBox from 'app/components/resolutionBox';
import SuggestProjectCTA from 'app/components/suggestProjectCTA';
import { metric } from 'app/utils/analytics';
import fetchSentryAppInstallations from 'app/utils/fetchSentryAppInstallations';
import GroupEventToolbar from '../eventToolbar';
import ReprocessingProgress from '../reprocessingProgress';
import { getEventEnvironment, getGroupMostRecentActivity, ReprocessingStatus, } from '../utils';
var GroupEventDetails = /** @class */ (function (_super) {
    __extends(GroupEventDetails, _super);
    function GroupEventDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventNavLinks: '',
            releasesCompletion: null,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, project, organization, orgSlug, projSlug, projectId, releasesCompletionPromise, releasesCompletion;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, project = _a.project, organization = _a.organization;
                        orgSlug = organization.slug;
                        projSlug = project.slug;
                        projectId = project.id;
                        releasesCompletionPromise = api.requestPromise("/projects/" + orgSlug + "/" + projSlug + "/releases/completion/");
                        fetchSentryAppInstallations(api, orgSlug);
                        // TODO(marcos): Sometimes GlobalSelectionStore cannot pick a project.
                        if (projectId) {
                            fetchSentryAppComponents(api, orgSlug, projectId);
                        }
                        else {
                            Sentry.withScope(function (scope) {
                                scope.setExtra('props', _this.props);
                                scope.setExtra('state', _this.state);
                                Sentry.captureMessage('Project ID was not set');
                            });
                        }
                        return [4 /*yield*/, releasesCompletionPromise];
                    case 1:
                        releasesCompletion = _b.sent();
                        this.setState({ releasesCompletion: releasesCompletion });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    GroupEventDetails.prototype.componentDidMount = function () {
        this.fetchData();
        // First Meaningful Paint for /organizations/:orgId/issues/:groupId/
        metric.measure({
            name: 'app.page.perf.issue-details',
            start: 'page-issue-details-start',
            data: {
                // start_type is set on 'page-issue-details-start'
                org_id: parseInt(this.props.organization.id, 10),
                group: this.props.organization.features.includes('enterprise-perf')
                    ? 'enterprise-perf'
                    : 'control',
                milestone: 'first-meaningful-paint',
                is_enterprise: this.props.organization.features
                    .includes('enterprise-orgs')
                    .toString(),
                is_outlier: this.props.organization.features
                    .includes('enterprise-orgs-outliers')
                    .toString(),
            },
        });
    };
    GroupEventDetails.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, environments = _a.environments, params = _a.params, location = _a.location, organization = _a.organization, project = _a.project;
        var environmentsHaveChanged = !isEqual(prevProps.environments, environments);
        // If environments are being actively changed and will no longer contain the
        // current event's environment, redirect to latest
        if (environmentsHaveChanged &&
            prevProps.event &&
            params.eventId &&
            !['latest', 'oldest'].includes(params.eventId)) {
            var shouldRedirect = environments.length > 0 &&
                !environments.find(function (env) { return env.name === getEventEnvironment(prevProps.event); });
            if (shouldRedirect) {
                browserHistory.replace({
                    pathname: "/organizations/" + params.orgId + "/issues/" + params.groupId + "/",
                    query: location.query,
                });
                return;
            }
        }
        if (prevProps.organization.slug !== organization.slug ||
            prevProps.project.slug !== project.slug) {
            this.fetchData();
        }
    };
    GroupEventDetails.prototype.componentWillUnmount = function () {
        var api = this.props.api;
        api.clear();
    };
    Object.defineProperty(GroupEventDetails.prototype, "showExampleCommit", {
        get: function () {
            var project = this.props.project;
            var releasesCompletion = this.state.releasesCompletion;
            return ((project === null || project === void 0 ? void 0 : project.isMember) &&
                (project === null || project === void 0 ? void 0 : project.firstEvent) &&
                (releasesCompletion === null || releasesCompletion === void 0 ? void 0 : releasesCompletion.some(function (_a) {
                    var step = _a.step, complete = _a.complete;
                    return step === 'commit' && !complete;
                })));
        },
        enumerable: false,
        configurable: true
    });
    GroupEventDetails.prototype.renderContent = function (eventWithMeta) {
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization, environments = _a.environments, location = _a.location, loadingEvent = _a.loadingEvent, onRetry = _a.onRetry, eventError = _a.eventError;
        if (loadingEvent) {
            return <LoadingIndicator />;
        }
        if (eventError) {
            return (<GroupEventDetailsLoadingError environments={environments} onRetry={onRetry}/>);
        }
        return (<EventEntries group={group} event={eventWithMeta} organization={organization} project={project} location={location} showExampleCommit={this.showExampleCommit}/>);
    };
    GroupEventDetails.prototype.renderReprocessedBox = function (reprocessStatus, mostRecentActivity) {
        if (reprocessStatus !== ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT &&
            reprocessStatus !== ReprocessingStatus.REPROCESSED_AND_HAS_EVENT) {
            return null;
        }
        var _a = this.props, group = _a.group, organization = _a.organization;
        var count = group.count, groupId = group.id;
        var groupCount = Number(count);
        return (<ReprocessedBox reprocessActivity={mostRecentActivity} groupCount={groupCount} groupId={groupId} orgSlug={organization.slug}/>);
    };
    GroupEventDetails.prototype.render = function () {
        var _a;
        var _b = this.props, className = _b.className, group = _b.group, project = _b.project, organization = _b.organization, environments = _b.environments, location = _b.location, event = _b.event, groupReprocessingStatus = _b.groupReprocessingStatus;
        var eventWithMeta = withMeta(event);
        // Reprocessing
        var hasReprocessingV2Feature = (_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('reprocessing-v2');
        var activities = group.activity;
        var mostRecentActivity = getGroupMostRecentActivity(activities);
        return (<div className={className}>
        {event && (<ErrorBoundary customComponent={null}>
            <SuggestProjectCTA event={event} organization={organization}/>
          </ErrorBoundary>)}
        <div className="event-details-container">
          {hasReprocessingV2Feature &&
                groupReprocessingStatus === ReprocessingStatus.REPROCESSING ? (<ReprocessingProgress totalEvents={mostRecentActivity.data.eventCount} pendingEvents={group.statusDetails
                    .pendingEvents}/>) : (<React.Fragment>
              <div className="primary">
                {eventWithMeta && (<GroupEventToolbar group={group} event={eventWithMeta} organization={organization} location={location}/>)}
                {group.status === 'ignored' && (<MutedBox statusDetails={group.statusDetails}/>)}
                {group.status === 'resolved' && (<ResolutionBox statusDetails={group.statusDetails} projectId={project.id}/>)}
                {this.renderReprocessedBox(groupReprocessingStatus, mostRecentActivity)}
                {this.renderContent(eventWithMeta)}
              </div>
              <div className="secondary">
                <GroupSidebar organization={organization} project={project} group={group} event={eventWithMeta} environments={environments}/>
              </div>
            </React.Fragment>)}
        </div>
      </div>);
    };
    return GroupEventDetails;
}(React.Component));
export default styled(GroupEventDetails)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n"])));
var templateObject_1;
//# sourceMappingURL=groupEventDetails.jsx.map
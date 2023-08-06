import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import ErrorBoundary from 'app/components/errorBoundary';
import EventContexts from 'app/components/events/contexts';
import EventContextSummary from 'app/components/events/contextSummary/contextSummary';
import EventDevice from 'app/components/events/device';
import EventErrors from 'app/components/events/errors';
import EventAttachments from 'app/components/events/eventAttachments';
import EventCause from 'app/components/events/eventCause';
import EventCauseEmpty from 'app/components/events/eventCauseEmpty';
import EventDataSection from 'app/components/events/eventDataSection';
import EventExtraData from 'app/components/events/eventExtraData/eventExtraData';
import EventSdk from 'app/components/events/eventSdk';
import EventTags from 'app/components/events/eventTags/eventTags';
import EventGroupingInfo from 'app/components/events/groupingInfo';
import EventPackageData from 'app/components/events/packageData';
import RRWebIntegration from 'app/components/events/rrwebIntegration';
import EventSdkUpdates from 'app/components/events/sdkUpdates';
import { DataSection } from 'app/components/events/styles';
import EventUserFeedback from 'app/components/events/userFeedback';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { EntryType } from 'app/types/event';
import { isNotSharedOrganization } from 'app/types/utils';
import { defined, objectIsEmpty } from 'app/utils';
import { analytics } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import { projectProcessingIssuesMessages } from 'app/views/settings/project/projectProcessingIssues';
import findBestThread from './interfaces/threads/threadSelector/findBestThread';
import getThreadException from './interfaces/threads/threadSelector/getThreadException';
import EventEntry from './eventEntry';
var MINIFIED_DATA_JAVA_EVENT_REGEX_MATCH = /^(([\w\$]\.[\w\$]{1,2})|([\w\$]{2}\.[\w\$]\.[\w\$]))(\.|$)/g;
var defaultProps = {
    isShare: false,
    showExampleCommit: false,
    showTagSummary: true,
};
var EventEntries = /** @class */ (function (_super) {
    __extends(EventEntries, _super);
    function EventEntries() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            proGuardErrors: [],
        };
        return _this;
    }
    EventEntries.prototype.componentDidMount = function () {
        this.checkProGuardError();
        this.recordIssueError();
    };
    EventEntries.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        var _a = this.props, event = _a.event, showExampleCommit = _a.showExampleCommit;
        return ((event && nextProps.event && event.id !== nextProps.event.id) ||
            showExampleCommit !== nextProps.showExampleCommit ||
            nextState.isLoading !== this.state.isLoading);
    };
    EventEntries.prototype.fetchProguardMappingFiles = function (query) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, project, proguardMappingFiles, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, project = _a.project;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/files/dsyms/", {
                                method: 'GET',
                                query: {
                                    query: query,
                                    file_formats: 'proguard',
                                },
                            })];
                    case 2:
                        proguardMappingFiles = _b.sent();
                        return [2 /*return*/, proguardMappingFiles];
                    case 3:
                        error_1 = _b.sent();
                        Sentry.captureException(error_1);
                        // do nothing, the UI will not display extra error details
                        return [2 /*return*/, []];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    EventEntries.prototype.isDataMinified = function (str) {
        if (!str) {
            return false;
        }
        return !!__spreadArray([], __read(str.matchAll(MINIFIED_DATA_JAVA_EVENT_REGEX_MATCH))).length;
    };
    EventEntries.prototype.hasThreadOrExceptionMinifiedFrameData = function (event, bestThread) {
        var _this = this;
        var _a, _b, _c, _d, _e, _f, _g;
        if (!bestThread) {
            var exceptionValues = (_d = (_c = (_b = (_a = event.entries) === null || _a === void 0 ? void 0 : _a.find(function (e) { return e.type === EntryType.EXCEPTION; })) === null || _b === void 0 ? void 0 : _b.data) === null || _c === void 0 ? void 0 : _c.values) !== null && _d !== void 0 ? _d : [];
            return !!exceptionValues.find(function (exceptionValue) {
                var _a, _b;
                return (_b = (_a = exceptionValue.stacktrace) === null || _a === void 0 ? void 0 : _a.frames) === null || _b === void 0 ? void 0 : _b.find(function (frame) {
                    return _this.isDataMinified(frame.module);
                });
            });
        }
        var threadExceptionValues = (_e = getThreadException(event, bestThread)) === null || _e === void 0 ? void 0 : _e.values;
        return !!(threadExceptionValues
            ? threadExceptionValues.find(function (threadExceptionValue) {
                var _a, _b;
                return (_b = (_a = threadExceptionValue.stacktrace) === null || _a === void 0 ? void 0 : _a.frames) === null || _b === void 0 ? void 0 : _b.find(function (frame) {
                    return _this.isDataMinified(frame.module);
                });
            })
            : (_g = (_f = bestThread === null || bestThread === void 0 ? void 0 : bestThread.stacktrace) === null || _f === void 0 ? void 0 : _f.frames) === null || _g === void 0 ? void 0 : _g.find(function (frame) { return _this.isDataMinified(frame.module); }));
    };
    EventEntries.prototype.checkProGuardError = function () {
        var _a, _b, _c, _d, _e, _f, _g;
        return __awaiter(this, void 0, void 0, function () {
            var _h, event, isShare, hasEventErrorsProGuardMissingMapping, proGuardErrors, debugImages, proGuardImage, proGuardImageUuid, proguardMappingFiles, threads, bestThread, hasThreadOrExceptionMinifiedData;
            return __generator(this, function (_j) {
                switch (_j.label) {
                    case 0:
                        _h = this.props, event = _h.event, isShare = _h.isShare;
                        if (!event || event.platform !== 'java') {
                            this.setState({ isLoading: false });
                            return [2 /*return*/];
                        }
                        hasEventErrorsProGuardMissingMapping = (_a = event.errors) === null || _a === void 0 ? void 0 : _a.find(function (error) { return error.type === 'proguard_missing_mapping'; });
                        if (hasEventErrorsProGuardMissingMapping) {
                            this.setState({ isLoading: false });
                            return [2 /*return*/];
                        }
                        proGuardErrors = [];
                        debugImages = (_c = (_b = event.entries) === null || _b === void 0 ? void 0 : _b.find(function (e) { return e.type === EntryType.DEBUGMETA; })) === null || _c === void 0 ? void 0 : _c.data.images;
                        proGuardImage = debugImages === null || debugImages === void 0 ? void 0 : debugImages.find(function (debugImage) { return (debugImage === null || debugImage === void 0 ? void 0 : debugImage.type) === 'proguard'; });
                        proGuardImageUuid = proGuardImage === null || proGuardImage === void 0 ? void 0 : proGuardImage.uuid;
                        if (!defined(proGuardImageUuid)) return [3 /*break*/, 2];
                        if (isShare) {
                            this.setState({ isLoading: false });
                            return [2 /*return*/];
                        }
                        return [4 /*yield*/, this.fetchProguardMappingFiles(proGuardImageUuid)];
                    case 1:
                        proguardMappingFiles = _j.sent();
                        if (!proguardMappingFiles.length) {
                            proGuardErrors.push({
                                type: 'proguard_missing_mapping',
                                message: projectProcessingIssuesMessages.proguard_missing_mapping,
                                data: { mapping_uuid: proGuardImageUuid },
                            });
                        }
                        this.setState({ proGuardErrors: proGuardErrors, isLoading: false });
                        return [2 /*return*/];
                    case 2:
                        if (proGuardImage) {
                            Sentry.withScope(function (s) {
                                s.setLevel(Sentry.Severity.Warning);
                                if (event.sdk) {
                                    s.setTag('offending.event.sdk.name', event.sdk.name);
                                    s.setTag('offending.event.sdk.version', event.sdk.version);
                                }
                                Sentry.captureMessage('Event contains proguard image but not uuid');
                            });
                        }
                        _j.label = 3;
                    case 3:
                        threads = (_g = (_f = (_e = (_d = event.entries) === null || _d === void 0 ? void 0 : _d.find(function (e) { return e.type === EntryType.THREADS; })) === null || _e === void 0 ? void 0 : _e.data) === null || _f === void 0 ? void 0 : _f.values) !== null && _g !== void 0 ? _g : [];
                        bestThread = findBestThread(threads);
                        hasThreadOrExceptionMinifiedData = this.hasThreadOrExceptionMinifiedFrameData(event, bestThread);
                        if (hasThreadOrExceptionMinifiedData) {
                            proGuardErrors.push({
                                type: 'proguard_potentially_misconfigured_plugin',
                                message: tct('Some frames appear to be minified. Did you configure the [plugin]?', {
                                    plugin: (<ExternalLink href="https://docs.sentry.io/platforms/android/proguard/#gradle">
                Sentry Gradle Plugin
              </ExternalLink>),
                                }),
                            });
                            // This capture will be removed once we're confident with the level of effectiveness
                            Sentry.withScope(function (s) {
                                s.setLevel(Sentry.Severity.Warning);
                                if (event.sdk) {
                                    s.setTag('offending.event.sdk.name', event.sdk.name);
                                    s.setTag('offending.event.sdk.version', event.sdk.version);
                                }
                                Sentry.captureMessage(!proGuardImage
                                    ? 'No Proguard is used at all, but a frame did match the regex'
                                    : "Displaying ProGuard warning 'proguard_potentially_misconfigured_plugin' for suspected event");
                            });
                        }
                        this.setState({ proGuardErrors: proGuardErrors, isLoading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    EventEntries.prototype.recordIssueError = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, event = _a.event;
        if (!event || !event.errors || !(event.errors.length > 0)) {
            return;
        }
        var errors = event.errors;
        var errorTypes = errors.map(function (errorEntries) { return errorEntries.type; });
        var errorMessages = errors.map(function (errorEntries) { return errorEntries.message; });
        var orgId = organization.id;
        var platform = project.platform;
        analytics('issue_error_banner.viewed', __assign({ org_id: orgId ? parseInt(orgId, 10) : null, group: event === null || event === void 0 ? void 0 : event.groupID, error_type: errorTypes, error_message: errorMessages }, (platform && { platform: platform })));
    };
    EventEntries.prototype.renderEntries = function (event) {
        var _a = this.props, project = _a.project, organization = _a.organization, group = _a.group;
        var entries = event.entries;
        if (!Array.isArray(entries)) {
            return null;
        }
        return entries.map(function (entry, entryIdx) { return (<ErrorBoundary key={"entry-" + entryIdx} customComponent={<EventDataSection type={entry.type} title={entry.type}>
            <p>{t('There was an error rendering this data.')}</p>
          </EventDataSection>}>
        <EventEntry projectSlug={project.slug} groupId={group === null || group === void 0 ? void 0 : group.id} organization={organization} event={event} entry={entry}/>
      </ErrorBoundary>); });
    };
    EventEntries.prototype.render = function () {
        var _a = this.props, className = _a.className, organization = _a.organization, group = _a.group, isShare = _a.isShare, project = _a.project, event = _a.event, showExampleCommit = _a.showExampleCommit, showTagSummary = _a.showTagSummary, location = _a.location;
        var _b = this.state, proGuardErrors = _b.proGuardErrors, isLoading = _b.isLoading;
        var features = new Set(organization === null || organization === void 0 ? void 0 : organization.features);
        var hasQueryFeature = features.has('discover-query');
        if (!event) {
            return (<div style={{ padding: '15px 30px' }}>
          <h3>{t('Latest Event Not Available')}</h3>
        </div>);
        }
        var hasContext = !objectIsEmpty(event.user) || !objectIsEmpty(event.contexts);
        var hasErrors = !objectIsEmpty(event.errors) || !!proGuardErrors.length;
        return (<div className={className} data-test-id={"event-entries-loading-" + isLoading}>
        {hasErrors && !isLoading && (<EventErrors event={event} orgSlug={organization.slug} projectSlug={project.slug} proGuardErrors={proGuardErrors}/>)}
        {!isShare &&
                isNotSharedOrganization(organization) &&
                (showExampleCommit ? (<EventCauseEmpty organization={organization} project={project}/>) : (<EventCause organization={organization} project={project} event={event} group={group}/>))}
        {(event === null || event === void 0 ? void 0 : event.userReport) && group && (<StyledEventUserFeedback report={event.userReport} orgId={organization.slug} issueId={group.id} includeBorder={!hasErrors}/>)}
        {hasContext && showTagSummary && <EventContextSummary event={event}/>}
        {showTagSummary && (<EventTags event={event} organization={organization} projectId={project.slug} location={location} hasQueryFeature={hasQueryFeature}/>)}
        {this.renderEntries(event)}
        {hasContext && <EventContexts group={group} event={event}/>}
        {event && !objectIsEmpty(event.context) && <EventExtraData event={event}/>}
        {event && !objectIsEmpty(event.packages) && <EventPackageData event={event}/>}
        {event && !objectIsEmpty(event.device) && <EventDevice event={event}/>}
        {!isShare && features.has('event-attachments') && (<EventAttachments event={event} orgId={organization.slug} projectId={project.slug} location={location}/>)}
        {(event === null || event === void 0 ? void 0 : event.sdk) && !objectIsEmpty(event.sdk) && <EventSdk sdk={event.sdk}/>}
        {!isShare && (event === null || event === void 0 ? void 0 : event.sdkUpdates) && event.sdkUpdates.length > 0 && (<EventSdkUpdates event={__assign({ sdkUpdates: event.sdkUpdates }, event)}/>)}
        {!isShare && (event === null || event === void 0 ? void 0 : event.groupID) && (<EventGroupingInfo projectId={project.slug} event={event} showGroupingConfig={features.has('set-grouping-config')}/>)}
        {!isShare && features.has('event-attachments') && (<RRWebIntegration event={event} orgId={organization.slug} projectId={project.slug}/>)}
      </div>);
    };
    EventEntries.defaultProps = defaultProps;
    return EventEntries;
}(React.Component));
var ErrorContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"], ["\n  /*\n  Remove border on adjacent context summary box.\n  Once that component uses emotion this will be harder.\n  */\n  & + .context-summary {\n    border-top: none;\n  }\n"])));
var BorderlessEventEntries = styled(EventEntries)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  & ", " {\n    padding: ", " 0 0 0;\n  }\n  & ", ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & ", " {\n    margin-bottom: ", ";\n  }\n"], ["\n  & " /* sc-selector */, " {\n    padding: ", " 0 0 0;\n  }\n  & " /* sc-selector */, ":first-child {\n    padding-top: 0;\n    border-top: 0;\n  }\n  & " /* sc-selector */, " {\n    margin-bottom: ", ";\n  }\n"])), /* sc-selector */ DataSection, space(3), /* sc-selector */ DataSection, /* sc-selector */ ErrorContainer, space(2));
var StyledEventUserFeedback = styled(EventUserFeedback)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  border-radius: 0;\n  box-shadow: none;\n  padding: 20px 30px 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"], ["\n  border-radius: 0;\n  box-shadow: none;\n  padding: 20px 30px 0 40px;\n  border: 0;\n  ", "\n  margin: 0;\n"])), function (p) { return (p.includeBorder ? "border-top: 1px solid " + p.theme.innerBorder + ";" : ''); });
// TODO(ts): any required due to our use of SharedViewOrganization
export default withOrganization(withApi(EventEntries));
export { BorderlessEventEntries };
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=eventEntries.jsx.map
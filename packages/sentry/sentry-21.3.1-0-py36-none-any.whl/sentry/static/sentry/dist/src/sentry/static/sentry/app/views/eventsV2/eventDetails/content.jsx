import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { fetchTotalCount } from 'app/actionCreators/events';
import Feature from 'app/components/acl/feature';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import NotFound from 'app/components/errors/notFound';
import EventOrGroupTitle from 'app/components/eventOrGroupTitle';
import { BorderlessEventEntries } from 'app/components/events/eventEntries';
import EventMessage from 'app/components/events/eventMessage';
import EventMetadata from 'app/components/events/eventMetadata';
import EventVitals from 'app/components/events/eventVitals';
import * as SpanEntryContext from 'app/components/events/interfaces/spans/context';
import OpsBreakdown from 'app/components/events/opsBreakdown';
import RootSpanStatus from 'app/components/events/rootSpanStatus';
import FileSize from 'app/components/fileSize';
import * as Layout from 'app/components/layouts/thirds';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import TagsTable from 'app/components/tagsTable';
import { IconOpen } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { FIELD_TAGS } from 'app/utils/discover/fields';
import { eventDetailsRoute } from 'app/utils/discover/urls';
import { getMessage } from 'app/utils/events';
import * as QuickTraceContext from 'app/utils/performance/quickTrace/quickTraceContext';
import QuickTraceQuery from 'app/utils/performance/quickTrace/quickTraceQuery';
import { getTraceTimeRangeFromEvent, makeEventView, } from 'app/utils/performance/quickTrace/utils';
import Projects from 'app/utils/projects';
import EventMetas from 'app/views/performance/transactionDetails/eventMetas';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import DiscoverBreadcrumb from '../breadcrumb';
import { generateTitle, getExpandedResults } from '../utils';
import LinkedIssue from './linkedIssue';
var EventDetailsContent = /** @class */ (function (_super) {
    __extends(EventDetailsContent, _super);
    function EventDetailsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            // AsyncComponent state
            loading: true,
            reloading: false,
            error: false,
            errors: [],
            event: undefined,
            // local state
            isSidebarVisible: true,
            traceSize: undefined,
        };
        _this.toggleSidebar = function () {
            _this.setState({ isSidebarVisible: !_this.state.isSidebarVisible });
        };
        _this.generateTagKey = function (tag) {
            // Some tags may be normalized from context, but not all of them are.
            // This supports a user making a custom tag with the same name as one
            // that comes from context as all of these are also tags.
            if (tag.key in FIELD_TAGS) {
                return "tags[" + tag.key + "]";
            }
            return tag.key;
        };
        _this.generateTagUrl = function (tag) {
            var _a;
            var _b = _this.props, eventView = _b.eventView, organization = _b.organization;
            var event = _this.state.event;
            if (!event) {
                return '';
            }
            var eventReference = __assign({}, event);
            if (eventReference.id) {
                delete eventReference.id;
            }
            var tagKey = _this.generateTagKey(tag);
            var nextView = getExpandedResults(eventView, (_a = {}, _a[tagKey] = tag.value, _a), eventReference);
            return nextView.getResultsViewUrlTarget(organization.slug);
        };
        _this.getEventSlug = function () {
            var eventSlug = _this.props.params.eventSlug;
            if (typeof eventSlug === 'string') {
                return eventSlug.trim();
            }
            return '';
        };
        return _this;
    }
    EventDetailsContent.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a, _b, _c, _d, _e;
        var event = this.state.event;
        if (event &&
            ((_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== ((_e = (_d = (_c = prevState === null || prevState === void 0 ? void 0 : prevState.event) === null || _c === void 0 ? void 0 : _c.contexts) === null || _d === void 0 ? void 0 : _d.trace) === null || _e === void 0 ? void 0 : _e.trace_id)) {
            this.fetchTotal();
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    EventDetailsContent.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location, eventView = _a.eventView;
        var eventSlug = params.eventSlug;
        var query = eventView.getEventsAPIPayload(location);
        // Fields aren't used, reduce complexity by omitting from query entirely
        query.field = [];
        var url = "/organizations/" + organization.slug + "/events/" + eventSlug + "/";
        // Get a specific event. This could be coming from
        // a paginated group or standalone event.
        return [['event', url, { query: query }]];
    };
    Object.defineProperty(EventDetailsContent.prototype, "projectId", {
        get: function () {
            return this.props.eventSlug.split(':')[0];
        },
        enumerable: false,
        configurable: true
    });
    EventDetailsContent.prototype.fetchTotal = function () {
        var _a, _b, _c;
        return __awaiter(this, void 0, void 0, function () {
            var _d, location, organization, event, traceId, _e, start, end, apiPayload, traceSize;
            return __generator(this, function (_f) {
                switch (_f.label) {
                    case 0:
                        _d = this.props, location = _d.location, organization = _d.organization;
                        event = this.state.event;
                        if (!event) {
                            return [2 /*return*/];
                        }
                        traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : null;
                        if (!traceId) {
                            return [2 /*return*/];
                        }
                        _e = getTraceTimeRangeFromEvent(event), start = _e.start, end = _e.end;
                        apiPayload = makeEventView({ start: start, end: end });
                        apiPayload.query = "trace:" + traceId;
                        return [4 /*yield*/, fetchTotalCount(this.api, organization.slug, apiPayload.getEventsAPIPayload(location))];
                    case 1:
                        traceSize = _f.sent();
                        this.setState({ traceSize: traceSize });
                        return [2 /*return*/];
                }
            });
        });
    };
    EventDetailsContent.prototype.renderBody = function () {
        var event = this.state.event;
        if (!event) {
            return <NotFound />;
        }
        return this.renderContent(event);
    };
    EventDetailsContent.prototype.renderContent = function (event) {
        var _this = this;
        var _a;
        var _b = this.props, organization = _b.organization, location = _b.location, eventView = _b.eventView;
        var isSidebarVisible = this.state.isSidebarVisible;
        // metrics
        trackAnalyticsEvent({
            eventKey: 'discover_v2.event_details',
            eventName: 'Discoverv2: Opened Event Details',
            event_type: event.type,
            organization_id: parseInt(organization.id, 10),
        });
        var transactionName = (_a = event.tags.find(function (tag) { return tag.key === 'transaction'; })) === null || _a === void 0 ? void 0 : _a.value;
        var transactionSummaryTarget = event.type === 'transaction' && transactionName
            ? transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: transactionName,
                projectID: event.projectID,
                query: location.query,
            })
            : null;
        var eventJsonUrl = "/api/0/projects/" + organization.slug + "/" + this.projectId + "/events/" + event.eventID + "/json/";
        var renderContent = function (results) { return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <DiscoverBreadcrumb eventView={eventView} event={event} organization={organization} location={location}/>
            <EventHeader event={event}/>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <ButtonBar gap={1}>
              <Button onClick={_this.toggleSidebar}>
                {isSidebarVisible ? 'Hide Details' : 'Show Details'}
              </Button>
              {results && (<Button icon={<IconOpen />} href={eventJsonUrl} external>
                  {t('JSON')} (<FileSize bytes={event.size}/>)
                </Button>)}
              {transactionSummaryTarget && (<Feature organization={organization} features={['performance-view']}>
                  {function (_a) {
                    var hasFeature = _a.hasFeature;
                    return (<Button disabled={!hasFeature} priority="primary" to={transactionSummaryTarget}>
                      {t('Go to Summary')}
                    </Button>);
                }}
                </Feature>)}
            </ButtonBar>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          {results && (<Layout.Main fullWidth>
              <EventMetas quickTrace={results} event={event} organization={organization} projectId={_this.projectId} location={location} traceSize={_this.state.traceSize} errorDest="discover" transactionDest="discover"/>
            </Layout.Main>)}
          <Layout.Main fullWidth={!isSidebarVisible}>
            <Projects orgId={organization.slug} slugs={[_this.projectId]}>
              {function (_a) {
                var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded;
                return initiallyLoaded ? (<SpanEntryContext.Provider value={{
                        getViewChildTransactionTarget: function (childTransactionProps) {
                            var childTransactionLink = eventDetailsRoute({
                                eventSlug: childTransactionProps.eventSlug,
                                orgSlug: organization.slug,
                            });
                            return {
                                pathname: childTransactionLink,
                                query: eventView.generateQueryStringObject(),
                            };
                        },
                    }}>
                    <QuickTraceContext.Provider value={results}>
                      <BorderlessEventEntries organization={organization} event={event} project={projects[0]} location={location} showExampleCommit={false} showTagSummary={false} api={_this.api}/>
                    </QuickTraceContext.Provider>
                  </SpanEntryContext.Provider>) : (<LoadingIndicator />);
            }}
            </Projects>
          </Layout.Main>
          {isSidebarVisible && (<Layout.Side>
              {results === undefined && (<React.Fragment>
                  <EventMetadata event={event} organization={organization} projectId={_this.projectId}/>
                  <RootSpanStatus event={event}/>
                  <OpsBreakdown event={event}/>
                </React.Fragment>)}
              <EventVitals event={event}/>
              {event.groupID && (<LinkedIssue groupId={event.groupID} eventId={event.eventID}/>)}
              <TagsTable generateUrl={_this.generateTagUrl} event={event} query={eventView.query}/>
            </Layout.Side>)}
        </Layout.Body>
      </React.Fragment>); };
        var hasQuickTraceView = organization.features.includes('trace-view-quick') ||
            organization.features.includes('trace-view-summary');
        if (hasQuickTraceView) {
            return (<QuickTraceQuery event={event} location={location} orgSlug={organization.slug}>
          {function (results) { return renderContent(results); }}
        </QuickTraceQuery>);
        }
        return renderContent();
    };
    EventDetailsContent.prototype.renderError = function (error) {
        var notFound = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 404; });
        var permissionDenied = Object.values(this.state.errors).find(function (resp) { return resp && resp.status === 403; });
        if (notFound) {
            return <NotFound />;
        }
        if (permissionDenied) {
            return (<LoadingError message={t('You do not have permission to view that event.')}/>);
        }
        return _super.prototype.renderError.call(this, error, true, true);
    };
    EventDetailsContent.prototype.renderComponent = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization;
        var event = this.state.event;
        var eventSlug = this.getEventSlug();
        var projectSlug = eventSlug.split(':')[0];
        var title = generateTitle({ eventView: eventView, event: event, organization: organization });
        return (<SentryDocumentTitle title={title} orgSlug={organization.slug} projectSlug={projectSlug}>
        {_super.prototype.renderComponent.call(this)}
      </SentryDocumentTitle>);
    };
    return EventDetailsContent;
}(AsyncComponent));
var EventHeader = function (_a) {
    var event = _a.event;
    var message = getMessage(event);
    return (<EventHeaderContainer data-test-id="event-header">
      <TitleWrapper>
        <EventOrGroupTitle data={event}/>
      </TitleWrapper>
      {message && (<MessageWrapper>
          <EventMessage message={message}/>
        </MessageWrapper>)}
    </EventHeaderContainer>);
};
var EventHeaderContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-width: ", ";\n"], ["\n  max-width: ", ";\n"])), function (p) { return p.theme.breakpoints[0]; });
var TitleWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-top: 20px;\n"], ["\n  font-size: ", ";\n  margin-top: 20px;\n"])), function (p) { return p.theme.headerFontSize; });
var MessageWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(1));
export default EventDetailsContent;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=content.jsx.map
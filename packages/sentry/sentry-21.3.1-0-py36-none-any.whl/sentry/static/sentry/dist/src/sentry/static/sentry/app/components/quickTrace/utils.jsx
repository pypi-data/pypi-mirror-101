import { __assign, __read, __spreadArray } from "tslib";
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import EventView from 'app/utils/discover/eventView';
import { eventDetailsRouteWithEventView, generateEventSlug } from 'app/utils/discover/urls';
import { getTraceTimeRangeFromEvent } from 'app/utils/performance/quickTrace/utils';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { getTraceDetailsUrl } from 'app/views/performance/traceDetails/utils';
import { getTransactionDetailsUrl } from 'app/views/performance/utils';
function generateIssueEventTarget(event, organization) {
    return "/organizations/" + organization.slug + "/issues/" + event.issue_id + "/events/" + event.event_id;
}
function generatePerformanceEventTarget(event, organization, location) {
    var eventSlug = generateEventSlug({
        id: event.event_id,
        project: event.project_slug,
    });
    return getTransactionDetailsUrl(organization, eventSlug, event.transaction, location.query);
}
function generateDiscoverEventTarget(event, organization, location) {
    var eventSlug = generateEventSlug({
        id: event.event_id,
        project: event.project_slug,
    });
    return eventDetailsRouteWithEventView({
        orgSlug: organization.slug,
        eventSlug: eventSlug,
        eventView: EventView.fromLocation(location),
    });
}
export function generateSingleErrorTarget(event, organization, location, destination) {
    switch (destination) {
        case 'issue':
            return generateIssueEventTarget(event, organization);
        case 'discover':
        default:
            return generateDiscoverEventTarget(event, organization, location);
    }
}
export function generateSingleTransactionTarget(event, organization, location, destination) {
    switch (destination) {
        case 'performance':
            return generatePerformanceEventTarget(event, organization, location);
        case 'discover':
        default:
            return generateDiscoverEventTarget(event, organization, location);
    }
}
export function generateMultiTransactionsTarget(currentEvent, events, organization, groupType) {
    var queryResults = new QueryResults([]);
    var eventIds = events.map(function (child) { return child.event_id; });
    for (var i = 0; i < eventIds.length; i++) {
        queryResults.addOp(i === 0 ? '(' : 'OR');
        queryResults.addQuery("id:" + eventIds[i]);
        if (i === eventIds.length - 1) {
            queryResults.addOp(')');
        }
    }
    var _a = getTraceTimeRangeFromEvent(currentEvent), start = _a.start, end = _a.end;
    var traceEventView = EventView.fromSavedQuery({
        id: undefined,
        name: groupType + " Transactions of Event ID " + currentEvent.id,
        fields: ['transaction', 'project', 'trace.span', 'transaction.duration', 'timestamp'],
        orderby: '-timestamp',
        query: stringifyQueryObject(queryResults),
        projects: __spreadArray([], __read(new Set(events.map(function (child) { return child.project_id; })))),
        version: 2,
        start: start,
        end: end,
    });
    return traceEventView.getResultsViewUrlTarget(organization.slug);
}
export function generateTraceTarget(event, organization) {
    var _a, _b, _c;
    var traceId = (_c = (_b = (_a = event.contexts) === null || _a === void 0 ? void 0 : _a.trace) === null || _b === void 0 ? void 0 : _b.trace_id) !== null && _c !== void 0 ? _c : '';
    var dateSelection = getParams(getTraceTimeRangeFromEvent(event));
    if (organization.features.includes('trace-view-summary')) {
        // TODO(txiao): Should this persist the current query when going to trace view?
        return getTraceDetailsUrl(organization, traceId, dateSelection, {});
    }
    var eventView = EventView.fromSavedQuery(__assign({ id: undefined, name: "Transactions with Trace ID " + traceId, fields: ['transaction', 'project', 'trace.span', 'transaction.duration', 'timestamp'], orderby: '-timestamp', query: "event.type:transaction trace:" + traceId, projects: [ALL_ACCESS_PROJECTS], version: 2 }, dateSelection));
    return eventView.getResultsViewUrlTarget(organization.slug);
}
//# sourceMappingURL=utils.jsx.map
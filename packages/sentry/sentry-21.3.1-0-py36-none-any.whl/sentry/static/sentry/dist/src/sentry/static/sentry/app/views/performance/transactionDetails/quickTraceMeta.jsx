import React from 'react';
import ErrorBoundary from 'app/components/errorBoundary';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import QuickTrace from 'app/components/quickTrace';
import { generateTraceTarget } from 'app/components/quickTrace/utils';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getShortEventId } from 'app/utils/events';
import { MetaData } from './styles';
function handleTraceLink(organization) {
    trackAnalyticsEvent({
        eventKey: 'quick_trace.trace_id.clicked',
        eventName: 'Quick Trace: Trace ID clicked',
        organization_id: parseInt(organization.id, 10),
        source: 'events',
    });
}
export default function QuickTraceMeta(_a) {
    var _b, _c, _d;
    var event = _a.event, location = _a.location, organization = _a.organization, _e = _a.quickTrace, isLoading = _e.isLoading, error = _e.error, trace = _e.trace, type = _e.type, traceSize = _a.traceSize, errorDest = _a.errorDest, transactionDest = _a.transactionDest;
    var traceId = (_d = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id) !== null && _d !== void 0 ? _d : null;
    var traceTarget = generateTraceTarget(event, organization);
    var linkText = traceId === null
        ? null
        : t('Trace ID: %s (%s events)', getShortEventId(traceId), traceSize ? traceSize : '?');
    var body = isLoading ? (<Placeholder height="24px"/>) : error || trace === null ? ('\u2014') : (<ErrorBoundary mini>
      <QuickTrace event={event} quickTrace={{ type: type, trace: trace }} location={location} organization={organization} anchor="right" errorDest={errorDest} transactionDest={transactionDest}/>
    </ErrorBoundary>);
    return (<MetaData headingText={t('Quick Trace')} beta tooltipText={t('A minified version of the full trace.')} bodyText={body} subtext={traceId === null ? ('\u2014') : (<Link to={traceTarget} onClick={function () { return handleTraceLink(organization); }}>
            {linkText}
          </Link>)}/>);
}
//# sourceMappingURL=quickTraceMeta.jsx.map
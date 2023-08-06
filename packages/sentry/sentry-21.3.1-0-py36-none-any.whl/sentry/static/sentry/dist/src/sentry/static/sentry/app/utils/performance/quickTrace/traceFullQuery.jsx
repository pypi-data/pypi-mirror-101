import { __assign, __rest } from "tslib";
import React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import { beforeFetch, getQuickTraceRequestPayload, makeEventView, } from 'app/utils/performance/quickTrace/utils';
import withApi from 'app/utils/withApi';
function getTraceFullRequestPayload(_a) {
    var detailed = _a.detailed, props = __rest(_a, ["detailed"]);
    var additionalApiPayload = getQuickTraceRequestPayload(props);
    additionalApiPayload.detailed = detailed ? '1' : '0';
    return additionalApiPayload;
}
function EmptyTrace(_a) {
    var children = _a.children;
    return (<React.Fragment>
      {children({
            isLoading: false,
            error: null,
            traces: null,
            type: 'full',
        })}
    </React.Fragment>);
}
function GenericTraceFullQuery(_a) {
    var traceId = _a.traceId, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, children = _a.children, props = __rest(_a, ["traceId", "start", "end", "statsPeriod", "children"]);
    if (!traceId) {
        return <EmptyTrace>{children}</EmptyTrace>;
    }
    var eventView = makeEventView({ start: start, end: end, statsPeriod: statsPeriod });
    return (<GenericDiscoverQuery route={"events-trace/" + traceId} getRequestPayload={getTraceFullRequestPayload} beforeFetch={beforeFetch} eventView={eventView} {...props}>
      {function (_a) {
            var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
            return children(__assign({ 
                // This is using '||` instead of '??` here because
                // the client returns a empty string when the response
                // is 204. And we want the empty string, undefined and
                // null to be converted to null.
                traces: tableData || null, type: 'full' }, rest));
        }}
    </GenericDiscoverQuery>);
}
export var TraceFullQuery = withApi(function (props) { return (<GenericTraceFullQuery {...props} detailed={false}/>); });
export var TraceFullDetailedQuery = withApi(function (props) { return (<GenericTraceFullQuery {...props} detailed/>); });
//# sourceMappingURL=traceFullQuery.jsx.map
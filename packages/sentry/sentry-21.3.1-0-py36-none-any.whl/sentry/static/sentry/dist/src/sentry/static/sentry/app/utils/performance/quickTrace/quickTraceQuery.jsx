import { __assign, __rest, __values } from "tslib";
import React from 'react';
import { TraceFullQuery } from 'app/utils/performance/quickTrace/traceFullQuery';
import TraceLiteQuery from 'app/utils/performance/quickTrace/traceLiteQuery';
import { flattenRelevantPaths, getTraceTimeRangeFromEvent, } from 'app/utils/performance/quickTrace/utils';
export default function QuickTraceQuery(_a) {
    var _b, _c;
    var children = _a.children, event = _a.event, props = __rest(_a, ["children", "event"]);
    var traceId = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id;
    if (!traceId) {
        return (<React.Fragment>
        {children({
                isLoading: false,
                error: null,
                trace: [],
                type: 'empty',
            })}
      </React.Fragment>);
    }
    var _d = getTraceTimeRangeFromEvent(event), start = _d.start, end = _d.end;
    return (<TraceLiteQuery eventId={event.id} traceId={traceId} start={start} end={end} {...props}>
      {function (traceLiteResults) { return (<TraceFullQuery traceId={traceId} start={start} end={end} {...props}>
          {function (traceFullResults) {
                var e_1, _a;
                var _b;
                if (!traceFullResults.isLoading &&
                    traceFullResults.error === null &&
                    traceFullResults.traces !== null) {
                    try {
                        for (var _c = __values(traceFullResults.traces), _d = _c.next(); !_d.done; _d = _c.next()) {
                            var subtrace = _d.value;
                            try {
                                var trace = flattenRelevantPaths(event, subtrace);
                                return children(__assign(__assign({}, traceFullResults), { trace: trace }));
                            }
                            catch (_e) {
                                // let this fall through and check the next subtrace
                                // or use the trace lite results
                            }
                        }
                    }
                    catch (e_1_1) { e_1 = { error: e_1_1 }; }
                    finally {
                        try {
                            if (_d && !_d.done && (_a = _c.return)) _a.call(_c);
                        }
                        finally { if (e_1) throw e_1.error; }
                    }
                }
                if (!traceLiteResults.isLoading &&
                    traceLiteResults.error === null &&
                    traceLiteResults.trace !== null) {
                    return children(traceLiteResults);
                }
                return children({
                    isLoading: traceFullResults.isLoading || traceLiteResults.isLoading,
                    error: (_b = traceFullResults.error) !== null && _b !== void 0 ? _b : traceLiteResults.error,
                    trace: [],
                    type: 'empty',
                });
            }}
        </TraceFullQuery>); }}
    </TraceLiteQuery>);
}
//# sourceMappingURL=quickTraceQuery.jsx.map
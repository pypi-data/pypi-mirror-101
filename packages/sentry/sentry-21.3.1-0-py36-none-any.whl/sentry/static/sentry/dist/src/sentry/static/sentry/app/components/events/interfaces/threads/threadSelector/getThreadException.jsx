import { __assign } from "tslib";
import { defined } from 'app/utils';
function getException(exceptionData, exceptionDataValues, thread) {
    if (exceptionDataValues.length === 1 && !exceptionDataValues[0].stacktrace) {
        return __assign(__assign({}, exceptionData), { values: [
                __assign(__assign({}, exceptionDataValues[0]), { stacktrace: thread.stacktrace, rawStacktrace: thread.rawStacktrace }),
            ] });
    }
    var exceptionHasAtLeastOneStacktrace = !!exceptionDataValues.find(function (exceptionDataValue) { return exceptionDataValue.stacktrace; });
    if (!!exceptionHasAtLeastOneStacktrace) {
        return exceptionData;
    }
    return undefined;
}
function getThreadException(event, thread) {
    var exceptionEntry = event.entries.find(function (entry) { return entry.type === 'exception'; });
    if (!exceptionEntry) {
        return undefined;
    }
    var exceptionData = exceptionEntry.data;
    var exceptionDataValues = exceptionData.values;
    if (!(exceptionDataValues === null || exceptionDataValues === void 0 ? void 0 : exceptionDataValues.length) || !thread) {
        return undefined;
    }
    var matchedStacktraceAndExceptionThread = exceptionDataValues.find(function (exceptionDataValue) { return exceptionDataValue.threadId === thread.id; });
    if (matchedStacktraceAndExceptionThread) {
        return getException(exceptionData, exceptionDataValues, thread);
    }
    if (exceptionDataValues.every(function (exceptionDataValue) { return !defined(exceptionDataValue.threadId); }) &&
        thread.crashed) {
        return getException(exceptionData, exceptionDataValues, thread);
    }
    return undefined;
}
export default getThreadException;
//# sourceMappingURL=getThreadException.jsx.map
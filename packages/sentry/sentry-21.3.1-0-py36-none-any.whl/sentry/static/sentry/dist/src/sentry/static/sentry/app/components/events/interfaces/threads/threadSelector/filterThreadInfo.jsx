import { trimPackage } from 'app/components/events/interfaces/frame/utils';
import getRelevantFrame from './getRelevantFrame';
import getThreadException from './getThreadException';
import getThreadStacktrace from './getThreadStacktrace';
import trimFilename from './trimFilename';
function filterThreadInfo(event, thread, exception) {
    var _a;
    var threadInfo = {};
    var stacktrace = getThreadStacktrace(false, thread);
    if (thread.crashed) {
        var threadException = exception !== null && exception !== void 0 ? exception : getThreadException(event, thread);
        var matchedStacktraceAndExceptionThread = threadException === null || threadException === void 0 ? void 0 : threadException.values.find(function (exceptionDataValue) { return exceptionDataValue.threadId === thread.id; });
        if (matchedStacktraceAndExceptionThread) {
            stacktrace = (_a = matchedStacktraceAndExceptionThread.stacktrace) !== null && _a !== void 0 ? _a : undefined;
        }
        threadInfo.crashedInfo = threadException;
    }
    if (!stacktrace) {
        return threadInfo;
    }
    var relevantFrame = getRelevantFrame(stacktrace);
    if (relevantFrame.filename) {
        threadInfo.filename = trimFilename(relevantFrame.filename);
    }
    if (relevantFrame.function) {
        threadInfo.label = relevantFrame.function;
        return threadInfo;
    }
    if (relevantFrame.package) {
        threadInfo.label = trimPackage(relevantFrame.package);
        return threadInfo;
    }
    if (relevantFrame.module) {
        threadInfo.label = relevantFrame.module;
        return threadInfo;
    }
    return threadInfo;
}
export default filterThreadInfo;
//# sourceMappingURL=filterThreadInfo.jsx.map
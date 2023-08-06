import { __read, __spreadArray } from "tslib";
import { EntryType } from 'app/types/event';
var NATIVE_PLATFORMS = ['cocoa', 'native'];
// Finds all frames in a given data blob and returns it's platforms
function getPlatforms(exceptionValue) {
    var _a, _b, _c, _d;
    var frames = (_a = exceptionValue === null || exceptionValue === void 0 ? void 0 : exceptionValue.frames) !== null && _a !== void 0 ? _a : [];
    var stacktraceFrames = (_d = (_c = (_b = exceptionValue) === null || _b === void 0 ? void 0 : _b.stacktrace) === null || _c === void 0 ? void 0 : _c.frames) !== null && _d !== void 0 ? _d : [];
    if (!frames.length && !stacktraceFrames.length) {
        return [];
    }
    return __spreadArray(__spreadArray([], __read(frames)), __read(stacktraceFrames)).map(function (frame) { return frame.platform; })
        .filter(function (platform) { return !!platform; });
}
function getStackTracePlatforms(event, exceptionEntry) {
    var _a, _b, _c, _d, _e;
    // Fetch platforms in stack traces of an exception entry
    var exceptionEntryPlatforms = ((_a = exceptionEntry.data.values) !== null && _a !== void 0 ? _a : []).flatMap(getPlatforms);
    // Fetch platforms in an exception entry
    var stackTraceEntry = ((_c = (_b = event.entries.find(function (entry) { return entry.type === EntryType.STACKTRACE; })) === null || _b === void 0 ? void 0 : _b.data) !== null && _c !== void 0 ? _c : {});
    // Fetch platforms in an exception entry
    var stackTraceEntryPlatforms = Object.keys(stackTraceEntry).flatMap(function (key) {
        return getPlatforms(stackTraceEntry[key]);
    });
    // Fetch platforms in an thread entry
    var threadEntry = ((_e = (_d = event.entries.find(function (entry) { return entry.type === EntryType.THREADS; })) === null || _d === void 0 ? void 0 : _d.data.values) !== null && _e !== void 0 ? _e : []);
    // Fetch platforms in a thread entry
    var threadEntryPlatforms = threadEntry.flatMap(function (_a) {
        var stacktrace = _a.stacktrace;
        return getPlatforms(stacktrace);
    });
    return new Set(__spreadArray(__spreadArray(__spreadArray([], __read(exceptionEntryPlatforms)), __read(stackTraceEntryPlatforms)), __read(threadEntryPlatforms)));
}
// Checks whether an event indicates that it has an apple crash report.
function isNativeEvent(event, exceptionEntry) {
    var platform = event.platform;
    if (platform && NATIVE_PLATFORMS.includes(platform)) {
        return true;
    }
    var stackTracePlatforms = getStackTracePlatforms(event, exceptionEntry);
    return NATIVE_PLATFORMS.some(function (nativePlatform) { return stackTracePlatforms.has(nativePlatform); });
}
//  Checks whether an event indicates that it has an associated minidump.
function isMinidumpEvent(exceptionEntry) {
    var _a;
    var data = exceptionEntry.data;
    return ((_a = data.values) !== null && _a !== void 0 ? _a : []).some(function (value) { var _a; return ((_a = value.mechanism) === null || _a === void 0 ? void 0 : _a.type) === 'minidump'; });
}
// Checks whether an event indicates that it has an apple crash report.
function isAppleCrashReportEvent(exceptionEntry) {
    var _a;
    var data = exceptionEntry.data;
    return ((_a = data.values) !== null && _a !== void 0 ? _a : []).some(function (value) { var _a; return ((_a = value.mechanism) === null || _a === void 0 ? void 0 : _a.type) === 'applecrashreport'; });
}
export function displayReprocessEventAction(orgFeatures, event) {
    if (!event || !orgFeatures.includes('reprocessing-v2')) {
        return false;
    }
    var entries = event.entries;
    var exceptionEntry = entries.find(function (entry) { return entry.type === EntryType.EXCEPTION; });
    if (!exceptionEntry) {
        return false;
    }
    // We want to show the reprocessing button if the issue in question is native or contains native frames.
    // The logic is taken from the symbolication pipeline in Python, where it is used to determine whether reprocessing
    // payloads should be stored:
    // https://github.com/getsentry/sentry/blob/cb7baef414890336881d67b7a8433ee47198c701/src/sentry/lang/native/processing.py#L425-L426
    // It is still not ideal as one can always merge native and non-native events together into one issue,
    // but it's the best approximation we have.
    if (!isMinidumpEvent(exceptionEntry) &&
        !isAppleCrashReportEvent(exceptionEntry) &&
        !isNativeEvent(event, exceptionEntry)) {
        return false;
    }
    return true;
}
//# sourceMappingURL=displayReprocessEventAction.jsx.map
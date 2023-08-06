function getThreadStacktrace(raw, thread) {
    if (!thread) {
        return undefined;
    }
    if (raw && thread.rawStacktrace) {
        return thread.rawStacktrace;
    }
    if (thread.stacktrace) {
        return thread.stacktrace;
    }
    return undefined;
}
export default getThreadStacktrace;
//# sourceMappingURL=getThreadStacktrace.jsx.map
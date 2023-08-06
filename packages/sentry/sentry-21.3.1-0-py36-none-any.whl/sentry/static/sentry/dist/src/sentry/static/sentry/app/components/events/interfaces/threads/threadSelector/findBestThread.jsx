function findBestThread(threads) {
    // search the entire threads list for a crashed thread with stack trace
    return (threads.find(function (thread) { return thread.crashed; }) ||
        threads.find(function (thread) { return thread.stacktrace; }) ||
        threads[0]);
}
export default findBestThread;
//# sourceMappingURL=findBestThread.jsx.map
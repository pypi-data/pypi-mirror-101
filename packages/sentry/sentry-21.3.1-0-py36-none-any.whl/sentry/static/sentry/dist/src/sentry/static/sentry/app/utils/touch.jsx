function isReactEvent(maybe) {
    return 'nativeEvent' in maybe;
}
/**
 * Handle getting position out of both React and Raw DOM events
 * as both are handled here due to mousedown/mousemove events
 * working differently.
 */
export function getPointerPosition(event, property) {
    var actual = isReactEvent(event) ? event.nativeEvent : event;
    if (window.TouchEvent && actual instanceof TouchEvent) {
        return actual.targetTouches[0][property];
    }
    if (actual instanceof MouseEvent) {
        return actual[property];
    }
    return 0;
}
//# sourceMappingURL=touch.jsx.map
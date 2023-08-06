/**
 * Combine refs to allow assignment to all passed refs
 */
export default function mergeRefs(refs) {
    return function (value) {
        refs.forEach(function (ref) {
            if (typeof ref === 'function') {
                ref(value);
            }
            else if (ref !== null && ref !== undefined) {
                ref.current = value;
            }
        });
    };
}
//# sourceMappingURL=mergeRefs.jsx.map
// hook from https://usehooks.com/useOnClickOutside/
import { useEffect } from 'react';
function useOnClickOutside(ref, handler) {
    useEffect(function () {
        var listener = function (event) {
            var el = ref === null || ref === void 0 ? void 0 : ref.current;
            // Do nothing if clicking ref's element or descendent elements
            if (!el || el.contains(event.target)) {
                return;
            }
            handler(event);
        };
        document.addEventListener('mousedown', listener);
        document.addEventListener('touchstart', listener);
        return function () {
            document.removeEventListener('mousedown', listener);
            document.removeEventListener('touchstart', listener);
        };
    }, 
    // Reload only if ref or handler changes
    [ref, handler]);
}
export default useOnClickOutside;
//# sourceMappingURL=useOnClickOutside.jsx.map
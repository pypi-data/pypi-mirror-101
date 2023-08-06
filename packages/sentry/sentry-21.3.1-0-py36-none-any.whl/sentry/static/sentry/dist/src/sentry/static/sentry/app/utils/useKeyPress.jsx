import { __read } from "tslib";
// hook from https://usehooks.com/useKeyPress/
import { useEffect, useState } from 'react';
function useKeyPress(targetKey) {
    // State for keeping track of whether key is pressed
    var _a = __read(useState(false), 2), keyPressed = _a[0], setKeyPressed = _a[1];
    // If pressed key is the target key then set to true
    function downHandler(_a) {
        var key = _a.key;
        if (key === targetKey) {
            setKeyPressed(true);
        }
    }
    // If released key is the target key then set to false
    function upHandler(_a) {
        var key = _a.key;
        if (key === targetKey) {
            setKeyPressed(false);
        }
    }
    // Add event listeners
    useEffect(function () {
        window.addEventListener('keydown', downHandler);
        window.addEventListener('keyup', upHandler);
        // Remove event listeners on cleanup
        return function () {
            window.removeEventListener('keydown', downHandler);
            window.removeEventListener('keyup', upHandler);
        };
    }, []); // Empty array ensures that effect is only run on mount and unmount
    return keyPressed;
}
export default useKeyPress;
//# sourceMappingURL=useKeyPress.jsx.map
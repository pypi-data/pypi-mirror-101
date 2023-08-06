import { __read, __spreadArray } from "tslib";
/**
 * Remove item at `index` in `array` without mutating `array`
 */
export function removeAtArrayIndex(array, index) {
    var newArray = __spreadArray([], __read(array));
    newArray.splice(index, 1);
    return newArray;
}
//# sourceMappingURL=removeAtArrayIndex.jsx.map
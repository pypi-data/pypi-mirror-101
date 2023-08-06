function isStringList(maybe) {
    return typeof maybe[0] === 'string';
}
/**
 * Converts arg from a `select2` choices array to a `react-select` `options` array
 * This contains some any hacks as this is creates type errors with the generics
 * used in SelectControl as the generics conflict with the concrete types here.
 */
var convertFromSelect2Choices = function (choices) {
    // TODO(ts): This is to make sure that this function is backwards compatible, ideally,
    // this function only accepts arrays
    if (!Array.isArray(choices)) {
        return undefined;
    }
    if (isStringList(choices)) {
        return choices.map(function (choice) { return ({ value: choice, label: choice }); });
    }
    return choices.map(function (choice) { return ({ value: choice[0], label: choice[1] }); });
};
export default convertFromSelect2Choices;
//# sourceMappingURL=convertFromSelect2Choices.jsx.map
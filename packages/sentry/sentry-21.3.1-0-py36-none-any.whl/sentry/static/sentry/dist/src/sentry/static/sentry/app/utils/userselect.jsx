export var setBodyUserSelect = function (nextValues) {
    // NOTE: Vendor prefixes other than `ms` should begin with a capital letter.
    // ref: https://reactjs.org/docs/dom-elements.html#style
    var previousValues = {
        userSelect: document.body.style.userSelect,
        // MozUserSelect is not typed in TS
        // @ts-expect-error
        MozUserSelect: document.body.style.MozUserSelect,
        // msUserSelect is not typed in TS
        // @ts-expect-error
        msUserSelect: document.body.style.msUserSelect,
        webkitUserSelect: document.body.style.webkitUserSelect,
    };
    document.body.style.userSelect = nextValues.userSelect || '';
    // MozUserSelect is not typed in TS
    // @ts-expect-error
    document.body.style.MozUserSelect = nextValues.MozUserSelect || '';
    // msUserSelect is not typed in TS
    // @ts-expect-error
    document.body.style.msUserSelect = nextValues.msUserSelect || '';
    document.body.style.webkitUserSelect = nextValues.webkitUserSelect || '';
    return previousValues;
};
//# sourceMappingURL=userselect.jsx.map
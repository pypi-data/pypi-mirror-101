function createLocalStorage() {
    try {
        var localStorage_1 = window.localStorage;
        var mod = 'sentry';
        localStorage_1.setItem(mod, mod);
        localStorage_1.removeItem(mod);
        return {
            setItem: localStorage_1.setItem.bind(localStorage_1),
            getItem: localStorage_1.getItem.bind(localStorage_1),
            removeItem: localStorage_1.removeItem.bind(localStorage_1),
        };
    }
    catch (e) {
        return {
            setItem: function () {
                return;
            },
            // Returns null if key doesn't exist:
            // https://developer.mozilla.org/en-US/docs/Web/API/Storage/getItem
            getItem: function () {
                return null;
            },
            removeItem: function () {
                return null;
            },
        };
    }
}
var functions = createLocalStorage();
export default functions;
//# sourceMappingURL=localStorage.jsx.map
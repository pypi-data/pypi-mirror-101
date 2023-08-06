import getCookie from 'app/utils/getCookie';
export default function getCsrfToken() {
    var _a, _b;
    return (_b = getCookie((_a = window.csrfCookieName) !== null && _a !== void 0 ? _a : 'sc')) !== null && _b !== void 0 ? _b : '';
}
//# sourceMappingURL=getCsrfToken.jsx.map
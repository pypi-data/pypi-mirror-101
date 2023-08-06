import { __assign } from "tslib";
import isString from 'lodash/isString';
import * as queryString from 'query-string';
import { escapeDoubleQuotes } from 'app/utils';
// remove leading and trailing whitespace and remove double spaces
export function formatQueryString(qs) {
    return qs.trim().replace(/\s+/g, ' ');
}
export function addQueryParamsToExistingUrl(origUrl, queryParams) {
    var url;
    try {
        url = new URL(origUrl);
    }
    catch (_a) {
        return '';
    }
    var searchEntries = url.searchParams.entries();
    // Order the query params alphabetically.
    // Otherwise ``queryString`` orders them randomly and it's impossible to test.
    var params = JSON.parse(JSON.stringify(queryParams));
    var query = __assign(__assign({}, Object.fromEntries(searchEntries)), params);
    return url.protocol + "//" + url.host + url.pathname + "?" + queryString.stringify(query);
}
/**
 * Append a tag key:value to a query string.
 *
 * Handles spacing and quoting if necessary.
 */
export function appendTagCondition(query, key, value) {
    var currentQuery = Array.isArray(query) ? query.pop() : isString(query) ? query : '';
    if (typeof value === 'string' && /[:\s\(\)\\"]/g.test(value)) {
        value = "\"" + escapeDoubleQuotes(value) + "\"";
    }
    if (currentQuery) {
        currentQuery += " " + key + ":" + value;
    }
    else {
        currentQuery = key + ":" + value;
    }
    return currentQuery;
}
export function decodeScalar(value, fallback) {
    if (!value) {
        return fallback;
    }
    var unwrapped = Array.isArray(value) && value.length > 0
        ? value[0]
        : isString(value)
            ? value
            : fallback;
    return isString(unwrapped) ? unwrapped : fallback;
}
export function decodeList(value) {
    if (!value) {
        return [];
    }
    return Array.isArray(value) ? value : isString(value) ? [value] : [];
}
export default {
    decodeList: decodeList,
    decodeScalar: decodeScalar,
    formatQueryString: formatQueryString,
    addQueryParamsToExistingUrl: addQueryParamsToExistingUrl,
    appendTagCondition: appendTagCondition,
};
//# sourceMappingURL=queryString.jsx.map
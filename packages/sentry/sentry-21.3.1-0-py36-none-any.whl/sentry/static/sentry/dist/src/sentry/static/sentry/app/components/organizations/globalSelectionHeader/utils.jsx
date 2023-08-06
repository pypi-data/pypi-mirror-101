import identity from 'lodash/identity';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import pickBy from 'lodash/pickBy';
import { DATE_TIME_KEYS, URL_PARAM } from 'app/constants/globalSelectionHeader';
import { defined } from 'app/utils';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { getParams } from './getParams';
var DEFAULT_PARAMS = getParams({});
export function getStateFromQuery(query, _a) {
    var _b = _a === void 0 ? {} : _a, _c = _b.allowEmptyPeriod, allowEmptyPeriod = _c === void 0 ? false : _c, _d = _b.allowAbsoluteDatetime, allowAbsoluteDatetime = _d === void 0 ? true : _d;
    var parsedParams = getParams(query, { allowEmptyPeriod: allowEmptyPeriod, allowAbsoluteDatetime: allowAbsoluteDatetime });
    var projectFromQuery = query[URL_PARAM.PROJECT];
    var environmentFromQuery = query[URL_PARAM.ENVIRONMENT];
    var period = parsedParams.statsPeriod;
    var utc = parsedParams.utc;
    var hasAbsolute = allowAbsoluteDatetime && !!parsedParams.start && !!parsedParams.end;
    var project;
    if (defined(projectFromQuery) && Array.isArray(projectFromQuery)) {
        project = projectFromQuery.map(function (p) { return parseInt(p, 10); });
    }
    else if (defined(projectFromQuery)) {
        var projectFromQueryIdInt = parseInt(projectFromQuery, 10);
        project = isNaN(projectFromQueryIdInt) ? [] : [projectFromQueryIdInt];
    }
    else {
        project = projectFromQuery;
    }
    var environment = defined(environmentFromQuery) && !Array.isArray(environmentFromQuery)
        ? [environmentFromQuery]
        : environmentFromQuery;
    var start = hasAbsolute ? getUtcToLocalDateObject(parsedParams.start) : null;
    var end = hasAbsolute ? getUtcToLocalDateObject(parsedParams.end) : null;
    return {
        project: project,
        environment: environment,
        period: period || null,
        start: start || null,
        end: end || null,
        // params from URL will be a string
        utc: typeof utc !== 'undefined' ? utc === 'true' : null,
    };
}
/**
 * Extract the global selection parameters from an object
 * Useful for extracting global selection properties from the current URL
 * when building another URL.
 */
export function extractSelectionParameters(query) {
    return pickBy(pick(query, Object.values(URL_PARAM)), identity);
}
/**
 * Extract the global selection datetime parameters from an object.
 */
export function extractDatetimeSelectionParameters(query) {
    return pickBy(pick(query, Object.values(DATE_TIME_KEYS)), identity);
}
export function getDefaultSelection() {
    var utc = DEFAULT_PARAMS.utc;
    return {
        projects: [],
        environments: [],
        datetime: {
            start: DEFAULT_PARAMS.start || null,
            end: DEFAULT_PARAMS.end || null,
            period: DEFAULT_PARAMS.statsPeriod || '',
            utc: typeof utc !== 'undefined' ? utc === 'true' : null,
        },
    };
}
/**
 * Compare the non-utc values of two selections.
 * Useful when re-fetching data based on globalselection changing.
 *
 * utc is not compared as there is a problem somewhere in the selection
 * data flow that results in it being undefined | null | boolean instead of null | boolean.
 * The additional undefined state makes this function just as unreliable as isEqual(selection, other)
 */
export function isSelectionEqual(selection, other) {
    var _a, _b, _c, _d;
    if (!isEqual(selection.projects, other.projects) ||
        !isEqual(selection.environments, other.environments)) {
        return false;
    }
    // Use string comparison as we aren't interested in the identity of the datetimes.
    if (selection.datetime.period !== other.datetime.period ||
        ((_a = selection.datetime.start) === null || _a === void 0 ? void 0 : _a.toString()) !== ((_b = other.datetime.start) === null || _b === void 0 ? void 0 : _b.toString()) ||
        ((_c = selection.datetime.end) === null || _c === void 0 ? void 0 : _c.toString()) !== ((_d = other.datetime.end) === null || _d === void 0 ? void 0 : _d.toString())) {
        return false;
    }
    return true;
}
//# sourceMappingURL=utils.jsx.map
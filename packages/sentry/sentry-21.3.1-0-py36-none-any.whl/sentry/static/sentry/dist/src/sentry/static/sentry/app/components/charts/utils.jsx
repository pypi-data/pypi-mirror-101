import moment from 'moment';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { defined, escape } from 'app/utils';
import { parsePeriodToHours } from 'app/utils/dates';
import { decodeList } from 'app/utils/queryString';
var DEFAULT_TRUNCATE_LENGTH = 80;
// In minutes
export var SIXTY_DAYS = 86400;
export var THIRTY_DAYS = 43200;
export var TWO_WEEKS = 20160;
export var ONE_WEEK = 10080;
export var TWENTY_FOUR_HOURS = 1440;
export var ONE_HOUR = 60;
/**
 * If there are more releases than this number we hide "Releases" series by default
 */
export var RELEASE_LINES_THRESHOLD = 50;
export function truncationFormatter(value, truncate) {
    if (!truncate) {
        return escape(value);
    }
    var truncationLength = truncate && typeof truncate === 'number' ? truncate : DEFAULT_TRUNCATE_LENGTH;
    var truncated = value.length > truncationLength ? value.substring(0, truncationLength) + '…' : value;
    return escape(truncated);
}
/**
 * Use a shorter interval if the time difference is <= 24 hours.
 */
export function useShortInterval(datetimeObj) {
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    return diffInMinutes <= TWENTY_FOUR_HOURS;
}
export function getInterval(datetimeObj, highFidelity) {
    if (highFidelity === void 0) { highFidelity = false; }
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes >= SIXTY_DAYS) {
        // Greater than or equal to 60 days
        return highFidelity ? '4h' : '1d';
    }
    if (diffInMinutes >= THIRTY_DAYS) {
        // Greater than or equal to 30 days
        return highFidelity ? '1h' : '4h';
    }
    if (diffInMinutes > TWENTY_FOUR_HOURS) {
        // Greater than 24 hours
        return highFidelity ? '30m' : '1h';
    }
    if (diffInMinutes <= ONE_HOUR) {
        // Less than or equal to 1 hour
        return highFidelity ? '1m' : '5m';
    }
    // Between 1 hour and 24 hours
    return highFidelity ? '5m' : '15m';
}
export function getDiffInMinutes(datetimeObj) {
    var period = datetimeObj.period, start = datetimeObj.start, end = datetimeObj.end;
    if (start && end) {
        return moment(end).diff(start, 'minutes');
    }
    return (parsePeriodToHours(typeof period === 'string' ? period : DEFAULT_STATS_PERIOD) * 60);
}
// Max period (in hours) before we can no long include previous period
var MAX_PERIOD_HOURS_INCLUDE_PREVIOUS = 45 * 24;
export function canIncludePreviousPeriod(includePrevious, period) {
    if (!includePrevious) {
        return false;
    }
    if (period && parsePeriodToHours(period) > MAX_PERIOD_HOURS_INCLUDE_PREVIOUS) {
        return false;
    }
    // otherwise true
    return !!includePrevious;
}
/**
 * Generates a series selection based on the query parameters defined by the location.
 */
export function getSeriesSelection(location, parameter) {
    if (parameter === void 0) { parameter = 'unselectedSeries'; }
    var unselectedSeries = decodeList(location === null || location === void 0 ? void 0 : location.query[parameter]);
    return unselectedSeries.reduce(function (selection, series) {
        selection[series] = false;
        return selection;
    }, {});
}
export function isMultiSeriesStats(data) {
    return defined(data) && data.data === undefined && data.totals === undefined;
}
// If dimension is a number convert it to pixels, otherwise use dimension
// without transform
export var getDimensionValue = function (dimension) {
    if (typeof dimension === 'number') {
        return dimension + "px";
    }
    if (dimension === null) {
        return undefined;
    }
    return dimension;
};
//# sourceMappingURL=utils.jsx.map
import moment from 'moment';
import { DataCategory } from 'app/types';
import { formatUsageWithUnits } from '../utils';
export function getDateFromMoment(m) {
    return m.format('MMM D');
}
export function getDateFromUnixTimestamp(timestamp) {
    var date = moment.unix(timestamp);
    return getDateFromMoment(date);
}
export function getDateRange(dateStart, dateEnd) {
    var range = [];
    var start = moment(dateStart);
    var end = moment(dateEnd);
    while (!start.isAfter(end, 'd')) {
        range.push(getDateFromMoment(start));
        start.add(1, 'd');
    }
    return range;
}
export function getTooltipFormatter(dataCategory) {
    if (dataCategory === DataCategory.ATTACHMENTS) {
        return function (val) {
            if (val === void 0) { val = 0; }
            return formatUsageWithUnits(val, DataCategory.ATTACHMENTS, { useUnitScaling: true });
        };
    }
    return function (val) {
        if (val === void 0) { val = 0; }
        return val.toLocaleString();
    };
}
//# sourceMappingURL=utils.jsx.map
import { __rest } from "tslib";
import merge from 'lodash/merge';
import { getFormattedDate, getTimeFormat } from 'app/utils/dates';
import { truncationFormatter, useShortInterval } from '../utils';
export default function XAxis(_a) {
    var isGroupedByDate = _a.isGroupedByDate, useShortDate = _a.useShortDate, theme = _a.theme, start = _a.start, end = _a.end, period = _a.period, utc = _a.utc, props = __rest(_a, ["isGroupedByDate", "useShortDate", "theme", "start", "end", "period", "utc"]);
    var axisLabelFormatter = function (value, index) {
        if (isGroupedByDate) {
            var timeFormat = getTimeFormat();
            var dateFormat = useShortDate ? 'MMM Do' : "MMM D " + timeFormat;
            var firstItem = index === 0;
            var format = useShortInterval({ start: start, end: end, period: period }) && !firstItem ? timeFormat : dateFormat;
            return getFormattedDate(value, format, { local: !utc });
        }
        else if (props.truncate) {
            return truncationFormatter(value, props.truncate);
        }
        else {
            return undefined;
        }
    };
    return merge({
        type: isGroupedByDate ? 'time' : 'category',
        boundaryGap: false,
        axisLine: {
            lineStyle: {
                color: theme.chartLabel,
            },
        },
        axisTick: {
            lineStyle: {
                color: theme.chartLabel,
            },
        },
        splitLine: {
            show: false,
        },
        axisLabel: {
            color: theme.chartLabel,
            fontFamily: theme.text.family,
            margin: 12,
            // This was default with ChartZoom, we are making it default for all charts now
            // Otherwise the xAxis can look congested when there is always a min/max label
            showMaxLabel: false,
            showMinLabel: false,
            formatter: axisLabelFormatter,
        },
        axisPointer: {
            show: true,
            type: 'line',
            label: {
                show: false,
            },
            lineStyle: {
                width: 0.5,
            },
        },
    }, props);
}
//# sourceMappingURL=xAxis.jsx.map
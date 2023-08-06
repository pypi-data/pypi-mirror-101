import { __rest } from "tslib";
import merge from 'lodash/merge';
export default function YAxis(_a) {
    var theme = _a.theme, props = __rest(_a, ["theme"]);
    return merge({
        axisLine: {
            show: false,
        },
        axisTick: {
            show: false,
        },
        axisLabel: {
            color: theme.chartLabel,
            fontFamily: theme.text.family,
        },
        splitLine: {
            lineStyle: {
                color: theme.chartLineColor,
                opacity: 0.3,
            },
        },
    }, props);
}
//# sourceMappingURL=yAxis.jsx.map
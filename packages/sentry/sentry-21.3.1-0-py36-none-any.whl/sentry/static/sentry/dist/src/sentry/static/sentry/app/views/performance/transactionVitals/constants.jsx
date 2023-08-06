import { __assign, __read, __spreadArray } from "tslib";
import { t } from 'app/locale';
import { WebVital } from 'app/utils/discover/fields';
import { WEB_VITAL_DETAILS } from 'app/utils/performance/vitals/constants';
import theme from 'app/utils/theme';
export var NUM_BUCKETS = 100;
export var PERCENTILE = 0.75;
export var FILTER_OPTIONS = [
    { label: t('Exclude Outliers'), value: 'exclude_outliers' },
    { label: t('View All'), value: 'all' },
];
/**
 * This defines the grouping for histograms. Histograms that are in the same group
 * will be queried together on initial load for alignment. However, the zoom controls
 * are defined for each measurement independently.
 */
var _VITAL_GROUPS = [
    {
        vitals: [WebVital.FP, WebVital.FCP, WebVital.LCP],
        min: 0,
    },
    {
        vitals: [WebVital.FID],
        min: 0,
        precision: 2,
    },
    {
        vitals: [WebVital.CLS],
        min: 0,
        precision: 2,
    },
];
var _COLORS = __spreadArray([], __read(theme.charts.getColorPalette(_VITAL_GROUPS.reduce(function (count, _a) {
    var vitals = _a.vitals;
    return count + vitals.length;
}, 0) - 1))).reverse();
export var VITAL_GROUPS = _VITAL_GROUPS.map(function (group) { return (__assign(__assign({}, group), { colors: _COLORS.splice(0, group.vitals.length) })); });
export var ZOOM_KEYS = _VITAL_GROUPS.reduce(function (keys, _a) {
    var vitals = _a.vitals;
    vitals.forEach(function (vital) {
        var vitalSlug = WEB_VITAL_DETAILS[vital].slug;
        keys.push(vitalSlug + "Start");
        keys.push(vitalSlug + "End");
    });
    return keys;
}, []);
//# sourceMappingURL=constants.jsx.map
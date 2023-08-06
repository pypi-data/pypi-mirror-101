/**
 * Defines the keys which may be passed into the chartcuterie chart rendering
 * service.
 *
 * When adding or removing from this list, please also update the
 * sentry/charts/types.py file
 */
export var ChartType;
(function (ChartType) {
    ChartType["SLACK_DISCOVER_TOTAL_PERIOD"] = "slack:discover.totalPeriod";
    ChartType["SLACK_DISCOVER_TOTAL_DAILY"] = "slack:discover.totalDaily";
    ChartType["SLACK_DISCOVER_TOP5_PERIOD"] = "slack:discover.top5Period";
    ChartType["SLACK_DISCOVER_TOP5_DAILY"] = "slack:discover.top5Daily";
})(ChartType || (ChartType = {}));
//# sourceMappingURL=types.jsx.map
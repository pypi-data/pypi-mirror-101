import { __assign, __read } from "tslib";
import XAxis from 'app/components/charts/components/xAxis';
import AreaSeries from 'app/components/charts/series/areaSeries';
import BarSeries from 'app/components/charts/series/barSeries';
import { lightTheme as theme } from 'app/utils/theme';
import { slackChartDefaults, slackChartSize } from './slack';
import { ChartType } from './types';
var discoverxAxis = XAxis({
    theme: theme,
    boundaryGap: true,
    splitNumber: 3,
    isGroupedByDate: true,
    axisLabel: { fontSize: 11 },
});
export var discoverCharts = [];
discoverCharts.push(__assign({ key: ChartType.SLACK_DISCOVER_TOTAL_PERIOD, getOption: function (data) {
        var color = theme.charts.getColorPalette(data.stats.data.length - 2);
        var areaSeries = AreaSeries({
            name: data.seriesName,
            data: data.stats.data.map(function (_a) {
                var _b = __read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                return [
                    timestamp * 1000,
                    countsForTimestamp.reduce(function (acc, _a) {
                        var count = _a.count;
                        return acc + count;
                    }, 0),
                ];
            }),
            lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
            areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
        });
        return __assign(__assign({}, slackChartDefaults), { useUTC: true, color: color, series: [areaSeries] });
    } }, slackChartSize));
discoverCharts.push(__assign({ key: ChartType.SLACK_DISCOVER_TOTAL_DAILY, getOption: function (data) {
        var color = theme.charts.getColorPalette(data.stats.data.length - 2);
        var barSeries = BarSeries({
            name: data.seriesName,
            data: data.stats.data.map(function (_a) {
                var _b = __read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                return ({
                    value: [
                        timestamp * 1000,
                        countsForTimestamp.reduce(function (acc, _a) {
                            var count = _a.count;
                            return acc + count;
                        }, 0),
                    ],
                });
            }),
            itemStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
        });
        return __assign(__assign({}, slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color: color, series: [barSeries] });
    } }, slackChartSize));
discoverCharts.push(__assign({ key: ChartType.SLACK_DISCOVER_TOP5_PERIOD, getOption: function (data) {
        var stats = Object.values(data.stats);
        var color = theme.charts.getColorPalette(stats.length - 2);
        var series = stats
            .sort(function (a, b) { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map(function (topSeries, i) {
            return AreaSeries({
                stack: 'area',
                data: topSeries.data.map(function (_a) {
                    var _b = __read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                    return [
                        timestamp * 1000,
                        countsForTimestamp.reduce(function (acc, _a) {
                            var count = _a.count;
                            return acc + count;
                        }, 0),
                    ];
                }),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
            });
        });
        return __assign(__assign({}, slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color: color,
            series: series });
    } }, slackChartSize));
discoverCharts.push(__assign({ key: ChartType.SLACK_DISCOVER_TOP5_DAILY, getOption: function (data) {
        var stats = Object.values(data.stats);
        var color = theme.charts.getColorPalette(stats.length - 2);
        var series = stats
            .sort(function (a, b) { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map(function (topSeries, i) {
            return BarSeries({
                stack: 'area',
                data: topSeries.data.map(function (_a) {
                    var _b = __read(_a, 2), timestamp = _b[0], countsForTimestamp = _b[1];
                    return [
                        timestamp * 1000,
                        countsForTimestamp.reduce(function (acc, _a) {
                            var count = _a.count;
                            return acc + count;
                        }, 0),
                    ];
                }),
                itemStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
            });
        });
        return __assign(__assign({}, slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color: color,
            series: series });
    } }, slackChartSize));
//# sourceMappingURL=discover.jsx.map
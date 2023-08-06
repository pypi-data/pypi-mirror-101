import { __assign, __makeTemplateObject, __read, __spreadArray } from "tslib";
import 'zrender/lib/svg/svg';
import React from 'react';
import styled from '@emotion/styled';
import echarts from 'echarts/lib/echarts';
import ReactEchartsCore from 'echarts-for-react/lib/core';
import { withTheme } from 'emotion-theming';
import { IS_ACCEPTANCE_TEST } from 'app/constants';
import space from 'app/styles/space';
import Grid from './components/grid';
import Legend from './components/legend';
import Tooltip from './components/tooltip';
import XAxis from './components/xAxis';
import YAxis from './components/yAxis';
import LineSeries from './series/lineSeries';
import { getDimensionValue } from './utils';
// TODO(ts): What is the series type? EChartOption.Series's data cannot have
// `onClick` since it's typically an array.
//
// Handle series item clicks (e.g. Releases mark line or a single series
// item) This is different than when you hover over an "axis" line on a chart
// (e.g.  if there are 2 series for an axis and you're not directly hovered
// over an item)
//
// Calls "onClick" inside of series data
var handleClick = function (clickSeries, instance) {
    var _a, _b;
    if (clickSeries.data) {
        (_b = (_a = clickSeries.data).onClick) === null || _b === void 0 ? void 0 : _b.call(_a, clickSeries, instance);
    }
};
function BaseChartUnwrapped(_a) {
    var _b, _c, _d, _e, _f, _g;
    var theme = _a.theme, colors = _a.colors, grid = _a.grid, tooltip = _a.tooltip, legend = _a.legend, dataZoom = _a.dataZoom, toolBox = _a.toolBox, graphic = _a.graphic, axisPointer = _a.axisPointer, previousPeriod = _a.previousPeriod, echartsTheme = _a.echartsTheme, devicePixelRatio = _a.devicePixelRatio, showTimeInTooltip = _a.showTimeInTooltip, useShortDate = _a.useShortDate, start = _a.start, end = _a.end, period = _a.period, utc = _a.utc, yAxes = _a.yAxes, xAxes = _a.xAxes, style = _a.style, forwardedRef = _a.forwardedRef, onClick = _a.onClick, onLegendSelectChanged = _a.onLegendSelectChanged, onHighlight = _a.onHighlight, onMouseOver = _a.onMouseOver, onDataZoom = _a.onDataZoom, onRestore = _a.onRestore, onFinished = _a.onFinished, onRendered = _a.onRendered, _h = _a.options, options = _h === void 0 ? {} : _h, _j = _a.series, series = _j === void 0 ? [] : _j, _k = _a.yAxis, yAxis = _k === void 0 ? {} : _k, _l = _a.xAxis, xAxis = _l === void 0 ? {} : _l, _m = _a.height, height = _m === void 0 ? 200 : _m, _o = _a.width, width = _o === void 0 ? 'auto' : _o, _p = _a.renderer, renderer = _p === void 0 ? 'svg' : _p, _q = _a.notMerge, notMerge = _q === void 0 ? true : _q, _r = _a.lazyUpdate, lazyUpdate = _r === void 0 ? false : _r, _s = _a.isGroupedByDate, isGroupedByDate = _s === void 0 ? false : _s, _t = _a.transformSinglePointToBar, transformSinglePointToBar = _t === void 0 ? false : _t, _u = _a.onChartReady, onChartReady = _u === void 0 ? function () { } : _u;
    var hasSinglePoints = (_b = series) === null || _b === void 0 ? void 0 : _b.every(function (s) { return Array.isArray(s.data) && s.data.length <= 1; });
    var transformedSeries = (_d = (hasSinglePoints && transformSinglePointToBar
        ? (_c = series) === null || _c === void 0 ? void 0 : _c.map(function (s) {
            var _a;
            return (__assign(__assign({}, s), { type: 'bar', barWidth: 40, barGap: 0, itemStyle: __assign({}, ((_a = s.areaStyle) !== null && _a !== void 0 ? _a : {})) }));
        })
        : series)) !== null && _d !== void 0 ? _d : [];
    var transformedPreviousPeriod = (_e = previousPeriod === null || previousPeriod === void 0 ? void 0 : previousPeriod.map(function (previous) {
        return LineSeries({
            name: previous.seriesName,
            data: previous.data.map(function (_a) {
                var name = _a.name, value = _a.value;
                return [name, value];
            }),
            lineStyle: { color: theme.gray200, type: 'dotted' },
            itemStyle: { color: theme.gray200 },
        });
    })) !== null && _e !== void 0 ? _e : [];
    var resolvedSeries = !previousPeriod
        ? transformedSeries
        : __spreadArray(__spreadArray([], __read(transformedSeries)), __read(transformedPreviousPeriod));
    var defaultAxesProps = { theme: theme };
    var yAxisOrCustom = !yAxes
        ? yAxis !== null
            ? YAxis(__assign({ theme: theme }, yAxis))
            : undefined
        : Array.isArray(yAxes)
            ? yAxes.map(function (axis) { return YAxis(__assign(__assign({}, axis), { theme: theme })); })
            : [YAxis(defaultAxesProps), YAxis(defaultAxesProps)];
    var xAxisOrCustom = !xAxes
        ? xAxis !== null
            ? XAxis(__assign(__assign({}, xAxis), { theme: theme,
                useShortDate: useShortDate,
                start: start,
                end: end,
                period: period,
                isGroupedByDate: isGroupedByDate,
                utc: utc }))
            : undefined
        : Array.isArray(xAxes)
            ? xAxes.map(function (axis) {
                return XAxis(__assign(__assign({}, axis), { theme: theme, useShortDate: useShortDate, start: start, end: end, period: period, isGroupedByDate: isGroupedByDate, utc: utc }));
            })
            : [XAxis(defaultAxesProps), XAxis(defaultAxesProps)];
    // Maybe changing the series type to types/echarts Series[] would be a better
    // solution and can't use ignore for multiline blocks
    var seriesValid = series && ((_f = series[0]) === null || _f === void 0 ? void 0 : _f.data) && series[0].data.length > 1;
    var seriesData = seriesValid ? series[0].data : undefined;
    var bucketSize = seriesData ? seriesData[1][0] - seriesData[0][0] : undefined;
    var tooltipOrNone = tooltip !== null
        ? Tooltip(__assign({ showTimeInTooltip: showTimeInTooltip,
            isGroupedByDate: isGroupedByDate,
            utc: utc,
            bucketSize: bucketSize }, tooltip))
        : undefined;
    var color = colors ||
        (series.length ? theme.charts.getColorPalette(series.length) : theme.charts.colors);
    var chartOption = __assign(__assign({}, options), { animation: IS_ACCEPTANCE_TEST ? false : (_g = options.animation) !== null && _g !== void 0 ? _g : true, useUTC: utc, color: color, grid: Array.isArray(grid) ? grid.map(Grid) : Grid(grid), tooltip: tooltipOrNone, legend: legend ? Legend(__assign({ theme: theme }, legend)) : undefined, yAxis: yAxisOrCustom, xAxis: xAxisOrCustom, series: resolvedSeries, toolbox: toolBox, axisPointer: axisPointer,
        dataZoom: dataZoom,
        graphic: graphic });
    var chartStyles = __assign({ height: getDimensionValue(height), width: getDimensionValue(width) }, style);
    // XXX(epurkhiser): Echarts can become unhappy if one of these event handlers
    // causes the chart to re-render and be passed a whole different instance of
    // event handlers.
    //
    // We use React.useMemo to keep the value across renders
    //
    // eslint-disable-next-line sentry/no-react-hooks
    var eventsMap = React.useMemo(function () {
        return ({
            click: function (props, instance) {
                handleClick(props, instance);
                onClick === null || onClick === void 0 ? void 0 : onClick(props, instance);
            },
            highlight: function (props, instance) { return onHighlight === null || onHighlight === void 0 ? void 0 : onHighlight(props, instance); },
            mouseover: function (props, instance) { return onMouseOver === null || onMouseOver === void 0 ? void 0 : onMouseOver(props, instance); },
            datazoom: function (props, instance) { return onDataZoom === null || onDataZoom === void 0 ? void 0 : onDataZoom(props, instance); },
            restore: function (props, instance) { return onRestore === null || onRestore === void 0 ? void 0 : onRestore(props, instance); },
            finished: function (props, instance) { return onFinished === null || onFinished === void 0 ? void 0 : onFinished(props, instance); },
            rendered: function (props, instance) { return onRendered === null || onRendered === void 0 ? void 0 : onRendered(props, instance); },
            legendselectchanged: function (props, instance) {
                return onLegendSelectChanged === null || onLegendSelectChanged === void 0 ? void 0 : onLegendSelectChanged(props, instance);
            },
        });
    }, [onclick, onHighlight, onMouseOver, onDataZoom, onRestore, onFinished, onRendered]);
    return (<ChartContainer>
      <ReactEchartsCore ref={forwardedRef} echarts={echarts} notMerge={notMerge} lazyUpdate={lazyUpdate} theme={echartsTheme} onChartReady={onChartReady} onEvents={eventsMap} style={chartStyles} opts={{ height: height, width: width, renderer: renderer, devicePixelRatio: devicePixelRatio }} option={chartOption}/>
    </ChartContainer>);
}
// Contains styling for chart elements as we can't easily style those
// elements directly
var ChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* Tooltip styling */\n  .tooltip-series,\n  .tooltip-date {\n    color: ", ";\n    font-family: ", ";\n    background: ", ";\n    padding: ", " ", ";\n    border-radius: ", " ", " 0 0;\n  }\n  .tooltip-series-solo {\n    border-radius: ", ";\n  }\n  .tooltip-label {\n    margin-right: ", ";\n  }\n  .tooltip-label strong {\n    font-weight: normal;\n    color: ", ";\n  }\n  .tooltip-series > div {\n    display: flex;\n    justify-content: space-between;\n    align-items: baseline;\n  }\n  .tooltip-date {\n    border-top: 1px solid ", ";\n    text-align: center;\n    position: relative;\n    width: auto;\n    border-radius: ", ";\n  }\n  .tooltip-arrow {\n    top: 100%;\n    left: 50%;\n    border: 0px solid transparent;\n    content: ' ';\n    height: 0;\n    width: 0;\n    position: absolute;\n    pointer-events: none;\n    border-top-color: ", ";\n    border-width: 8px;\n    margin-left: -8px;\n  }\n\n  .echarts-for-react div:first-of-type {\n    width: 100% !important;\n  }\n\n  /* Tooltip description styling */\n  .tooltip-description {\n    color: ", ";\n    border-radius: ", ";\n    background: #000;\n    opacity: 0.9;\n    padding: 5px 10px;\n    position: relative;\n    font-weight: bold;\n    font-size: ", ";\n    line-height: 1.4;\n    font-family: ", ";\n    max-width: 230px;\n    min-width: 230px;\n    white-space: normal;\n    text-align: center;\n    :after {\n      content: '';\n      position: absolute;\n      top: 100%;\n      left: 50%;\n      width: 0;\n      height: 0;\n      border-left: 5px solid transparent;\n      border-right: 5px solid transparent;\n      border-top: 5px solid #000;\n      transform: translateX(-50%);\n    }\n  }\n"], ["\n  /* Tooltip styling */\n  .tooltip-series,\n  .tooltip-date {\n    color: ", ";\n    font-family: ", ";\n    background: ", ";\n    padding: ", " ", ";\n    border-radius: ", " ", " 0 0;\n  }\n  .tooltip-series-solo {\n    border-radius: ", ";\n  }\n  .tooltip-label {\n    margin-right: ", ";\n  }\n  .tooltip-label strong {\n    font-weight: normal;\n    color: ", ";\n  }\n  .tooltip-series > div {\n    display: flex;\n    justify-content: space-between;\n    align-items: baseline;\n  }\n  .tooltip-date {\n    border-top: 1px solid ", ";\n    text-align: center;\n    position: relative;\n    width: auto;\n    border-radius: ", ";\n  }\n  .tooltip-arrow {\n    top: 100%;\n    left: 50%;\n    border: 0px solid transparent;\n    content: ' ';\n    height: 0;\n    width: 0;\n    position: absolute;\n    pointer-events: none;\n    border-top-color: ", ";\n    border-width: 8px;\n    margin-left: -8px;\n  }\n\n  .echarts-for-react div:first-of-type {\n    width: 100% !important;\n  }\n\n  /* Tooltip description styling */\n  .tooltip-description {\n    color: ", ";\n    border-radius: ", ";\n    background: #000;\n    opacity: 0.9;\n    padding: 5px 10px;\n    position: relative;\n    font-weight: bold;\n    font-size: ", ";\n    line-height: 1.4;\n    font-family: ", ";\n    max-width: 230px;\n    min-width: 230px;\n    white-space: normal;\n    text-align: center;\n    :after {\n      content: '';\n      position: absolute;\n      top: 100%;\n      left: 50%;\n      width: 0;\n      height: 0;\n      border-left: 5px solid transparent;\n      border-right: 5px solid transparent;\n      border-top: 5px solid #000;\n      transform: translateX(-50%);\n    }\n  }\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.text.family; }, function (p) { return p.theme.gray500; }, space(1), space(2), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, space(1), function (p) { return p.theme.white; }, function (p) { return p.theme.gray400; }, function (p) { return p.theme.borderRadiusBottom; }, function (p) { return p.theme.gray500; }, function (p) { return p.theme.white; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.text.family; });
var BaseChartWithTheme = withTheme(BaseChartUnwrapped);
var BaseChart = React.forwardRef(function (props, ref) { return <BaseChartWithTheme forwardedRef={ref} {...props}/>; });
BaseChart.displayName = 'forwardRef(BaseChart)';
export default BaseChart;
var templateObject_1;
//# sourceMappingURL=baseChart.jsx.map
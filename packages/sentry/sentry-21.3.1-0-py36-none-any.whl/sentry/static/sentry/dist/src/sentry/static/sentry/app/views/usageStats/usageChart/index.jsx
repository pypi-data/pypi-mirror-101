import { __assign, __extends, __read } from "tslib";
import React from 'react';
import Color from 'color';
import { withTheme } from 'emotion-theming';
import BaseChart from 'app/components/charts/baseChart';
import Legend from 'app/components/charts/components/legend';
import Tooltip from 'app/components/charts/components/tooltip';
import xAxis from 'app/components/charts/components/xAxis';
import barSeries from 'app/components/charts/series/barSeries';
import { ChartContainer, HeaderTitleLegend } from 'app/components/charts/styles';
import Panel from 'app/components/panels/panel';
import ChartPalette from 'app/constants/chartPalette';
import { t } from 'app/locale';
import { DataCategory } from 'app/types';
import { formatAbbreviatedNumber } from 'app/utils/formatters';
import commonTheme from 'app/utils/theme';
import { formatUsageWithUnits, GIGABYTE } from '../utils';
import { getDateRange, getTooltipFormatter } from './utils';
var COLOR_ERRORS = ChartPalette[4][3];
var COLOR_ERRORS_DROPPED = Color(COLOR_ERRORS).lighten(0.25).string();
var COLOR_TRANSACTIONS = ChartPalette[4][2];
var COLOR_TRANSACTIONS_DROPPED = Color(COLOR_TRANSACTIONS).lighten(0.25).string();
var COLOR_ATTACHMENTS = ChartPalette[4][1];
var COLOR_ATTACHMENTS_DROPPED = Color(COLOR_ATTACHMENTS).lighten(0.5).string();
var COLOR_PROJECTED = commonTheme.gray200;
export var CHART_OPTIONS_DATACATEGORY = [
    {
        label: 'Errors',
        value: DataCategory.ERRORS,
        disabled: false,
    },
    {
        label: 'Transactions',
        value: DataCategory.TRANSACTIONS,
        disabled: false,
    },
    {
        label: 'Attachments',
        value: DataCategory.ATTACHMENTS,
        disabled: false,
    },
];
export var ChartDataTransform;
(function (ChartDataTransform) {
    ChartDataTransform["CUMULATIVE"] = "cumulative";
    ChartDataTransform["DAILY"] = "daily";
})(ChartDataTransform || (ChartDataTransform = {}));
export var CHART_OPTIONS_DATA_TRANSFORM = [
    {
        label: t('Cumulative'),
        value: ChartDataTransform.CUMULATIVE,
        disabled: false,
    },
    {
        label: t('Day-to-Day'),
        value: ChartDataTransform.DAILY,
        disabled: false,
    },
];
export var SeriesTypes;
(function (SeriesTypes) {
    SeriesTypes["ACCEPTED"] = "Accepted";
    SeriesTypes["DROPPED"] = "Dropped";
    SeriesTypes["PROJECTED"] = "Projected";
})(SeriesTypes || (SeriesTypes = {}));
var UsageChart = /** @class */ (function (_super) {
    __extends(UsageChart, _super);
    function UsageChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            xAxisDates: [],
        };
        return _this;
    }
    UsageChart.getDerivedStateFromProps = function (nextProps, prevState) {
        var usageDateStart = nextProps.usageDateStart, usageDateEnd = nextProps.usageDateEnd;
        var xAxisDates = getDateRange(usageDateStart, usageDateEnd);
        return __assign(__assign({}, prevState), { xAxisDates: xAxisDates });
    };
    Object.defineProperty(UsageChart.prototype, "chartColors", {
        get: function () {
            var dataCategory = this.props.dataCategory;
            if (dataCategory === DataCategory.ERRORS) {
                return [COLOR_ERRORS, COLOR_ERRORS_DROPPED, COLOR_PROJECTED];
            }
            if (dataCategory === DataCategory.ATTACHMENTS) {
                return [COLOR_ATTACHMENTS, COLOR_ATTACHMENTS_DROPPED, COLOR_PROJECTED];
            }
            return [COLOR_TRANSACTIONS, COLOR_TRANSACTIONS_DROPPED, COLOR_PROJECTED];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartMetadata", {
        get: function () {
            var _a = this.props, usageStats = _a.usageStats, dataCategory = _a.dataCategory, dataTransform = _a.dataTransform, handleDataTransformation = _a.handleDataTransformation;
            var xAxisDates = this.state.xAxisDates;
            var selectDataCategory = CHART_OPTIONS_DATACATEGORY.find(function (o) { return o.value === dataCategory; });
            if (!selectDataCategory) {
                throw new Error('Selected item is not supported');
            }
            // Do not assume that handleDataTransformation is a pure function
            var chartData = __assign({}, handleDataTransformation(usageStats, dataTransform));
            Object.keys(chartData).forEach(function (k) {
                var isProjected = k === SeriesTypes.PROJECTED;
                // Map the array and destructure elements to avoid side-effects
                chartData[k] = chartData[k].map(function (stat) {
                    return __assign(__assign({}, stat), { tooltip: { show: false }, itemStyle: { opacity: isProjected ? 0.6 : 1 } });
                });
            });
            var label = selectDataCategory.label, value = selectDataCategory.value;
            if (value === DataCategory.ERRORS || value === DataCategory.TRANSACTIONS) {
                return {
                    chartLabel: label,
                    chartData: chartData,
                    xAxisData: xAxisDates,
                    yAxisMinInterval: 1000,
                    yAxisFormatter: formatAbbreviatedNumber,
                    tooltipValueFormatter: getTooltipFormatter(dataCategory),
                };
            }
            return {
                chartLabel: label,
                chartData: chartData,
                xAxisData: xAxisDates,
                yAxisMinInterval: 1 * GIGABYTE,
                yAxisFormatter: function (val) {
                    return formatUsageWithUnits(val, DataCategory.ATTACHMENTS, {
                        isAbbreviated: true,
                        useUnitScaling: true,
                    });
                },
                tooltipValueFormatter: getTooltipFormatter(dataCategory),
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartSeries", {
        get: function () {
            var chartSeries = this.props.chartSeries;
            var chartData = this.chartMetadata.chartData;
            var series = [
                barSeries({
                    name: SeriesTypes.ACCEPTED,
                    data: chartData.accepted,
                    barMinHeight: 1,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
                barSeries({
                    name: SeriesTypes.DROPPED,
                    data: chartData.dropped,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
                barSeries({
                    name: SeriesTypes.PROJECTED,
                    data: chartData.projected,
                    barMinHeight: 1,
                    stack: 'usage',
                    legendHoverLink: false,
                }),
            ];
            // Additional series passed by parent component
            if (chartSeries) {
                series.concat(chartSeries);
            }
            return series;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartLegend", {
        get: function () {
            var chartData = this.chartMetadata.chartData;
            var legend = [
                {
                    name: SeriesTypes.ACCEPTED,
                },
            ];
            if (chartData.dropped.length > 0) {
                legend.push({
                    name: SeriesTypes.DROPPED,
                });
            }
            if (chartData.projected.length > 0) {
                legend.push({
                    name: SeriesTypes.PROJECTED,
                });
            }
            return legend;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UsageChart.prototype, "chartTooltip", {
        get: function () {
            var chartTooltip = this.props.chartTooltip;
            if (chartTooltip) {
                return chartTooltip;
            }
            var tooltipValueFormatter = this.chartMetadata.tooltipValueFormatter;
            return Tooltip({
                // Trigger to axis prevents tooltip from redrawing when hovering
                // over individual bars
                trigger: 'axis',
                valueFormatter: tooltipValueFormatter,
            });
        },
        enumerable: false,
        configurable: true
    });
    UsageChart.prototype.render = function () {
        var _a = this.props, theme = _a.theme, title = _a.title, footer = _a.footer;
        var _b = this.chartMetadata, xAxisData = _b.xAxisData, yAxisMinInterval = _b.yAxisMinInterval, yAxisFormatter = _b.yAxisFormatter;
        return (<Panel id="usage-chart">
        <ChartContainer>
          <HeaderTitleLegend>{title || t('Current Usage Period')}</HeaderTitleLegend>
          <BaseChart colors={this.chartColors} grid={{ bottom: '3px', left: '0px', right: '10px', top: '40px' }} xAxis={xAxis({
                show: true,
                type: 'category',
                name: 'Date',
                boundaryGap: true,
                data: xAxisData,
                truncate: 6,
                axisTick: {
                    interval: 6,
                    alignWithLabel: true,
                },
                axisLabel: {
                    interval: 6,
                },
                theme: theme,
            })} yAxis={{
                min: 0,
                minInterval: yAxisMinInterval,
                axisLabel: {
                    formatter: yAxisFormatter,
                    color: theme.chartLabel,
                },
            }} series={this.chartSeries} tooltip={this.chartTooltip} onLegendSelectChanged={function () { }} legend={Legend({
                right: 10,
                top: 5,
                data: this.chartLegend,
                theme: theme,
            })}/>
        </ChartContainer>
        {footer}
      </Panel>);
    };
    UsageChart.defaultProps = {
        handleDataTransformation: function (stats, transform) {
            var chartData = {
                accepted: [],
                dropped: [],
                projected: [],
            };
            var isCumulative = transform === ChartDataTransform.CUMULATIVE;
            Object.keys(stats).forEach(function (k) {
                var count = 0;
                chartData[k] = stats[k].map(function (stat) {
                    var _a = __read(stat.value, 2), x = _a[0], y = _a[1];
                    count = isCumulative ? count + y : y;
                    return __assign(__assign({}, stat), { value: [x, count] });
                });
            });
            return chartData;
        },
    };
    return UsageChart;
}(React.Component));
export { UsageChart };
export default withTheme(UsageChart);
//# sourceMappingURL=index.jsx.map
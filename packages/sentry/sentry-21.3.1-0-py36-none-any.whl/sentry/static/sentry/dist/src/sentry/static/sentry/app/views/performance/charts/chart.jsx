import { __assign, __extends } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
import max from 'lodash/max';
import min from 'lodash/min';
import AreaChart from 'app/components/charts/areaChart';
import ChartZoom from 'app/components/charts/chartZoom';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import { aggregateOutputType } from 'app/utils/discover/fields';
// adapted from https://stackoverflow.com/questions/11397239/rounding-up-for-a-graph-maximum
function computeAxisMax(data) {
    // assumes min is 0
    var valuesDict = data.map(function (value) { return value.data.map(function (point) { return point.value; }); });
    var maxValue = max(valuesDict.map(max));
    if (maxValue <= 1) {
        return 1;
    }
    var power = Math.log10(maxValue);
    var magnitude = min([max([Math.pow(10, (power - Math.floor(power))), 0]), 10]);
    var scale;
    if (magnitude <= 2.5) {
        scale = 0.2;
    }
    else if (magnitude <= 5) {
        scale = 0.5;
    }
    else if (magnitude <= 7.5) {
        scale = 1.0;
    }
    else {
        scale = 2.0;
    }
    var step = Math.pow(10, Math.floor(power)) * scale;
    return Math.round(Math.ceil(maxValue / step) * step);
}
var Chart = /** @class */ (function (_super) {
    __extends(Chart, _super);
    function Chart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Chart.prototype.render = function () {
        var _a = this.props, theme = _a.theme, data = _a.data, router = _a.router, statsPeriod = _a.statsPeriod, start = _a.start, end = _a.end, utc = _a.utc, loading = _a.loading, height = _a.height, grid = _a.grid, disableMultiAxis = _a.disableMultiAxis;
        if (!data || data.length <= 0) {
            return null;
        }
        var colors = theme.charts.getColorPalette(4);
        var durationOnly = data.every(function (value) { return aggregateOutputType(value.seriesName) === 'duration'; });
        var dataMax = durationOnly ? computeAxisMax(data) : undefined;
        var xAxes = disableMultiAxis
            ? undefined
            : [
                {
                    gridIndex: 0,
                    type: 'time',
                },
                {
                    gridIndex: 1,
                    type: 'time',
                },
            ];
        var yAxes = disableMultiAxis
            ? undefined
            : [
                {
                    gridIndex: 0,
                    scale: true,
                    max: dataMax,
                    axisLabel: {
                        color: theme.chartLabel,
                        formatter: function (value) {
                            return axisLabelFormatter(value, data[0].seriesName);
                        },
                    },
                },
                {
                    gridIndex: 1,
                    scale: true,
                    max: dataMax,
                    axisLabel: {
                        color: theme.chartLabel,
                        formatter: function (value) {
                            return axisLabelFormatter(value, data[1].seriesName);
                        },
                    },
                },
            ];
        var axisPointer = disableMultiAxis
            ? undefined
            : {
                // Link the two series x-axis together.
                link: [{ xAxisIndex: [0, 1] }],
            };
        var areaChartProps = {
            seriesOptions: {
                showSymbol: false,
            },
            grid: disableMultiAxis
                ? grid
                : [
                    {
                        top: '8px',
                        left: '24px',
                        right: '52%',
                        bottom: '16px',
                    },
                    {
                        top: '8px',
                        left: '52%',
                        right: '24px',
                        bottom: '16px',
                    },
                ],
            axisPointer: axisPointer,
            xAxes: xAxes,
            yAxes: yAxes,
            utc: utc,
            isGroupedByDate: true,
            showTimeInTooltip: true,
            colors: [colors[0], colors[1]],
            tooltip: {
                valueFormatter: function (value, seriesName) {
                    return tooltipFormatter(value, seriesName);
                },
                nameFormatter: function (value) {
                    return value === 'epm()' ? 'tpm()' : value;
                },
            },
        };
        if (loading) {
            return <AreaChart height={height} series={[]} {...areaChartProps}/>;
        }
        var series = data.map(function (values, i) { return (__assign(__assign({}, values), { yAxisIndex: i, xAxisIndex: i })); });
        return (<ChartZoom router={router} period={statsPeriod} start={start} end={end} utc={utc} xAxisIndex={disableMultiAxis ? undefined : [0, 1]}>
        {function (zoomRenderProps) { return (<AreaChart height={height} {...zoomRenderProps} series={series} {...areaChartProps}/>); }}
      </ChartZoom>);
    };
    return Chart;
}(React.Component));
export default withTheme(Chart);
//# sourceMappingURL=chart.jsx.map
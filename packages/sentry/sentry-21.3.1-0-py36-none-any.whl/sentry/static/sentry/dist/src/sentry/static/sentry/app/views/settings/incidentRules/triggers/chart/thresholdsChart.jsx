import { __assign, __extends, __read, __rest, __spreadArray } from "tslib";
import React from 'react';
import color from 'color';
import debounce from 'lodash/debounce';
import flatten from 'lodash/flatten';
import Graphic from 'app/components/charts/components/graphic';
import LineChart from 'app/components/charts/lineChart';
import space from 'app/styles/space';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import theme from 'app/utils/theme';
import { AlertRuleThresholdType } from '../../types';
var CHART_GRID = {
    left: space(2),
    right: space(2),
    top: space(4),
    bottom: space(2),
};
// Colors to use for trigger thresholds
var COLOR = {
    RESOLUTION_FILL: color(theme.green200).alpha(0.1).rgb().string(),
    CRITICAL_FILL: color(theme.red300).alpha(0.25).rgb().string(),
    WARNING_FILL: color(theme.yellow200).alpha(0.1).rgb().string(),
};
/**
 * This chart displays shaded regions that represent different Trigger thresholds in a
 * Metric Alert rule.
 */
var ThresholdsChart = /** @class */ (function (_super) {
    __extends(ThresholdsChart, _super);
    function ThresholdsChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            width: -1,
            height: -1,
            yAxisMax: null,
        };
        _this.ref = null;
        // If we have ref to chart and data, try to update chart axis so that
        // alertThreshold or resolveThreshold is visible in chart
        _this.handleUpdateChartAxis = function () {
            var _a, _b;
            var _c = _this.props, triggers = _c.triggers, resolveThreshold = _c.resolveThreshold;
            var chartRef = (_b = (_a = _this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (chartRef) {
                _this.updateChartAxis(Math.max.apply(Math, __spreadArray([], __read(flatten(triggers.map(function (trigger) { return [trigger.alertThreshold || 0, resolveThreshold || 0]; }))))));
            }
        };
        /**
         * Updates the chart so that yAxis is within bounds of our max value
         */
        _this.updateChartAxis = debounce(function (threshold) {
            var maxValue = _this.props.maxValue;
            if (typeof maxValue !== 'undefined' && threshold > maxValue) {
                // We need to force update after we set a new yAxis max because `convertToPixel`
                // can return a negitive position (probably because yAxisMax is not synced with chart yet)
                _this.setState({ yAxisMax: Math.round(threshold * 1.1) }, _this.forceUpdate);
            }
            else {
                _this.setState({ yAxisMax: null }, _this.forceUpdate);
            }
        }, 150);
        /**
         * Syncs component state with the chart's width/heights
         */
        _this.updateDimensions = function () {
            var _a, _b;
            var chartRef = (_b = (_a = _this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (!chartRef) {
                return;
            }
            var width = chartRef.getWidth();
            var height = chartRef.getHeight();
            if (width !== _this.state.width || height !== _this.state.height) {
                _this.setState({
                    width: width,
                    height: height,
                });
            }
        };
        _this.handleRef = function (ref) {
            // When chart initially renders, we want to update state with its width, as well as initialize starting
            // locations (on y axis) for the draggable lines
            if (ref && !_this.ref) {
                _this.ref = ref;
                _this.updateDimensions();
                _this.handleUpdateChartAxis();
            }
            if (!ref) {
                _this.ref = null;
            }
        };
        /**
         * Draws the boundary lines and shaded areas for the chart.
         *
         * May need to refactor so that they are aware of other trigger thresholds.
         *
         * e.g. draw warning from threshold -> critical threshold instead of the entire height of chart
         */
        _this.getThresholdLine = function (trigger, type, isResolution) {
            var _a, _b, _c;
            var _d = _this.props, thresholdType = _d.thresholdType, resolveThreshold = _d.resolveThreshold, maxValue = _d.maxValue;
            var position = type === 'alertThreshold'
                ? _this.getChartPixelForThreshold(trigger[type])
                : _this.getChartPixelForThreshold(resolveThreshold);
            var isInverted = thresholdType === AlertRuleThresholdType.BELOW;
            var chartRef = (_b = (_a = _this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (typeof position !== 'number' ||
                isNaN(position) ||
                !_this.state.height ||
                !chartRef) {
                return [];
            }
            var yAxisPixelPosition = chartRef.convertToPixel({ yAxisIndex: 0 }, '0');
            var yAxisPosition = typeof yAxisPixelPosition === 'number' ? yAxisPixelPosition : 0;
            // As the yAxis gets larger we want to start our line/area further to the right
            // Handle case where the graph max is 1 and includes decimals
            var yAxisMax = (Math.round(Math.max(maxValue !== null && maxValue !== void 0 ? maxValue : 1, (_c = _this.state.yAxisMax) !== null && _c !== void 0 ? _c : 1)) * 100) / 100;
            var yAxisSize = 15 + (yAxisMax <= 1 ? 15 : ("" + (yAxisMax !== null && yAxisMax !== void 0 ? yAxisMax : '')).length * 8);
            // Shave off the right margin and yAxisSize from the width to get the actual area we want to render content in
            var graphAreaWidth = _this.state.width - parseInt(CHART_GRID.right.slice(0, -2), 10) - yAxisSize;
            // Distance from the top of the chart to save for the legend
            var legendPadding = 20;
            // Shave off the left margin
            var graphAreaMargin = 7;
            var isCritical = trigger.label === 'critical';
            var LINE_STYLE = {
                stroke: isResolution ? theme.green300 : isCritical ? theme.red300 : theme.yellow300,
                lineDash: [2],
            };
            return __spreadArray([
                // This line is used as a "border" for the shaded region
                // and represents the threshold value.
                {
                    type: 'line',
                    // Resolution is considered "off" if it is -1
                    invisible: position === null,
                    draggable: false,
                    position: [yAxisSize, position],
                    shape: { y1: 1, y2: 1, x1: graphAreaMargin, x2: graphAreaWidth },
                    style: LINE_STYLE,
                }
            ], __read((position !== null
                ? [
                    {
                        type: 'rect',
                        draggable: false,
                        position: isResolution !== isInverted
                            ? [yAxisSize + graphAreaMargin, position + 1]
                            : [yAxisSize + graphAreaMargin, legendPadding],
                        shape: {
                            width: graphAreaWidth - graphAreaMargin,
                            height: isResolution !== isInverted
                                ? yAxisPosition - position
                                : position - legendPadding,
                        },
                        style: {
                            fill: isResolution
                                ? COLOR.RESOLUTION_FILL
                                : isCritical
                                    ? COLOR.CRITICAL_FILL
                                    : COLOR.WARNING_FILL,
                        },
                        // This needs to be below the draggable line
                        z: 100,
                    },
                ]
                : [])));
        };
        _this.getChartPixelForThreshold = function (threshold) {
            var _a, _b;
            var chartRef = (_b = (_a = _this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            return (threshold !== '' &&
                chartRef &&
                chartRef.convertToPixel({ yAxisIndex: 0 }, "" + threshold));
        };
        return _this;
    }
    ThresholdsChart.prototype.componentDidUpdate = function (prevProps) {
        if (this.props.triggers !== prevProps.triggers ||
            this.props.data !== prevProps.data) {
            this.handleUpdateChartAxis();
        }
    };
    ThresholdsChart.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, data = _b.data, triggers = _b.triggers, period = _b.period;
        var dataWithoutRecentBucket = data === null || data === void 0 ? void 0 : data.map(function (_a) {
            var eventData = _a.data, restOfData = __rest(_a, ["data"]);
            return (__assign(__assign({}, restOfData), { data: eventData.slice(0, -1) }));
        });
        // Disable all lines by default but the 1st one
        var selected = dataWithoutRecentBucket.reduce(function (acc, _a, index) {
            var seriesName = _a.seriesName;
            acc[seriesName] = index === 0;
            return acc;
        }, {});
        var legend = {
            right: 10,
            top: 0,
            selected: selected,
        };
        var chartOptions = {
            tooltip: {
                valueFormatter: function (value, seriesName) {
                    return tooltipFormatter(value, seriesName);
                },
            },
            yAxis: {
                max: (_a = this.state.yAxisMax) !== null && _a !== void 0 ? _a : undefined,
                axisLabel: {
                    formatter: function (value) {
                        return axisLabelFormatter(value, data.length ? data[0].seriesName : '');
                    },
                },
            },
        };
        return (<LineChart isGroupedByDate showTimeInTooltip period={period} forwardedRef={this.handleRef} grid={CHART_GRID} {...chartOptions} legend={legend} graphic={Graphic({
                elements: flatten(triggers.map(function (trigger) { return __spreadArray(__spreadArray([], __read(_this.getThresholdLine(trigger, 'alertThreshold', false))), __read(_this.getThresholdLine(trigger, 'resolveThreshold', true))); })),
            })} series={dataWithoutRecentBucket} onFinished={function () {
                // We want to do this whenever the chart finishes re-rendering so that we can update the dimensions of
                // any graphics related to the triggers (e.g. the threshold areas + boundaries)
                _this.updateDimensions();
            }}/>);
    };
    ThresholdsChart.defaultProps = {
        data: [],
    };
    return ThresholdsChart;
}(React.PureComponent));
export default ThresholdsChart;
//# sourceMappingURL=thresholdsChart.jsx.map
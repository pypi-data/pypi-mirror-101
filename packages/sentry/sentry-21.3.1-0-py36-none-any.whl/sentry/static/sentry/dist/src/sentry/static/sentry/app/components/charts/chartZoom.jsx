import { __assign, __extends, __rest } from "tslib";
import React from 'react';
import moment from 'moment';
import { updateDateTime } from 'app/actionCreators/globalSelection';
import DataZoomInside from 'app/components/charts/components/dataZoomInside';
import ToolBox from 'app/components/charts/components/toolBox';
import { callIfFunction } from 'app/utils/callIfFunction';
import { getUtcToLocalDateObject } from 'app/utils/dates';
var getDate = function (date) {
    return date ? moment.utc(date).format(moment.HTML5_FMT.DATETIME_LOCAL_SECONDS) : null;
};
var ZoomPropKeys = [
    'period',
    'xAxis',
    'onChartReady',
    'onDataZoom',
    'onRestore',
    'onFinished',
];
/**
 * This is a very opinionated component that takes a render prop through `children`. It
 * will provide props to be passed to `BaseChart` to enable support of zooming without
 * eCharts' clunky zoom toolboxes.
 *
 * This also is very tightly coupled with the Global Selection Header. We can make it more
 * generic if need be in the future.
 */
var ChartZoom = /** @class */ (function (_super) {
    __extends(ChartZoom, _super);
    function ChartZoom(props) {
        var _this = _super.call(this, props) || this;
        _this.zooming = null;
        /**
         * Save current period state from period in props to be used
         * in handling chart's zoom history state
         */
        _this.saveCurrentPeriod = function (props) {
            _this.currentPeriod = {
                period: props.period,
                start: getDate(props.start),
                end: getDate(props.end),
            };
        };
        /**
         * Sets the new period due to a zoom related action
         *
         * Saves the current period to an instance property so that we
         * can control URL state when zoom history is being manipulated
         * by the chart controls.
         *
         * Saves a callback function to be called after chart animation is completed
         */
        _this.setPeriod = function (_a, saveHistory) {
            var period = _a.period, start = _a.start, end = _a.end;
            if (saveHistory === void 0) { saveHistory = false; }
            var _b = _this.props, router = _b.router, onZoom = _b.onZoom;
            var startFormatted = getDate(start);
            var endFormatted = getDate(end);
            // Save period so that we can revert back to it when using echarts "back" navigation
            if (saveHistory) {
                _this.history.push(_this.currentPeriod);
            }
            // Callback to let parent component know zoom has changed
            // This is required for some more perceived responsiveness since
            // we delay updating URL state so that chart animation can finish
            //
            // Parent container can use this to change into a loading state before
            // URL parameters are changed
            callIfFunction(onZoom, {
                period: period,
                start: startFormatted,
                end: endFormatted,
            });
            _this.zooming = function () {
                updateDateTime({
                    period: period,
                    start: startFormatted
                        ? getUtcToLocalDateObject(startFormatted)
                        : startFormatted,
                    end: endFormatted ? getUtcToLocalDateObject(endFormatted) : endFormatted,
                }, router);
                _this.saveCurrentPeriod({ period: period, start: start, end: end });
            };
        };
        /**
         * Enable zoom immediately instead of having to toggle to zoom
         */
        _this.handleChartReady = function (chart) {
            chart.dispatchAction({
                type: 'takeGlobalCursor',
                key: 'dataZoomSelect',
                dataZoomSelectActive: true,
            });
            callIfFunction(_this.props.onChartReady, chart);
        };
        /**
         * Restores the chart to initial viewport/zoom level
         *
         * Updates URL state to reflect initial params
         */
        _this.handleZoomRestore = function (evt, chart) {
            if (!_this.history.length) {
                return;
            }
            _this.setPeriod(_this.history[0]);
            // reset history
            _this.history = [];
            callIfFunction(_this.props.onRestore, evt, chart);
        };
        _this.handleDataZoom = function (evt, chart) {
            var model = chart.getModel();
            var xAxis = model.option.xAxis;
            var axis = xAxis[0];
            // if `rangeStart` and `rangeEnd` are null, then we are going back
            if (axis.rangeStart === null && axis.rangeEnd === null) {
                var previousPeriod = _this.history.pop();
                if (!previousPeriod) {
                    return;
                }
                _this.setPeriod(previousPeriod);
            }
            else {
                var start = moment.utc(axis.rangeStart);
                // Add a day so we go until the end of the day (e.g. next day at midnight)
                var end = moment.utc(axis.rangeEnd);
                _this.setPeriod({ period: null, start: start, end: end }, true);
            }
            callIfFunction(_this.props.onDataZoom, evt, chart);
        };
        /**
         * Chart event when *any* rendering+animation finishes
         *
         * `this.zooming` acts as a callback function so that
         * we can let the native zoom animation on the chart complete
         * before we update URL state and re-render
         */
        _this.handleChartFinished = function () {
            if (typeof _this.zooming === 'function') {
                _this.zooming();
                _this.zooming = null;
            }
            callIfFunction(_this.props.onFinished);
        };
        // Zoom history
        _this.history = [];
        // Initialize current period instance state for zoom history
        _this.saveCurrentPeriod(props);
        return _this;
    }
    ChartZoom.prototype.componentDidUpdate = function () {
        if (this.props.disabled) {
            return;
        }
        // When component updates, make sure we sync current period state
        // for use in zoom history
        this.saveCurrentPeriod(this.props);
    };
    ChartZoom.prototype.render = function () {
        var _a = this.props, _utc = _a.utc, _start = _a.start, _end = _a.end, disabled = _a.disabled, children = _a.children, xAxisIndex = _a.xAxisIndex, _router = _a.router, _onZoom = _a.onZoom, _onRestore = _a.onRestore, _onChartReady = _a.onChartReady, _onDataZoom = _a.onDataZoom, _onFinished = _a.onFinished, props = __rest(_a, ["utc", "start", "end", "disabled", "children", "xAxisIndex", "router", "onZoom", "onRestore", "onChartReady", "onDataZoom", "onFinished"]);
        var utc = _utc !== null && _utc !== void 0 ? _utc : undefined;
        var start = _start ? getUtcToLocalDateObject(_start) : undefined;
        var end = _end ? getUtcToLocalDateObject(_end) : undefined;
        if (disabled) {
            return children(__assign({ utc: utc,
                start: start,
                end: end }, props));
        }
        var renderProps = __assign({ 
            // Zooming only works when grouped by date
            isGroupedByDate: true, onChartReady: this.handleChartReady, utc: utc,
            start: start,
            end: end, dataZoom: DataZoomInside({ xAxisIndex: xAxisIndex }), showTimeInTooltip: true, toolBox: ToolBox({}, {
                dataZoom: {
                    title: {
                        zoom: '',
                        back: '',
                    },
                    iconStyle: {
                        borderWidth: 0,
                        color: 'transparent',
                        opacity: 0,
                    },
                },
            }), onDataZoom: this.handleDataZoom, onFinished: this.handleChartFinished, onRestore: this.handleZoomRestore }, props);
        return children(renderProps);
    };
    return ChartZoom;
}(React.Component));
export default ChartZoom;
//# sourceMappingURL=chartZoom.jsx.map
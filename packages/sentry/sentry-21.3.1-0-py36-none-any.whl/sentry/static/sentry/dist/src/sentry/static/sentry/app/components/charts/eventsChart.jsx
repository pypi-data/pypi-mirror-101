import { __assign, __extends, __read, __rest, __spreadArray } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import AreaChart from 'app/components/charts/areaChart';
import BarChart from 'app/components/charts/barChart';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LineChart from 'app/components/charts/lineChart';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getInterval, RELEASE_LINES_THRESHOLD } from 'app/components/charts/utils';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import { aggregateMultiPlotType } from 'app/utils/discover/fields';
import EventsRequest from './eventsRequest';
var Chart = /** @class */ (function (_super) {
    __extends(Chart, _super);
    function Chart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            seriesSelection: {},
            forceUpdate: false,
        };
        _this.handleLegendSelectChanged = function (legendChange) {
            var _a = _this.props.disableableSeries, disableableSeries = _a === void 0 ? [] : _a;
            var selected = legendChange.selected;
            var seriesSelection = Object.keys(selected).reduce(function (state, key) {
                // we only want them to be able to disable the Releases series,
                // and not any of the other possible series here
                var disableable = key === 'Releases' || disableableSeries.includes(key);
                state[key] = disableable ? selected[key] : true;
                return state;
            }, {});
            // we have to force an update here otherwise ECharts will
            // update its internal state and disable the series
            _this.setState({ seriesSelection: seriesSelection, forceUpdate: true }, function () {
                return _this.setState({ forceUpdate: false });
            });
        };
        return _this;
    }
    Chart.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextState.forceUpdate) {
            return true;
        }
        if (!isEqual(this.state.seriesSelection, nextState.seriesSelection)) {
            return true;
        }
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if (isEqual(this.props.timeseriesData, nextProps.timeseriesData) &&
            isEqual(this.props.releaseSeries, nextProps.releaseSeries) &&
            isEqual(this.props.previousTimeseriesData, nextProps.previousTimeseriesData)) {
            return false;
        }
        return true;
    };
    Chart.prototype.getChartComponent = function () {
        var _a = this.props, showDaily = _a.showDaily, timeseriesData = _a.timeseriesData, yAxis = _a.yAxis, chartComponent = _a.chartComponent;
        if (defined(chartComponent)) {
            return chartComponent;
        }
        if (showDaily) {
            return BarChart;
        }
        if (timeseriesData.length > 1) {
            switch (aggregateMultiPlotType(yAxis)) {
                case 'line':
                    return LineChart;
                case 'area':
                    return AreaChart;
                default:
                    throw new Error("Unknown multi plot type for " + yAxis);
            }
        }
        return AreaChart;
    };
    Chart.prototype.render = function () {
        var _a;
        var _b, _c, _d;
        var _e = this.props, theme = _e.theme, _loading = _e.loading, _reloading = _e.reloading, yAxis = _e.yAxis, releaseSeries = _e.releaseSeries, zoomRenderProps = _e.zoomRenderProps, timeseriesData = _e.timeseriesData, previousTimeseriesData = _e.previousTimeseriesData, showLegend = _e.showLegend, legendOptions = _e.legendOptions, chartOptionsProp = _e.chartOptions, currentSeriesName = _e.currentSeriesName, previousSeriesName = _e.previousSeriesName, seriesTransformer = _e.seriesTransformer, colors = _e.colors, props = __rest(_e, ["theme", "loading", "reloading", "yAxis", "releaseSeries", "zoomRenderProps", "timeseriesData", "previousTimeseriesData", "showLegend", "legendOptions", "chartOptions", "currentSeriesName", "previousSeriesName", "seriesTransformer", "colors"]);
        var seriesSelection = this.state.seriesSelection;
        var data = [currentSeriesName !== null && currentSeriesName !== void 0 ? currentSeriesName : t('Current'), previousSeriesName !== null && previousSeriesName !== void 0 ? previousSeriesName : t('Previous')];
        var releasesLegend = t('Releases');
        if (Array.isArray(releaseSeries)) {
            data.push(releasesLegend);
        }
        // Temporary fix to improve performance on pages with a high number of releases.
        var releases = releaseSeries && releaseSeries[0];
        var hideReleasesByDefault = Array.isArray(releaseSeries) &&
            ((_c = (_b = releases) === null || _b === void 0 ? void 0 : _b.markLine) === null || _c === void 0 ? void 0 : _c.data) &&
            releases.markLine.data.length >= RELEASE_LINES_THRESHOLD;
        var selected = !Array.isArray(releaseSeries)
            ? seriesSelection
            : Object.keys(seriesSelection).length === 0 && hideReleasesByDefault
                ? (_a = {}, _a[releasesLegend] = false, _a) : seriesSelection;
        var legend = showLegend
            ? __assign({ right: 16, top: 12, data: data,
                selected: selected }, (legendOptions !== null && legendOptions !== void 0 ? legendOptions : {})) : undefined;
        var series = Array.isArray(releaseSeries)
            ? __spreadArray(__spreadArray([], __read(timeseriesData)), __read(releaseSeries)) : timeseriesData;
        if (seriesTransformer) {
            series = seriesTransformer(series);
        }
        var chartOptions = __assign({ colors: timeseriesData.length
                ? (_d = colors === null || colors === void 0 ? void 0 : colors.slice(0, series.length)) !== null && _d !== void 0 ? _d : __spreadArray([], __read(theme.charts.getColorPalette(timeseriesData.length - 2)))
                : undefined, grid: {
                left: '24px',
                right: '24px',
                top: '32px',
                bottom: '12px',
            }, seriesOptions: {
                showSymbol: false,
            }, tooltip: {
                trigger: 'axis',
                truncate: 80,
                valueFormatter: function (value) { return tooltipFormatter(value, yAxis); },
            }, yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter: function (value) { return axisLabelFormatter(value, yAxis); },
                },
            } }, (chartOptionsProp !== null && chartOptionsProp !== void 0 ? chartOptionsProp : {}));
        var Component = this.getChartComponent();
        return (<Component {...props} {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={this.handleLegendSelectChanged} series={series} previousPeriod={previousTimeseriesData ? [previousTimeseriesData] : undefined}/>);
    };
    return Chart;
}(React.Component));
var ThemedChart = withTheme(Chart);
var EventsChart = /** @class */ (function (_super) {
    __extends(EventsChart, _super);
    function EventsChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    EventsChart.prototype.render = function () {
        var _a = this.props, api = _a.api, period = _a.period, utc = _a.utc, query = _a.query, router = _a.router, start = _a.start, end = _a.end, projects = _a.projects, environments = _a.environments, showLegend = _a.showLegend, yAxis = _a.yAxis, disablePrevious = _a.disablePrevious, disableReleases = _a.disableReleases, emphasizeReleases = _a.emphasizeReleases, currentName = _a.currentSeriesName, previousName = _a.previousSeriesName, seriesTransformer = _a.seriesTransformer, field = _a.field, interval = _a.interval, showDaily = _a.showDaily, topEvents = _a.topEvents, orderby = _a.orderby, confirmedQuery = _a.confirmedQuery, colors = _a.colors, chartHeader = _a.chartHeader, legendOptions = _a.legendOptions, chartOptions = _a.chartOptions, preserveReleaseQueryParams = _a.preserveReleaseQueryParams, releaseQueryExtra = _a.releaseQueryExtra, disableableSeries = _a.disableableSeries, chartComponent = _a.chartComponent, props = __rest(_a, ["api", "period", "utc", "query", "router", "start", "end", "projects", "environments", "showLegend", "yAxis", "disablePrevious", "disableReleases", "emphasizeReleases", "currentSeriesName", "previousSeriesName", "seriesTransformer", "field", "interval", "showDaily", "topEvents", "orderby", "confirmedQuery", "colors", "chartHeader", "legendOptions", "chartOptions", "preserveReleaseQueryParams", "releaseQueryExtra", "disableableSeries", "chartComponent"]);
        // Include previous only on relative dates (defaults to relative if no start and end)
        var includePrevious = !disablePrevious && !start && !end;
        var previousSeriesName = previousName !== null && previousName !== void 0 ? previousName : (yAxis ? t('previous %s', yAxis) : undefined);
        var currentSeriesName = currentName !== null && currentName !== void 0 ? currentName : yAxis;
        var intervalVal = showDaily ? '1d' : interval || getInterval(this.props, true);
        var chartImplementation = function (_a) {
            var zoomRenderProps = _a.zoomRenderProps, releaseSeries = _a.releaseSeries, errored = _a.errored, loading = _a.loading, reloading = _a.reloading, results = _a.results, timeseriesData = _a.timeseriesData, previousTimeseriesData = _a.previousTimeseriesData;
            if (errored) {
                return (<ErrorPanel>
            <IconWarning color="gray300" size="lg"/>
          </ErrorPanel>);
            }
            var seriesData = results ? results : timeseriesData;
            return (<TransitionChart loading={loading} reloading={reloading}>
          <TransparentLoadingMask visible={reloading}/>

          {React.isValidElement(chartHeader) && chartHeader}

          <ThemedChart zoomRenderProps={zoomRenderProps} loading={loading} reloading={reloading} showLegend={showLegend} releaseSeries={releaseSeries || []} timeseriesData={seriesData !== null && seriesData !== void 0 ? seriesData : []} previousTimeseriesData={previousTimeseriesData} currentSeriesName={currentSeriesName} previousSeriesName={previousSeriesName} seriesTransformer={seriesTransformer} stacked={typeof topEvents === 'number' && topEvents > 0} yAxis={yAxis} showDaily={showDaily} colors={colors} legendOptions={legendOptions} chartOptions={chartOptions} disableableSeries={disableableSeries} chartComponent={chartComponent}/>
        </TransitionChart>);
        };
        if (!disableReleases) {
            var previousChart_1 = chartImplementation;
            chartImplementation = function (chartProps) { return (<ReleaseSeries utc={utc} period={period} start={start} end={end} projects={projects} environments={environments} emphasizeReleases={emphasizeReleases} preserveQueryParams={preserveReleaseQueryParams} queryExtra={releaseQueryExtra}>
          {function (_a) {
                var releaseSeries = _a.releaseSeries;
                return previousChart_1(__assign(__assign({}, chartProps), { releaseSeries: releaseSeries }));
            }}
        </ReleaseSeries>); };
        }
        return (<ChartZoom router={router} period={period} start={start} end={end} utc={utc} {...props}>
        {function (zoomRenderProps) { return (<EventsRequest {...props} api={api} period={period} project={projects} environment={environments} start={start} end={end} interval={intervalVal} query={query} includePrevious={includePrevious} currentSeriesName={currentSeriesName} previousSeriesName={previousSeriesName} yAxis={yAxis} field={field} orderby={orderby} topEvents={topEvents} confirmedQuery={confirmedQuery} partial>
            {function (eventData) {
                    return chartImplementation(__assign(__assign({}, eventData), { zoomRenderProps: zoomRenderProps }));
                }}
          </EventsRequest>); }}
      </ChartZoom>);
    };
    return EventsChart;
}(React.Component));
export default EventsChart;
//# sourceMappingURL=eventsChart.jsx.map
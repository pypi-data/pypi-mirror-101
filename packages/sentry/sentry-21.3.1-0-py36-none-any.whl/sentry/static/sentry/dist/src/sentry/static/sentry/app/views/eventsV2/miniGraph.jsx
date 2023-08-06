import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import AreaChart from 'app/components/charts/areaChart';
import BarChart from 'app/components/charts/barChart';
import EventsRequest from 'app/components/charts/eventsRequest';
import LineChart from 'app/components/charts/lineChart';
import { getInterval } from 'app/components/charts/utils';
import LoadingContainer from 'app/components/loading/loadingContainer';
import LoadingIndicator from 'app/components/loadingIndicator';
import { IconWarning } from 'app/icons';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { axisLabelFormatter } from 'app/utils/discover/charts';
import { aggregateMultiPlotType } from 'app/utils/discover/fields';
import { DisplayModes, TOP_N } from 'app/utils/discover/types';
import { decodeScalar } from 'app/utils/queryString';
import withApi from 'app/utils/withApi';
var MiniGraph = /** @class */ (function (_super) {
    __extends(MiniGraph, _super);
    function MiniGraph() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    MiniGraph.prototype.shouldComponentUpdate = function (nextProps) {
        // We pay for the cost of the deep comparison here since it is cheaper
        // than the cost for rendering the graph, which can take ~200ms to ~300ms to
        // render.
        return !isEqual(this.getRefreshProps(this.props), this.getRefreshProps(nextProps));
    };
    MiniGraph.prototype.getRefreshProps = function (props) {
        // get props that are relevant to the API payload for the graph
        var organization = props.organization, location = props.location, eventView = props.eventView;
        var apiPayload = eventView.getEventsAPIPayload(location);
        var query = apiPayload.query;
        var start = apiPayload.start ? getUtcToLocalDateObject(apiPayload.start) : null;
        var end = apiPayload.end ? getUtcToLocalDateObject(apiPayload.end) : null;
        var period = apiPayload.statsPeriod;
        var display = eventView.getDisplayMode();
        var isTopEvents = display === DisplayModes.TOP5 || display === DisplayModes.DAILYTOP5;
        var isDaily = display === DisplayModes.DAILYTOP5 || display === DisplayModes.DAILY;
        var field = isTopEvents ? apiPayload.field : undefined;
        var topEvents = isTopEvents ? TOP_N : undefined;
        var orderby = isTopEvents ? decodeScalar(apiPayload.sort) : undefined;
        var interval = isDaily ? '1d' : getInterval({ start: start, end: end, period: period }, true);
        return {
            organization: organization,
            apiPayload: apiPayload,
            query: query,
            start: start,
            end: end,
            period: period,
            interval: interval,
            project: eventView.project,
            environment: eventView.environment,
            yAxis: eventView.getYAxis(),
            field: field,
            topEvents: topEvents,
            orderby: orderby,
            showDaily: isDaily,
            expired: eventView.expired,
            name: eventView.name,
        };
    };
    MiniGraph.prototype.getChartType = function (_a) {
        var showDaily = _a.showDaily, yAxis = _a.yAxis, timeseriesData = _a.timeseriesData;
        if (showDaily) {
            return 'bar';
        }
        if (timeseriesData.length > 1) {
            switch (aggregateMultiPlotType(yAxis)) {
                case 'line':
                    return 'line';
                case 'area':
                    return 'area';
                default:
                    throw new Error("Unknown multi plot type for " + yAxis);
            }
        }
        return 'area';
    };
    MiniGraph.prototype.getChartComponent = function (chartType) {
        switch (chartType) {
            case 'bar':
                return BarChart;
            case 'line':
                return LineChart;
            case 'area':
                return AreaChart;
            default:
                throw new Error("Unknown multi plot type for " + chartType);
        }
    };
    MiniGraph.prototype.render = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, api = _a.api;
        var _b = this.getRefreshProps(this.props), query = _b.query, start = _b.start, end = _b.end, period = _b.period, interval = _b.interval, organization = _b.organization, project = _b.project, environment = _b.environment, yAxis = _b.yAxis, field = _b.field, topEvents = _b.topEvents, orderby = _b.orderby, showDaily = _b.showDaily, expired = _b.expired, name = _b.name;
        return (<EventsRequest organization={organization} api={api} query={query} start={start} end={end} period={period} interval={interval} project={project} environment={environment} includePrevious={false} yAxis={yAxis} field={field} topEvents={topEvents} orderby={orderby} expired={expired} name={name} partial>
        {function (_a) {
                var _b;
                var loading = _a.loading, timeseriesData = _a.timeseriesData, results = _a.results, errored = _a.errored;
                if (errored) {
                    return (<StyledGraphContainer>
                <IconWarning color="gray300" size="md"/>
              </StyledGraphContainer>);
                }
                if (loading) {
                    return (<StyledGraphContainer>
                <LoadingIndicator mini/>
              </StyledGraphContainer>);
                }
                var allSeries = (_b = timeseriesData !== null && timeseriesData !== void 0 ? timeseriesData : results) !== null && _b !== void 0 ? _b : [];
                var chartType = _this.getChartType({
                    showDaily: showDaily,
                    yAxis: yAxis,
                    timeseriesData: allSeries,
                });
                var data = allSeries.map(function (series) { return (__assign(__assign({}, series), { lineStyle: {
                        opacity: chartType === 'line' ? 1 : 0,
                    }, smooth: true })); });
                var chartOptions = {
                    colors: __spreadArray([], __read(theme.charts.getColorPalette(allSeries.length - 2))),
                    height: 100,
                    series: __spreadArray([], __read(data)),
                    xAxis: {
                        show: false,
                        axisPointer: {
                            show: false,
                        },
                    },
                    yAxis: {
                        show: true,
                        axisLine: {
                            show: false,
                        },
                        axisLabel: {
                            color: theme.chartLabel,
                            fontFamily: theme.text.family,
                            fontSize: 12,
                            formatter: function (value) { return axisLabelFormatter(value, yAxis, true); },
                            inside: true,
                            showMinLabel: false,
                            showMaxLabel: false,
                        },
                        splitNumber: 3,
                        splitLine: {
                            show: false,
                        },
                        zlevel: theme.zIndex.header,
                    },
                    tooltip: {
                        show: false,
                    },
                    toolBox: {
                        show: false,
                    },
                    grid: {
                        left: 0,
                        top: 0,
                        right: 0,
                        bottom: 0,
                        containLabel: false,
                    },
                    stacked: typeof topEvents === 'number' && topEvents > 0,
                };
                var Component = _this.getChartComponent(chartType);
                return <Component {...chartOptions}/>;
            }}
      </EventsRequest>);
    };
    return MiniGraph;
}(React.Component));
var StyledGraphContainer = styled(function (props) { return (<LoadingContainer {...props} maskBackgroundColor="transparent"/>); })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 100px;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"], ["\n  height: 100px;\n\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"])));
export default withApi(withTheme(MiniGraph));
var templateObject_1;
//# sourceMappingURL=miniGraph.jsx.map
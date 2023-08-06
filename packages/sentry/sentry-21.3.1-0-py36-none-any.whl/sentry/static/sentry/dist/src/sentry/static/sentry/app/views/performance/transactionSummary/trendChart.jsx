import { __assign, __extends, __read, __spreadArray } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import { browserHistory } from 'react-router';
import { withTheme } from 'emotion-theming';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import EventsRequest from 'app/components/charts/eventsRequest';
import LineChart from 'app/components/charts/lineChart';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getInterval, getSeriesSelection } from 'app/components/charts/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import getDynamicText from 'app/utils/getDynamicText';
import withApi from 'app/utils/withApi';
import { transformEventStatsSmoothed } from '../trends/utils';
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
var TrendChart = /** @class */ (function (_super) {
    __extends(TrendChart, _super);
    function TrendChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var location = _this.props.location;
            var selected = legendChange.selected;
            var unselected = Object.keys(selected).filter(function (key) { return !selected[key]; });
            var to = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { trendsUnselectedSeries: unselected }) });
            browserHistory.push(to);
        };
        return _this;
    }
    TrendChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, api = _a.api, project = _a.project, environment = _a.environment, location = _a.location, organization = _a.organization, query = _a.query, statsPeriod = _a.statsPeriod, router = _a.router, trendDisplay = _a.trendDisplay, queryExtra = _a.queryExtra;
        var start = this.props.start ? getUtcToLocalDateObject(this.props.start) : null;
        var end = this.props.end ? getUtcToLocalDateObject(this.props.end) : null;
        var utc = getParams(location.query).utc;
        var legend = {
            right: 10,
            top: 0,
            selected: getSeriesSelection(location, 'trendsUnselectedSeries'),
        };
        var datetimeSelection = {
            start: start,
            end: end,
            period: statsPeriod,
        };
        var chartOptions = {
            grid: {
                left: '10px',
                right: '10px',
                top: '40px',
                bottom: '0px',
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: function (value) { return tooltipFormatter(value, 'p50()'); },
            },
            yAxis: {
                min: 0,
                axisLabel: {
                    color: theme.chartLabel,
                    // p50() coerces the axis to be time based
                    formatter: function (value) { return axisLabelFormatter(value, 'p50()'); },
                },
            },
        };
        return (<React.Fragment>
        <HeaderTitleLegend>
          {t('Trend')}
          <QuestionTooltip size="sm" position="top" title={t("Trends shows the smoothed value of an aggregate over time.")}/>
        </HeaderTitleLegend>
        <ChartZoom router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
          {function (zoomRenderProps) { return (<EventsRequest api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={getInterval(datetimeSelection, true)} showLoading={false} query={query} includePrevious={false} yAxis={trendDisplay} currentSeriesName={trendDisplay} partial>
              {function (_a) {
                    var errored = _a.errored, loading = _a.loading, reloading = _a.reloading, timeseriesData = _a.timeseriesData;
                    if (errored) {
                        return (<ErrorPanel>
                      <IconWarning color="gray300" size="lg"/>
                    </ErrorPanel>);
                    }
                    var series = timeseriesData
                        ? timeseriesData
                            .map(function (values) {
                            return __assign(__assign({}, values), { color: theme.purple300, lineStyle: {
                                    opacity: 0.75,
                                    width: 1,
                                } });
                        })
                            .reverse()
                        : [];
                    var smoothedResults = transformEventStatsSmoothed(timeseriesData, t('Smoothed')).smoothedResults;
                    var smoothedSeries = smoothedResults
                        ? smoothedResults.map(function (values) {
                            return __assign(__assign({}, values), { color: theme.purple300, lineStyle: {
                                    opacity: 1,
                                } });
                        })
                        : [];
                    return (<ReleaseSeries start={start} end={end} queryExtra={queryExtra} period={statsPeriod} utc={utc === 'true'} projects={project} environments={environment}>
                    {function (_a) {
                            var releaseSeries = _a.releaseSeries;
                            return (<TransitionChart loading={loading} reloading={reloading}>
                        <TransparentLoadingMask visible={reloading}/>
                        {getDynamicText({
                                    value: (<LineChart {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={_this.handleLegendSelectChanged} series={__spreadArray(__spreadArray(__spreadArray([], __read(series)), __read(smoothedSeries)), __read(releaseSeries))}/>),
                                    fixed: <Placeholder height="200px" testId="skeleton-ui"/>,
                                })}
                      </TransitionChart>);
                        }}
                  </ReleaseSeries>);
                }}
            </EventsRequest>); }}
        </ChartZoom>
      </React.Fragment>);
    };
    return TrendChart;
}(React.Component));
export default withApi(withTheme(ReactRouter.withRouter(TrendChart)));
//# sourceMappingURL=trendChart.jsx.map
import { __assign, __extends, __read, __spreadArray } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import * as ReactRouter from 'react-router';
import { withTheme } from 'emotion-theming';
import AreaChart from 'app/components/charts/areaChart';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import EventsRequest from 'app/components/charts/eventsRequest';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getInterval, getSeriesSelection } from 'app/components/charts/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import getDynamicText from 'app/utils/getDynamicText';
import withApi from 'app/utils/withApi';
import { filterToField, SpanOperationBreakdownFilter } from './filter';
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
function generateYAxisValues(filter) {
    if (filter === SpanOperationBreakdownFilter.None) {
        return ['p50()', 'p75()', 'p95()', 'p99()', 'p100()'];
    }
    var field = filterToField(filter);
    return [
        "p50(" + field + ")",
        "p75(" + field + ")",
        "p95(" + field + ")",
        "p99(" + field + ")",
        "p100(" + field + ")",
    ];
}
/**
 * Fetch and render a stacked area chart that shows duration
 * percentiles over the past 7 days
 */
var DurationChart = /** @class */ (function (_super) {
    __extends(DurationChart, _super);
    function DurationChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLegendSelectChanged = function (legendChange) {
            var location = _this.props.location;
            var selected = legendChange.selected;
            var unselected = Object.keys(selected).filter(function (key) { return !selected[key]; });
            var to = __assign(__assign({}, location), { query: __assign(__assign({}, location.query), { unselectedSeries: unselected }) });
            browserHistory.push(to);
        };
        return _this;
    }
    DurationChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, api = _a.api, project = _a.project, environment = _a.environment, location = _a.location, organization = _a.organization, query = _a.query, statsPeriod = _a.statsPeriod, router = _a.router, queryExtra = _a.queryExtra, currentFilter = _a.currentFilter;
        var start = this.props.start ? getUtcToLocalDateObject(this.props.start) : null;
        var end = this.props.end ? getUtcToLocalDateObject(this.props.end) : null;
        var utc = getParams(location.query).utc;
        var legend = {
            right: 10,
            top: 5,
            selected: getSeriesSelection(location),
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
                valueFormatter: tooltipFormatter,
            },
            yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    // p50() coerces the axis to be time based
                    formatter: function (value) { return axisLabelFormatter(value, 'p50()'); },
                },
            },
        };
        var headerTitle = currentFilter === SpanOperationBreakdownFilter.None
            ? t('Duration Breakdown')
            : tct('Span Operation Breakdown - [operationName]', {
                operationName: currentFilter,
            });
        return (<React.Fragment>
        <HeaderTitleLegend>
          {headerTitle}
          <QuestionTooltip size="sm" position="top" title={t("Duration Breakdown reflects transaction durations by percentile over time.")}/>
        </HeaderTitleLegend>
        <ChartZoom router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
          {function (zoomRenderProps) { return (<EventsRequest api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={getInterval(datetimeSelection, true)} showLoading={false} query={query} includePrevious={false} yAxis={generateYAxisValues(currentFilter)} partial>
              {function (_a) {
                    var results = _a.results, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
                    if (errored) {
                        return (<ErrorPanel>
                      <IconWarning color="gray300" size="lg"/>
                    </ErrorPanel>);
                    }
                    var colors = (results && theme.charts.getColorPalette(results.length - 2)) || [];
                    // Create a list of series based on the order of the fields,
                    // We need to flip it at the end to ensure the series stack right.
                    var series = results
                        ? results
                            .map(function (values, i) {
                            return __assign(__assign({}, values), { color: colors[i], lineStyle: {
                                    opacity: 0,
                                } });
                        })
                            .reverse()
                        : [];
                    return (<ReleaseSeries start={start} end={end} queryExtra={queryExtra} period={statsPeriod} utc={utc === 'true'} projects={project} environments={environment}>
                    {function (_a) {
                            var releaseSeries = _a.releaseSeries;
                            return (<TransitionChart loading={loading} reloading={reloading}>
                        <TransparentLoadingMask visible={reloading}/>
                        {getDynamicText({
                                    value: (<AreaChart {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={_this.handleLegendSelectChanged} series={__spreadArray(__spreadArray([], __read(series)), __read(releaseSeries))}/>),
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
    return DurationChart;
}(React.Component));
export default withApi(withTheme(ReactRouter.withRouter(DurationChart)));
//# sourceMappingURL=durationChart.jsx.map
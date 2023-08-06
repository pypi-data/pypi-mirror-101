import { __assign, __extends, __read, __spreadArray } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import * as ReactRouter from 'react-router';
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
import { getAggregateArg, getMeasurementSlug } from 'app/utils/discover/fields';
import getDynamicText from 'app/utils/getDynamicText';
import withApi from 'app/utils/withApi';
import { TransactionsListOption } from 'app/views/releases/detail/overview';
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
var YAXIS_VALUES = [
    'p75(measurements.fp)',
    'p75(measurements.fcp)',
    'p75(measurements.lcp)',
    'p75(measurements.fid)',
];
var VitalsChart = /** @class */ (function (_super) {
    __extends(VitalsChart, _super);
    function VitalsChart() {
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
    VitalsChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, api = _a.api, project = _a.project, environment = _a.environment, location = _a.location, organization = _a.organization, query = _a.query, statsPeriod = _a.statsPeriod, router = _a.router, queryExtra = _a.queryExtra;
        var start = this.props.start ? getUtcToLocalDateObject(this.props.start) : null;
        var end = this.props.end ? getUtcToLocalDateObject(this.props.end) : null;
        var utc = getParams(location.query).utc;
        var legend = {
            right: 10,
            top: 0,
            selected: getSeriesSelection(location),
            formatter: function (seriesName) {
                var arg = getAggregateArg(seriesName);
                if (arg !== null) {
                    var slug = getMeasurementSlug(arg);
                    if (slug !== null) {
                        seriesName = slug.toUpperCase();
                    }
                }
                return seriesName;
            },
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
                    // p75(measurements.fcp) coerces the axis to be time based
                    formatter: function (value) {
                        return axisLabelFormatter(value, 'p75(measurements.fcp)');
                    },
                },
            },
        };
        return (<React.Fragment>
        <HeaderTitleLegend>
          {t('Web Vitals Breakdown')}
          <QuestionTooltip size="sm" position="top" title={t("Web Vitals Breakdown reflects the 75th percentile of web vitals over time.")}/>
        </HeaderTitleLegend>
        <ChartZoom router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'}>
          {function (zoomRenderProps) { return (<EventsRequest api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={getInterval(datetimeSelection, true)} showLoading={false} query={query} includePrevious={false} yAxis={YAXIS_VALUES} partial>
              {function (_a) {
                    var results = _a.results, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
                    if (errored) {
                        return (<ErrorPanel>
                      <IconWarning color="gray500" size="lg"/>
                    </ErrorPanel>);
                    }
                    var colors = (results && theme.charts.getColorPalette(results.length - 2)) || [];
                    // Create a list of series based on the order of the fields,
                    var series = results
                        ? results.map(function (values, i) { return (__assign(__assign({}, values), { color: colors[i] })); })
                        : [];
                    return (<ReleaseSeries start={start} end={end} queryExtra={__assign(__assign({}, queryExtra), { showTransactions: TransactionsListOption.SLOW_LCP })} period={statsPeriod} utc={utc === 'true'} projects={project} environments={environment}>
                    {function (_a) {
                            var releaseSeries = _a.releaseSeries;
                            return (<TransitionChart loading={loading} reloading={reloading}>
                        <TransparentLoadingMask visible={reloading}/>
                        {getDynamicText({
                                    value: (<LineChart {...zoomRenderProps} {...chartOptions} legend={legend} onLegendSelectChanged={_this.handleLegendSelectChanged} series={__spreadArray(__spreadArray([], __read(series)), __read(releaseSeries))}/>),
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
    return VitalsChart;
}(React.Component));
export default withApi(withTheme(ReactRouter.withRouter(VitalsChart)));
//# sourceMappingURL=vitalsChart.jsx.map
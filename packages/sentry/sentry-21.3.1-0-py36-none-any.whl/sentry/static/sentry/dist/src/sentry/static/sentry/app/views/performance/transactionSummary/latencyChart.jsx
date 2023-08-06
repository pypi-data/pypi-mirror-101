import { __extends, __read, __spreadArray } from "tslib";
import React from 'react';
import BarChart from 'app/components/charts/barChart';
import BarChartZoom from 'app/components/charts/barChartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LoadingPanel from 'app/components/charts/loadingPanel';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import EventView from 'app/utils/discover/eventView';
import HistogramQuery from 'app/utils/performance/histogram/histogramQuery';
import { computeBuckets, formatHistogramData } from 'app/utils/performance/histogram/utils';
import { decodeScalar } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import { filterToColour, filterToField, SpanOperationBreakdownFilter } from './filter';
var NUM_BUCKETS = 50;
var QUERY_KEYS = [
    'environment',
    'project',
    'query',
    'start',
    'end',
    'statsPeriod',
];
/**
 * Fetch and render a bar chart that shows event volume
 * for each duration bucket. We always render 50 buckets of
 * equal widths based on the endpoints min + max durations.
 *
 * This graph visualizes how many transactions were recorded
 * at each duration bucket, showing the modality of the transaction.
 */
var LatencyChart = /** @class */ (function (_super) {
    __extends(LatencyChart, _super);
    function LatencyChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            zoomError: false,
        };
        _this.handleMouseOver = function () {
            // Hide the zoom error tooltip on the next hover.
            if (_this.state.zoomError) {
                _this.setState({ zoomError: false });
            }
        };
        _this.handleDataZoom = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.latency_chart.zoom',
                eventName: 'Performance Views: Transaction Summary Latency Chart Zoom',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleDataZoomCancelled = function () {
            _this.setState({ zoomError: true });
        };
        return _this;
    }
    LatencyChart.prototype.bucketWidth = function (data) {
        // We can assume that all buckets are of equal width, use the first two
        // buckets to get the width. The value of each histogram function indicates
        // the beginning of the bucket.
        return data.length > 2 ? data[1].bin - data[0].bin : 0;
    };
    LatencyChart.prototype.renderLoading = function () {
        return <LoadingPanel data-test-id="histogram-loading"/>;
    };
    LatencyChart.prototype.renderError = function () {
        // Don't call super as we don't really need issues for this.
        return (<ErrorPanel>
        <IconWarning color="gray300" size="lg"/>
      </ErrorPanel>);
    };
    LatencyChart.prototype.renderChart = function (data) {
        var _this = this;
        var _a = this.props, location = _a.location, currentFilter = _a.currentFilter;
        var zoomError = this.state.zoomError;
        var xAxis = {
            type: 'category',
            truncate: true,
            axisTick: {
                interval: 0,
                alignWithLabel: true,
            },
        };
        var colors = currentFilter === SpanOperationBreakdownFilter.None
            ? __spreadArray([], __read(theme.charts.getColorPalette(1))) : [filterToColour(currentFilter)];
        // Use a custom tooltip formatter as we need to replace
        // the tooltip content entirely when zooming is no longer available.
        var tooltip = {
            formatter: function (series) {
                var seriesData = Array.isArray(series) ? series : [series];
                var contents = [];
                if (!zoomError) {
                    // Replicate the necessary logic from app/components/charts/components/tooltip.jsx
                    contents = seriesData.map(function (item) {
                        var label = item.seriesName;
                        var value = item.value[1].toLocaleString();
                        return [
                            '<div class="tooltip-series">',
                            "<div><span class=\"tooltip-label\">" + item.marker + " <strong>" + label + "</strong></span> " + value + "</div>",
                            '</div>',
                        ].join('');
                    });
                    var seriesLabel = seriesData[0].value[0];
                    contents.push("<div class=\"tooltip-date\">" + seriesLabel + "</div>");
                }
                else {
                    contents = [
                        '<div class="tooltip-series tooltip-series-solo">',
                        t('Target zoom region too small'),
                        '</div>',
                    ];
                }
                contents.push('<div class="tooltip-arrow"></div>');
                return contents.join('');
            },
        };
        var series = {
            seriesName: t('Count'),
            data: formatHistogramData(data, { type: 'duration' }),
        };
        return (<BarChartZoom minZoomWidth={NUM_BUCKETS} location={location} paramStart="startDuration" paramEnd="endDuration" xAxisIndex={[0]} buckets={computeBuckets(data)} onDataZoomCancelled={this.handleDataZoomCancelled}>
        {function (zoomRenderProps) { return (<BarChart grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} xAxis={xAxis} yAxis={{ type: 'value' }} series={[series]} tooltip={tooltip} colors={colors} onMouseOver={_this.handleMouseOver} {...zoomRenderProps}/>); }}
      </BarChartZoom>);
    };
    LatencyChart.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, organization = _b.organization, query = _b.query, start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod, environment = _b.environment, project = _b.project, location = _b.location, currentFilter = _b.currentFilter;
        var eventView = EventView.fromNewQueryWithLocation({
            id: undefined,
            version: 2,
            name: '',
            fields: ['transaction.duration'],
            projects: project,
            range: statsPeriod,
            query: query,
            environment: environment,
            start: start,
            end: end,
        }, location);
        var min = parseInt(decodeScalar(location.query.startDuration, '0'), 10);
        var field = (_a = filterToField(currentFilter)) !== null && _a !== void 0 ? _a : 'transaction.duration';
        var headerTitle = currentFilter === SpanOperationBreakdownFilter.None
            ? t('Duration Distribution')
            : tct('Span Operation Distribution - [operationName]', {
                operationName: currentFilter,
            });
        return (<React.Fragment>
        <HeaderTitleLegend>
          {headerTitle}
          <QuestionTooltip position="top" size="sm" title={t("Duration Distribution reflects the volume of transactions per median duration.")}/>
        </HeaderTitleLegend>
        <HistogramQuery location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} fields={[field]} min={min} dataFilter="exclude_outliers">
          {function (_a) {
                var _b;
                var histograms = _a.histograms, isLoading = _a.isLoading, error = _a.error;
                if (isLoading) {
                    return _this.renderLoading();
                }
                else if (error) {
                    return _this.renderError();
                }
                var data = (_b = histograms === null || histograms === void 0 ? void 0 : histograms[field]) !== null && _b !== void 0 ? _b : [];
                return _this.renderChart(data);
            }}
        </HistogramQuery>
      </React.Fragment>);
    };
    return LatencyChart;
}(React.Component));
export default LatencyChart;
//# sourceMappingURL=latencyChart.jsx.map
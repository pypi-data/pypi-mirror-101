import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import throttle from 'lodash/throttle';
import BarChart from 'app/components/charts/barChart';
import BarChartZoom from 'app/components/charts/barChartZoom';
import MarkLine from 'app/components/charts/components/markLine';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import DiscoverButton from 'app/components/discoverButton';
import Placeholder from 'app/components/placeholder';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { formatAbbreviatedNumber, formatFloat, getDuration } from 'app/utils/formatters';
import getDynamicText from 'app/utils/getDynamicText';
import { computeBuckets, formatHistogramData } from 'app/utils/performance/histogram/utils';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import { VitalBar } from '../landing/vitalsCards';
import { VitalState, vitalStateColors, webVitalMeh, webVitalPoor, } from '../vitalDetail/utils';
import { NUM_BUCKETS, PERCENTILE } from './constants';
import { Card, CardSectionHeading, CardSummary, Description, StatNumber } from './styles';
import { asPixelRect, findNearestBucketIndex, getRefRect, mapPoint } from './utils';
var VitalCard = /** @class */ (function (_super) {
    __extends(VitalCard, _super);
    function VitalCard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            refDataRect: null,
            refPixelRect: null,
        };
        _this.trackOpenInDiscoverClicked = function () {
            var organization = _this.props.organization;
            var vital = _this.props.vitalDetails;
            trackAnalyticsEvent({
                eventKey: 'performance_views.vitals.open_in_discover',
                eventName: 'Performance Views: Open vitals in discover',
                organization_id: organization.id,
                vital: vital.slug,
            });
        };
        /**
         * This callback happens everytime ECharts renders. This is NOT when ECharts
         * finishes rendering, so it can be called quite frequently. The calculations
         * here can get expensive if done frequently, furthermore, this can trigger a
         * state change leading to a re-render. So slow down the updates here as they
         * do not need to be updated every single time.
         */
        _this.handleRendered = throttle(function (_, chartRef) {
            var chartData = _this.props.chartData;
            var refDataRect = _this.state.refDataRect;
            if (refDataRect === null || chartData.length < 1) {
                return;
            }
            var refPixelRect = refDataRect === null ? null : asPixelRect(chartRef, refDataRect);
            if (refPixelRect !== null && !isEqual(refPixelRect, _this.state.refPixelRect)) {
                _this.setState({ refPixelRect: refPixelRect });
            }
        }, 200, { leading: true });
        _this.handleDataZoomCancelled = function () { };
        return _this;
    }
    VitalCard.getDerivedStateFromProps = function (nextProps, prevState) {
        var isLoading = nextProps.isLoading, error = nextProps.error, chartData = nextProps.chartData;
        if (isLoading || error === null) {
            return __assign({}, prevState);
        }
        var refDataRect = getRefRect(chartData);
        if (prevState.refDataRect === null ||
            (refDataRect !== null && !isEqual(refDataRect, prevState.refDataRect))) {
            return __assign(__assign({}, prevState), { refDataRect: refDataRect });
        }
        return __assign({}, prevState);
    };
    VitalCard.prototype.showVitalColours = function () {
        return this.props.organization.features.includes('performance-vitals-overview');
    };
    Object.defineProperty(VitalCard.prototype, "summary", {
        get: function () {
            var _a;
            var summaryData = this.props.summaryData;
            return (_a = summaryData === null || summaryData === void 0 ? void 0 : summaryData.p75) !== null && _a !== void 0 ? _a : null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(VitalCard.prototype, "failureRate", {
        get: function () {
            var _a, _b;
            var summaryData = this.props.summaryData;
            var numerator = (_a = summaryData === null || summaryData === void 0 ? void 0 : summaryData.poor) !== null && _a !== void 0 ? _a : 0;
            var denominator = (_b = summaryData === null || summaryData === void 0 ? void 0 : summaryData.total) !== null && _b !== void 0 ? _b : 0;
            return denominator <= 0 ? 0 : numerator / denominator;
        },
        enumerable: false,
        configurable: true
    });
    VitalCard.prototype.getFormattedStatNumber = function () {
        var vital = this.props.vitalDetails;
        var summary = this.summary;
        var type = vital.type;
        return summary === null
            ? '\u2014'
            : type === 'duration'
                ? getDuration(summary / 1000, 2, true)
                : formatFloat(summary, 2);
    };
    VitalCard.prototype.renderSummary = function () {
        var _a;
        var _b = this.props, vital = _b.vitalDetails, eventView = _b.eventView, organization = _b.organization, min = _b.min, max = _b.max;
        var slug = vital.slug, name = vital.name, description = vital.description;
        var column = "measurements." + slug;
        var newEventView = eventView
            .withColumns([
            { kind: 'field', field: 'transaction' },
            { kind: 'function', function: ['percentile', column, PERCENTILE.toString()] },
            { kind: 'function', function: ['count', '', ''] },
        ])
            .withSorts([
            {
                kind: 'desc',
                field: getAggregateAlias("percentile(" + column + "," + PERCENTILE.toString() + ")"),
            },
        ]);
        var query = tokenizeSearch((_a = newEventView.query) !== null && _a !== void 0 ? _a : '');
        query.addTagValues('has', [column]);
        // add in any range constraints if any
        if (min !== undefined || max !== undefined) {
            if (min !== undefined) {
                query.addTagValues(column, [">=" + min]);
            }
            if (max !== undefined) {
                query.addTagValues(column, ["<=" + max]);
            }
        }
        newEventView.query = stringifyQueryObject(query);
        return (<CardSummary>
        <SummaryHeading>
          <CardSectionHeading>{name + " (" + slug.toUpperCase() + ")"}</CardSectionHeading>
        </SummaryHeading>
        <StatNumber>
          {getDynamicText({
                value: this.getFormattedStatNumber(),
                fixed: '\u2014',
            })}
        </StatNumber>
        <Description>{description}</Description>
        <div>
          <DiscoverButton size="small" to={newEventView.getResultsViewUrlTarget(organization.slug)} onClick={this.trackOpenInDiscoverClicked}>
            {t('Open in Discover')}
          </DiscoverButton>
        </div>
      </CardSummary>);
    };
    VitalCard.prototype.renderHistogram = function () {
        var _a;
        var _this = this;
        var _b = this.props, theme = _b.theme, location = _b.location, isLoading = _b.isLoading, chartData = _b.chartData, summaryData = _b.summaryData, error = _b.error, colors = _b.colors, vital = _b.vital, vitalDetails = _b.vitalDetails, _c = _b.precision, precision = _c === void 0 ? 0 : _c;
        var slug = vitalDetails.slug;
        var series = this.getSeries();
        var xAxis = {
            type: 'category',
            truncate: true,
            axisTick: {
                alignWithLabel: true,
            },
        };
        var values = series.data.map(function (point) { return point.value; });
        var max = values.length ? Math.max.apply(Math, __spreadArray([], __read(values))) : undefined;
        var yAxis = {
            type: 'value',
            max: max,
            axisLabel: {
                color: theme.chartLabel,
                formatter: formatAbbreviatedNumber,
            },
        };
        var allSeries = [series];
        if (!isLoading && !error) {
            var baselineSeries = this.getBaselineSeries();
            if (baselineSeries !== null) {
                allSeries.push(baselineSeries);
            }
        }
        var vitalData = !isLoading && !error && summaryData !== null ? (_a = {}, _a[vital] = summaryData, _a) : {};
        return (<BarChartZoom minZoomWidth={Math.pow(10, -precision) * NUM_BUCKETS} location={location} paramStart={slug + "Start"} paramEnd={slug + "End"} xAxisIndex={[0]} buckets={computeBuckets(chartData)} onDataZoomCancelled={this.handleDataZoomCancelled}>
        {function (zoomRenderProps) { return (<Container>
            <TransparentLoadingMask visible={isLoading}/>
            <PercentContainer>
              <VitalBar isLoading={isLoading} data={vitalData} vital={vital} showBar={false} showStates={false} showVitalPercentNames={false} showDurationDetail={false}/>
            </PercentContainer>
            {getDynamicText({
                    value: (<BarChart series={allSeries} xAxis={xAxis} yAxis={yAxis} colors={colors} onRendered={_this.handleRendered} grid={{
                            left: space(3),
                            right: space(3),
                            top: space(3),
                            bottom: space(1.5),
                        }} stacked {...zoomRenderProps}/>),
                    fixed: <Placeholder testId="skeleton-ui" height="200px"/>,
                })}
          </Container>); }}
      </BarChartZoom>);
    };
    VitalCard.prototype.bucketWidth = function () {
        var chartData = this.props.chartData;
        // We can assume that all buckets are of equal width, use the first two
        // buckets to get the width. The value of each histogram function indicates
        // the beginning of the bucket.
        return chartData.length >= 2 ? chartData[1].bin - chartData[0].bin : 0;
    };
    VitalCard.prototype.getSeries = function () {
        var _this = this;
        var _a = this.props, theme = _a.theme, chartData = _a.chartData, precision = _a.precision, vitalDetails = _a.vitalDetails, vital = _a.vital;
        var additionalFieldsFn = function (bucket) {
            if (_this.showVitalColours()) {
                return {
                    itemStyle: { color: theme[_this.getVitalsColor(vital, bucket)] },
                };
            }
            return {};
        };
        var data = formatHistogramData(chartData, {
            precision: precision === 0 ? undefined : precision,
            type: vitalDetails.type,
            additionalFieldsFn: additionalFieldsFn,
        });
        return {
            seriesName: t('Count'),
            data: data,
        };
    };
    VitalCard.prototype.getVitalsColor = function (vital, value) {
        var poorThreshold = webVitalPoor[vital];
        var mehThreshold = webVitalMeh[vital];
        if (value >= poorThreshold) {
            return vitalStateColors[VitalState.POOR];
        }
        else if (value >= mehThreshold) {
            return vitalStateColors[VitalState.MEH];
        }
        else {
            return vitalStateColors[VitalState.GOOD];
        }
    };
    VitalCard.prototype.getBaselineSeries = function () {
        var _a = this.props, theme = _a.theme, chartData = _a.chartData;
        var summary = this.summary;
        if (summary === null || this.state.refPixelRect === null) {
            return null;
        }
        var summaryBucket = findNearestBucketIndex(chartData, summary);
        if (summaryBucket === null || summaryBucket === -1) {
            return null;
        }
        var thresholdPixelBottom = mapPoint({
            // subtract 0.5 from the x here to ensure that the threshold lies between buckets
            x: summaryBucket - 0.5,
            y: 0,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (thresholdPixelBottom === null) {
            return null;
        }
        var thresholdPixelTop = mapPoint({
            // subtract 0.5 from the x here to ensure that the threshold lies between buckets
            x: summaryBucket - 0.5,
            y: Math.max.apply(Math, __spreadArray([], __read(chartData.map(function (data) { return data.count; })))) || 1,
        }, this.state.refDataRect, this.state.refPixelRect);
        if (thresholdPixelTop === null) {
            return null;
        }
        var markLine = MarkLine({
            animationDuration: 200,
            data: [[thresholdPixelBottom, thresholdPixelTop]],
            label: {
                show: false,
            },
            lineStyle: {
                color: theme.textColor,
                type: 'solid',
            },
        });
        // TODO(tonyx): This conflicts with the types declaration of `MarkLine`
        // if we add it in the constructor. So we opt to add it here so typescript
        // doesn't complain.
        markLine.tooltip = {
            formatter: function () {
                return [
                    '<div class="tooltip-series tooltip-series-solo">',
                    '<span class="tooltip-label">',
                    "<strong>" + t('p75') + "</strong>",
                    '</span>',
                    '</div>',
                    '<div class="tooltip-arrow"></div>',
                ].join('');
            },
        };
        return {
            seriesName: t('p75'),
            data: [],
            markLine: markLine,
        };
    };
    VitalCard.prototype.render = function () {
        return (<Card>
        {this.renderSummary()}
        {this.renderHistogram()}
      </Card>);
    };
    return VitalCard;
}(React.Component));
var SummaryHeading = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var PercentContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n  z-index: 2;\n"], ["\n  position: absolute;\n  top: ", ";\n  right: ", ";\n  z-index: 2;\n"])), space(2), space(3));
export default withTheme(VitalCard);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=vitalCard.jsx.map
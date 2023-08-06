import { __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import BarChart from 'app/components/charts/barChart';
import BarChartZoom from 'app/components/charts/barChartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons/iconWarning';
import { t } from 'app/locale';
import space from 'app/styles/space';
import getDynamicText from 'app/utils/getDynamicText';
import HistogramQuery from 'app/utils/performance/histogram/histogramQuery';
import { computeBuckets, formatHistogramData } from 'app/utils/performance/histogram/utils';
import { DoubleHeaderContainer } from '../../styles';
var NUM_BUCKETS = 50;
var PRECISION = 0;
export function HistogramChart(props) {
    var theme = props.theme, location = props.location, onFilterChange = props.onFilterChange, organization = props.organization, eventView = props.eventView, field = props.field, title = props.title, titleTooltip = props.titleTooltip;
    var xAxis = {
        type: 'category',
        truncate: true,
        boundaryGap: false,
        axisTick: {
            alignWithLabel: true,
        },
    };
    return (<div>
      <DoubleHeaderContainer>
        <HeaderTitleLegend>
          {title}
          <QuestionTooltip position="top" size="sm" title={titleTooltip}/>
        </HeaderTitleLegend>
      </DoubleHeaderContainer>
      <HistogramQuery location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} precision={PRECISION} fields={[field]} dataFilter="exclude_outliers">
        {function (results) {
            var _a;
            var loading = results.isLoading;
            var errored = results.error !== null;
            var chartData = (_a = results.histograms) === null || _a === void 0 ? void 0 : _a[field];
            if (errored) {
                return (<ErrorPanel height="250px">
                <IconWarning color="gray300" size="lg"/>
              </ErrorPanel>);
            }
            if (!chartData) {
                return null;
            }
            var series = {
                seriesName: t('Count'),
                data: formatHistogramData(chartData, { type: 'duration' }),
            };
            var allSeries = [];
            if (!loading && !errored) {
                allSeries.push(series);
            }
            var values = series.data.map(function (point) { return point.value; });
            var max = values.length ? Math.max.apply(Math, __spreadArray([], __read(values))) : undefined;
            var yAxis = {
                type: 'value',
                max: max,
                axisLabel: {
                    color: theme.chartLabel,
                },
            };
            return (<React.Fragment>
              <BarChartZoom minZoomWidth={Math.pow(10, -PRECISION) * NUM_BUCKETS} location={location} paramStart={field + ":>="} paramEnd={field + ":<="} xAxisIndex={[0]} buckets={computeBuckets(chartData)} onHistoryPush={onFilterChange}>
                {function (zoomRenderProps) {
                    return (<BarChartContainer>
                      <MaskContainer>
                        <TransparentLoadingMask visible={loading}/>
                        {getDynamicText({
                            value: (<BarChart height={250} series={allSeries} xAxis={xAxis} yAxis={yAxis} grid={{
                                    left: space(3),
                                    right: space(3),
                                    top: space(3),
                                    bottom: loading ? space(4) : space(1.5),
                                }} stacked {...zoomRenderProps}/>),
                            fixed: <Placeholder height="250px" testId="skeleton-ui"/>,
                        })}
                      </MaskContainer>
                    </BarChartContainer>);
                }}
              </BarChartZoom>
            </React.Fragment>);
        }}
      </HistogramQuery>
    </div>);
}
var BarChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-top: ", ";\n  position: relative;\n"], ["\n  padding-top: ", ";\n  position: relative;\n"])), space(1));
var MaskContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
export default withTheme(HistogramChart);
var templateObject_1, templateObject_2;
//# sourceMappingURL=histogramChart.jsx.map
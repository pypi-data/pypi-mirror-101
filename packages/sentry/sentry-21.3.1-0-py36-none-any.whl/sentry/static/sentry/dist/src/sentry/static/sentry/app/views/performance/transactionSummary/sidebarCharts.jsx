import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import EventsRequest from 'app/components/charts/eventsRequest';
import LineChart from 'app/components/charts/lineChart';
import { SectionHeading } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getInterval } from 'app/components/charts/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import { tooltipFormatter } from 'app/utils/discover/charts';
import { formatAbbreviatedNumber, formatFloat, formatPercentage, } from 'app/utils/formatters';
import withApi from 'app/utils/withApi';
import { getTermHelp, PERFORMANCE_TERM } from 'app/views/performance/data';
function SidebarCharts(_a) {
    var theme = _a.theme, api = _a.api, location = _a.location, eventView = _a.eventView, organization = _a.organization, router = _a.router, isLoading = _a.isLoading, error = _a.error, totals = _a.totals;
    var statsPeriod = eventView.statsPeriod;
    var start = eventView.start ? getUtcToLocalDateObject(eventView.start) : undefined;
    var end = eventView.end ? getUtcToLocalDateObject(eventView.end) : undefined;
    var utc = getParams(location.query).utc;
    var colors = theme.charts.getColorPalette(3);
    var axisLineConfig = {
        scale: true,
        axisLine: {
            show: false,
        },
        axisTick: {
            show: false,
        },
        splitLine: {
            show: false,
        },
    };
    var chartOptions = {
        height: 480,
        grid: [
            {
                top: '60px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
            {
                top: '220px',
                left: '10px',
                right: '10px',
                height: '100px',
            },
            {
                top: '380px',
                left: '10px',
                right: '10px',
                height: '120px',
            },
        ],
        axisPointer: {
            // Link each x-axis together.
            link: [{ xAxisIndex: [0, 1, 2] }],
        },
        xAxes: Array.from(new Array(3)).map(function (_i, index) { return ({
            gridIndex: index,
            type: 'time',
            show: false,
        }); }),
        yAxes: [
            __assign({ 
                // apdex
                gridIndex: 0, interval: 0.2, axisLabel: {
                    formatter: function (value) { return formatFloat(value, 1); },
                    color: theme.chartLabel,
                } }, axisLineConfig),
            __assign({ 
                // failure rate
                gridIndex: 1, splitNumber: 4, interval: 0.5, max: 1.0, axisLabel: {
                    formatter: function (value) { return formatPercentage(value, 0); },
                    color: theme.chartLabel,
                } }, axisLineConfig),
            __assign({ 
                // throughput
                gridIndex: 2, splitNumber: 4, axisLabel: {
                    formatter: formatAbbreviatedNumber,
                    color: theme.chartLabel,
                } }, axisLineConfig),
        ],
        utc: utc === 'true',
        isGroupedByDate: true,
        showTimeInTooltip: true,
        colors: [colors[0], colors[1], colors[2]],
        tooltip: {
            trigger: 'axis',
            truncate: 80,
            valueFormatter: tooltipFormatter,
            nameFormatter: function (value) {
                return value === 'epm()' ? 'tpm()' : value;
            },
        },
    };
    var datetimeSelection = {
        start: start || null,
        end: end || null,
        period: statsPeriod,
    };
    var project = eventView.project;
    var environment = eventView.environment;
    var threshold = organization.apdexThreshold;
    return (<RelativeBox>
      <ChartLabel top="0px">
        <ChartTitle>
          {t('Apdex')}
          <QuestionTooltip position="top" title={getTermHelp(organization, PERFORMANCE_TERM.APDEX)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? formatFloat(totals["apdex_" + threshold], 4) : null}/>
      </ChartLabel>

      <ChartLabel top="160px">
        <ChartTitle>
          {t('Failure Rate')}
          <QuestionTooltip position="top" title={getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? formatPercentage(totals.failure_rate) : null}/>
      </ChartLabel>

      <ChartLabel top="320px">
        <ChartTitle>
          {t('TPM')}
          <QuestionTooltip position="top" title={getTermHelp(organization, PERFORMANCE_TERM.TPM)} size="sm"/>
        </ChartTitle>
        <ChartSummaryValue isLoading={isLoading} error={error} value={totals ? tct('[tpm] tpm', { tpm: formatFloat(totals.tpm, 4) }) : null}/>
      </ChartLabel>

      <ChartZoom router={router} period={statsPeriod} start={start} end={end} utc={utc === 'true'} xAxisIndex={[0, 1, 2]}>
        {function (zoomRenderProps) { return (<EventsRequest api={api} organization={organization} period={statsPeriod} project={project} environment={environment} start={start} end={end} interval={getInterval(datetimeSelection)} showLoading={false} query={eventView.query} includePrevious={false} yAxis={["apdex(" + organization.apdexThreshold + ")", 'failure_rate()', 'epm()']} partial>
            {function (_a) {
                var results = _a.results, errored = _a.errored, loading = _a.loading, reloading = _a.reloading;
                if (errored) {
                    return (<ErrorPanel height="580px">
                    <IconWarning color="gray300" size="lg"/>
                  </ErrorPanel>);
                }
                var series = results
                    ? results.map(function (values, i) { return (__assign(__assign({}, values), { yAxisIndex: i, xAxisIndex: i })); })
                    : [];
                return (<TransitionChart loading={loading} reloading={reloading} height="580px">
                  <TransparentLoadingMask visible={reloading}/>
                  <LineChart {...zoomRenderProps} {...chartOptions} series={series}/>
                </TransitionChart>);
            }}
          </EventsRequest>); }}
      </ChartZoom>
    </RelativeBox>);
}
function ChartSummaryValue(_a) {
    var error = _a.error, isLoading = _a.isLoading, value = _a.value;
    if (error) {
        return <div>{'\u2014'}</div>;
    }
    else if (isLoading) {
        return <Placeholder height="24px"/>;
    }
    else {
        return <ChartValue>{value}</ChartValue>;
    }
}
var RelativeBox = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ChartTitle = styled(SectionHeading)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var ChartLabel = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  top: ", ";\n  z-index: 1;\n"], ["\n  position: absolute;\n  top: ", ";\n  z-index: 1;\n"])), function (p) { return p.top; });
var ChartValue = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
export default withApi(withTheme(ReactRouter.withRouter(SidebarCharts)));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sidebarCharts.jsx.map
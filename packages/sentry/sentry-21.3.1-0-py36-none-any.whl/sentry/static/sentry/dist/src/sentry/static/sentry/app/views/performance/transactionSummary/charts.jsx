import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import OptionSelector from 'app/components/charts/optionSelector';
import { ChartContainer, ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import { Panel } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { t } from 'app/locale';
import { decodeScalar } from 'app/utils/queryString';
import { TransactionsListOption } from 'app/views/releases/detail/overview';
import { YAxis } from 'app/views/releases/detail/overview/chart/releaseChartControls';
import { TrendColumnField, TrendFunctionField } from '../trends/types';
import { generateTrendFunctionAsString, TRENDS_FUNCTIONS, TRENDS_PARAMETERS, } from '../trends/utils';
import DurationChart from './durationChart';
import DurationPercentileChart from './durationPercentileChart';
import { SpanOperationBreakdownFilter } from './filter';
import LatencyChart from './latencyChart';
import TrendChart from './trendChart';
import VitalsChart from './vitalsChart';
export var DisplayModes;
(function (DisplayModes) {
    DisplayModes["DURATION_PERCENTILE"] = "durationpercentile";
    DisplayModes["DURATION"] = "duration";
    DisplayModes["LATENCY"] = "latency";
    DisplayModes["TREND"] = "trend";
    DisplayModes["VITALS"] = "vitals";
})(DisplayModes || (DisplayModes = {}));
function generateDisplayOptions(currentFilter) {
    if (currentFilter === SpanOperationBreakdownFilter.None) {
        return [
            { value: DisplayModes.DURATION, label: t('Duration Breakdown') },
            { value: DisplayModes.DURATION_PERCENTILE, label: t('Duration Percentiles') },
            { value: DisplayModes.LATENCY, label: t('Duration Distribution') },
            { value: DisplayModes.TREND, label: t('Trends') },
            { value: DisplayModes.VITALS, label: t('Web Vitals') },
        ];
    }
    // A span operation name breakdown has been chosen.
    return [
        { value: DisplayModes.DURATION, label: t('Span Operation Breakdown') },
        { value: DisplayModes.DURATION_PERCENTILE, label: t('Span Operation Percentiles') },
        { value: DisplayModes.LATENCY, label: t('Span Operation Distribution') },
        { value: DisplayModes.TREND, label: t('Trends') },
        { value: DisplayModes.VITALS, label: t('Web Vitals') },
    ];
}
var TREND_FUNCTIONS_OPTIONS = TRENDS_FUNCTIONS.map(function (_a) {
    var field = _a.field, label = _a.label;
    return ({
        value: field,
        label: label,
    });
});
var TREND_PARAMETERS_OPTIONS = TRENDS_PARAMETERS.map(function (_a) {
    var column = _a.column, label = _a.label;
    return ({
        value: column,
        label: label,
    });
});
var TransactionSummaryCharts = /** @class */ (function (_super) {
    __extends(TransactionSummaryCharts, _super);
    function TransactionSummaryCharts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDisplayChange = function (value) {
            var location = _this.props.location;
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { display: value }),
            });
        };
        _this.handleTrendDisplayChange = function (value) {
            var location = _this.props.location;
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { trendFunction: value }),
            });
        };
        _this.handleTrendColumnChange = function (value) {
            var location = _this.props.location;
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { trendColumn: value }),
            });
        };
        return _this;
    }
    TransactionSummaryCharts.prototype.render = function () {
        var _a = this.props, totalValues = _a.totalValues, eventView = _a.eventView, organization = _a.organization, location = _a.location, currentFilter = _a.currentFilter;
        var display = decodeScalar(location.query.display, DisplayModes.DURATION);
        var trendFunction = decodeScalar(location.query.trendFunction, TREND_FUNCTIONS_OPTIONS[0].value);
        var trendColumn = decodeScalar(location.query.trendColumn, TREND_PARAMETERS_OPTIONS[0].value);
        if (!Object.values(DisplayModes).includes(display)) {
            display = DisplayModes.DURATION;
        }
        if (!Object.values(TrendFunctionField).includes(trendFunction)) {
            trendFunction = TrendFunctionField.P50;
        }
        if (!Object.values(TrendColumnField).includes(trendColumn)) {
            trendColumn = TrendColumnField.DURATION;
        }
        var releaseQueryExtra = {
            yAxis: display === DisplayModes.VITALS ? YAxis.COUNT_VITAL : YAxis.COUNT_DURATION,
            showTransactions: display === DisplayModes.VITALS
                ? TransactionsListOption.SLOW_LCP
                : display === DisplayModes.DURATION
                    ? TransactionsListOption.SLOW
                    : undefined,
        };
        return (<Panel>
        <ChartContainer>
          {display === DisplayModes.LATENCY && (<LatencyChart organization={organization} location={location} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter}/>)}
          {display === DisplayModes.DURATION && (<DurationChart organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter}/>)}
          {display === DisplayModes.DURATION_PERCENTILE && (<DurationPercentileChart organization={organization} location={location} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod} currentFilter={currentFilter}/>)}
          {display === DisplayModes.TREND && (<TrendChart trendDisplay={generateTrendFunctionAsString(trendFunction, trendColumn)} organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
          {display === DisplayModes.VITALS && (<VitalsChart organization={organization} query={eventView.query} queryExtra={releaseQueryExtra} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>)}
        </ChartContainer>

        <ChartControls>
          <InlineContainer>
            <SectionHeading key="total-heading">{t('Total Transactions')}</SectionHeading>
            <SectionValue key="total-value">
              {totalValues === null ? (<Placeholder height="24px"/>) : (totalValues.toLocaleString())}
            </SectionValue>
          </InlineContainer>
          <InlineContainer>
            {display === DisplayModes.TREND && (<OptionSelector title={t('Trend')} selected={trendFunction} options={TREND_FUNCTIONS_OPTIONS} onChange={this.handleTrendDisplayChange}/>)}
            {display === DisplayModes.TREND && (<OptionSelector title={t('Parameter')} selected={trendColumn} options={TREND_PARAMETERS_OPTIONS} onChange={this.handleTrendColumnChange}/>)}
            <OptionSelector title={t('Display')} selected={display} options={generateDisplayOptions(currentFilter)} onChange={this.handleDisplayChange}/>
          </InlineContainer>
        </ChartControls>
      </Panel>);
    };
    return TransactionSummaryCharts;
}(React.Component));
export default TransactionSummaryCharts;
//# sourceMappingURL=charts.jsx.map
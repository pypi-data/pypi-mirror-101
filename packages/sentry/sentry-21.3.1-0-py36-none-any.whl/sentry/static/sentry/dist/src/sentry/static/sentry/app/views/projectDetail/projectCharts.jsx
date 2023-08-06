import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { withTheme } from 'emotion-theming';
import BarChart from 'app/components/charts/barChart';
import LoadingPanel from 'app/components/charts/loadingPanel';
import OptionSelector from 'app/components/charts/optionSelector';
import { ChartContainer, ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import { getDiffInMinutes, ONE_HOUR, ONE_WEEK, TWENTY_FOUR_HOURS, TWO_WEEKS, } from 'app/components/charts/utils';
import { Panel } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import CHART_PALETTE from 'app/constants/chartPalette';
import NOT_AVAILABLE_MESSAGES from 'app/constants/notAvailableMessages';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
import withApi from 'app/utils/withApi';
import { getSessionTermDescription, SessionTerm, } from 'app/views/releases/utils/sessionTerm';
import { getTermHelp, PERFORMANCE_TERM } from '../performance/data';
import ProjectBaseEventsChart from './charts/projectBaseEventsChart';
import ProjectBaseSessionsChart from './charts/projectBaseSessionsChart';
import ProjectErrorsBasicChart from './charts/projectErrorsBasicChart';
export var DisplayModes;
(function (DisplayModes) {
    DisplayModes["APDEX"] = "apdex";
    DisplayModes["FAILURE_RATE"] = "failure_rate";
    DisplayModes["TPM"] = "tpm";
    DisplayModes["ERRORS"] = "errors";
    DisplayModes["TRANSACTIONS"] = "transactions";
    DisplayModes["STABILITY"] = "crash_free";
    DisplayModes["SESSIONS"] = "sessions";
})(DisplayModes || (DisplayModes = {}));
var ProjectCharts = /** @class */ (function (_super) {
    __extends(ProjectCharts, _super);
    function ProjectCharts() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            totalValues: null,
        };
        _this.handleDisplayModeChange = function (value) {
            var _a;
            var _b = _this.props, location = _b.location, chartId = _b.chartId, chartIndex = _b.chartIndex, organization = _b.organization;
            trackAnalyticsEvent({
                eventKey: "project_detail.change_chart" + (chartIndex + 1),
                eventName: "Project Detail: Change Chart #" + (chartIndex + 1),
                organization_id: parseInt(organization.id, 10),
                metric: value,
            });
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), (_a = {}, _a[chartId] = value, _a)),
            });
        };
        _this.handleTotalValuesChange = function (value) {
            if (value !== _this.state.totalValues) {
                _this.setState({ totalValues: value });
            }
        };
        return _this;
    }
    Object.defineProperty(ProjectCharts.prototype, "defaultDisplayModes", {
        get: function () {
            var _a = this.props, hasSessions = _a.hasSessions, hasTransactions = _a.hasTransactions;
            if (!hasSessions && !hasTransactions) {
                return [DisplayModes.ERRORS];
            }
            if (hasSessions && !hasTransactions) {
                return [DisplayModes.STABILITY, DisplayModes.ERRORS];
            }
            if (!hasSessions && hasTransactions) {
                return [DisplayModes.FAILURE_RATE, DisplayModes.APDEX];
            }
            return [DisplayModes.STABILITY, DisplayModes.APDEX];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "otherActiveDisplayModes", {
        get: function () {
            var _this = this;
            var _a = this.props, location = _a.location, visibleCharts = _a.visibleCharts, chartId = _a.chartId;
            return visibleCharts
                .filter(function (visibleChartId) { return visibleChartId !== chartId; })
                .map(function (urlKey) {
                return decodeScalar(location.query[urlKey], _this.defaultDisplayModes[visibleCharts.findIndex(function (value) { return value === urlKey; })]);
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "displayMode", {
        get: function () {
            var _a = this.props, location = _a.location, chartId = _a.chartId, chartIndex = _a.chartIndex;
            var displayMode = decodeScalar(location.query[chartId]) || this.defaultDisplayModes[chartIndex];
            if (!Object.values(DisplayModes).includes(displayMode)) {
                return this.defaultDisplayModes[chartIndex];
            }
            return displayMode;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "displayModes", {
        get: function () {
            var _a = this.props, organization = _a.organization, hasSessions = _a.hasSessions, hasTransactions = _a.hasTransactions;
            var hasPerformance = organization.features.includes('performance-view');
            var noPerformanceTooltip = NOT_AVAILABLE_MESSAGES.performance;
            var noHealthTooltip = NOT_AVAILABLE_MESSAGES.releaseHealth;
            return [
                {
                    value: DisplayModes.STABILITY,
                    label: t('Crash Free Sessions'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.STABILITY) || !hasSessions,
                    tooltip: !hasSessions ? noHealthTooltip : undefined,
                },
                {
                    value: DisplayModes.APDEX,
                    label: t('Apdex'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.APDEX) ||
                        !hasPerformance ||
                        !hasTransactions,
                    tooltip: hasPerformance && hasTransactions
                        ? getTermHelp(organization, PERFORMANCE_TERM.APDEX)
                        : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.FAILURE_RATE,
                    label: t('Failure Rate'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.FAILURE_RATE) ||
                        !hasPerformance ||
                        !hasTransactions,
                    tooltip: hasPerformance && hasTransactions
                        ? getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE)
                        : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.TPM,
                    label: t('Transactions Per Minute'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.TPM) ||
                        !hasPerformance ||
                        !hasTransactions,
                    tooltip: hasPerformance && hasTransactions
                        ? getTermHelp(organization, PERFORMANCE_TERM.TPM)
                        : noPerformanceTooltip,
                },
                {
                    value: DisplayModes.ERRORS,
                    label: t('Number of Errors'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.ERRORS),
                },
                {
                    value: DisplayModes.SESSIONS,
                    label: t('Number of Sessions'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.SESSIONS) || !hasSessions,
                    tooltip: !hasSessions ? noHealthTooltip : undefined,
                },
                {
                    value: DisplayModes.TRANSACTIONS,
                    label: t('Number of Transactions'),
                    disabled: this.otherActiveDisplayModes.includes(DisplayModes.TRANSACTIONS) ||
                        !hasPerformance ||
                        !hasTransactions,
                    tooltip: hasPerformance && hasTransactions ? undefined : noPerformanceTooltip,
                },
            ];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "summaryHeading", {
        get: function () {
            switch (this.displayMode) {
                case DisplayModes.ERRORS:
                    return t('Total Errors');
                case DisplayModes.STABILITY:
                case DisplayModes.SESSIONS:
                    return t('Total Sessions');
                case DisplayModes.APDEX:
                case DisplayModes.FAILURE_RATE:
                case DisplayModes.TPM:
                case DisplayModes.TRANSACTIONS:
                default:
                    return t('Total Transactions');
            }
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectCharts.prototype, "barChartInterval", {
        get: function () {
            var query = this.props.location.query;
            var diffInMinutes = getDiffInMinutes(__assign(__assign({}, query), { period: decodeScalar(query.statsPeriod) }));
            if (diffInMinutes >= TWO_WEEKS) {
                return '1d';
            }
            if (diffInMinutes >= ONE_WEEK) {
                return '12h';
            }
            if (diffInMinutes > TWENTY_FOUR_HOURS) {
                return '6h';
            }
            if (diffInMinutes === TWENTY_FOUR_HOURS) {
                return '1h';
            }
            if (diffInMinutes <= ONE_HOUR) {
                return '1m';
            }
            return '15m';
        },
        enumerable: false,
        configurable: true
    });
    ProjectCharts.prototype.render = function () {
        var _a = this.props, api = _a.api, router = _a.router, location = _a.location, organization = _a.organization, theme = _a.theme, projectId = _a.projectId, hasSessions = _a.hasSessions;
        var totalValues = this.state.totalValues;
        var hasDiscover = organization.features.includes('discover-basic');
        var displayMode = this.displayMode;
        return (<Panel>
        <ChartContainer>
          {!defined(hasSessions) ? (<LoadingPanel />) : (<React.Fragment>
              {displayMode === DisplayModes.APDEX && (<ProjectBaseEventsChart title={t('Apdex')} help={getTermHelp(organization, PERFORMANCE_TERM.APDEX)} query="event.type:transaction" yAxis={"apdex(" + organization.apdexThreshold + ")"} field={["apdex(" + organization.apdexThreshold + ")"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[CHART_PALETTE[0][0], theme.purple200]}/>)}
              {displayMode === DisplayModes.FAILURE_RATE && (<ProjectBaseEventsChart title={t('Failure Rate')} help={getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE)} query="event.type:transaction" yAxis="failure_rate()" field={["failure_rate()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.red300, theme.purple200]}/>)}
              {displayMode === DisplayModes.TPM && (<ProjectBaseEventsChart title={t('Transactions Per Minute')} help={getTermHelp(organization, PERFORMANCE_TERM.TPM)} query="event.type:transaction" yAxis="tpm()" field={["tpm()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.yellow300, theme.purple200]} disablePrevious/>)}
              {displayMode === DisplayModes.ERRORS &&
                    (hasDiscover ? (<ProjectBaseEventsChart title={t('Number of Errors')} query="!event.type:transaction" yAxis="count()" field={["count()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.purple300, theme.purple200]} interval={this.barChartInterval} chartComponent={BarChart} disableReleases/>) : (<ProjectErrorsBasicChart organization={organization} projectId={projectId} location={location} onTotalValuesChange={this.handleTotalValuesChange}/>))}
              {displayMode === DisplayModes.TRANSACTIONS && (<ProjectBaseEventsChart title={t('Number of Transactions')} query="event.type:transaction" yAxis="count()" field={["count()"]} api={api} router={router} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} colors={[theme.gray200, theme.purple200]} interval={this.barChartInterval} chartComponent={BarChart} disableReleases/>)}
              {displayMode === DisplayModes.STABILITY && (<ProjectBaseSessionsChart title={t('Crash Free Sessions')} help={getSessionTermDescription(SessionTerm.STABILITY, null)} router={router} api={api} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} displayMode={displayMode}/>)}
              {displayMode === DisplayModes.SESSIONS && (<ProjectBaseSessionsChart title={t('Number of Sessions')} router={router} api={api} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} displayMode={displayMode} disablePrevious/>)}
            </React.Fragment>)}
        </ChartContainer>
        <ChartControls>
          {/* if hasSessions is not yet defined, it means that request is still in progress and we can't decide what default chart to show */}
          {defined(hasSessions) ? (<React.Fragment>
              <InlineContainer>
                <SectionHeading>{this.summaryHeading}</SectionHeading>
                <SectionValue>
                  {typeof totalValues === 'number'
                    ? totalValues.toLocaleString()
                    : '\u2014'}
                </SectionValue>
              </InlineContainer>
              <InlineContainer>
                <OptionSelector title={t('Display')} selected={displayMode} options={this.displayModes} onChange={this.handleDisplayModeChange}/>
              </InlineContainer>
            </React.Fragment>) : (<Placeholder height="34px"/>)}
        </ChartControls>
      </Panel>);
    };
    return ProjectCharts;
}(React.Component));
export default withApi(withTheme(ProjectCharts));
//# sourceMappingURL=projectCharts.jsx.map
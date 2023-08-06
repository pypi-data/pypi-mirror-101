import { __extends, __read, __spreadArray } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LineChart from 'app/components/charts/lineChart';
import ReleaseSeries from 'app/components/charts/releaseSeries';
import StackedAreaChart from 'app/components/charts/stackedAreaChart';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { RELEASE_LINES_THRESHOLD } from 'app/components/charts/utils';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import getDynamicText from 'app/utils/getDynamicText';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import { displayCrashFreePercent } from 'app/views/releases/utils';
import { sessionTerm } from 'app/views/releases/utils/sessionTerm';
import { DisplayModes } from '../projectCharts';
import SessionsRequest from './sessionsRequest';
function ProjectBaseSessionsChart(_a) {
    var title = _a.title, theme = _a.theme, organization = _a.organization, router = _a.router, selection = _a.selection, api = _a.api, onTotalValuesChange = _a.onTotalValuesChange, displayMode = _a.displayMode, help = _a.help, disablePrevious = _a.disablePrevious;
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period, utc = datetime.utc;
    return (<React.Fragment>
      {getDynamicText({
            value: (<ChartZoom router={router} period={period} start={start} end={end} utc={utc}>
            {function (zoomRenderProps) { return (<SessionsRequest api={api} selection={selection} organization={organization} onTotalValuesChange={onTotalValuesChange} displayMode={displayMode} disablePrevious={disablePrevious}>
                {function (_a) {
                        var errored = _a.errored, loading = _a.loading, reloading = _a.reloading, timeseriesData = _a.timeseriesData, previousTimeseriesData = _a.previousTimeseriesData;
                        return (<ReleaseSeries utc={utc} period={period} start={start} end={end} projects={projects} environments={environments}>
                    {function (_a) {
                                var releaseSeries = _a.releaseSeries;
                                if (errored) {
                                    return (<ErrorPanel>
                            <IconWarning color="gray300" size="lg"/>
                          </ErrorPanel>);
                                }
                                return (<TransitionChart loading={loading} reloading={reloading}>
                          <TransparentLoadingMask visible={reloading}/>

                          <HeaderTitleLegend>
                            {title}
                            {help && (<QuestionTooltip size="sm" position="top" title={help}/>)}
                          </HeaderTitleLegend>

                          <Chart theme={theme} zoomRenderProps={zoomRenderProps} reloading={reloading} timeSeries={timeseriesData} previousTimeSeries={previousTimeseriesData
                                        ? [previousTimeseriesData]
                                        : undefined} releaseSeries={releaseSeries} displayMode={displayMode}/>
                        </TransitionChart>);
                            }}
                  </ReleaseSeries>);
                    }}
              </SessionsRequest>); }}
          </ChartZoom>),
            fixed: title + " Chart",
        })}
    </React.Fragment>);
}
var Chart = /** @class */ (function (_super) {
    __extends(Chart, _super);
    function Chart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            seriesSelection: {},
            forceUpdate: false,
        };
        // inspired by app/components/charts/eventsChart.tsx@handleLegendSelectChanged
        _this.handleLegendSelectChanged = function (_a) {
            var selected = _a.selected;
            var seriesSelection = Object.keys(selected).reduce(function (state, key) {
                state[key] = selected[key];
                return state;
            }, {});
            // we have to force an update here otherwise ECharts will
            // update its internal state and disable the series
            _this.setState({ seriesSelection: seriesSelection, forceUpdate: true }, function () {
                return _this.setState({ forceUpdate: false });
            });
        };
        return _this;
    }
    Chart.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextState.forceUpdate) {
            return true;
        }
        if (!isEqual(this.state.seriesSelection, nextState.seriesSelection)) {
            return true;
        }
        if (nextProps.releaseSeries !== this.props.releaseSeries &&
            !nextProps.reloading &&
            !this.props.reloading) {
            return true;
        }
        if (this.props.reloading && !nextProps.reloading) {
            return true;
        }
        if (nextProps.timeSeries !== this.props.timeSeries) {
            return true;
        }
        return false;
    };
    Object.defineProperty(Chart.prototype, "legend", {
        get: function () {
            var _a;
            var _b, _c;
            var _d = this.props, theme = _d.theme, timeSeries = _d.timeSeries, previousTimeSeries = _d.previousTimeSeries, releaseSeries = _d.releaseSeries;
            var seriesSelection = this.state.seriesSelection;
            var hideReleasesByDefault = ((_c = (_b = releaseSeries[0]) === null || _b === void 0 ? void 0 : _b.markLine) === null || _c === void 0 ? void 0 : _c.data.length) >= RELEASE_LINES_THRESHOLD;
            var hideHealthyByDefault = timeSeries
                .filter(function (s) { return sessionTerm.healthy !== s.seriesName; })
                .some(function (s) { return s.data.some(function (d) { return d.value > 0; }); });
            var selected = Object.keys(seriesSelection).length === 0 &&
                (hideReleasesByDefault || hideHealthyByDefault)
                ? (_a = {},
                    _a[t('Releases')] = !hideReleasesByDefault,
                    _a[sessionTerm.healthy] = !hideHealthyByDefault,
                    _a) : seriesSelection;
            return {
                right: 10,
                top: 0,
                icon: 'circle',
                itemHeight: 8,
                itemWidth: 8,
                itemGap: 12,
                align: 'left',
                textStyle: {
                    color: theme.textColor,
                    verticalAlign: 'top',
                    fontSize: 11,
                    fontFamily: theme.text.family,
                },
                data: __spreadArray(__spreadArray(__spreadArray([], __read(timeSeries.map(function (s) { return s.seriesName; }))), __read((previousTimeSeries !== null && previousTimeSeries !== void 0 ? previousTimeSeries : []).map(function (s) { return s.seriesName; }))), __read(releaseSeries.map(function (s) { return s.seriesName; }))),
                selected: selected,
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Chart.prototype, "chartOptions", {
        get: function () {
            var _a = this.props, theme = _a.theme, displayMode = _a.displayMode;
            return {
                grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' },
                seriesOptions: {
                    showSymbol: false,
                },
                tooltip: {
                    trigger: 'axis',
                    truncate: 80,
                    valueFormatter: function (value) {
                        if (value === null) {
                            return '\u2014';
                        }
                        if (displayMode === DisplayModes.STABILITY) {
                            return displayCrashFreePercent(value, 0, 3);
                        }
                        return typeof value === 'number' ? value.toLocaleString() : value;
                    },
                },
                yAxis: displayMode === DisplayModes.STABILITY
                    ? {
                        axisLabel: {
                            color: theme.gray200,
                            formatter: function (value) { return displayCrashFreePercent(value); },
                        },
                        scale: true,
                        max: 100,
                    }
                    : { min: 0 },
            };
        },
        enumerable: false,
        configurable: true
    });
    Chart.prototype.render = function () {
        var _a = this.props, zoomRenderProps = _a.zoomRenderProps, timeSeries = _a.timeSeries, previousTimeSeries = _a.previousTimeSeries, releaseSeries = _a.releaseSeries, displayMode = _a.displayMode;
        var ChartComponent = displayMode === DisplayModes.STABILITY ? LineChart : StackedAreaChart;
        return (<ChartComponent {...zoomRenderProps} {...this.chartOptions} legend={this.legend} series={Array.isArray(releaseSeries) ? __spreadArray(__spreadArray([], __read(timeSeries)), __read(releaseSeries)) : timeSeries} previousPeriod={previousTimeSeries} onLegendSelectChanged={this.handleLegendSelectChanged} transformSinglePointToBar/>);
    };
    return Chart;
}(React.Component));
export default withGlobalSelection(withTheme(ProjectBaseSessionsChart));
//# sourceMappingURL=projectBaseSessionsChart.jsx.map
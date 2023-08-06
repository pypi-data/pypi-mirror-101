import { __extends, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import styled from '@emotion/styled';
import color from 'color';
import moment from 'moment';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import Graphic from 'app/components/charts/components/graphic';
import MarkLine from 'app/components/charts/components/markLine';
import EventsRequest from 'app/components/charts/eventsRequest';
import LineChart from 'app/components/charts/lineChart';
import { Panel, PanelBody, PanelFooter } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import { IconCheckmark, IconFire, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getFormattedDate, getUtcDateString } from 'app/utils/dates';
import theme from 'app/utils/theme';
import { makeDefaultCta } from 'app/views/settings/incidentRules/incidentRulePresets';
import { IncidentActivityType, IncidentStatus } from '../../types';
import { getIncidentRuleMetricPreset } from '../../utils';
var X_AXIS_BOUNDARY_GAP = 20;
var VERTICAL_PADDING = 22;
function createThresholdSeries(lineColor, threshold) {
    return {
        seriesName: 'Threshold Line',
        type: 'line',
        markLine: MarkLine({
            silent: true,
            lineStyle: { color: lineColor, type: 'dashed', width: 1 },
            data: [{ yAxis: threshold }],
        }),
        data: [],
    };
}
function createStatusAreaSeries(lineColor, startTime, endTime) {
    return {
        seriesName: 'Status Area',
        type: 'line',
        markLine: MarkLine({
            silent: true,
            lineStyle: { color: lineColor, type: 'solid', width: 4 },
            data: [[{ coord: [startTime, 0] }, { coord: [endTime, 0] }]],
        }),
        data: [],
    };
}
function createIncidentSeries(router, orgSlug, lineColor, incidentTimestamp, identifier, dataPoint, seriesName) {
    var series = {
        seriesName: 'Incident Line',
        type: 'line',
        markLine: MarkLine({
            silent: false,
            lineStyle: { color: lineColor, type: 'solid' },
            data: [
                {
                    xAxis: incidentTimestamp,
                    onClick: function () {
                        router.push({
                            pathname: "/organizations/" + orgSlug + "/alerts/" + identifier + "/",
                            query: { redirect: false },
                        });
                    },
                },
            ],
            label: {
                show: !!identifier,
                position: 'insideEndBottom',
                formatter: identifier || '-',
                color: lineColor,
                fontSize: 10,
                fontFamily: 'Rubik',
            },
        }),
        data: [],
    };
    // tooltip conflicts with MarkLine types
    series.markLine.tooltip = {
        trigger: 'item',
        alwaysShowContent: true,
        formatter: function (_a) {
            var _b;
            var value = _a.value, marker = _a.marker;
            var time = getFormattedDate(value, 'MMM D, YYYY LT');
            return [
                "<div class=\"tooltip-series\"><div>",
                "<span class=\"tooltip-label\">" + marker + " <strong>" + t('Alert') + " #" + identifier + "</strong></span>" + seriesName + " " + ((_b = dataPoint === null || dataPoint === void 0 ? void 0 : dataPoint.value) === null || _b === void 0 ? void 0 : _b.toLocaleString()),
                "</div></div>",
                "<div class=\"tooltip-date\">" + time + "</div>",
                "<div class=\"tooltip-arrow\"></div>",
            ].join('');
        },
    };
    return series;
}
var MetricChart = /** @class */ (function (_super) {
    __extends(MetricChart, _super);
    function MetricChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            width: -1,
            height: -1,
        };
        _this.ref = null;
        /**
         * Syncs component state with the chart's width/heights
         */
        _this.updateDimensions = function () {
            var _a, _b;
            var chartRef = (_b = (_a = _this.ref) === null || _a === void 0 ? void 0 : _a.getEchartsInstance) === null || _b === void 0 ? void 0 : _b.call(_a);
            if (!chartRef) {
                return;
            }
            var width = chartRef.getWidth();
            var height = chartRef.getHeight();
            if (width !== _this.state.width || height !== _this.state.height) {
                _this.setState({
                    width: width,
                    height: height,
                });
            }
        };
        _this.handleRef = function (ref) {
            if (ref && !_this.ref) {
                _this.ref = ref;
                _this.updateDimensions();
            }
            if (!ref) {
                _this.ref = null;
            }
        };
        _this.getRuleChangeThresholdElements = function (data) {
            var _a = _this.state, height = _a.height, width = _a.width;
            var dateModified = (_this.props.rule || {}).dateModified;
            if (!data.length || !data[0].data.length || !dateModified) {
                return [];
            }
            var seriesData = data[0].data;
            var seriesStart = seriesData[0].name;
            var seriesEnd = seriesData[seriesData.length - 1].name;
            var ruleChanged = moment(dateModified).valueOf();
            if (ruleChanged < seriesStart) {
                return [];
            }
            var chartWidth = width - X_AXIS_BOUNDARY_GAP;
            var position = X_AXIS_BOUNDARY_GAP +
                Math.round((chartWidth * (ruleChanged - seriesStart)) / (seriesEnd - seriesStart));
            return [
                {
                    type: 'line',
                    draggable: false,
                    position: [position, 0],
                    shape: { y1: 0, y2: height - VERTICAL_PADDING, x1: 1, x2: 1 },
                    style: {
                        stroke: theme.gray200,
                    },
                },
                {
                    type: 'rect',
                    draggable: false,
                    position: [X_AXIS_BOUNDARY_GAP, 0],
                    shape: {
                        // +1 makes the gray area go midway onto the dashed line above
                        width: position - X_AXIS_BOUNDARY_GAP + 1,
                        height: height - VERTICAL_PADDING,
                    },
                    style: {
                        fill: color(theme.gray100).alpha(0.42).rgb().string(),
                    },
                    z: 100,
                },
            ];
        };
        return _this;
    }
    Object.defineProperty(MetricChart.prototype, "metricPreset", {
        get: function () {
            var rule = this.props.rule;
            return rule ? getIncidentRuleMetricPreset(rule) : undefined;
        },
        enumerable: false,
        configurable: true
    });
    MetricChart.prototype.renderChartActions = function (totalDuration, criticalDuration, warningDuration) {
        var _a = this.props, rule = _a.rule, orgId = _a.orgId, projects = _a.projects, timePeriod = _a.timePeriod;
        var preset = this.metricPreset;
        var ctaOpts = {
            orgSlug: orgId,
            projects: projects,
            rule: rule,
            start: timePeriod.start,
            end: timePeriod.end,
        };
        var _b = preset
            ? preset.makeCtaParams(ctaOpts)
            : makeDefaultCta(ctaOpts), buttonText = _b.buttonText, props = __rest(_b, ["buttonText"]);
        var resolvedPercent = ((100 * Math.max(totalDuration - criticalDuration - warningDuration, 0)) /
            totalDuration).toFixed(2);
        var criticalPercent = (100 * Math.min(criticalDuration / totalDuration, 1)).toFixed(2);
        var warningPercent = (100 * Math.min(warningDuration / totalDuration, 1)).toFixed(2);
        return (<ChartActions>
        <ChartSummary>
          <SummaryText>{t('SUMMARY')}</SummaryText>
          <SummaryStats>
            <StatItem>
              <IconCheckmark color="green300" isCircled/>
              <StatCount>{resolvedPercent}%</StatCount>
            </StatItem>
            <StatItem>
              <IconWarning color="yellow300"/>
              <StatCount>{warningPercent}%</StatCount>
            </StatItem>
            <StatItem>
              <IconFire color="red300"/>
              <StatCount>{criticalPercent}%</StatCount>
            </StatItem>
          </SummaryStats>
        </ChartSummary>
        <Feature features={['discover-basic']}>
          <Button size="small" disabled={!rule} {...props}>
            {buttonText}
          </Button>
        </Feature>
      </ChartActions>);
    };
    MetricChart.prototype.renderChart = function (data, series, maxThresholdValue, maxSeriesValue) {
        var _this = this;
        var _a = this.props.rule || {}, dateModified = _a.dateModified, timeWindow = _a.timeWindow;
        return (<LineChart isGroupedByDate showTimeInTooltip forwardedRef={this.handleRef} grid={{
                left: 0,
                right: 0,
                top: space(2),
                bottom: 0,
            }} yAxis={maxThresholdValue > maxSeriesValue ? { max: maxThresholdValue } : undefined} series={series} graphic={Graphic({
                elements: this.getRuleChangeThresholdElements(data),
            })} tooltip={{
                formatter: function (seriesParams) {
                    // seriesParams can be object instead of array
                    var pointSeries = Array.isArray(seriesParams)
                        ? seriesParams
                        : [seriesParams];
                    var _a = pointSeries[0], marker = _a.marker, pointData = _a.data, seriesName = _a.seriesName;
                    var _b = __read(pointData, 2), pointX = _b[0], pointY = _b[1];
                    var isModified = dateModified && pointX <= new Date(dateModified).getTime();
                    var startTime = getFormattedDate(new Date(pointX), 'MMM D LT');
                    var endTime = getFormattedDate(moment(new Date(pointX)).add(timeWindow, 'minutes'), 'MMM D LT');
                    var title = isModified
                        ? "<strong>" + t('Alert Rule Modified') + "</strong>"
                        : marker + " <strong>" + seriesName + "</strong>";
                    var value = isModified
                        ? seriesName + " " + pointY.toLocaleString()
                        : pointY.toLocaleString();
                    return [
                        "<div class=\"tooltip-series\"><div>",
                        "<span class=\"tooltip-label\">" + title + "</span>" + value,
                        "</div></div>",
                        "<div class=\"tooltip-date\">" + startTime + " &mdash; " + endTime + "</div>",
                        "<div class=\"tooltip-arrow\"></div>",
                    ].join('');
                },
            }} onFinished={function () {
                // We want to do this whenever the chart finishes re-rendering so that we can update the dimensions of
                // any graphics related to the triggers (e.g. the threshold areas + boundaries)
                _this.updateDimensions();
            }}/>);
    };
    MetricChart.prototype.renderEmpty = function () {
        return (<ChartPanel>
        <PanelBody withPadding>
          <Placeholder height="200px"/>
        </PanelBody>
      </ChartPanel>);
    };
    MetricChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, router = _a.router, rule = _a.rule, organization = _a.organization, timePeriod = _a.timePeriod, projects = _a.projects, interval = _a.interval, metricText = _a.metricText, filter = _a.filter, query = _a.query, incidents = _a.incidents;
        if (!rule) {
            return this.renderEmpty();
        }
        var criticalTrigger = rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        // If the chart duration isn't as long as the rollup duration the events-stats
        // endpoint will return an invalid timeseriesData data set
        var viableStartDate = getUtcDateString(moment.min(moment.utc(timePeriod.start), moment.utc(timePeriod.end).subtract(rule.timeWindow, 'minutes')));
        return (<EventsRequest api={api} organization={organization} query={query} environment={rule.environment ? [rule.environment] : undefined} project={projects.map(function (project) { return Number(project.id); })} interval={interval} start={viableStartDate} end={timePeriod.end} yAxis={rule.aggregate} includePrevious={false} currentSeriesName={rule.aggregate} partial={false}>
        {function (_a) {
                var _b, _c;
                var loading = _a.loading, timeseriesData = _a.timeseriesData;
                if (loading || !timeseriesData) {
                    return _this.renderEmpty();
                }
                var series = __spreadArray([], __read(timeseriesData));
                // Ensure series data appears above incident lines
                series[0].z = 100;
                var dataArr = timeseriesData[0].data;
                var maxSeriesValue = dataArr.reduce(function (currMax, coord) { return Math.max(currMax, coord.value); }, 0);
                var firstPoint = Number(dataArr[0].name);
                var lastPoint = dataArr[dataArr.length - 1].name;
                var totalDuration = lastPoint - firstPoint;
                var criticalDuration = 0;
                var warningDuration = 0;
                series.push(createStatusAreaSeries(theme.green300, firstPoint, lastPoint));
                if (incidents) {
                    // select incidents that fall within the graph range
                    var periodStart_1 = moment.utc(firstPoint);
                    incidents
                        .filter(function (incident) {
                        return !incident.dateClosed || moment(incident.dateClosed).isAfter(periodStart_1);
                    })
                        .forEach(function (incident) {
                        var _a, _b;
                        var statusChanges = (_a = incident.activities) === null || _a === void 0 ? void 0 : _a.filter(function (_a) {
                            var type = _a.type, value = _a.value;
                            return type === IncidentActivityType.STATUS_CHANGE &&
                                value &&
                                [
                                    "" + IncidentStatus.WARNING,
                                    "" + IncidentStatus.CRITICAL,
                                ].includes(value);
                        }).sort(function (a, b) {
                            return moment(a.dateCreated).valueOf() - moment(b.dateCreated).valueOf();
                        });
                        var incidentEnd = (_b = incident.dateClosed) !== null && _b !== void 0 ? _b : moment().valueOf();
                        var timeWindowMs = rule.timeWindow * 60 * 1000;
                        var incidentStartDate = moment(incident.dateStarted).valueOf();
                        var incidentStartValue = dataArr.find(function (point) { return point.name >= incidentStartDate; });
                        series.push(createIncidentSeries(router, organization.slug, warningTrigger &&
                            statusChanges &&
                            !statusChanges.find(function (_a) {
                                var value = _a.value;
                                return value === "" + IncidentStatus.CRITICAL;
                            })
                            ? theme.yellow300
                            : theme.red300, incidentStartDate, incident.identifier, incidentStartValue, series[0].seriesName));
                        var areaStart = Math.max(moment(incident.dateStarted).valueOf(), firstPoint);
                        var areaEnd = Math.min((statusChanges === null || statusChanges === void 0 ? void 0 : statusChanges.length) && statusChanges[0].dateCreated
                            ? moment(statusChanges[0].dateCreated).valueOf() - timeWindowMs
                            : moment(incidentEnd).valueOf(), lastPoint);
                        var areaColor = warningTrigger ? theme.yellow300 : theme.red300;
                        series.push(createStatusAreaSeries(areaColor, areaStart, areaEnd));
                        if (areaColor === theme.yellow300) {
                            warningDuration += areaEnd - areaStart;
                        }
                        else {
                            criticalDuration += areaEnd - areaStart;
                        }
                        statusChanges === null || statusChanges === void 0 ? void 0 : statusChanges.forEach(function (activity, idx) {
                            var statusAreaStart = Math.max(moment(activity.dateCreated).valueOf() - timeWindowMs, firstPoint);
                            var statusAreaEnd = Math.min(idx === statusChanges.length - 1
                                ? moment(incidentEnd).valueOf()
                                : moment(statusChanges[idx + 1].dateCreated).valueOf() -
                                    timeWindowMs, lastPoint);
                            var statusAreaColor = activity.value === "" + IncidentStatus.CRITICAL
                                ? theme.red300
                                : theme.yellow300;
                            series.push(createStatusAreaSeries(statusAreaColor, statusAreaStart, statusAreaEnd));
                            if (statusAreaColor === theme.yellow300) {
                                warningDuration += statusAreaEnd - statusAreaStart;
                            }
                            else {
                                criticalDuration += statusAreaEnd - statusAreaStart;
                            }
                        });
                    });
                }
                var maxThresholdValue = 0;
                if (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) {
                    var alertThreshold = warningTrigger.alertThreshold;
                    var warningThresholdLine = createThresholdSeries(theme.yellow300, alertThreshold);
                    series.push(warningThresholdLine);
                    maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
                }
                if (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) {
                    var alertThreshold = criticalTrigger.alertThreshold;
                    var criticalThresholdLine = createThresholdSeries(theme.red300, alertThreshold);
                    series.push(criticalThresholdLine);
                    maxThresholdValue = Math.max(maxThresholdValue, alertThreshold);
                }
                return (<ChartPanel>
              <PanelBody withPadding>
                <ChartHeader>
                  <ChartTitle>
                    <PresetName>
                      {(_c = (_b = _this.metricPreset) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : t('Custom metric')}
                    </PresetName>
                    {metricText}
                  </ChartTitle>
                  {filter}
                </ChartHeader>
                {_this.renderChart(timeseriesData, series, maxThresholdValue, maxSeriesValue)}
              </PanelBody>
              {_this.renderChartActions(totalDuration, criticalDuration, warningDuration)}
            </ChartPanel>);
            }}
      </EventsRequest>);
    };
    return MetricChart;
}(React.PureComponent));
export default withRouter(MetricChart);
var ChartPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
var ChartHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var ChartTitle = styled('header')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n"], ["\n  display: flex;\n  flex-direction: row;\n"])));
var PresetName = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  text-transform: capitalize;\n  margin-right: ", ";\n"], ["\n  text-transform: capitalize;\n  margin-right: ", ";\n"])), space(0.5));
var ChartActions = styled(PanelFooter)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  padding: ", " 20px;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  padding: ", " 20px;\n"])), space(1));
var ChartSummary = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  margin-right: auto;\n"], ["\n  display: flex;\n  margin-right: auto;\n"])));
var SummaryText = styled('span')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-top: ", ";\n  font-weight: bold;\n  font-size: ", ";\n"], ["\n  margin-top: ", ";\n  font-weight: bold;\n  font-size: ", ";\n"])), space(0.25), function (p) { return p.theme.fontSizeSmall; });
var SummaryStats = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 ", ";\n"])), space(2));
var StatItem = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0 ", " 0 0;\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0 ", " 0 0;\n"])), space(2));
var StatCount = styled('span')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  margin-left: ", ";\n  margin-top: ", ";\n  color: ", ";\n"], ["\n  margin-left: ", ";\n  margin-top: ", ";\n  color: ", ";\n"])), space(0.5), space(0.25), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=metricChart.jsx.map
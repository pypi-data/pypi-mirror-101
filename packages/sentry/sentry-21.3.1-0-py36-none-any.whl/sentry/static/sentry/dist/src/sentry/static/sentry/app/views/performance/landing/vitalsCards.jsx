import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Card from 'app/components/card';
import EventsRequest from 'app/components/charts/eventsRequest';
import { HeaderTitle } from 'app/components/charts/styles';
import { getInterval } from 'app/components/charts/utils';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import Sparklines from 'app/components/sparklines';
import SparklinesLine from 'app/components/sparklines/line';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getUtcToLocalDateObject } from 'app/utils/dates';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getAggregateAlias, WebVital } from 'app/utils/discover/fields';
import { WEB_VITAL_DETAILS } from 'app/utils/performance/vitals/constants';
import VitalsCardsDiscoverQuery from 'app/utils/performance/vitals/vitalsCardsDiscoverQuery';
import { decodeList } from 'app/utils/queryString';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
import ColorBar from '../vitalDetail/colorBar';
import { vitalAbbreviations, vitalDetailRouteWithQuery, vitalMap, VitalState, vitalStateColors, } from '../vitalDetail/utils';
import VitalPercents from '../vitalDetail/vitalPercents';
import { backendCardDetails, getBackendFunction, getDefaultDisplayFieldForPlatform, LandingDisplayField, } from './utils';
export function FrontendCards(props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, projects = props.projects, _a = props.frontendOnly, frontendOnly = _a === void 0 ? false : _a;
    if (frontendOnly) {
        var defaultDisplay = getDefaultDisplayFieldForPlatform(projects, eventView);
        var isFrontend = defaultDisplay === LandingDisplayField.FRONTEND_PAGELOAD;
        if (!isFrontend) {
            return null;
        }
    }
    var vitals = [WebVital.FCP, WebVital.LCP, WebVital.FID, WebVital.CLS];
    return (<VitalsCardsDiscoverQuery eventView={eventView} location={location} orgSlug={organization.slug} vitals={vitals}>
      {function (_a) {
            var isLoading = _a.isLoading, vitalsData = _a.vitalsData;
            return (<VitalsContainer>
            {vitals.map(function (vital) {
                    var _a, _b, _c;
                    var target = vitalDetailRouteWithQuery({
                        orgSlug: organization.slug,
                        query: eventView.generateQueryStringObject(),
                        vitalName: vital,
                        projectID: decodeList(location.query.project),
                    });
                    var value = isLoading
                        ? '\u2014'
                        : getP75((_a = vitalsData === null || vitalsData === void 0 ? void 0 : vitalsData[vital]) !== null && _a !== void 0 ? _a : null, vital);
                    var chart = (<VitalBarContainer>
                  <VitalBar isLoading={isLoading} vital={vital} data={vitalsData}/>
                </VitalBarContainer>);
                    return (<Link key={vital} to={target} data-test-id={"vitals-linked-card-" + vitalAbbreviations[vital]}>
                  <VitalCard title={(_b = vitalMap[vital]) !== null && _b !== void 0 ? _b : ''} tooltip={(_c = WEB_VITAL_DETAILS[vital].description) !== null && _c !== void 0 ? _c : ''} value={isLoading ? '\u2014' : value} chart={chart} minHeight={150}/>
                </Link>);
                })}
          </VitalsContainer>);
        }}
    </VitalsCardsDiscoverQuery>);
}
var VitalBarContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(1.5));
function _BackendCards(props) {
    var api = props.api, baseEventView = props.eventView, location = props.location, organization = props.organization;
    var functionNames = [
        'p75',
        'tpm',
        'failure_rate',
        'apdex',
    ];
    var functions = functionNames.map(function (fn) { return getBackendFunction(fn, organization); });
    var eventView = baseEventView.withColumns(functions);
    // construct request parameters for fetching chart data
    var globalSelection = eventView.getGlobalSelection();
    var start = globalSelection.datetime.start
        ? getUtcToLocalDateObject(globalSelection.datetime.start)
        : undefined;
    var end = globalSelection.datetime.end
        ? getUtcToLocalDateObject(globalSelection.datetime.end)
        : undefined;
    return (<DiscoverQuery location={location} eventView={eventView} orgSlug={organization.slug} limit={1} referrer="api.performance.vitals-cards">
      {function (_a) {
            var isSummaryLoading = _a.isLoading, tableData = _a.tableData;
            return (<EventsRequest api={api} organization={organization} period={globalSelection.datetime.period} project={globalSelection.projects} environment={globalSelection.environments} start={start} end={end} interval={getInterval({
                    start: start || null,
                    end: end || null,
                    period: globalSelection.datetime.period,
                })} query={eventView.getEventsAPIPayload(location).query} includePrevious={false} yAxis={eventView.getFields()} partial>
          {function (_a) {
                    var results = _a.results;
                    var series = results === null || results === void 0 ? void 0 : results.reduce(function (allSeries, oneSeries) {
                        allSeries[oneSeries.seriesName] = oneSeries.data.map(function (item) { return item.value; });
                        return allSeries;
                    }, {});
                    var fields = eventView
                        .getFields()
                        .map(function (fn, i) { return [functionNames[i], fn, series === null || series === void 0 ? void 0 : series[fn]]; });
                    return (<VitalsContainer>
                {fields.map(function (_a) {
                            var _b, _c;
                            var _d = __read(_a, 3), name = _d[0], fn = _d[1], data = _d[2];
                            var _e = backendCardDetails(organization)[name], title = _e.title, tooltip = _e.tooltip, formatter = _e.formatter;
                            var alias = getAggregateAlias(fn);
                            var rawValue = (_c = (_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0]) === null || _c === void 0 ? void 0 : _c[alias];
                            var value = isSummaryLoading || rawValue === undefined
                                ? '\u2014'
                                : formatter(rawValue);
                            var chart = <SparklineChart data={data}/>;
                            return (<VitalCard key={name} title={title} tooltip={tooltip} value={value} chart={chart} horizontal minHeight={102} isNotInteractive/>);
                        })}
              </VitalsContainer>);
                }}
        </EventsRequest>);
        }}
    </DiscoverQuery>);
}
export var BackendCards = withApi(_BackendCards);
function SparklineChart(props) {
    var data = props.data;
    var width = 150;
    var height = 24;
    var lineColor = theme.charts.getColorPalette(1)[0];
    return (<SparklineContainer data-test-id="sparkline" width={width} height={height}>
      <Sparklines data={data} width={width} height={height}>
        <SparklinesLine style={{ stroke: lineColor, fill: 'none', strokeWidth: 3 }}/>
      </Sparklines>
    </SparklineContainer>);
}
var SparklineContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 4;\n  max-height: ", "px;\n  max-width: ", "px;\n  margin: ", " ", " ", " ", ";\n"], ["\n  flex-grow: 4;\n  max-height: ", "px;\n  max-width: ", "px;\n  margin: ", " ", " ", " ", ";\n"])), function (p) { return p.height; }, function (p) { return p.width; }, space(1), space(0), space(1.5), space(3));
var VitalsContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-column-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-column-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(2, 1fr);\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; });
export function VitalBar(props) {
    var _a;
    var isLoading = props.isLoading, data = props.data, vital = props.vital, value = props.value, _b = props.showBar, showBar = _b === void 0 ? true : _b, _c = props.showStates, showStates = _c === void 0 ? false : _c, _d = props.showDurationDetail, showDurationDetail = _d === void 0 ? false : _d, _e = props.showVitalPercentNames, showVitalPercentNames = _e === void 0 ? false : _e;
    if (isLoading) {
        return showStates ? <Placeholder height="48px"/> : null;
    }
    var emptyState = showStates ? (<EmptyVitalBar small>{t('No vitals found')}</EmptyVitalBar>) : null;
    if (!data) {
        return emptyState;
    }
    var counts = {
        poor: 0,
        meh: 0,
        good: 0,
        total: 0,
    };
    var vitals = Array.isArray(vital) ? vital : [vital];
    vitals.forEach(function (vitalName) {
        var _a;
        var c = (_a = data === null || data === void 0 ? void 0 : data[vitalName]) !== null && _a !== void 0 ? _a : {};
        Object.keys(counts).forEach(function (countKey) { return (counts[countKey] += c[countKey]); });
    });
    if (!counts.total) {
        return emptyState;
    }
    var p75 = Array.isArray(vital)
        ? null
        : value !== null && value !== void 0 ? value : getP75((_a = data === null || data === void 0 ? void 0 : data[vital]) !== null && _a !== void 0 ? _a : null, vital);
    var percents = getPercentsFromCounts(counts);
    var colorStops = getColorStopsFromPercents(percents);
    return (<React.Fragment>
      {showBar && <ColorBar colorStops={colorStops}/>}
      <BarDetail>
        {showDurationDetail && p75 && (<div>
            {t('The p75 for all transactions is ')}
            <strong>{p75}</strong>
          </div>)}
        <VitalPercents vital={vital} percents={percents} showVitalPercentNames={showVitalPercentNames}/>
      </BarDetail>
    </React.Fragment>);
}
var EmptyVitalBar = styled(EmptyStateWarning)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  height: 48px;\n  padding: ", " 15%;\n"], ["\n  height: 48px;\n  padding: ", " 15%;\n"])), space(1.5));
function VitalCard(props) {
    var chart = props.chart, minHeight = props.minHeight, horizontal = props.horizontal, title = props.title, tooltip = props.tooltip, value = props.value, isNotInteractive = props.isNotInteractive;
    return (<StyledCard interactive={!isNotInteractive} minHeight={minHeight}>
      <HeaderTitle>
        <OverflowEllipsis>{t(title)}</OverflowEllipsis>
        <QuestionTooltip size="sm" position="top" title={tooltip}/>
      </HeaderTitle>
      <CardContent horizontal={horizontal}>
        <CardValue>{value}</CardValue>
        {chart}
      </CardContent>
    </StyledCard>);
}
var CardContent = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 100%;\n  display: flex;\n  flex-direction: ", ";\n  justify-content: space-between;\n"], ["\n  width: 100%;\n  display: flex;\n  flex-direction: ", ";\n  justify-content: space-between;\n"])), function (p) { return (p.horizontal ? 'row' : 'column'); });
var StyledCard = styled(Card)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", " ", ";\n  align-items: flex-start;\n  margin-bottom: ", ";\n  ", ";\n"], ["\n  color: ", ";\n  padding: ", " ", ";\n  align-items: flex-start;\n  margin-bottom: ", ";\n  ", ";\n"])), function (p) { return p.theme.textColor; }, space(2), space(3), space(2), function (p) { return p.minHeight && "min-height: " + p.minHeight + "px"; });
function getP75(data, vitalName) {
    var _a;
    var p75 = (_a = data === null || data === void 0 ? void 0 : data.p75) !== null && _a !== void 0 ? _a : null;
    if (p75 === null) {
        return '\u2014';
    }
    else {
        return vitalName === WebVital.CLS ? p75.toFixed(2) : p75.toFixed(0) + "ms";
    }
}
function getPercentsFromCounts(_a) {
    var poor = _a.poor, meh = _a.meh, good = _a.good, total = _a.total;
    var poorPercent = poor / total;
    var mehPercent = meh / total;
    var goodPercent = good / total;
    var percents = [
        {
            vitalState: VitalState.GOOD,
            percent: goodPercent,
        },
        {
            vitalState: VitalState.MEH,
            percent: mehPercent,
        },
        {
            vitalState: VitalState.POOR,
            percent: poorPercent,
        },
    ];
    return percents;
}
function getColorStopsFromPercents(percents) {
    return percents.map(function (_a) {
        var percent = _a.percent, vitalState = _a.vitalState;
        return ({
            percent: percent,
            color: vitalStateColors[vitalState],
        });
    });
}
var BarDetail = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n    justify-content: space-between;\n  }\n"], ["\n  font-size: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n    justify-content: space-between;\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.breakpoints[0]; });
var CardValue = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: 32px;\n  margin-top: ", ";\n"], ["\n  font-size: 32px;\n  margin-top: ", ";\n"])), space(1));
var OverflowEllipsis = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=vitalsCards.jsx.map
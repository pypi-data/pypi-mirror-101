import { __assign, __read, __spreadArray } from "tslib";
import color from 'color';
import { getDiffInMinutes, TWO_WEEKS } from 'app/components/charts/utils';
import CHART_PALETTE from 'app/constants/chartPalette';
import { t } from 'app/locale';
import { escapeDoubleQuotes, percent } from 'app/utils';
import { getUtcDateString } from 'app/utils/dates';
import EventView from 'app/utils/discover/eventView';
import { getAggregateAlias, WebVital } from 'app/utils/discover/fields';
import { formatVersion } from 'app/utils/formatters';
import { WEB_VITAL_DETAILS } from 'app/utils/performance/vitals/constants';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { getCrashFreePercent } from 'app/views/releases/utils';
import { sessionTerm } from 'app/views/releases/utils/sessionTerm';
import { EventType, YAxis } from './releaseChartControls';
var SESSIONS_CHART_PALETTE = CHART_PALETTE[3];
export function getInterval(datetimeObj) {
    var diffInMinutes = getDiffInMinutes(datetimeObj);
    if (diffInMinutes > TWO_WEEKS) {
        return '6h';
    }
    else {
        return '1h';
    }
}
export function getReleaseEventView(selection, version, yAxis, eventType, vitalType, organization, 
/**
 * Indicates that we're only interested in the current release.
 * This is useful for the event meta end point where we don't want
 * to include the other releases.
 */
currentOnly) {
    if (eventType === void 0) { eventType = EventType.ALL; }
    if (vitalType === void 0) { vitalType = WebVital.LCP; }
    var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
    var start = datetime.start, end = datetime.end, period = datetime.period;
    var releaseFilter = currentOnly ? "release:" + version : '';
    var toOther = "to_other(release,\"" + escapeDoubleQuotes(version) + "\",others,current)";
    // this orderby ensures that the order is [others, current]
    var toOtherAlias = getAggregateAlias(toOther);
    var baseQuery = {
        id: undefined,
        version: 2,
        name: t('Release') + " " + formatVersion(version),
        fields: ["count()", toOther],
        orderby: toOtherAlias,
        range: period,
        environment: environments,
        projects: projects,
        start: start ? getUtcDateString(start) : undefined,
        end: end ? getUtcDateString(end) : undefined,
    };
    switch (yAxis) {
        case YAxis.FAILED_TRANSACTIONS:
            var statusFilters = ['ok', 'cancelled', 'unknown'].map(function (s) { return "!transaction.status:" + s; });
            return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: stringifyQueryObject(new QueryResults(__spreadArray(['event.type:transaction', releaseFilter], __read(statusFilters)).filter(Boolean))) }));
        case YAxis.COUNT_VITAL:
        case YAxis.COUNT_DURATION:
            var column = yAxis === YAxis.COUNT_DURATION ? 'transaction.duration' : vitalType;
            var threshold = yAxis === YAxis.COUNT_DURATION
                ? organization === null || organization === void 0 ? void 0 : organization.apdexThreshold
                : WEB_VITAL_DETAILS[vitalType].poorThreshold;
            return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: stringifyQueryObject(new QueryResults([
                    'event.type:transaction',
                    releaseFilter,
                    threshold ? column + ":>" + threshold : '',
                ].filter(Boolean))) }));
        case YAxis.EVENTS:
            var eventTypeFilter = eventType === EventType.ALL ? '' : "event.type:" + eventType;
            return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { query: stringifyQueryObject(new QueryResults([releaseFilter, eventTypeFilter].filter(Boolean))) }));
        default:
            return EventView.fromSavedQuery(__assign(__assign({}, baseQuery), { fields: ['title', 'count()', 'event.type', 'issue', 'last_seen()'], query: stringifyQueryObject(new QueryResults(["release:" + version, '!event.type:transaction'])), orderby: '-last_seen' }));
    }
}
export function initSessionsBreakdownChartData() {
    return {
        healthy: {
            seriesName: sessionTerm.healthy,
            data: [],
            color: SESSIONS_CHART_PALETTE[3],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[3],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        errored: {
            seriesName: sessionTerm.errored,
            data: [],
            color: SESSIONS_CHART_PALETTE[0],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[0],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        abnormal: {
            seriesName: sessionTerm.abnormal,
            data: [],
            color: SESSIONS_CHART_PALETTE[1],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[1],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        crashed: {
            seriesName: sessionTerm.crashed,
            data: [],
            color: SESSIONS_CHART_PALETTE[2],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[2],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
export function initOtherSessionsBreakdownChartData() {
    return __assign({ healthy: {
            seriesName: sessionTerm.otherHealthy,
            data: [],
            color: SESSIONS_CHART_PALETTE[3],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[3],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, errored: {
            seriesName: sessionTerm.otherErrored,
            data: [],
            color: SESSIONS_CHART_PALETTE[0],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[0],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, abnormal: {
            seriesName: sessionTerm.otherAbnormal,
            data: [],
            color: SESSIONS_CHART_PALETTE[1],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[1],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, crashed: {
            seriesName: sessionTerm.otherCrashed,
            data: [],
            color: SESSIONS_CHART_PALETTE[2],
            areaStyle: {
                color: SESSIONS_CHART_PALETTE[2],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        } }, initOtherReleasesChartData());
}
export function initCrashFreeChartData() {
    return {
        users: {
            seriesName: sessionTerm['crash-free-users'],
            data: [],
            color: CHART_PALETTE[1][0],
            lineStyle: {
                color: CHART_PALETTE[1][0],
            },
        },
        sessions: {
            seriesName: sessionTerm['crash-free-sessions'],
            data: [],
            color: CHART_PALETTE[1][1],
            lineStyle: {
                color: CHART_PALETTE[1][1],
            },
        },
    };
}
export function initOtherCrashFreeChartData() {
    return __assign(__assign({}, initOtherReleasesChartData()), { users: {
            seriesName: sessionTerm.otherCrashFreeUsers,
            data: [],
            z: 0,
            color: color(CHART_PALETTE[1][0]).lighten(0.9).alpha(0.9).string(),
            lineStyle: {
                color: CHART_PALETTE[1][0],
                opacity: 0.1,
            },
        }, sessions: {
            seriesName: sessionTerm.otherCrashFreeSessions,
            data: [],
            z: 0,
            color: color(CHART_PALETTE[1][1]).lighten(0.5).alpha(0.9).string(),
            lineStyle: {
                color: CHART_PALETTE[1][1],
                opacity: 0.3,
            },
        } });
}
export function initSessionDurationChartData() {
    return {
        0: {
            seriesName: sessionTerm.duration,
            data: [],
            color: CHART_PALETTE[0][0],
            areaStyle: {
                color: CHART_PALETTE[0][0],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
export function initOtherSessionDurationChartData() {
    return {
        0: {
            seriesName: sessionTerm.otherReleases,
            data: [],
            z: 0,
            color: color(CHART_PALETTE[0][0]).alpha(0.4).string(),
            areaStyle: {
                color: CHART_PALETTE[0][0],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
// this series will never be filled with data - we use it to act as an alias in legend (we don't display other healthy, other crashes, etc. there)
// if you click on it, we toggle all "other" series (other healthy, other crashed, ...)
function initOtherReleasesChartData() {
    return {
        otherReleases: {
            seriesName: sessionTerm.otherReleases,
            data: [],
            color: color(CHART_PALETTE[0][0]).alpha(0.4).string(),
        },
    };
}
export function isOtherSeries(series) {
    return [
        sessionTerm.otherCrashed,
        sessionTerm.otherAbnormal,
        sessionTerm.otherErrored,
        sessionTerm.otherHealthy,
        sessionTerm.otherCrashFreeUsers,
        sessionTerm.otherCrashFreeSessions,
    ].includes(series.seriesName);
}
var seriesOrder = [
    sessionTerm.healthy,
    sessionTerm.errored,
    sessionTerm.crashed,
    sessionTerm.abnormal,
    sessionTerm.otherHealthy,
    sessionTerm.otherErrored,
    sessionTerm.otherCrashed,
    sessionTerm.otherAbnormal,
    sessionTerm.duration,
    sessionTerm['crash-free-sessions'],
    sessionTerm['crash-free-users'],
    sessionTerm.otherCrashFreeSessions,
    sessionTerm.otherCrashFreeUsers,
    sessionTerm.otherReleases,
];
export function sortSessionSeries(a, b) {
    return seriesOrder.indexOf(a.seriesName) - seriesOrder.indexOf(b.seriesName);
}
export function getTotalsFromSessionsResponse(_a) {
    var response = _a.response, field = _a.field;
    return response.groups.reduce(function (acc, group) {
        return acc + group.totals[field];
    }, 0);
}
export function fillChartDataFromSessionsResponse(_a) {
    var response = _a.response, field = _a.field, groupBy = _a.groupBy, chartData = _a.chartData, valueFormatter = _a.valueFormatter;
    response.intervals.forEach(function (interval, index) {
        response.groups.forEach(function (group) {
            var value = group.series[field][index];
            chartData[groupBy === null ? 0 : group.by[groupBy]].data.push({
                name: interval,
                value: typeof valueFormatter === 'function' ? valueFormatter(value) : value,
            });
        });
    });
    return chartData;
}
export function fillCrashFreeChartDataFromSessionsReponse(_a) {
    var response = _a.response, field = _a.field, entity = _a.entity, chartData = _a.chartData;
    response.intervals.forEach(function (interval, index) {
        var _a, _b;
        var intervalTotalSessions = response.groups.reduce(function (acc, group) { return acc + group.series[field][index]; }, 0);
        var intervalCrashedSessions = (_b = (_a = response.groups.find(function (group) { return group.by['session.status'] === 'crashed'; })) === null || _a === void 0 ? void 0 : _a.series[field][index]) !== null && _b !== void 0 ? _b : 0;
        var crashedSessionsPercent = percent(intervalCrashedSessions, intervalTotalSessions);
        chartData[entity].data.push({
            name: interval,
            value: intervalTotalSessions === 0
                ? null
                : getCrashFreePercent(100 - crashedSessionsPercent),
        });
    });
    return chartData;
}
//# sourceMappingURL=utils.jsx.map
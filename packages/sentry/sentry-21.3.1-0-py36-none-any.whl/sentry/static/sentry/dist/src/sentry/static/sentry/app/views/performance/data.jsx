import { t } from 'app/locale';
import EventView from 'app/utils/discover/eventView';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import { getCurrentLandingDisplay, LandingDisplayField } from './landing/utils';
import { getVitalDetailTableMehStatusFunction, getVitalDetailTablePoorStatusFunction, vitalNameFromLocation, } from './vitalDetail/utils';
import { FilterViews } from './landing';
import { getCurrentPerformanceView } from './utils';
export var DEFAULT_STATS_PERIOD = '24h';
export var COLUMN_TITLES = [
    'transaction',
    'project',
    'tpm',
    'p50',
    'p95',
    'failure rate',
    'apdex',
    'users',
    'user misery',
];
export var PERFORMANCE_TERM;
(function (PERFORMANCE_TERM) {
    PERFORMANCE_TERM["APDEX"] = "apdex";
    PERFORMANCE_TERM["TPM"] = "tpm";
    PERFORMANCE_TERM["THROUGHPUT"] = "throughput";
    PERFORMANCE_TERM["FAILURE_RATE"] = "failureRate";
    PERFORMANCE_TERM["P50"] = "p50";
    PERFORMANCE_TERM["P75"] = "p75";
    PERFORMANCE_TERM["P95"] = "p95";
    PERFORMANCE_TERM["P99"] = "p99";
    PERFORMANCE_TERM["LCP"] = "lcp";
    PERFORMANCE_TERM["USER_MISERY"] = "userMisery";
    PERFORMANCE_TERM["STATUS_BREAKDOWN"] = "statusBreakdown";
    PERFORMANCE_TERM["DURATION_DISTRIBUTION"] = "durationDistribution";
})(PERFORMANCE_TERM || (PERFORMANCE_TERM = {}));
export function getAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX),
            value: "apdex(" + organization.apdexThreshold + ")",
            label: t('Apdex'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: t('Transactions Per Minute'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            value: 'failure_rate()',
            label: t('Failure Rate'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: 'p50()',
            label: t('p50 Duration'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: 'p95()',
            label: t('p95 Duration'),
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P99),
            value: 'p99()',
            label: t('p99 Duration'),
        },
    ];
}
export function getFrontendAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.LCP),
            value: "p75(lcp)",
            label: t('LCP p75'),
            field: 'p75(measurements.lcp)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'lcp_distribution',
            label: t('LCP Distribution'),
            field: 'measurements.lcp',
            isDistribution: true,
            isRightDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: t('Transactions Per Minute'),
            field: 'tpm()',
        },
    ];
}
export function getFrontendOtherAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: "p50()",
            label: t('Duration p50'),
            field: 'p50(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P75),
            value: "p75()",
            label: t('Duration p75'),
            field: 'p75(transaction.duration)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: "p95()",
            label: t('Duration p95'),
            field: 'p95(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'duration_distribution',
            label: t('Duration Distribution'),
            field: 'transaction.duration',
            isDistribution: true,
            isRightDefault: true,
        },
    ];
}
export function getBackendAxisOptions(organization) {
    return [
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P50),
            value: "p50()",
            label: t('Duration p50'),
            field: 'p50(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P75),
            value: "p75()",
            label: t('Duration p75'),
            field: 'p75(transaction.duration)',
            isLeftDefault: true,
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P95),
            value: "p95()",
            label: t('Duration p95'),
            field: 'p95(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P99),
            value: "p99()",
            label: t('Duration p99'),
            field: 'p99(transaction.duration)',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX),
            value: "apdex(" + organization.apdexThreshold + ")",
            label: t('Apdex'),
            field: "apdex(" + organization.apdexThreshold + ")",
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.TPM),
            value: 'tpm()',
            label: t('Transactions Per Minute'),
            field: 'tpm()',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            value: 'failure_rate()',
            label: t('Failure Rate'),
            field: 'failure_rate()',
        },
        {
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.DURATION_DISTRIBUTION),
            value: 'duration_distribution',
            label: t('Duration Distribution'),
            field: 'transaction.duration',
            isDistribution: true,
            isRightDefault: true,
        },
    ];
}
var PERFORMANCE_TERMS = {
    apdex: function () {
        return t('Apdex is the ratio of both satisfactory and tolerable response times to all response times. To adjust the tolerable threshold, go to performance settings.');
    },
    tpm: function () { return t('TPM is the number of recorded transaction events per minute.'); },
    throughput: function () {
        return t('Throughput is the number of recorded transaction events per minute.');
    },
    failureRate: function () {
        return t('Failure rate is the percentage of recorded transactions that had a known and unsuccessful status.');
    },
    p50: function () { return t('p50 indicates the duration that 50% of transactions are faster than.'); },
    p75: function () { return t('p75 indicates the duration that 75% of transactions are faster than.'); },
    p95: function () { return t('p95 indicates the duration that 95% of transactions are faster than.'); },
    p99: function () { return t('p99 indicates the duration that 99% of transactions are faster than.'); },
    lcp: function () {
        return t('Largest contentful paint (LCP) is a web vital meant to represent user load times');
    },
    userMisery: function (organization) {
        return t("User Misery is a score that represents the number of unique users who have experienced load times 4x your organization's apdex threshold of %sms.", organization.apdexThreshold);
    },
    statusBreakdown: function () {
        return t('The breakdown of transaction statuses. This may indicate what type of failure it is.');
    },
    durationDistribution: function () {
        return t('Distribution buckets counts of transactions at specifics times for your current date range');
    },
};
export function getTermHelp(organization, term) {
    if (!PERFORMANCE_TERMS.hasOwnProperty(term)) {
        return '';
    }
    return PERFORMANCE_TERMS[term](organization);
}
function generateGenericPerformanceEventView(organization, location) {
    var query = location.query;
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'key_transaction',
            'transaction',
            'project',
            'tpm()',
            'p50()',
            'p95()',
            'failure_rate()',
            "apdex(" + organization.apdexThreshold + ")",
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = decodeScalar(query.sort, '-tpm');
    var searchQuery = decodeScalar(query.query, '');
    var conditions = tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"]);
        conditions.query = [];
    }
    savedQuery.query = stringifyQueryObject(conditions);
    var eventView = EventView.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions.addTagValues('event.type', ['transaction']);
    return eventView;
}
function generateBackendPerformanceEventView(organization, location) {
    var query = location.query;
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'key_transaction',
            'transaction',
            'transaction.op',
            'project',
            'tpm()',
            'p50()',
            'p95()',
            'failure_rate()',
            "apdex(" + organization.apdexThreshold + ")",
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = decodeScalar(query.sort, '-tpm');
    var searchQuery = decodeScalar(query.query, '');
    var conditions = tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"]);
        conditions.query = [];
    }
    savedQuery.query = stringifyQueryObject(conditions);
    var eventView = EventView.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions.addTagValues('event.type', ['transaction']);
    return eventView;
}
function generateFrontendPageloadPerformanceEventView(organization, location) {
    var query = location.query;
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'key_transaction',
            'transaction',
            'project',
            'tpm()',
            'p75(measurements.fcp)',
            'p75(measurements.lcp)',
            'p75(measurements.fid)',
            'p75(measurements.cls)',
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = decodeScalar(query.sort, '-tpm');
    var searchQuery = decodeScalar(query.query, '');
    var conditions = tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"]);
        conditions.query = [];
    }
    savedQuery.query = stringifyQueryObject(conditions);
    var eventView = EventView.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addTagValues('event.type', ['transaction'])
        .addTagValues('transaction.op', ['pageload']);
    return eventView;
}
function generateFrontendOtherPerformanceEventView(organization, location) {
    var query = location.query;
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: t('Performance'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'key_transaction',
            'transaction',
            'transaction.op',
            'project',
            'tpm()',
            'p50(transaction.duration)',
            'p75(transaction.duration)',
            'p95(transaction.duration)',
            'count_unique(user)',
            "count_miserable(user," + organization.apdexThreshold + ")",
            "user_misery(" + organization.apdexThreshold + ")",
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = decodeScalar(query.sort, '-tpm');
    var searchQuery = decodeScalar(query.query, '');
    var conditions = tokenizeSearch(searchQuery);
    // This is not an override condition since we want the duration to appear in the search bar as a default.
    if (!conditions.hasTag('transaction.duration')) {
        conditions.setTagValues('transaction.duration', ['<15m']);
    }
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"]);
        conditions.query = [];
    }
    savedQuery.query = stringifyQueryObject(conditions);
    var eventView = EventView.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addTagValues('event.type', ['transaction'])
        .addTagValues('!transaction.op', ['pageload']);
    return eventView;
}
export function generatePerformanceEventView(organization, location, projects) {
    var eventView = generateGenericPerformanceEventView(organization, location);
    var currentPerformanceView = getCurrentPerformanceView(location);
    if (!organization.features.includes('performance-landing-v2') ||
        currentPerformanceView === FilterViews.TRENDS) {
        return eventView;
    }
    var display = getCurrentLandingDisplay(location, projects, eventView);
    switch (display === null || display === void 0 ? void 0 : display.field) {
        case LandingDisplayField.FRONTEND_PAGELOAD:
            return generateFrontendPageloadPerformanceEventView(organization, location);
        case LandingDisplayField.FRONTEND_OTHER:
            return generateFrontendOtherPerformanceEventView(organization, location);
        case LandingDisplayField.BACKEND:
            return generateBackendPerformanceEventView(organization, location);
        default:
            return eventView;
    }
}
export function generatePerformanceVitalDetailView(_organization, location) {
    var query = location.query;
    var vitalName = vitalNameFromLocation(location);
    var hasStartAndEnd = query.start && query.end;
    var savedQuery = {
        id: undefined,
        name: t('Vitals Performance Details'),
        query: 'event.type:transaction',
        projects: [],
        fields: [
            'key_transaction',
            'transaction',
            'project',
            'count_unique(user)',
            'count()',
            "p50(" + vitalName + ")",
            "p75(" + vitalName + ")",
            "p95(" + vitalName + ")",
            getVitalDetailTablePoorStatusFunction(vitalName),
            getVitalDetailTableMehStatusFunction(vitalName),
        ],
        version: 2,
    };
    if (!query.statsPeriod && !hasStartAndEnd) {
        savedQuery.range = DEFAULT_STATS_PERIOD;
    }
    savedQuery.orderby = decodeScalar(query.sort, '-count');
    var searchQuery = decodeScalar(query.query, '');
    var conditions = tokenizeSearch(searchQuery);
    // If there is a bare text search, we want to treat it as a search
    // on the transaction name.
    if (conditions.query.length > 0) {
        conditions.setTagValues('transaction', ["*" + conditions.query.join(' ') + "*"]);
        conditions.query = [];
    }
    savedQuery.query = stringifyQueryObject(conditions);
    var eventView = EventView.fromNewQueryWithLocation(savedQuery, location);
    eventView.additionalConditions
        .addTagValues('event.type', ['transaction'])
        .addTagValues('has', [vitalName]);
    return eventView;
}
//# sourceMappingURL=data.jsx.map
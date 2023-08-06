import { __read, __spreadArray } from "tslib";
import { t } from 'app/locale';
import { DisplayModes } from 'app/utils/discover/types';
import { tokenizeSearch } from 'app/utils/tokenizeSearch';
import { getIncidentRuleDiscoverUrl } from 'app/views/alerts/utils/getIncidentRuleDiscoverUrl';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
import { Dataset } from 'app/views/settings/incidentRules/types';
export var ALERT_RULE_PRESET_AGGREGATES = [
    {
        name: t('Error count'),
        match: /^count\(\)/,
        validDataset: [Dataset.ERRORS],
        default: 'count()',
        /**
         * Simple "Open in Discover" button
         */
        makeCtaParams: makeDefaultCta,
    },
    {
        name: t('Users affected'),
        match: /^count_unique\(tags\[sentry:user\]\)/,
        validDataset: [Dataset.ERRORS],
        default: 'count_unique(tags[sentry:user])',
        /**
         * Simple "Open in Discover" button
         */
        makeCtaParams: makeDefaultCta,
    },
    {
        name: t('Latency'),
        match: /^(p[0-9]{2,3}|percentile\(transaction\.duration,[^)]+\)|avg\([^)]+\))/,
        validDataset: [Dataset.TRANSACTIONS],
        default: 'percentile(transaction.duration, 0.95)',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: function (opts) {
            return makeGenericTransactionCta({
                opts: opts,
                tooltip: t('Latency by Transaction'),
            });
        },
    },
    {
        name: t('Apdex'),
        match: /^apdex\([0-9.]+\)/,
        validDataset: [Dataset.TRANSACTIONS],
        default: 'apdex(300)',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: function (opts) {
            return makeGenericTransactionCta({
                opts: opts,
                tooltip: t('Apdex by Transaction'),
            });
        },
    },
    {
        name: t('Transaction count'),
        match: /^count\(\)/,
        validDataset: [Dataset.TRANSACTIONS],
        default: 'count()',
        /**
         * see: makeGenericTransactionCta
         */
        makeCtaParams: function (opts) { return makeGenericTransactionCta({ opts: opts }); },
    },
    {
        name: t('Failure rate'),
        match: /^failure_rate\(\)/,
        validDataset: [Dataset.TRANSACTIONS],
        default: 'failure_rate()',
        /**
         * See makeFailureRateCta
         */
        makeCtaParams: makeFailureRateCta,
    },
];
/**
 * - CASE 1: If has a specific transaction filter
 *   - CTA is: "View Transaction Summary"
 *   - Tooltip is the transaction name
 *   - the same period as the alert rule graph
 *
 * - CASE 2: If transaction is NOT filtered, or has a * filter:
 *   - "Open in Discover" button with optional tooltip which opens a discover view with...
 *      - fields {transaction, count(), <metric>} sorted by count()
 *      - top-5 activated
 */
function makeGenericTransactionCta(opts) {
    var _a, _b;
    var _c = opts.opts, orgSlug = _c.orgSlug, projects = _c.projects, rule = _c.rule, start = _c.start, end = _c.end, tooltip = opts.tooltip;
    if (!rule || (!start && !end)) {
        return { to: '', buttonText: t('Alert rule details') };
    }
    var query = tokenizeSearch((_a = rule.query) !== null && _a !== void 0 ? _a : '');
    var transaction = (_b = query
        .getTagValues('transaction')) === null || _b === void 0 ? void 0 : _b.find(function (filter) { return !filter.includes('*'); });
    // CASE 1
    if (transaction !== undefined) {
        var summaryUrl = transactionSummaryRouteWithQuery({
            orgSlug: orgSlug,
            transaction: transaction,
            projectID: projects
                .filter(function (_a) {
                var slug = _a.slug;
                return rule.projects.includes(slug);
            })
                .map(function (_a) {
                var id = _a.id;
                return id;
            }),
            query: { start: start, end: end },
        });
        return {
            to: summaryUrl,
            buttonText: t('View Transaction Summary'),
            title: transaction,
        };
    }
    // CASE 2
    var extraQueryParams = {
        fields: __spreadArray([], __read(new Set(['transaction', 'count()', rule.aggregate]))),
        orderby: '-count',
        display: DisplayModes.TOP5,
    };
    var discoverUrl = getIncidentRuleDiscoverUrl({
        orgSlug: orgSlug,
        projects: projects,
        rule: rule,
        start: start,
        end: end,
        extraQueryParams: extraQueryParams,
    });
    return {
        to: discoverUrl,
        buttonText: t('Open in Discover'),
        title: tooltip,
    };
}
/**
 * - CASE 1: Filtered to a specific transaction, "Open in Discover" with...
 *   - fields [transaction.status, count()] sorted by count(),
 *   - "Top 5 period" activated.
 *
 * - CASE 2: If filtered on multiple transactions, "Open in Discover" button
 *   with tooltip "Failure rate by transaction" which opens a discover view
 *   - fields [transaction, failure_rate()] sorted by failure_rate
 *   - top 5 activated
 */
function makeFailureRateCta(_a) {
    var _b, _c;
    var orgSlug = _a.orgSlug, rule = _a.rule, projects = _a.projects, start = _a.start, end = _a.end;
    if (!rule || (!start && !end)) {
        return { to: '', buttonText: t('Alert rule details') };
    }
    var query = tokenizeSearch((_b = rule.query) !== null && _b !== void 0 ? _b : '');
    var transaction = (_c = query
        .getTagValues('transaction')) === null || _c === void 0 ? void 0 : _c.find(function (filter) { return !filter.includes('*'); });
    var extraQueryParams = transaction !== undefined
        ? // CASE 1
            {
                fields: ['transaction.status', 'count()'],
                orderby: '-count',
                display: DisplayModes.TOP5,
            }
        : // Case 2
            {
                fields: ['transaction', 'failure_rate()'],
                orderby: '-failure_rate',
                display: DisplayModes.TOP5,
            };
    var discoverUrl = getIncidentRuleDiscoverUrl({
        orgSlug: orgSlug,
        projects: projects,
        rule: rule,
        start: start,
        end: end,
        extraQueryParams: extraQueryParams,
    });
    return {
        to: discoverUrl,
        buttonText: t('Open in Discover'),
        title: transaction === undefined ? t('Failure rate by transaction') : undefined,
    };
}
/**
 * Get the CTA used for alert rules that do not have a preset
 */
export function makeDefaultCta(_a) {
    var orgSlug = _a.orgSlug, projects = _a.projects, rule = _a.rule, start = _a.start, end = _a.end;
    if (!rule) {
        return {
            buttonText: t('Open in Discover'),
            to: '',
        };
    }
    var extraQueryParams = {
        display: DisplayModes.TOP5,
    };
    return {
        buttonText: t('Open in Discover'),
        to: getIncidentRuleDiscoverUrl({
            orgSlug: orgSlug,
            projects: projects,
            rule: rule,
            start: start,
            end: end,
            extraQueryParams: extraQueryParams,
        }),
    };
}
//# sourceMappingURL=incidentRulePresets.jsx.map
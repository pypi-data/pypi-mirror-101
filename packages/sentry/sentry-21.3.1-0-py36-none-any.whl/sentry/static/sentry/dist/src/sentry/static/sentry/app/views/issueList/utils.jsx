import { __read } from "tslib";
import React from 'react';
import ExternalLink from 'app/components/links/externalLink';
import { t, tct } from 'app/locale';
export var Query;
(function (Query) {
    Query["FOR_REVIEW"] = "is:unresolved is:for_review assigned_or_suggested:me_or_none";
    Query["UNRESOLVED"] = "is:unresolved";
    Query["IGNORED"] = "is:ignored";
    Query["REPROCESSING"] = "is:reprocessing";
})(Query || (Query = {}));
/**
 * Get a list of currently active tabs
 */
export function getTabs(organization) {
    var tabs = [
        [
            Query.UNRESOLVED,
            {
                name: t('All Unresolved'),
                analyticsName: 'unresolved',
                count: true,
                enabled: true,
                tooltipTitle: t("All unresolved issues."),
            },
        ],
        [
            Query.FOR_REVIEW,
            {
                name: t('For Review'),
                analyticsName: 'needs_review',
                count: true,
                enabled: true,
                tooltipTitle: t("Unresolved issues that are new or have reopened. Review, ignore,\n        or resolve an issue to move it out of this list. After 7 days these\n        issues are automatically marked as reviewed."),
            },
        ],
        [
            Query.IGNORED,
            {
                name: t('Ignored'),
                analyticsName: 'ignored',
                count: true,
                enabled: true,
                tooltipTitle: t("Ignored issues don\u2019t trigger alerts. When their ignore\n        conditions are met they become Unresolved and are flagged for review."),
            },
        ],
        [
            Query.REPROCESSING,
            {
                name: t('Reprocessing'),
                analyticsName: 'reprocessing',
                count: true,
                enabled: organization.features.includes('reprocessing-v2'),
                tooltipTitle: tct("These [link:reprocessing issues] will take some time to complete.\n        Any new issues that are created during reprocessing will be flagged for review.", {
                    link: (<ExternalLink href="https://docs.sentry.io/product/error-monitoring/reprocessing/"/>),
                }),
                tooltipHoverable: true,
            },
        ],
    ];
    return tabs.filter(function (_a) {
        var _b = __read(_a, 2), _query = _b[0], tab = _b[1];
        return tab.enabled;
    });
}
/**
 * @returns queries that should have counts fetched
 */
export function getTabsWithCounts(organization) {
    var tabs = getTabs(organization);
    return tabs.filter(function (_a) {
        var _b = __read(_a, 2), _query = _b[0], tab = _b[1];
        return tab.count;
    }).map(function (_a) {
        var _b = __read(_a, 1), query = _b[0];
        return query;
    });
}
export function isForReviewQuery(query) {
    return !!query && /\bis:for_review\b/.test(query);
}
// the tab counts will look like 99+
export var TAB_MAX_COUNT = 99;
export var IssueSortOptions;
(function (IssueSortOptions) {
    IssueSortOptions["DATE"] = "date";
    IssueSortOptions["NEW"] = "new";
    IssueSortOptions["PRIORITY"] = "priority";
    IssueSortOptions["FREQ"] = "freq";
    IssueSortOptions["USER"] = "user";
    IssueSortOptions["TREND"] = "trend";
    IssueSortOptions["INBOX"] = "inbox";
})(IssueSortOptions || (IssueSortOptions = {}));
export function getSortLabel(key) {
    switch (key) {
        case IssueSortOptions.NEW:
            return t('First Seen');
        case IssueSortOptions.PRIORITY:
            return t('Priority');
        case IssueSortOptions.FREQ:
            return t('Events');
        case IssueSortOptions.USER:
            return t('Users');
        case IssueSortOptions.TREND:
            return t('Relative Change');
        case IssueSortOptions.INBOX:
            return t('Date Added');
        case IssueSortOptions.DATE:
        default:
            return t('Last Seen');
    }
}
//# sourceMappingURL=utils.jsx.map
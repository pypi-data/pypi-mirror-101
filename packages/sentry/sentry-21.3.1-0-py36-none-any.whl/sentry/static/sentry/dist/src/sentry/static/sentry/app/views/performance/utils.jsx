import { __assign } from "tslib";
import React from 'react';
import Duration from 'app/components/duration';
import { defined } from 'app/utils';
import { statsPeriodToDays } from 'app/utils/dates';
import getCurrentSentryReactTransaction from 'app/utils/getCurrentSentryReactTransaction';
import { decodeScalar } from 'app/utils/queryString';
import { FilterViews } from './landing';
export function getPerformanceLandingUrl(organization) {
    return "/organizations/" + organization.slug + "/performance/";
}
export function getTransactionSearchQuery(location, query) {
    if (query === void 0) { query = ''; }
    return decodeScalar(location.query.query, query).trim();
}
export function getCurrentPerformanceView(location) {
    var currentView = location.query.view;
    if (Object.values(FilterViews).includes(currentView)) {
        return currentView;
    }
    return FilterViews.ALL_TRANSACTIONS;
}
export function getTransactionDetailsUrl(organization, eventSlug, transaction, query) {
    return {
        pathname: "/organizations/" + organization.slug + "/performance/" + eventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
export function getTransactionComparisonUrl(_a) {
    var organization = _a.organization, baselineEventSlug = _a.baselineEventSlug, regressionEventSlug = _a.regressionEventSlug, transaction = _a.transaction, query = _a.query;
    return {
        pathname: "/organizations/" + organization.slug + "/performance/compare/" + baselineEventSlug + "/" + regressionEventSlug + "/",
        query: __assign(__assign({}, query), { transaction: transaction }),
    };
}
export function addRoutePerformanceContext(selection) {
    var transaction = getCurrentSentryReactTransaction();
    var days = statsPeriodToDays(selection.datetime.period, selection.datetime.start, selection.datetime.end);
    var oneDay = 86400;
    var seconds = Math.floor(days * oneDay);
    transaction === null || transaction === void 0 ? void 0 : transaction.setTag('query.period', seconds.toString());
    var groupedPeriod = '>30d';
    if (seconds <= oneDay)
        groupedPeriod = '<=1d';
    else if (seconds <= oneDay * 7)
        groupedPeriod = '<=7d';
    else if (seconds <= oneDay * 14)
        groupedPeriod = '<=14d';
    else if (seconds <= oneDay * 30)
        groupedPeriod = '<=30d';
    transaction === null || transaction === void 0 ? void 0 : transaction.setTag('query.period.grouped', groupedPeriod);
}
export function getTransactionName(location) {
    var transaction = location.query.transaction;
    return decodeScalar(transaction);
}
var hasMilliseconds = function (props) {
    return defined(props.milliseconds);
};
export function PerformanceDuration(props) {
    var normalizedSeconds = hasMilliseconds(props)
        ? props.milliseconds / 1000
        : props.seconds;
    return (<Duration seconds={normalizedSeconds} fixedDigits={normalizedSeconds > 1 ? 2 : 0}/>);
}
//# sourceMappingURL=utils.jsx.map
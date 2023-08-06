import { __assign, __rest } from "tslib";
import EventView from 'app/utils/discover/eventView';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { Dataset } from 'app/views/settings/incidentRules/types';
/**
 * Gets the URL for a discover view of the rule with the following default
 * parameters:
 *
 * - Ordered by the rule aggregate, descending
 * - yAxis maps to the aggregate
 * - The following fields are displayed:
 *   - For Error dataset alert rules: [issue, count(), count_unique(user)]
 *   - For Transaction dataset alert rules: [transaction, count()]
 * - Start and end are the period's values selected in the chart header
 */
export function getIncidentRuleDiscoverUrl(opts) {
    var _a;
    var orgSlug = opts.orgSlug, projects = opts.projects, rule = opts.rule, start = opts.start, end = opts.end, extraQueryParams = opts.extraQueryParams;
    if (!projects || !projects.length || !rule || (!start && !end)) {
        return '';
    }
    var timeWindowString = rule.timeWindow + "m";
    var discoverQuery = __assign({ id: undefined, name: (rule && rule.name) || '', orderby: "-" + getAggregateAlias(rule.aggregate), yAxis: rule.aggregate, query: (_a = rule === null || rule === void 0 ? void 0 : rule.query) !== null && _a !== void 0 ? _a : '', projects: projects
            .filter(function (_a) {
            var slug = _a.slug;
            return rule.projects.includes(slug);
        })
            .map(function (_a) {
            var id = _a.id;
            return Number(id);
        }), version: 2, fields: rule.dataset === Dataset.ERRORS
            ? ['issue', 'count()', 'count_unique(user)']
            : ['transaction', rule.aggregate], start: start,
        end: end }, extraQueryParams);
    var discoverView = EventView.fromSavedQuery(discoverQuery);
    var _b = discoverView.getResultsViewUrlTarget(orgSlug), query = _b.query, toObject = __rest(_b, ["query"]);
    return __assign({ query: __assign(__assign({}, query), { interval: timeWindowString }) }, toObject);
}
//# sourceMappingURL=getIncidentRuleDiscoverUrl.jsx.map
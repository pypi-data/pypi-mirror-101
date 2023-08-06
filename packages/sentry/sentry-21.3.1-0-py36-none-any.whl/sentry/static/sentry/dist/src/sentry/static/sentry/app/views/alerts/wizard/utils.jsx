var _a;
import { __read } from "tslib";
import { Dataset } from 'app/views/settings/incidentRules/types';
// A set of unique identifiers to be able to tie aggregate and dataset back to a wizard alert type
var alertTypeIdentifiers = (_a = {},
    _a[Dataset.ERRORS] = {
        num_errors: 'count()',
        users_experiencing_errors: 'count_unique(tags[sentry:user])',
    },
    _a[Dataset.TRANSACTIONS] = {
        throughput: 'count()',
        trans_duration: 'transaction.duration',
        apdex: 'apdex',
        failure_rate: 'failure_rate()',
        lcp: 'measurements.lcp',
        fid: 'measurements.fid',
        cls: 'measurements.cls',
        fcp: 'measurements.fcp',
    },
    _a);
/**
 * Given an aggregate and dataset object, will return the corresponding wizard alert type
 * e.g. {aggregate: 'count()', dataset: 'events'} will yield 'num_errors'
 * @param template
 */
export function getAlertTypeFromAggregateDataset(_a) {
    var aggregate = _a.aggregate, dataset = _a.dataset;
    var identifierForDataset = alertTypeIdentifiers[dataset];
    var matchingAlertTypeEntry = Object.entries(identifierForDataset).find(function (_a) {
        var _b = __read(_a, 2), _alertType = _b[0], identifier = _b[1];
        return identifier && aggregate.includes(identifier);
    });
    var alertType = matchingAlertTypeEntry && matchingAlertTypeEntry[0];
    return alertType ? alertType : 'custom';
}
//# sourceMappingURL=utils.jsx.map
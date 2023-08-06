import { convertDatasetEventTypesToSource } from 'app/views/alerts/utils';
import { DATASET_EVENT_TYPE_FILTERS, DATASOURCE_EVENT_TYPE_FILTERS } from '../constants';
import { Dataset, Datasource } from '../types';
export function extractEventTypeFilterFromRule(metricRule) {
    var dataset = metricRule.dataset, eventTypes = metricRule.eventTypes;
    return getEventTypeFilter(dataset, eventTypes);
}
export function getEventTypeFilter(dataset, eventTypes) {
    var _a;
    if (eventTypes) {
        return DATASOURCE_EVENT_TYPE_FILTERS[(_a = convertDatasetEventTypesToSource(dataset, eventTypes)) !== null && _a !== void 0 ? _a : Datasource.ERROR];
    }
    else {
        return DATASET_EVENT_TYPE_FILTERS[dataset !== null && dataset !== void 0 ? dataset : Dataset.ERRORS];
    }
}
//# sourceMappingURL=getEventTypeFilter.jsx.map
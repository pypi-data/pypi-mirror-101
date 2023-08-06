import cloneDeep from 'lodash/cloneDeep';
import { getUtcDateString } from 'app/utils/dates';
import EventView from 'app/utils/discover/eventView';
export function cloneDashboard(dashboard) {
    return cloneDeep(dashboard);
}
export function eventViewFromWidget(title, query, selection) {
    var _a = selection.datetime, start = _a.start, end = _a.end, statsPeriod = _a.period;
    var projects = selection.projects;
    return EventView.fromSavedQuery({
        id: undefined,
        name: title,
        version: 2,
        fields: query.fields,
        query: query.conditions,
        orderby: query.orderby,
        projects: projects,
        range: statsPeriod,
        start: start ? getUtcDateString(start) : undefined,
        end: end ? getUtcDateString(end) : undefined,
    });
}
//# sourceMappingURL=utils.jsx.map
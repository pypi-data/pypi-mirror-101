import { canIncludePreviousPeriod } from 'app/components/charts/utils';
export function shouldFetchPreviousPeriod(datetime) {
    var start = datetime.start, end = datetime.end, period = datetime.period;
    return !start && !end && canIncludePreviousPeriod(true, period);
}
export function didProjectOrEnvironmentChange(location1, location2) {
    return (location1.query.environment !== location2.query.environment ||
        location1.query.project !== location2.query.project);
}
//# sourceMappingURL=utils.jsx.map
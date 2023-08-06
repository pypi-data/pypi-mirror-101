import round from 'lodash/round';
import { tn } from 'app/locale';
import { ReleaseStatus } from 'app/types';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import { DisplayOption } from '../list/utils';
export var roundDuration = function (seconds) {
    return round(seconds, seconds > 60 ? 0 : 3);
};
export var getCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = 95; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    return round(percent, percent > decimalThreshold ? decimalPlaces : 0);
};
export var displayCrashFreePercent = function (percent, decimalThreshold, decimalPlaces) {
    if (decimalThreshold === void 0) { decimalThreshold = 95; }
    if (decimalPlaces === void 0) { decimalPlaces = 3; }
    if (isNaN(percent)) {
        return '\u2015';
    }
    if (percent < 1 && percent > 0) {
        return "<1%";
    }
    var rounded = getCrashFreePercent(percent, decimalThreshold, decimalPlaces).toLocaleString();
    return rounded + "%";
};
export var getReleaseNewIssuesUrl = function (orgSlug, projectId, version) {
    return {
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId,
            // we are resetting time selector because releases' new issues count doesn't take time selector into account
            statsPeriod: undefined,
            start: undefined,
            end: undefined,
            query: stringifyQueryObject(new QueryResults(["firstRelease:" + version])),
        },
    };
};
export var getReleaseUnhandledIssuesUrl = function (orgSlug, projectId, version) {
    return {
        pathname: "/organizations/" + orgSlug + "/issues/",
        query: {
            project: projectId,
            query: stringifyQueryObject(new QueryResults(["release:" + version, 'error.unhandled:true'])),
        },
    };
};
export var isReleaseArchived = function (release) {
    return release.status === ReleaseStatus.Archived;
};
export function releaseDisplayLabel(displayOption, count) {
    if (displayOption === DisplayOption.USERS) {
        return tn('user', 'users', count);
    }
    return tn('session', 'sessions', count);
}
//# sourceMappingURL=index.jsx.map
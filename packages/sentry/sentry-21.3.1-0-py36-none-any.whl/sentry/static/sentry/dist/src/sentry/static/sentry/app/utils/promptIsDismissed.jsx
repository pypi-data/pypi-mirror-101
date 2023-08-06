import { snoozedDays } from './promptsActivity';
export var promptIsDismissed = function (prompt, daysToSnooze) {
    if (daysToSnooze === void 0) { daysToSnooze = 14; }
    var _a = prompt || {}, snoozedTime = _a.snoozedTime, dismissedTime = _a.dismissedTime;
    // check if the prompt has been dismissed
    if (dismissedTime) {
        return true;
    }
    //check if it has been snoozed
    return !snoozedTime ? false : snoozedDays(snoozedTime) < daysToSnooze;
};
//# sourceMappingURL=promptIsDismissed.jsx.map
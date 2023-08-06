var _a;
import { t } from 'app/locale';
import { TimePeriod, TimeWindow } from 'app/views/settings/incidentRules/types';
export var TIME_OPTIONS = [
    { label: t('Last 6 hours'), value: TimePeriod.SIX_HOURS },
    { label: t('Last 24 hours'), value: TimePeriod.ONE_DAY },
    { label: t('Last 3 days'), value: TimePeriod.THREE_DAYS },
    { label: t('Last 7 days'), value: TimePeriod.SEVEN_DAYS },
];
export var ALERT_RULE_DETAILS_DEFAULT_PERIOD = TimePeriod.ONE_DAY;
export var TIME_WINDOWS = (_a = {},
    _a[TimePeriod.SIX_HOURS] = TimeWindow.ONE_HOUR * 6 * 60 * 1000,
    _a[TimePeriod.ONE_DAY] = TimeWindow.ONE_DAY * 60 * 1000,
    _a[TimePeriod.THREE_DAYS] = TimeWindow.ONE_DAY * 3 * 60 * 1000,
    _a[TimePeriod.SEVEN_DAYS] = TimeWindow.ONE_DAY * 7 * 60 * 1000,
    _a);
export var API_INTERVAL_POINTS_LIMIT = 10000;
export var API_INTERVAL_POINTS_MIN = 150;
//# sourceMappingURL=constants.jsx.map
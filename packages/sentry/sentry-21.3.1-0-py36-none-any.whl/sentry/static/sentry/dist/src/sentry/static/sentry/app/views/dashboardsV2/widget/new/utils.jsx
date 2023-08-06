var _a;
import { t } from 'app/locale';
import { DisplayType } from '../../types';
export var visualizationColors = [{ label: t('Default Color'), value: 'purple' }];
export var metrics = [
    'sentry.response',
    'sentry.events.failed',
    'sentry.events.processed',
    'sentry.events.processed.javascript',
    'sentry.events.processed.java',
    'sentry.events.processed.node',
    'symbolicator.healthcheck',
];
export var metricTags = {
    browser: { values: [], key: 'browser', name: 'Browser', value: 'Chrome 89.0.4389' },
    'browser.name': {
        values: [],
        name: 'Browser.Name',
        key: 'browser.name',
        value: 'Chrome',
    },
    'device.family': {
        values: [],
        name: 'Device.Family',
        key: 'device.family',
        value: 'Mac',
    },
    environment: { values: [], name: 'Environment', key: 'environment', value: 'prod' },
    'http.status_code': {
        values: [],
        name: 'Http.Status_Code',
        key: 'http.status_code',
        value: '200',
    },
};
export var metricGroupByOptions = [
    ['status.code', 'status.code'],
    ['method', 'method'],
];
// The aggregation method chosen determines how the metrics are aggregated into a single line
export var Aggregation;
(function (Aggregation) {
    Aggregation["COUNTER"] = "counter";
    Aggregation["DISTRIBUTION"] = "distribution";
    Aggregation["SET"] = "set";
    Aggregation["GAUGE"] = "gauge";
})(Aggregation || (Aggregation = {}));
export var displayTypes = (_a = {},
    _a[DisplayType.AREA] = t('Area Chart'),
    _a[DisplayType.BAR] = t('Bar Chart'),
    _a[DisplayType.LINE] = t('Line Chart'),
    _a[DisplayType.TABLE] = t('Table'),
    _a[DisplayType.WORLD_MAP] = t('World Map'),
    _a[DisplayType.BIG_NUMBER] = t('Big Number'),
    _a);
//# sourceMappingURL=utils.jsx.map
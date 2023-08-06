import React from 'react';
import OptionSelector from 'app/components/charts/optionSelector';
import { ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import QuestionTooltip from 'app/components/questionTooltip';
import NOT_AVAILABLE_MESSAGES from 'app/constants/notAvailableMessages';
import { t } from 'app/locale';
import { WebVital } from 'app/utils/discover/fields';
import { WEB_VITAL_DETAILS } from 'app/utils/performance/vitals/constants';
export var YAxis;
(function (YAxis) {
    YAxis["SESSIONS"] = "sessions";
    YAxis["USERS"] = "users";
    YAxis["CRASH_FREE"] = "crashFree";
    YAxis["SESSION_DURATION"] = "sessionDuration";
    YAxis["EVENTS"] = "events";
    YAxis["FAILED_TRANSACTIONS"] = "failedTransactions";
    YAxis["COUNT_DURATION"] = "countDuration";
    YAxis["COUNT_VITAL"] = "countVital";
})(YAxis || (YAxis = {}));
export var EventType;
(function (EventType) {
    EventType["ALL"] = "all";
    EventType["CSP"] = "csp";
    EventType["DEFAULT"] = "default";
    EventType["ERROR"] = "error";
    EventType["TRANSACTION"] = "transaction";
})(EventType || (EventType = {}));
export var PERFORMANCE_AXIS = [
    YAxis.FAILED_TRANSACTIONS,
    YAxis.COUNT_DURATION,
    YAxis.COUNT_VITAL,
];
var ReleaseChartControls = function (_a) {
    var summary = _a.summary, yAxis = _a.yAxis, onYAxisChange = _a.onYAxisChange, organization = _a.organization, hasHealthData = _a.hasHealthData, hasDiscover = _a.hasDiscover, hasPerformance = _a.hasPerformance, _b = _a.eventType, eventType = _b === void 0 ? EventType.ALL : _b, onEventTypeChange = _a.onEventTypeChange, _c = _a.vitalType, vitalType = _c === void 0 ? WebVital.LCP : _c, onVitalTypeChange = _a.onVitalTypeChange;
    var noHealthDataTooltip = !hasHealthData
        ? NOT_AVAILABLE_MESSAGES.releaseHealth
        : undefined;
    var noDiscoverTooltip = !hasDiscover ? NOT_AVAILABLE_MESSAGES.discover : undefined;
    var noPerformanceTooltip = !hasPerformance
        ? NOT_AVAILABLE_MESSAGES.performance
        : undefined;
    var yAxisOptions = [
        {
            value: YAxis.SESSIONS,
            label: t('Session Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.SESSION_DURATION,
            label: t('Session Duration'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.USERS,
            label: t('User Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.CRASH_FREE,
            label: t('Crash Free Rate'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.FAILED_TRANSACTIONS,
            label: t('Failure Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.COUNT_DURATION,
            label: t('Slow Duration Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.COUNT_VITAL,
            label: t('Slow Vital Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.EVENTS,
            label: t('Event Count'),
            disabled: !hasDiscover && !hasPerformance,
            tooltip: noDiscoverTooltip,
        },
    ];
    var getSummaryHeading = function () {
        switch (yAxis) {
            case YAxis.USERS:
                return t('Total Active Users');
            case YAxis.CRASH_FREE:
                return t('Average Rate');
            case YAxis.SESSION_DURATION:
                return t('Median Duration');
            case YAxis.EVENTS:
                return t('Total Events');
            case YAxis.FAILED_TRANSACTIONS:
                return t('Failed Transactions');
            case YAxis.COUNT_DURATION:
                return t('Count over %sms', organization.apdexThreshold);
            case YAxis.COUNT_VITAL:
                return vitalType !== WebVital.CLS
                    ? t('Count over %sms', WEB_VITAL_DETAILS[vitalType].poorThreshold)
                    : t('Count over %s', WEB_VITAL_DETAILS[vitalType].poorThreshold);
            case YAxis.SESSIONS:
            default:
                return t('Total Sessions');
        }
    };
    return (<ChartControls>
      <InlineContainer>
        <SectionHeading key="total-label">{getSummaryHeading()}</SectionHeading>
        <SectionValue key="total-value">{summary}</SectionValue>
        <QuestionTooltip position="top" size="sm" title={t('This value includes only the current release.')}/>
      </InlineContainer>
      <InlineContainer>
        <SecondarySelector yAxis={yAxis} eventType={eventType} onEventTypeChange={onEventTypeChange} vitalType={vitalType} onVitalTypeChange={onVitalTypeChange}/>
        <OptionSelector title={t('Display')} selected={yAxis} options={yAxisOptions} onChange={onYAxisChange}/>
      </InlineContainer>
    </ChartControls>);
};
var eventTypeOptions = [
    { value: EventType.ALL, label: t('All') },
    { value: EventType.CSP, label: t('CSP') },
    { value: EventType.DEFAULT, label: t('Default') },
    { value: EventType.ERROR, label: 'Error' },
    { value: EventType.TRANSACTION, label: t('Transaction') },
];
var vitalTypeOptions = [
    WebVital.FP,
    WebVital.FCP,
    WebVital.LCP,
    WebVital.FID,
    WebVital.CLS,
].map(function (vital) { return ({ value: vital, label: WEB_VITAL_DETAILS[vital].name }); });
function SecondarySelector(_a) {
    var yAxis = _a.yAxis, eventType = _a.eventType, onEventTypeChange = _a.onEventTypeChange, vitalType = _a.vitalType, onVitalTypeChange = _a.onVitalTypeChange;
    switch (yAxis) {
        case YAxis.EVENTS:
            return (<OptionSelector title={t('Event Type')} selected={eventType} options={eventTypeOptions} onChange={onEventTypeChange}/>);
        case YAxis.COUNT_VITAL:
            return (<OptionSelector title={t('Vital')} selected={vitalType} options={vitalTypeOptions} onChange={onVitalTypeChange}/>);
        default:
            return null;
    }
}
export default ReleaseChartControls;
//# sourceMappingURL=releaseChartControls.jsx.map
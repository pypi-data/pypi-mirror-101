export var DynamicSamplingRuleType;
(function (DynamicSamplingRuleType) {
    /**
     * The rule applies to traces (transaction events considered in the context of a trace)
     */
    DynamicSamplingRuleType["TRACE"] = "trace";
    /**
     *  The rule applies to transaction events considered independently
     */
    DynamicSamplingRuleType["TRANSACTION"] = "transaction";
    /**
     * The rule applies to error events (not transaction events)
     */
    DynamicSamplingRuleType["ERROR"] = "error";
})(DynamicSamplingRuleType || (DynamicSamplingRuleType = {}));
export var DynamicSamplingConditionOperator;
(function (DynamicSamplingConditionOperator) {
    /**
     * The not combinator has a similar structure with the only difference that "inner" is not an array
     * and contains directly the negated condition
     */
    DynamicSamplingConditionOperator["NOT"] = "not";
    /**
     * Combine multiple sub-conditions with the operator 'or'
     */
    DynamicSamplingConditionOperator["OR"] = "or";
    /**
     * Combine multiple sub-conditions with the operator 'and'
     */
    DynamicSamplingConditionOperator["AND"] = "and";
})(DynamicSamplingConditionOperator || (DynamicSamplingConditionOperator = {}));
export var DynamicSamplingInnerOperator;
(function (DynamicSamplingInnerOperator) {
    /**
     * It uses glob matches for checking (e.g. releases use glob matching "1.1.*" will match release 1.1.1 and 1.1.2)
     */
    DynamicSamplingInnerOperator["GLOB_MATCH"] = "glob";
    /**
     * It uses simple equality for checking
     */
    DynamicSamplingInnerOperator["EQUAL"] = "eq";
    /**
     * Custom Operation
     */
    DynamicSamplingInnerOperator["CUSTOM"] = "custom";
})(DynamicSamplingInnerOperator || (DynamicSamplingInnerOperator = {}));
export var DynamicSamplingInnerName;
(function (DynamicSamplingInnerName) {
    DynamicSamplingInnerName["TRACE_RELEASE"] = "trace.release";
    DynamicSamplingInnerName["TRACE_ENVIRONMENT"] = "trace.environment";
    DynamicSamplingInnerName["TRACE_USER_ID"] = "trace.user.id";
    DynamicSamplingInnerName["TRACE_USER_SEGMENT"] = "trace.user.segment";
    DynamicSamplingInnerName["EVENT_RELEASE"] = "event.release";
    DynamicSamplingInnerName["EVENT_ENVIRONMENT"] = "event.environment";
    DynamicSamplingInnerName["EVENT_USER_ID"] = "event.user.id";
    DynamicSamplingInnerName["EVENT_USER_SEGMENT"] = "event.user.segment";
    DynamicSamplingInnerName["EVENT_LOCALHOST"] = "event.is_local_ip";
    DynamicSamplingInnerName["EVENT_WEB_CRAWLERS"] = "event.web_crawlers";
    DynamicSamplingInnerName["EVENT_BROWSER_EXTENSIONS"] = "event.has_bad_browser_extensions";
    DynamicSamplingInnerName["EVENT_LEGACY_BROWSER"] = "event.legacy_browser";
})(DynamicSamplingInnerName || (DynamicSamplingInnerName = {}));
export var LegacyBrowser;
(function (LegacyBrowser) {
    LegacyBrowser["IE_PRE_9"] = "ie_pre_9";
    LegacyBrowser["IE9"] = "ie9";
    LegacyBrowser["IE10"] = "ie10";
    LegacyBrowser["IE11"] = "ie11";
    LegacyBrowser["SAFARI_PRE_6"] = "safari_pre_6";
    LegacyBrowser["OPERA_PRE_15"] = "opera_pre_15";
    LegacyBrowser["OPERA_MINI_PRE_8"] = "opera_mini_pre_8";
    LegacyBrowser["ANDROID_PRE_4"] = "android_pre_4";
})(LegacyBrowser || (LegacyBrowser = {}));
//# sourceMappingURL=dynamicSampling.jsx.map
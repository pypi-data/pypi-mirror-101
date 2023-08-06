import { __assign } from "tslib";
import * as qs from 'query-string';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { growthEventMap } from 'app/utils/growthAnalyticsEvents';
import { uniqueId } from 'app/utils/guid';
import { integrationEventMap, } from 'app/utils/integrationEvents';
var ANALYTICS_SESSION = 'ANALYTICS_SESSION';
export var startAnalyticsSession = function () {
    var sessionId = uniqueId();
    window.sessionStorage.setItem(ANALYTICS_SESSION, sessionId);
    return sessionId;
};
export var clearAnalyticsSession = function () {
    window.sessionStorage.removeItem(ANALYTICS_SESSION);
};
export var getAnalyticsSessionId = function () {
    return window.sessionStorage.getItem(ANALYTICS_SESSION);
};
var hasAnalyticsDebug = function () { return window.localStorage.getItem('DEBUG_ANALYTICS') === '1'; };
var allEventMap = __assign(__assign({}, integrationEventMap), growthEventMap);
/**
 * Tracks an event for analytics.
 * Must be tied to an organization.
 * Uses the current session ID or generates a new one if startSession == true.
 * An analytics session corresponds to a single action funnel such as installation.
 * Tracking by session allows us to track individual funnel attempts for a single user.
 */
export function trackAdvancedAnalyticsEvent(eventKey, analyticsParams, org, //we should pass in org whenever we can but not every place guarantees this
options, mapValuesFn) {
    try {
        var startSession = (options || {}).startSession;
        var sessionId = startSession ? startAnalyticsSession() : getAnalyticsSessionId();
        var eventName = allEventMap[eventKey];
        //we should always have a session id but if we don't, we should generate one
        if (hasAnalyticsDebug() && !sessionId) {
            // eslint-disable-next-line no-console
            console.warn("analytics_session_id absent from event " + eventKey);
            sessionId = startAnalyticsSession();
        }
        var custom_referrer = void 0;
        try {
            //pull the referrer from the query parameter of the page
            var referrer = (qs.parse(window.location.search) || {}).referrer;
            if (typeof referrer === 'string') {
                // Amplitude has its own referrer which inteferes with our custom referrer
                custom_referrer = referrer;
            }
        }
        catch (_a) {
            // ignore if this fails to parse
            // this can happen if we have an invalid query string
            // e.g. unencoded "%"
        }
        var params = __assign({ eventKey: eventKey,
            eventName: eventName, analytics_session_id: sessionId, organization_id: org === null || org === void 0 ? void 0 : org.id, role: org === null || org === void 0 ? void 0 : org.role, custom_referrer: custom_referrer }, analyticsParams);
        if (mapValuesFn) {
            params = mapValuesFn(params);
        }
        //TODO(steve): remove once we pass in org always
        if (hasAnalyticsDebug() && !org) {
            // eslint-disable-next-line no-console
            console.warn("Organization absent from event " + eventKey);
        }
        //could put this into a debug method or for the main trackAnalyticsEvent event
        if (hasAnalyticsDebug()) {
            // eslint-disable-next-line no-console
            console.log('trackAdvancedAnalytics', params);
        }
        trackAnalyticsEvent(params);
    }
    catch (e) {
        // eslint-disable-next-line no-console
        console.error('Error tracking analytics event', e);
    }
}
//# sourceMappingURL=advancedAnalytics.jsx.map
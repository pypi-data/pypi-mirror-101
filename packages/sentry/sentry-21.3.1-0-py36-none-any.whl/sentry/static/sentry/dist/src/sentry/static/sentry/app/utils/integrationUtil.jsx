import { __assign, __read, __spreadArray } from "tslib";
import React from 'react';
import capitalize from 'lodash/capitalize';
import * as qs from 'query-string';
import { IconBitbucket, IconGeneric, IconGithub, IconGitlab, IconJira, IconVsts, } from 'app/icons';
import HookStore from 'app/stores/hookStore';
import { trackAdvancedAnalyticsEvent } from 'app/utils/advancedAnalytics';
var mapIntegrationParams = function (analyticsParams) {
    //Reload expects integration_status even though it's not relevant for non-sentry apps
    //Passing in a dummy value of published in those cases
    var fullParams = __assign({}, analyticsParams);
    if (analyticsParams.integration && analyticsParams.integration_type !== 'sentry_app') {
        fullParams.integration_status = 'published';
    }
    return fullParams;
};
//wrapper around trackAdvancedAnalyticsEvent which has some extra
//data massaging above
export function trackIntegrationEvent(eventKey, analyticsParams, org, options) {
    return trackAdvancedAnalyticsEvent(eventKey, analyticsParams, org, options, mapIntegrationParams);
}
/**
 * In sentry.io the features list supports rendering plan details. If the hook
 * is not registered for rendering the features list like this simply show the
 * features as a normal list.
 */
var generateFeaturesList = function (p) { return (<ul>
    {p.features.map(function (f, i) { return (<li key={i}>{f.description}</li>); })}
  </ul>); };
var generateIntegrationFeatures = function (p) {
    return p.children({
        disabled: false,
        disabledReason: null,
        ungatedFeatures: p.features,
        gatedFeatureGroups: [],
    });
};
var defaultFeatureGateComponents = {
    IntegrationFeatures: generateIntegrationFeatures,
    IntegrationDirectoryFeatures: generateIntegrationFeatures,
    FeatureList: generateFeaturesList,
    IntegrationDirectoryFeatureList: generateFeaturesList,
};
export var getIntegrationFeatureGate = function () {
    var defaultHook = function () { return defaultFeatureGateComponents; };
    var featureHook = HookStore.get('integrations:feature-gates')[0] || defaultHook;
    return featureHook();
};
export var getSentryAppInstallStatus = function (install) {
    if (install) {
        return capitalize(install.status);
    }
    return 'Not Installed';
};
export var getCategories = function (features) {
    var transform = features.map(function (_a) {
        var featureGate = _a.featureGate;
        var feature = featureGate
            .replace(/integrations/g, '')
            .replace(/-/g, ' ')
            .trim();
        switch (feature) {
            case 'actionable notification':
                return 'notification action';
            case 'issue basic':
            case 'issue link':
            case 'issue sync':
                return 'project management';
            case 'commits':
                return 'source code management';
            case 'chat unfurl':
                return 'chat';
            default:
                return feature;
        }
    });
    return __spreadArray([], __read(new Set(transform)));
};
export var getCategoriesForIntegration = function (integration) {
    if (isSentryApp(integration)) {
        return ['internal', 'unpublished'].includes(integration.status)
            ? [integration.status]
            : getCategories(integration.featureData);
    }
    if (isPlugin(integration)) {
        return getCategories(integration.featureDescriptions);
    }
    if (isDocumentIntegration(integration)) {
        return getCategories(integration.features);
    }
    return getCategories(integration.metadata.features);
};
export function isSentryApp(integration) {
    return !!integration.uuid;
}
export function isPlugin(integration) {
    return integration.hasOwnProperty('shortName');
}
export function isDocumentIntegration(integration) {
    return integration.hasOwnProperty('docUrl');
}
export var getIntegrationType = function (integration) {
    if (isSentryApp(integration)) {
        return 'sentry_app';
    }
    if (isPlugin(integration)) {
        return 'plugin';
    }
    if (isDocumentIntegration(integration)) {
        return 'document';
    }
    return 'first_party';
};
export var convertIntegrationTypeToSnakeCase = function (type) {
    switch (type) {
        case 'firstParty':
            return 'first_party';
        case 'sentryApp':
            return 'sentry_app';
        case 'documentIntegration':
            return 'document';
        default:
            return type;
    }
};
export var safeGetQsParam = function (param) {
    try {
        var query = qs.parse(window.location.search) || {};
        return query[param];
    }
    catch (_a) {
        return undefined;
    }
};
export var getIntegrationIcon = function (integrationType, size) {
    var iconSize = size || 'md';
    switch (integrationType) {
        case 'bitbucket':
            return <IconBitbucket size={iconSize}/>;
        case 'gitlab':
            return <IconGitlab size={iconSize}/>;
        case 'github':
        case 'github_enterprise':
            return <IconGithub size={iconSize}/>;
        case 'jira':
        case 'jira_server':
            return <IconJira size={iconSize}/>;
        case 'vsts':
            return <IconVsts size={iconSize}/>;
        default:
            return <IconGeneric size={iconSize}/>;
    }
};
//used for project creation and onboarding
//determines what integration maps to what project platform
export var platfromToIntegrationMap = {
    'node-awslambda': 'aws_lambda',
    'python-awslambda': 'aws_lambda',
};
//# sourceMappingURL=integrationUtil.jsx.map
var _a;
import { __makeTemplateObject } from "tslib";
import { css } from '@emotion/core';
import { t } from 'app/locale';
import { DynamicSamplingInnerName, LegacyBrowser } from 'app/types/dynamicSampling';
import theme from 'app/utils/theme';
export var modalCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 95%;\n      margin-left: -47.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 75%;\n      margin-left: -37.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 65%;\n      margin-left: -37.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 55%;\n      margin-left: -27.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 45%;\n      margin-left: -22.5%;\n    }\n  }\n"], ["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 95%;\n      margin-left: -47.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 75%;\n      margin-left: -37.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 65%;\n      margin-left: -37.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 55%;\n      margin-left: -27.5%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 45%;\n      margin-left: -22.5%;\n    }\n  }\n"])), theme.breakpoints[0], theme.breakpoints[1], theme.breakpoints[2], theme.breakpoints[3], theme.breakpoints[4]);
export var LEGACY_BROWSER_LIST = (_a = {},
    _a[LegacyBrowser.IE_PRE_9] = {
        icon: 'internet-explorer',
        title: t('Internet Explorer Version 8 and lower'),
    },
    _a[LegacyBrowser.IE9] = {
        icon: 'internet-explorer',
        title: t('Internet Explorer Version 9'),
    },
    _a[LegacyBrowser.IE10] = {
        icon: 'internet-explorer',
        title: t('Internet Explorer Version 10'),
    },
    _a[LegacyBrowser.IE11] = {
        icon: 'internet-explorer',
        title: t('Internet Explorer Version 11'),
    },
    _a[LegacyBrowser.SAFARI_PRE_6] = {
        icon: 'safari',
        title: t('Safari Version 5 and lower'),
    },
    _a[LegacyBrowser.OPERA_PRE_15] = {
        icon: 'opera',
        title: t('Opera Version 14 and lower'),
    },
    _a[LegacyBrowser.OPERA_MINI_PRE_8] = {
        icon: 'opera',
        title: t('Opera Mini Version 8 and lower'),
    },
    _a[LegacyBrowser.ANDROID_PRE_4] = {
        icon: 'android',
        title: t('Android Version 3 and lower'),
    },
    _a);
export var Transaction;
(function (Transaction) {
    Transaction["ALL"] = "all";
    Transaction["MATCH_CONDITIONS"] = "match-conditions";
})(Transaction || (Transaction = {}));
export function isLegacyBrowser(maybe) {
    return maybe.every(function (m) { return !!LEGACY_BROWSER_LIST[m]; });
}
export function getMatchFieldPlaceholder(category) {
    switch (category) {
        case DynamicSamplingInnerName.EVENT_LEGACY_BROWSER:
            return t('Match all selected legacy browsers below');
        case DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS:
            return t('Match all browser extensions');
        case DynamicSamplingInnerName.EVENT_LOCALHOST:
            return t('Match all localhosts');
        case DynamicSamplingInnerName.EVENT_WEB_CRAWLERS:
            return t('Match all web crawlers');
        case DynamicSamplingInnerName.EVENT_USER_ID:
        case DynamicSamplingInnerName.TRACE_USER_ID:
            return t('ex. 4711 (Multiline)');
        case DynamicSamplingInnerName.EVENT_USER_SEGMENT:
        case DynamicSamplingInnerName.TRACE_USER_SEGMENT:
            return t('ex. paid, common (Multiline)');
        case DynamicSamplingInnerName.TRACE_ENVIRONMENT:
        case DynamicSamplingInnerName.EVENT_ENVIRONMENT:
            return t('ex. prod or dev (Multiline)');
        case DynamicSamplingInnerName.TRACE_RELEASE:
        case DynamicSamplingInnerName.EVENT_RELEASE:
            return t('ex. 1* or [I3].[0-9].* (Multiline)');
        default:
            return '';
    }
}
var templateObject_1;
//# sourceMappingURL=utils.jsx.map
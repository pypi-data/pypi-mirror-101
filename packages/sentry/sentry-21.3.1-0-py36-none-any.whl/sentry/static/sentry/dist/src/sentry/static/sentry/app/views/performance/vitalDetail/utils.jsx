var _a, _b, _c, _d, _e, _f, _g;
import { __values } from "tslib";
import React from 'react';
import { IconCheckmark, IconFire, IconWarning } from 'app/icons';
import { getAggregateAlias, WebVital } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
export function generateVitalDetailRoute(_a) {
    var orgSlug = _a.orgSlug;
    return "/organizations/" + orgSlug + "/performance/vitaldetail/";
}
export var webVitalPoor = (_a = {},
    _a[WebVital.FP] = 3000,
    _a[WebVital.FCP] = 3000,
    _a[WebVital.LCP] = 4000,
    _a[WebVital.FID] = 300,
    _a[WebVital.CLS] = 0.25,
    _a);
export var webVitalMeh = (_b = {},
    _b[WebVital.FP] = 1000,
    _b[WebVital.FCP] = 1000,
    _b[WebVital.LCP] = 2500,
    _b[WebVital.FID] = 100,
    _b[WebVital.CLS] = 0.1,
    _b);
export var VitalState;
(function (VitalState) {
    VitalState["POOR"] = "Poor";
    VitalState["MEH"] = "Meh";
    VitalState["GOOD"] = "Good";
})(VitalState || (VitalState = {}));
export var vitalStateColors = (_c = {},
    _c[VitalState.POOR] = 'red300',
    _c[VitalState.MEH] = 'yellow300',
    _c[VitalState.GOOD] = 'green300',
    _c);
export var vitalStateIcons = (_d = {},
    _d[VitalState.POOR] = <IconFire color={vitalStateColors[VitalState.POOR]}/>,
    _d[VitalState.MEH] = <IconWarning color={vitalStateColors[VitalState.MEH]}/>,
    _d[VitalState.GOOD] = (<IconCheckmark color={vitalStateColors[VitalState.GOOD]} isCircled/>),
    _d);
export function vitalDetailRouteWithQuery(_a) {
    var orgSlug = _a.orgSlug, vitalName = _a.vitalName, projectID = _a.projectID, query = _a.query;
    var pathname = generateVitalDetailRoute({
        orgSlug: orgSlug,
    });
    return {
        pathname: pathname,
        query: {
            vitalName: vitalName,
            project: projectID,
            environment: query.environment,
            statsPeriod: query.statsPeriod,
            start: query.start,
            end: query.end,
            query: query.query,
        },
    };
}
export function vitalNameFromLocation(location) {
    var _vitalName = decodeScalar(location.query.vitalName);
    var vitalName = Object.values(WebVital).find(function (v) { return v === _vitalName; });
    if (vitalName) {
        return vitalName;
    }
    else {
        return WebVital.LCP;
    }
}
export function getVitalDetailTablePoorStatusFunction(vitalName) {
    var vitalThreshold = webVitalPoor[vitalName];
    var statusFunction = "compare_numeric_aggregate(" + getAggregateAlias("p75(" + vitalName + ")") + ",greater," + vitalThreshold + ")";
    return statusFunction;
}
export function getVitalDetailTableMehStatusFunction(vitalName) {
    var vitalThreshold = webVitalMeh[vitalName];
    var statusFunction = "compare_numeric_aggregate(" + getAggregateAlias("p75(" + vitalName + ")") + ",greater," + vitalThreshold + ")";
    return statusFunction;
}
export var vitalMap = (_e = {},
    _e[WebVital.FCP] = 'First Contentful Paint',
    _e[WebVital.CLS] = 'Cumulative Layout Shift',
    _e[WebVital.FID] = 'First Input Delay',
    _e[WebVital.LCP] = 'Largest Contentful Paint',
    _e);
export var vitalChartTitleMap = vitalMap;
export var vitalDescription = (_f = {},
    _f[WebVital.FCP] = 'First Contentful Paint (FCP) measures the amount of time the first content takes to render in the viewport. Like FP, this could also show up in any form from the document object model (DOM), such as images, SVGs, or text blocks.',
    _f[WebVital.CLS] = 'Cumulative Layout Shift (CLS) is the sum of individual layout shift scores for every unexpected element shift during the rendering process. Imagine navigating to an article and trying to click a link before the page finishes loading. Before your cursor even gets there, the link may have shifted down due to an image rendering. Rather than using duration for this Web Vital, the CLS score represents the degree of disruptive and visually unstable shifts.',
    _f[WebVital.FID] = 'First Input Delay measures the response time when the user tries to interact with the viewport. Actions maybe include clicking a button, link or other custom Javascript controller. It is key in helping the user determine if a page is usable or not.',
    _f[WebVital.LCP] = 'Largest Contentful Paint (LCP) measures the render time for the largest content to appear in the viewport. This may be in any form from the document object model (DOM), such as images, SVGs, or text blocks. It’s the largest pixel area in the viewport, thus most visually defining. LCP helps developers understand how long it takes to see the main content on the page.',
    _f);
export var vitalAbbreviations = (_g = {},
    _g[WebVital.FCP] = 'FCP',
    _g[WebVital.CLS] = 'CLS',
    _g[WebVital.FID] = 'FID',
    _g[WebVital.LCP] = 'LCP',
    _g);
export function getMaxOfSeries(series) {
    var e_1, _a, e_2, _b;
    var max = -Infinity;
    try {
        for (var series_1 = __values(series), series_1_1 = series_1.next(); !series_1_1.done; series_1_1 = series_1.next()) {
            var data = series_1_1.value.data;
            try {
                for (var data_1 = (e_2 = void 0, __values(data)), data_1_1 = data_1.next(); !data_1_1.done; data_1_1 = data_1.next()) {
                    var point = data_1_1.value;
                    max = Math.max(max, point.value);
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (data_1_1 && !data_1_1.done && (_b = data_1.return)) _b.call(data_1);
                }
                finally { if (e_2) throw e_2.error; }
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (series_1_1 && !series_1_1.done && (_a = series_1.return)) _a.call(series_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return max;
}
//# sourceMappingURL=utils.jsx.map
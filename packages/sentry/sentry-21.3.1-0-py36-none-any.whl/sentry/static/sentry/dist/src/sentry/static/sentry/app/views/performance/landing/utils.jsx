import { __read, __spreadArray } from "tslib";
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { backend, frontend } from 'app/data/platformCategories';
import { t } from 'app/locale';
import { formatAbbreviatedNumber, formatFloat, formatPercentage, getDuration, } from 'app/utils/formatters';
import { decodeScalar } from 'app/utils/queryString';
import { getTermHelp, PERFORMANCE_TERM } from '../data';
export var LEFT_AXIS_QUERY_KEY = 'left';
export var RIGHT_AXIS_QUERY_KEY = 'right';
export var LandingDisplayField;
(function (LandingDisplayField) {
    LandingDisplayField["ALL"] = "all";
    LandingDisplayField["FRONTEND_PAGELOAD"] = "frontend_pageload";
    LandingDisplayField["FRONTEND_OTHER"] = "frontend_other";
    LandingDisplayField["BACKEND"] = "backend";
})(LandingDisplayField || (LandingDisplayField = {}));
export var LANDING_DISPLAYS = [
    {
        label: 'All Transactions',
        field: LandingDisplayField.ALL,
    },
    {
        label: 'Frontend (Pageload)',
        field: LandingDisplayField.FRONTEND_PAGELOAD,
    },
    {
        label: 'Frontend (Other)',
        field: LandingDisplayField.FRONTEND_OTHER,
    },
    {
        label: 'Backend',
        field: LandingDisplayField.BACKEND,
    },
];
export function getCurrentLandingDisplay(location, projects, eventView) {
    var _a;
    var landingField = decodeScalar((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.landingDisplay);
    var display = LANDING_DISPLAYS.find(function (_a) {
        var field = _a.field;
        return field === landingField;
    });
    if (display) {
        return display;
    }
    var defaultDisplayField = getDefaultDisplayFieldForPlatform(projects, eventView);
    var defaultDisplay = LANDING_DISPLAYS.find(function (_a) {
        var field = _a.field;
        return field === defaultDisplayField;
    });
    return defaultDisplay || LANDING_DISPLAYS[0];
}
export function getChartWidth(chartData, refPixelRect) {
    var distance = refPixelRect ? refPixelRect.point2.x - refPixelRect.point1.x : 0;
    var chartWidth = chartData.length * distance;
    return {
        chartWidth: chartWidth,
    };
}
export function getBackendFunction(functionName, organization) {
    switch (functionName) {
        case 'p75':
            return { kind: 'function', function: ['p75', 'transaction.duration', undefined] };
        case 'tpm':
            return { kind: 'function', function: ['tpm', '', undefined] };
        case 'failure_rate':
            return { kind: 'function', function: ['failure_rate', '', undefined] };
        case 'apdex':
            return {
                kind: 'function',
                function: ['apdex', "" + organization.apdexThreshold, undefined],
            };
        default:
            throw new Error("Unsupported backend function: " + functionName);
    }
}
var VITALS_FRONTEND_PLATFORMS = __spreadArray([], __read(frontend));
var VITALS_BACKEND_PLATFORMS = __spreadArray([], __read(backend));
export function getDefaultDisplayFieldForPlatform(projects, eventView) {
    if (!eventView) {
        return LandingDisplayField.ALL;
    }
    var projectIds = eventView.project;
    if (projectIds.length === 0 || projectIds[0] === ALL_ACCESS_PROJECTS) {
        return LandingDisplayField.ALL;
    }
    var selectedProjects = projects.filter(function (p) { return projectIds.includes(parseInt(p.id, 10)); });
    if (selectedProjects.length === 0 || selectedProjects.some(function (p) { return !p.platform; })) {
        return LandingDisplayField.ALL;
    }
    if (selectedProjects.every(function (project) {
        return VITALS_FRONTEND_PLATFORMS.includes(project.platform);
    })) {
        return LandingDisplayField.FRONTEND_PAGELOAD;
    }
    if (selectedProjects.every(function (project) {
        return VITALS_BACKEND_PLATFORMS.includes(project.platform);
    })) {
        return LandingDisplayField.BACKEND;
    }
    return LandingDisplayField.ALL;
}
export var backendCardDetails = function (organization) {
    return {
        p75: {
            title: t('Duration (p75)'),
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.P75),
            formatter: function (value) { return getDuration(value / 1000, value >= 1000 ? 3 : 0, true); },
        },
        tpm: {
            title: t('Throughput'),
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.THROUGHPUT),
            formatter: formatAbbreviatedNumber,
        },
        failure_rate: {
            title: t('Failure Rate'),
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.FAILURE_RATE),
            formatter: function (value) { return formatPercentage(value, 2); },
        },
        apdex: {
            title: t('Apdex'),
            tooltip: getTermHelp(organization, PERFORMANCE_TERM.APDEX),
            formatter: function (value) { return formatFloat(value, 4); },
        },
    };
};
export function getDisplayAxes(options, location) {
    var leftDefault = options.find(function (opt) { return opt.isLeftDefault; }) || options[0];
    var rightDefault = options.find(function (opt) { return opt.isRightDefault; }) || options[1];
    var leftAxis = options.find(function (opt) { return opt.value === location.query[LEFT_AXIS_QUERY_KEY]; }) || leftDefault;
    var rightAxis = options.find(function (opt) { return opt.value === location.query[RIGHT_AXIS_QUERY_KEY]; }) ||
        rightDefault;
    return {
        leftAxis: leftAxis,
        rightAxis: rightAxis,
    };
}
//# sourceMappingURL=utils.jsx.map
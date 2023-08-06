import { __assign, __extends, __read } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { withTheme } from 'emotion-theming';
import AsyncComponent from 'app/components/asyncComponent';
import BaseChart from 'app/components/charts/baseChart';
import { HeaderTitleLegend } from 'app/components/charts/styles';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { t } from 'app/locale';
import getDynamicText from 'app/utils/getDynamicText';
var ALLOWED_TIME_PERIODS = ['1h', '24h', '7d', '14d', '30d'];
var ProjectErrorsBasicChart = /** @class */ (function (_super) {
    __extends(ProjectErrorsBasicChart, _super);
    function ProjectErrorsBasicChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectErrorsBasicChart.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { projects: null });
    };
    ProjectErrorsBasicChart.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId;
        if (!projectId) {
            return [];
        }
        return [
            [
                'projects',
                "/organizations/" + organization.slug + "/projects/",
                {
                    query: {
                        statsPeriod: this.getStatsPeriod(),
                        query: "id:" + projectId,
                    },
                },
            ],
        ];
    };
    ProjectErrorsBasicChart.prototype.componentDidMount = function () {
        var location = this.props.location;
        if (!ALLOWED_TIME_PERIODS.includes(location.query.statsPeriod)) {
            browserHistory.replace({
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { statsPeriod: this.getStatsPeriod(), start: undefined, end: undefined }),
            });
        }
    };
    ProjectErrorsBasicChart.prototype.onLoadAllEndpointsSuccess = function () {
        var _a, _b, _c, _d;
        this.props.onTotalValuesChange((_d = (_c = (_b = (_a = this.state.projects) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.stats) === null || _c === void 0 ? void 0 : _c.reduce(function (acc, _a) {
            var _b = __read(_a, 2), value = _b[1];
            return acc + value;
        }, 0)) !== null && _d !== void 0 ? _d : null);
    };
    ProjectErrorsBasicChart.prototype.getStatsPeriod = function () {
        var location = this.props.location;
        var statsPeriod = location.query.statsPeriod;
        if (ALLOWED_TIME_PERIODS.includes(statsPeriod)) {
            return statsPeriod;
        }
        return DEFAULT_STATS_PERIOD;
    };
    ProjectErrorsBasicChart.prototype.getSeries = function () {
        var _a, _b, _c;
        var projects = this.state.projects;
        return [
            {
                cursor: 'normal',
                name: t('Errors'),
                type: 'bar',
                data: (_c = (_b = (_a = projects === null || projects === void 0 ? void 0 : projects[0]) === null || _a === void 0 ? void 0 : _a.stats) === null || _b === void 0 ? void 0 : _b.map(function (_a) {
                    var _b = __read(_a, 2), timestamp = _b[0], value = _b[1];
                    return [timestamp * 1000, value];
                })) !== null && _c !== void 0 ? _c : [],
            },
        ];
    };
    ProjectErrorsBasicChart.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectErrorsBasicChart.prototype.renderBody = function () {
        var theme = this.props.theme;
        var _a = this.state, loading = _a.loading, reloading = _a.reloading;
        return getDynamicText({
            value: (<TransitionChart loading={loading} reloading={reloading}>
          <TransparentLoadingMask visible={reloading}/>

          <HeaderTitleLegend>{t('Daily Errors')}</HeaderTitleLegend>

          <BaseChart series={this.getSeries()} isGroupedByDate showTimeInTooltip colors={[theme.purple300, theme.purple200]} grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }}/>
        </TransitionChart>),
            fixed: t('Number of Errors Chart'),
        });
    };
    return ProjectErrorsBasicChart;
}(AsyncComponent));
export default withTheme(ProjectErrorsBasicChart);
//# sourceMappingURL=projectErrorsBasicChart.jsx.map
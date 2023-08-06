import { __assign, __extends } from "tslib";
import React from 'react';
import round from 'lodash/round';
import AsyncComponent from 'app/components/asyncComponent';
import Count from 'app/components/count';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { parseStatsPeriod } from 'app/components/organizations/timeRangeSelector/utils';
import ScoreCard from 'app/components/scoreCard';
import { IconArrow } from 'app/icons';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { getPeriod } from 'app/utils/getPeriod';
import { getTermHelp, PERFORMANCE_TERM } from 'app/views/performance/data';
import MissingPerformanceButtons from '../missingFeatureButtons/missingPerformanceButtons';
import { shouldFetchPreviousPeriod } from '../utils';
var ProjectApdexScoreCard = /** @class */ (function (_super) {
    __extends(ProjectApdexScoreCard, _super);
    function ProjectApdexScoreCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectApdexScoreCard.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { currentApdex: null, previousApdex: null });
    };
    ProjectApdexScoreCard.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasTransactions = _a.hasTransactions;
        if (!this.hasFeature() || !isProjectStabilized || !hasTransactions) {
            return [];
        }
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var period = datetime.period;
        var commonQuery = {
            environment: environments,
            project: projects.map(function (proj) { return String(proj); }),
            field: ["apdex(" + organization.apdexThreshold + ")"],
            query: 'event.type:transaction count():>0',
        };
        var endpoints = [
            [
                'currentApdex',
                "/organizations/" + organization.slug + "/eventsv2/",
                { query: __assign(__assign({}, commonQuery), getParams(datetime)) },
            ],
        ];
        if (shouldFetchPreviousPeriod(datetime)) {
            var previousStart = parseStatsPeriod(getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: true })
                .statsPeriod).start;
            var previousEnd = parseStatsPeriod(getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: false })
                .statsPeriod).start;
            endpoints.push([
                'previousApdex',
                "/organizations/" + organization.slug + "/eventsv2/",
                { query: __assign(__assign({}, commonQuery), { start: previousStart, end: previousEnd }) },
            ]);
        }
        return endpoints;
    };
    ProjectApdexScoreCard.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasTransactions = _a.hasTransactions;
        if ((prevProps.selection !== selection ||
            prevProps.hasTransactions !== hasTransactions) &&
            isProjectStabilized) {
            this.remountComponent();
        }
    };
    ProjectApdexScoreCard.prototype.hasFeature = function () {
        return this.props.organization.features.includes('performance-view');
    };
    Object.defineProperty(ProjectApdexScoreCard.prototype, "cardTitle", {
        get: function () {
            return t('Apdex');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "cardHelp", {
        get: function () {
            var baseHelp = getTermHelp(this.props.organization, PERFORMANCE_TERM.APDEX);
            if (this.trend) {
                return baseHelp + t(' This shows how it has changed since the last period.');
            }
            return baseHelp;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "currentApdex", {
        get: function () {
            var _a;
            var organization = this.props.organization;
            var currentApdex = this.state.currentApdex;
            var apdex = (_a = currentApdex === null || currentApdex === void 0 ? void 0 : currentApdex.data[0]) === null || _a === void 0 ? void 0 : _a[getAggregateAlias("apdex(" + organization.apdexThreshold + ")")];
            return typeof apdex === 'undefined' ? undefined : Number(apdex);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "previousApdex", {
        get: function () {
            var _a;
            var organization = this.props.organization;
            var previousApdex = this.state.previousApdex;
            var apdex = (_a = previousApdex === null || previousApdex === void 0 ? void 0 : previousApdex.data[0]) === null || _a === void 0 ? void 0 : _a[getAggregateAlias("apdex(" + organization.apdexThreshold + ")")];
            return typeof apdex === 'undefined' ? undefined : Number(apdex);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "trend", {
        get: function () {
            if (this.currentApdex && this.previousApdex) {
                return round(this.currentApdex - this.previousApdex, 3);
            }
            return null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectApdexScoreCard.prototype, "trendStatus", {
        get: function () {
            if (!this.trend) {
                return undefined;
            }
            return this.trend > 0 ? 'good' : 'bad';
        },
        enumerable: false,
        configurable: true
    });
    ProjectApdexScoreCard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectApdexScoreCard.prototype.renderMissingFeatureCard = function () {
        var organization = this.props.organization;
        return (<ScoreCard title={this.cardTitle} help={this.cardHelp} score={<MissingPerformanceButtons organization={organization}/>}/>);
    };
    ProjectApdexScoreCard.prototype.renderScore = function () {
        return defined(this.currentApdex) ? <Count value={this.currentApdex}/> : '\u2014';
    };
    ProjectApdexScoreCard.prototype.renderTrend = function () {
        // we want to show trend only after currentApdex has loaded to prevent jumping
        return defined(this.currentApdex) && defined(this.trend) ? (<React.Fragment>
        {this.trend >= 0 ? (<IconArrow direction="up" size="xs"/>) : (<IconArrow direction="down" size="xs"/>)}
        <Count value={Math.abs(this.trend)}/>
      </React.Fragment>) : null;
    };
    ProjectApdexScoreCard.prototype.renderBody = function () {
        var hasTransactions = this.props.hasTransactions;
        if (!this.hasFeature() || hasTransactions === false) {
            return this.renderMissingFeatureCard();
        }
        return (<ScoreCard title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    };
    return ProjectApdexScoreCard;
}(AsyncComponent));
export default ProjectApdexScoreCard;
//# sourceMappingURL=projectApdexScoreCard.jsx.map
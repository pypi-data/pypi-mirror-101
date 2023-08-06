import { __assign, __extends } from "tslib";
import React from 'react';
import round from 'lodash/round';
import AsyncComponent from 'app/components/asyncComponent';
import { getDiffInMinutes } from 'app/components/charts/utils';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import ScoreCard from 'app/components/scoreCard';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { IconArrow } from 'app/icons';
import { t } from 'app/locale';
import { defined, percent } from 'app/utils';
import { formatAbbreviatedNumber } from 'app/utils/formatters';
import { getPeriod } from 'app/utils/getPeriod';
import { displayCrashFreePercent, getCrashFreePercent } from 'app/views/releases/utils';
import { getSessionTermDescription, SessionTerm, } from 'app/views/releases/utils/sessionTerm';
import MissingReleasesButtons from '../missingFeatureButtons/missingReleasesButtons';
import { shouldFetchPreviousPeriod } from '../utils';
var ProjectStabilityScoreCard = /** @class */ (function (_super) {
    __extends(ProjectStabilityScoreCard, _super);
    function ProjectStabilityScoreCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectStabilityScoreCard.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { currentSessions: null, previousSessions: null });
    };
    ProjectStabilityScoreCard.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasSessions = _a.hasSessions;
        if (!isProjectStabilized || !hasSessions) {
            return [];
        }
        var projects = selection.projects, environment = selection.environments, datetime = selection.datetime;
        var period = datetime.period;
        var commonQuery = {
            environment: environment,
            project: projects[0],
            field: 'sum(session)',
            groupBy: 'session.status',
            interval: getDiffInMinutes(datetime) >= 24 * 60 ? '1d' : '1h',
        };
        // Unfortunately we can't do something like statsPeriod=28d&interval=14d to get scores for this and previous interval with the single request
        // https://github.com/getsentry/sentry/pull/22770#issuecomment-758595553
        var endpoints = [
            [
                'currentSessions',
                "/organizations/" + organization.slug + "/sessions/",
                {
                    query: __assign(__assign({}, commonQuery), getParams(datetime)),
                },
            ],
        ];
        if (shouldFetchPreviousPeriod(datetime)) {
            var doubledPeriod = getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: true }).statsPeriod;
            endpoints.push([
                'previousSessions',
                "/organizations/" + organization.slug + "/sessions/",
                {
                    query: __assign(__assign({}, commonQuery), { statsPeriodStart: doubledPeriod, statsPeriodEnd: period !== null && period !== void 0 ? period : DEFAULT_STATS_PERIOD }),
                },
            ]);
        }
        return endpoints;
    };
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "cardTitle", {
        get: function () {
            return t('Crash Free Sessions');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "cardHelp", {
        get: function () {
            return this.trend
                ? t('The percentage of crash free sessions and how it has changed since the last period.')
                : getSessionTermDescription(SessionTerm.STABILITY, null);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "score", {
        get: function () {
            var currentSessions = this.state.currentSessions;
            return this.calculateCrashFree(currentSessions);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "trend", {
        get: function () {
            var previousSessions = this.state.previousSessions;
            var previousScore = this.calculateCrashFree(previousSessions);
            if (!defined(this.score) || !defined(previousScore)) {
                return undefined;
            }
            return round(this.score - previousScore, 3);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectStabilityScoreCard.prototype, "trendStatus", {
        get: function () {
            if (!this.trend) {
                return undefined;
            }
            return this.trend > 0 ? 'good' : 'bad';
        },
        enumerable: false,
        configurable: true
    });
    ProjectStabilityScoreCard.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasSessions = _a.hasSessions;
        if ((prevProps.selection !== selection || prevProps.hasSessions !== hasSessions) &&
            isProjectStabilized) {
            this.remountComponent();
        }
    };
    ProjectStabilityScoreCard.prototype.calculateCrashFree = function (data) {
        var _a;
        if (!data) {
            return undefined;
        }
        var totalSessions = data.groups.reduce(function (acc, group) { return acc + group.totals['sum(session)']; }, 0);
        var crashedSessions = (_a = data.groups.find(function (group) { return group.by['session.status'] === 'crashed'; })) === null || _a === void 0 ? void 0 : _a.totals['sum(session)'];
        if (totalSessions === 0 || !defined(totalSessions) || !defined(crashedSessions)) {
            return undefined;
        }
        var crashedSessionsPercent = percent(crashedSessions, totalSessions);
        return getCrashFreePercent(100 - crashedSessionsPercent);
    };
    ProjectStabilityScoreCard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectStabilityScoreCard.prototype.renderMissingFeatureCard = function () {
        var organization = this.props.organization;
        return (<ScoreCard title={this.cardTitle} help={this.cardHelp} score={<MissingReleasesButtons organization={organization} health/>}/>);
    };
    ProjectStabilityScoreCard.prototype.renderScore = function () {
        var loading = this.state.loading;
        if (loading || !defined(this.score)) {
            return '\u2014';
        }
        return displayCrashFreePercent(this.score);
    };
    ProjectStabilityScoreCard.prototype.renderTrend = function () {
        var loading = this.state.loading;
        if (loading || !defined(this.score) || !defined(this.trend)) {
            return null;
        }
        return (<div>
        {this.trend >= 0 ? (<IconArrow direction="up" size="xs"/>) : (<IconArrow direction="down" size="xs"/>)}
        {formatAbbreviatedNumber(Math.abs(this.trend)) + "%"}
      </div>);
    };
    ProjectStabilityScoreCard.prototype.renderBody = function () {
        var hasSessions = this.props.hasSessions;
        if (hasSessions === false) {
            return this.renderMissingFeatureCard();
        }
        return (<ScoreCard title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    };
    return ProjectStabilityScoreCard;
}(AsyncComponent));
export default ProjectStabilityScoreCard;
//# sourceMappingURL=projectStabilityScoreCard.jsx.map
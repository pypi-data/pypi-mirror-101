import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import React from 'react';
import { fetchAnyReleaseExistence } from 'app/actionCreators/projects';
import AsyncComponent from 'app/components/asyncComponent';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { parseStatsPeriod } from 'app/components/organizations/timeRangeSelector/utils';
import ScoreCard from 'app/components/scoreCard';
import { IconArrow } from 'app/icons';
import { t } from 'app/locale';
import { defined } from 'app/utils';
import { getPeriod } from 'app/utils/getPeriod';
import MissingReleasesButtons from '../missingFeatureButtons/missingReleasesButtons';
import { shouldFetchPreviousPeriod } from '../utils';
var API_LIMIT = 1000;
var ProjectVelocityScoreCard = /** @class */ (function (_super) {
    __extends(ProjectVelocityScoreCard, _super);
    function ProjectVelocityScoreCard() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectVelocityScoreCard.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { currentReleases: null, previousReleases: null, noReleaseEver: false });
    };
    ProjectVelocityScoreCard.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized;
        if (!isProjectStabilized) {
            return [];
        }
        var projects = selection.projects, environments = selection.environments, datetime = selection.datetime;
        var period = datetime.period;
        var commonQuery = {
            environment: environments,
            project: projects[0],
        };
        var endpoints = [
            [
                'currentReleases',
                "/organizations/" + organization.slug + "/releases/stats/",
                {
                    includeAllArgs: true,
                    method: 'GET',
                    query: __assign(__assign({}, commonQuery), getParams(datetime)),
                },
            ],
        ];
        if (shouldFetchPreviousPeriod(datetime)) {
            var previousStart = parseStatsPeriod(getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: true })
                .statsPeriod).start;
            var previousEnd = parseStatsPeriod(getPeriod({ period: period, start: undefined, end: undefined }, { shouldDoublePeriod: false })
                .statsPeriod).start;
            endpoints.push([
                'previousReleases',
                "/organizations/" + organization.slug + "/releases/stats/",
                {
                    query: __assign(__assign({}, commonQuery), { start: previousStart, end: previousEnd }),
                },
            ]);
        }
        return endpoints;
    };
    /**
     * If our releases are empty, determine if we had a release in the last 90 days (empty message differs then)
     */
    ProjectVelocityScoreCard.prototype.onLoadAllEndpointsSuccess = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, currentReleases, previousReleases, _b, organization, selection, isProjectStabilized, hasOlderReleases;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.state, currentReleases = _a.currentReleases, previousReleases = _a.previousReleases;
                        _b = this.props, organization = _b.organization, selection = _b.selection, isProjectStabilized = _b.isProjectStabilized;
                        if (!isProjectStabilized) {
                            return [2 /*return*/];
                        }
                        if (__spreadArray(__spreadArray([], __read((currentReleases !== null && currentReleases !== void 0 ? currentReleases : []))), __read((previousReleases !== null && previousReleases !== void 0 ? previousReleases : []))).length !== 0) {
                            this.setState({ noReleaseEver: false });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        return [4 /*yield*/, fetchAnyReleaseExistence(this.api, organization.slug, selection.projects[0])];
                    case 1:
                        hasOlderReleases = _c.sent();
                        this.setState({ noReleaseEver: !hasOlderReleases, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(ProjectVelocityScoreCard.prototype, "cardTitle", {
        get: function () {
            return t('Number of Releases');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectVelocityScoreCard.prototype, "cardHelp", {
        get: function () {
            return this.trend
                ? t('The number of releases for this project and how it has changed since the last period.')
                : t('The number of releases for this project.');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectVelocityScoreCard.prototype, "trend", {
        get: function () {
            var _a = this.state, currentReleases = _a.currentReleases, previousReleases = _a.previousReleases;
            if (!defined(currentReleases) || !defined(previousReleases)) {
                return null;
            }
            return currentReleases.length - previousReleases.length;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(ProjectVelocityScoreCard.prototype, "trendStatus", {
        get: function () {
            if (!this.trend) {
                return undefined;
            }
            return this.trend > 0 ? 'good' : 'bad';
        },
        enumerable: false,
        configurable: true
    });
    ProjectVelocityScoreCard.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized;
        if (prevProps.selection !== selection ||
            prevProps.isProjectStabilized !== isProjectStabilized) {
            this.remountComponent();
        }
    };
    ProjectVelocityScoreCard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectVelocityScoreCard.prototype.renderMissingFeatureCard = function () {
        var organization = this.props.organization;
        return (<ScoreCard title={this.cardTitle} help={this.cardHelp} score={<MissingReleasesButtons organization={organization}/>}/>);
    };
    ProjectVelocityScoreCard.prototype.renderScore = function () {
        var _a = this.state, currentReleases = _a.currentReleases, loading = _a.loading;
        if (loading || !defined(currentReleases)) {
            return '\u2014';
        }
        return currentReleases.length === API_LIMIT
            ? API_LIMIT - 1 + "+"
            : currentReleases.length;
    };
    ProjectVelocityScoreCard.prototype.renderTrend = function () {
        var _a = this.state, loading = _a.loading, currentReleases = _a.currentReleases;
        if (loading || !defined(this.trend) || (currentReleases === null || currentReleases === void 0 ? void 0 : currentReleases.length) === API_LIMIT) {
            return null;
        }
        return (<React.Fragment>
        {this.trend >= 0 ? (<IconArrow direction="up" size="xs"/>) : (<IconArrow direction="down" size="xs"/>)}
        {Math.abs(this.trend)}
      </React.Fragment>);
    };
    ProjectVelocityScoreCard.prototype.renderBody = function () {
        var noReleaseEver = this.state.noReleaseEver;
        if (noReleaseEver) {
            return this.renderMissingFeatureCard();
        }
        return (<ScoreCard title={this.cardTitle} help={this.cardHelp} score={this.renderScore()} trend={this.renderTrend()} trendStatus={this.trendStatus}/>);
    };
    return ProjectVelocityScoreCard;
}(AsyncComponent));
export default ProjectVelocityScoreCard;
//# sourceMappingURL=projectVelocityScoreCard.jsx.map
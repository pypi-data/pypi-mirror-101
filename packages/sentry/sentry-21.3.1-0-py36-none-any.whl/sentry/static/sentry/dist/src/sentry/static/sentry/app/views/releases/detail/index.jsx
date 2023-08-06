import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import moment from 'moment';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { IconInfo, IconWarning } from 'app/icons';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import { formatVersion } from 'app/utils/formatters';
import routeTitleGen from 'app/utils/routeTitle';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import { DisplayOption } from '../list/utils';
import ReleaseHealthRequest from '../utils/releaseHealthRequest';
import PickProjectToContinue from './pickProjectToContinue';
import ReleaseHeader from './releaseHeader';
var DEFAULT_FRESH_RELEASE_STATS_PERIOD = '24h';
var ReleaseContext = React.createContext({});
var ReleasesDetail = /** @class */ (function (_super) {
    __extends(ReleasesDetail, _super);
    function ReleasesDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    ReleasesDetail.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, selection = _a.selection;
        var release = this.state.release;
        // The release details page will always have only one project selected
        var project = release === null || release === void 0 ? void 0 : release.projects.find(function (p) { return p.id === selection.projects[0]; });
        return routeTitleGen(t('Release %s', formatVersion(params.release)), organization.slug, false, project === null || project === void 0 ? void 0 : project.slug);
    };
    ReleasesDetail.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { deploys: [], sessions: null });
    };
    ReleasesDetail.prototype.getEndpoints = function () {
        var _a;
        var _b = this.props, organization = _b.organization, location = _b.location, params = _b.params, releaseMeta = _b.releaseMeta, defaultStatsPeriod = _b.defaultStatsPeriod;
        var basePath = "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/";
        var endpoints = [
            [
                'release',
                basePath,
                {
                    query: __assign({}, getParams(pick(location.query, __spreadArray([], __read(Object.values(URL_PARAM)))), {
                        defaultStatsPeriod: defaultStatsPeriod,
                    })),
                },
            ],
        ];
        if (releaseMeta.deployCount > 0) {
            endpoints.push(['deploys', basePath + "deploys/"]);
        }
        // Used to figure out if the release has any health data
        endpoints.push([
            'sessions',
            "/organizations/" + organization.slug + "/sessions/",
            {
                query: {
                    project: location.query.project,
                    environment: (_a = location.query.environment) !== null && _a !== void 0 ? _a : [],
                    query: "release:\"" + params.release + "\"",
                    field: 'sum(session)',
                    statsPeriod: '90d',
                    interval: '1d',
                },
            },
        ]);
        return endpoints;
    };
    ReleasesDetail.prototype.renderError = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var possiblyWrongProject = Object.values(this.state.errors).find(function (e) { return (e === null || e === void 0 ? void 0 : e.status) === 404 || (e === null || e === void 0 ? void 0 : e.status) === 403; });
        if (possiblyWrongProject) {
            return (<PageContent>
          <Alert type="error" icon={<IconWarning />}>
            {t('This release may not be in your selected project.')}
          </Alert>
        </PageContent>);
        }
        return _super.prototype.renderError.apply(this, __spreadArray([], __read(args)));
    };
    ReleasesDetail.prototype.renderLoading = function () {
        return (<PageContent>
        <LoadingIndicator />
      </PageContent>);
    };
    ReleasesDetail.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, selection = _a.selection, releaseMeta = _a.releaseMeta, defaultStatsPeriod = _a.defaultStatsPeriod, getHealthData = _a.getHealthData, isHealthLoading = _a.isHealthLoading;
        var _b = this.state, release = _b.release, deploys = _b.deploys, sessions = _b.sessions, reloading = _b.reloading;
        var project = release === null || release === void 0 ? void 0 : release.projects.find(function (p) { return p.id === selection.projects[0]; });
        if (!project || !release) {
            if (reloading) {
                return <LoadingIndicator />;
            }
            return null;
        }
        return (<LightWeightNoProjectMessage organization={organization}>
        <StyledPageContent>
          <ReleaseHeader location={location} organization={organization} release={release} project={project} releaseMeta={releaseMeta} refetchData={this.fetchData}/>
          <ReleaseContext.Provider value={{
                release: release,
                project: project,
                deploys: deploys,
                releaseMeta: releaseMeta,
                refetchData: this.fetchData,
                defaultStatsPeriod: defaultStatsPeriod,
                getHealthData: getHealthData,
                isHealthLoading: isHealthLoading,
                hasHealthData: !!(sessions === null || sessions === void 0 ? void 0 : sessions.groups[0].totals['sum(session)']),
            }}>
            {this.props.children}
          </ReleaseContext.Provider>
        </StyledPageContent>
      </LightWeightNoProjectMessage>);
    };
    return ReleasesDetail;
}(AsyncView));
var ReleasesDetailContainer = /** @class */ (function (_super) {
    __extends(ReleasesDetailContainer, _super);
    function ReleasesDetailContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    ReleasesDetailContainer.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        // fetch projects this release belongs to
        return [
            [
                'releaseMeta',
                "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/meta/",
            ],
        ];
    };
    ReleasesDetailContainer.prototype.renderError = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var has404Errors = Object.values(this.state.errors).find(function (e) { return (e === null || e === void 0 ? void 0 : e.status) === 404; });
        if (has404Errors) {
            // This catches a 404 coming from the release endpoint and displays a custom error message.
            return (<PageContent>
          <Alert type="error" icon={<IconWarning />}>
            {t('This release could not be found.')}
          </Alert>
        </PageContent>);
        }
        return _super.prototype.renderError.apply(this, __spreadArray([], __read(args)));
    };
    ReleasesDetailContainer.prototype.isProjectMissingInUrl = function () {
        var projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    };
    ReleasesDetailContainer.prototype.renderLoading = function () {
        return (<PageContent>
        <LoadingIndicator />
      </PageContent>);
    };
    ReleasesDetailContainer.prototype.renderProjectsFooterMessage = function () {
        return (<ProjectsFooterMessage>
        <IconInfo size="xs"/> {t('Only projects with this release are visible.')}
      </ProjectsFooterMessage>);
    };
    ReleasesDetailContainer.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, params = _a.params, router = _a.router, location = _a.location, selection = _a.selection;
        var releaseMeta = this.state.releaseMeta;
        if (!releaseMeta) {
            return null;
        }
        var projects = releaseMeta.projects;
        var isFreshRelease = moment(releaseMeta.released).isAfter(moment().subtract(24, 'hours'));
        var defaultStatsPeriod = isFreshRelease
            ? DEFAULT_FRESH_RELEASE_STATS_PERIOD
            : DEFAULT_STATS_PERIOD;
        if (this.isProjectMissingInUrl()) {
            return (<PickProjectToContinue orgSlug={organization.slug} version={params.release} router={router} projects={projects}/>);
        }
        return (<GlobalSelectionHeader lockedMessageSubject={t('release')} shouldForceProject={projects.length === 1} forceProject={projects.length === 1 ? __assign(__assign({}, projects[0]), { id: String(projects[0].id) }) : undefined} specificProjectSlugs={projects.map(function (p) { return p.slug; })} disableMultipleProjectSelection showProjectSettingsLink projectsFooterMessage={this.renderProjectsFooterMessage()} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: defaultStatsPeriod,
                },
            }}>
        <ReleaseHealthRequest releases={[params.release]} organization={organization} selection={selection} location={location} display={[DisplayOption.SESSIONS, DisplayOption.USERS]} defaultStatsPeriod={defaultStatsPeriod}>
          {function (_a) {
                var isHealthLoading = _a.isHealthLoading, getHealthData = _a.getHealthData;
                return (<ReleasesDetail {..._this.props} releaseMeta={releaseMeta} defaultStatsPeriod={defaultStatsPeriod} getHealthData={getHealthData} isHealthLoading={isHealthLoading}/>);
            }}
        </ReleaseHealthRequest>
      </GlobalSelectionHeader>);
    };
    return ReleasesDetailContainer;
}(AsyncComponent));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var ProjectsFooterMessage = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: min-content 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: min-content 1fr;\n  grid-gap: ", ";\n"])), space(1));
export { ReleaseContext, ReleasesDetailContainer };
export default withGlobalSelection(withOrganization(ReleasesDetailContainer));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map
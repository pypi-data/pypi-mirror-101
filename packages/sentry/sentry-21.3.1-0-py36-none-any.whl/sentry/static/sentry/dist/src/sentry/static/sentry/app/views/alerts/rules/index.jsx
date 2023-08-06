import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import flatten from 'lodash/flatten';
import { addErrorMessage } from 'app/actionCreators/indicator';
import Feature from 'app/components/acl/feature';
import AsyncComponent from 'app/components/asyncComponent';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import Pagination from 'app/components/pagination';
import { PanelTable, PanelTableHeader } from 'app/components/panels';
import SearchBar from 'app/components/searchBar';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { IconArrow, IconCheckmark } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import Projects from 'app/utils/projects';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withTeams from 'app/utils/withTeams';
import AlertHeader from '../list/header';
import { isIssueAlert } from '../utils';
import Filter from './filter';
import RuleListRow from './row';
var DOCS_URL = 'https://docs.sentry.io/product/alerts-notifications/metric-alerts/';
var ALERT_LIST_QUERY_DEFAULT_TEAMS = ['myteams', 'unassigned'];
var AlertRulesList = /** @class */ (function (_super) {
    __extends(AlertRulesList, _super);
    function AlertRulesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleChangeFilter = function (activeFilters) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = __rest(_b, ["cursor", "page"]);
            router.push({
                pathname: location.pathname,
                query: __assign(__assign({}, currentQuery), { team: __spreadArray([], __read(activeFilters)) }),
            });
        };
        _this.handleChangeSearch = function (name) {
            var _a = _this.props, router = _a.router, location = _a.location;
            var _b = location.query, _cursor = _b.cursor, _page = _b.page, currentQuery = __rest(_b, ["cursor", "page"]);
            router.push({
                pathname: location.pathname,
                query: __assign(__assign({}, currentQuery), { name: name }),
            });
        };
        _this.handleDeleteRule = function (projectId, rule) { return __awaiter(_this, void 0, void 0, function () {
            var params, orgId, alertPath, _err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        params = this.props.params;
                        orgId = params.orgId;
                        alertPath = isIssueAlert(rule) ? 'rules' : 'alert-rules';
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/" + alertPath + "/" + rule.id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _a.sent();
                        this.reloadData();
                        return [3 /*break*/, 4];
                    case 3:
                        _err_1 = _a.sent();
                        addErrorMessage(t('Error deleting rule'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AlertRulesList.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var query = location.query;
        return [
            [
                'ruleList',
                "/organizations/" + (params && params.orgId) + "/combined-rules/",
                {
                    query: query,
                },
            ],
        ];
    };
    AlertRulesList.prototype.tryRenderEmpty = function () {
        var ruleList = this.state.ruleList;
        if (ruleList && ruleList.length > 0) {
            return null;
        }
        return (<React.Fragment>
        {<IconWrapper>
            <IconCheckmark isCircled size="48"/>
          </IconWrapper>}
        {<Title>{t('No alert rules exist for these projects.')}</Title>}
        {<Description>
            {tct('Learn more about [link:Alerts]', {
                    link: <ExternalLink href={DOCS_URL}/>,
                })}
          </Description>}
      </React.Fragment>);
    };
    AlertRulesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    AlertRulesList.prototype.renderFilterBar = function () {
        var _a, _b;
        var _c = this.props, teams = _c.teams, location = _c.location;
        var teamQuery = (_a = location.query) === null || _a === void 0 ? void 0 : _a.team;
        var filteredTeams = typeof teamQuery === 'string' ? new Set([teamQuery]) : new Set(teamQuery);
        var additionalOptions = [
            { label: t('My Teams'), value: 'myteams' },
            { label: t('Unassigned'), value: 'unassigned' },
        ];
        var optionValues = __spreadArray(__spreadArray([], __read(teams.map(function (_a) {
            var id = _a.id;
            return id;
        }))), __read(additionalOptions.map(function (_a) {
            var value = _a.value;
            return value;
        })));
        return (<FilterWrapper>
        <Filter header={t('Team')} onFilterChange={this.handleChangeFilter} filterList={optionValues} selection={filteredTeams}>
          {function (_a) {
                var toggleFilter = _a.toggleFilter;
                return (<List>
              {additionalOptions.map(function (_a) {
                        var label = _a.label, value = _a.value;
                        return (<ListItem key={value} isChecked={filteredTeams.has(value)} onClick={function (event) {
                                event.stopPropagation();
                                toggleFilter(value);
                            }}>
                  <TeamName>{label}</TeamName>
                  <CheckboxFancy isChecked={filteredTeams.has(value)}/>
                </ListItem>);
                    })}
              {teams.map(function (_a) {
                        var id = _a.id, name = _a.name;
                        return (<ListItem key={id} isChecked={filteredTeams.has(id)} onClick={function (event) {
                                event.stopPropagation();
                                toggleFilter(id);
                            }}>
                  <TeamName>{name}</TeamName>
                  <CheckboxFancy isChecked={filteredTeams.has(id)}/>
                </ListItem>);
                    })}
            </List>);
            }}
        </Filter>
        <StyledSearchBar placeholder={t('Search by name')} query={(_b = location.query) === null || _b === void 0 ? void 0 : _b.name} onSearch={this.handleChangeSearch}/>
      </FilterWrapper>);
    };
    AlertRulesList.prototype.renderList = function () {
        var _this = this;
        var _a = this.props, orgId = _a.params.orgId, query = _a.location.query, organization = _a.organization, teams = _a.teams;
        var _b = this.state, loading = _b.loading, _c = _b.ruleList, ruleList = _c === void 0 ? [] : _c, ruleListPageLinks = _b.ruleListPageLinks;
        var allProjectsFromIncidents = new Set(flatten(ruleList === null || ruleList === void 0 ? void 0 : ruleList.map(function (_a) {
            var projects = _a.projects;
            return projects;
        })));
        var sort = {
            asc: query.asc === '1',
            field: query.sort || 'date_added',
        };
        var _cursor = query.cursor, _page = query.page, currentQuery = __rest(query, ["cursor", "page"]);
        var userTeams = new Set(teams.filter(function (_a) {
            var isMember = _a.isMember;
            return isMember;
        }).map(function (_a) {
            var id = _a.id;
            return id;
        }));
        return (<StyledLayoutBody>
        <Layout.Main fullWidth>
          <Feature organization={organization} features={['organizations:team-alerts-ownership']}>
            {function (_a) {
                var hasFeature = _a.hasFeature;
                return (<React.Fragment>
                {hasFeature && _this.renderFilterBar()}
                <StyledPanelTable headers={__spreadArray(__spreadArray([
                        t('Type'),
                        // eslint-disable-next-line react/jsx-key
                        <StyledSortLink to={{
                                pathname: location.pathname,
                                query: __assign(__assign({}, currentQuery), { asc: sort.field === 'name' && sort.asc ? undefined : '1', sort: 'name' }),
                            }}>
                      {t('Alert Name')}{' '}
                      {sort.field === 'name' && (<IconArrow color="gray300" size="xs" direction={sort.asc ? 'up' : 'down'}/>)}
                    </StyledSortLink>,
                        t('Project')
                    ], __read((hasFeature ? [t('Team')] : []))), [
                        t('Created By'),
                        // eslint-disable-next-line react/jsx-key
                        <StyledSortLink to={{
                                pathname: location.pathname,
                                query: __assign(__assign({}, currentQuery), { asc: sort.field === 'date_added' && sort.asc ? undefined : '1', sort: 'date_added' }),
                            }}>
                      {t('Created')}{' '}
                      {sort.field === 'date_added' && (<IconArrow color="gray300" size="xs" direction={sort.asc ? 'up' : 'down'}/>)}
                    </StyledSortLink>,
                        t('Actions'),
                    ])} isLoading={loading} isEmpty={(ruleList === null || ruleList === void 0 ? void 0 : ruleList.length) === 0} emptyMessage={_this.tryRenderEmpty()} showTeamCol={hasFeature}>
                  <Projects orgId={orgId} slugs={Array.from(allProjectsFromIncidents)}>
                    {function (_a) {
                        var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
                        return ruleList.map(function (rule) { return (<RuleListRow 
                        // Metric and issue alerts can have the same id
                        key={(isIssueAlert(rule) ? 'metric' : 'issue') + "-" + rule.id} projectsLoaded={initiallyLoaded} projects={projects} rule={rule} orgId={orgId} onDelete={_this.handleDeleteRule} organization={organization} userTeams={userTeams}/>); });
                    }}
                  </Projects>
                </StyledPanelTable>
              </React.Fragment>);
            }}
          </Feature>
          <Pagination pageLinks={ruleListPageLinks}/>
        </Layout.Main>
      </StyledLayoutBody>);
    };
    AlertRulesList.prototype.renderBody = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, router = _a.router;
        var orgId = params.orgId;
        return (<SentryDocumentTitle title={t('Alerts')} orgSlug={orgId}>
        <GlobalSelectionHeader organization={organization} showDateSelector={false} showEnvironmentSelector={false}>
          <AlertHeader organization={organization} router={router} activeTab="rules"/>
          {this.renderList()}
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return AlertRulesList;
}(AsyncComponent));
var AlertRulesListContainer = /** @class */ (function (_super) {
    __extends(AlertRulesListContainer, _super);
    function AlertRulesListContainer() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AlertRulesListContainer.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, router = _a.router, location = _a.location, selection = _a.selection;
        var query = {
            project: selection.projects,
            // TODO(workflow): Support environments from global selection header
            // environment: selection.environments,
        };
        if (organization.features.includes('team-alerts-ownership')) {
            query.team = ALERT_LIST_QUERY_DEFAULT_TEAMS;
        }
        router.replace({
            pathname: location.pathname,
            query: __assign(__assign({}, query), location.query),
        });
        this.trackView();
    };
    AlertRulesListContainer.prototype.componentDidUpdate = function (nextProps) {
        var _a, _b;
        if (((_a = nextProps.location.query) === null || _a === void 0 ? void 0 : _a.sort) !== ((_b = this.props.location.query) === null || _b === void 0 ? void 0 : _b.sort)) {
            this.trackView();
        }
    };
    AlertRulesListContainer.prototype.trackView = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        trackAnalyticsEvent({
            eventKey: 'alert_rules.viewed',
            eventName: 'Alert Rules: Viewed',
            organization_id: organization.id,
            sort: location.query.sort,
        });
    };
    AlertRulesListContainer.prototype.render = function () {
        return <AlertRulesList {...this.props}/>;
    };
    return AlertRulesListContainer;
}(React.Component));
export default withGlobalSelection(withTeams(AlertRulesListContainer));
var StyledLayoutBody = styled(Layout.Body)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: -20px;\n"], ["\n  margin-bottom: -20px;\n"])));
var StyledSortLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"], ["\n  color: inherit;\n\n  :hover {\n    color: inherit;\n  }\n"])));
var TeamName = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, overflowEllipsis);
var FilterWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space(1.5));
var StyledSearchBar = styled(SearchBar)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-grow: 1;\n  margin-left: ", ";\n"], ["\n  flex-grow: 1;\n  margin-left: ", ";\n"])), space(1.5));
var List = styled('ul')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"])));
var ListItem = styled('li')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n  ", " {\n    opacity: ", ";\n  }\n\n  &:hover ", " {\n    opacity: 1;\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space(1), space(1), space(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, CheckboxFancy, function (p) { return (p.isChecked ? 1 : 0.3); }, CheckboxFancy, function (p) { return p.theme.blue300; });
var StyledPanelTable = styled(PanelTable)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  ", " {\n    line-height: normal;\n  }\n  font-size: ", ";\n  grid-template-columns: auto 1.5fr 1fr 1fr 1fr ", " auto;\n  margin-bottom: 0;\n  white-space: nowrap;\n  ", "\n"], ["\n  ", " {\n    line-height: normal;\n  }\n  font-size: ", ";\n  grid-template-columns: auto 1.5fr 1fr 1fr 1fr ", " auto;\n  margin-bottom: 0;\n  white-space: nowrap;\n  ",
    "\n"])), PanelTableHeader, function (p) { return p.theme.fontSizeMedium; }, function (p) { return (p.showTeamCol ? '1fr' : ''); }, function (p) {
    return p.emptyMessage &&
        "svg:not([data-test-id='icon-check-mark']) {\n    display: none;";
});
var IconWrapper = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  color: ", ";\n  display: block;\n"], ["\n  color: ", ";\n  display: block;\n"])), function (p) { return p.theme.gray200; });
var Title = styled('strong')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(1));
var Description = styled('span')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  font-size: ", ";\n  display: block;\n  margin: 0;\n"], ["\n  font-size: ", ";\n  display: block;\n  margin: 0;\n"])), function (p) { return p.theme.fontSizeLarge; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=index.jsx.map
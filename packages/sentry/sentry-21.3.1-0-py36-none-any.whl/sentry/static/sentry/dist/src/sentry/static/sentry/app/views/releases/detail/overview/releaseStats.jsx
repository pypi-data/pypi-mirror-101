import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import { SectionHeading } from 'app/components/charts/styles';
import Count from 'app/components/count';
import DeployBadge from 'app/components/deployBadge';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import NotAvailable from 'app/components/notAvailable';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import NOT_AVAILABLE_MESSAGES from 'app/constants/notAvailableMessages';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { getTermHelp, PERFORMANCE_TERM } from 'app/views/performance/data';
import { getSessionTermDescription, SessionTerm, sessionTerm, } from 'app/views/releases/utils/sessionTerm';
import CrashFree from '../../list/crashFree';
import ReleaseAdoption from '../../list/releaseAdoption';
import { DisplayOption } from '../../list/utils';
import { getReleaseNewIssuesUrl, getReleaseUnhandledIssuesUrl } from '../../utils';
import { getReleaseEventView } from '../utils';
function ReleaseStats(_a) {
    var _b;
    var organization = _a.organization, release = _a.release, project = _a.project, location = _a.location, selection = _a.selection, isHealthLoading = _a.isHealthLoading, hasHealthData = _a.hasHealthData, getHealthData = _a.getHealthData;
    var lastDeploy = release.lastDeploy, dateCreated = release.dateCreated, newGroups = release.newGroups, version = release.version;
    var crashCount = getHealthData.getCrashCount(version, project.id, DisplayOption.SESSIONS);
    var crashFreeSessions = getHealthData.getCrashFreeRate(version, project.id, DisplayOption.SESSIONS);
    var crashFreeUsers = getHealthData.getCrashFreeRate(version, project.id, DisplayOption.USERS);
    var get24hSessionCountByRelease = getHealthData.get24hCountByRelease(version, project.id, DisplayOption.SESSIONS);
    var get24hSessionCountByProject = getHealthData.get24hCountByProject(project.id, DisplayOption.SESSIONS);
    var get24hUserCountByRelease = getHealthData.get24hCountByRelease(version, project.id, DisplayOption.USERS);
    var get24hUserCountByProject = getHealthData.get24hCountByProject(project.id, DisplayOption.USERS);
    var sessionAdoption = getHealthData.getAdoption(version, project.id, DisplayOption.SESSIONS);
    var userAdoption = getHealthData.getAdoption(version, project.id, DisplayOption.USERS);
    return (<Container>
      <div>
        <SectionHeading>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? t('Date Deployed') : t('Date Created')}
        </SectionHeading>
        <SectionContent>
          <TimeSince date={(_b = lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) !== null && _b !== void 0 ? _b : dateCreated}/>
        </SectionContent>
      </div>

      <div>
        <SectionHeading>{t('Last Deploy')}</SectionHeading>
        <SectionContent>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (<DeployBadge deploy={lastDeploy} orgSlug={organization.slug} version={version} projectId={project.id}/>) : (<NotAvailable />)}
        </SectionContent>
      </div>

      <CrashFreeSection>
        <SectionHeading>
          {t('Crash Free Rate')}
          <QuestionTooltip position="top" title={getSessionTermDescription(SessionTerm.CRASH_FREE, project.platform)} size="sm"/>
        </SectionHeading>
        {isHealthLoading ? (<Placeholder height="58px"/>) : (<SectionContent>
            {defined(crashFreeSessions) || defined(crashFreeUsers) ? (<CrashFreeWrapper>
                {defined(crashFreeSessions) && (<div>
                    <CrashFree percent={crashFreeSessions} iconSize="md" displayOption={DisplayOption.SESSIONS}/>
                  </div>)}

                {defined(crashFreeUsers) && (<div>
                    <CrashFree percent={crashFreeUsers} iconSize="md" displayOption={DisplayOption.USERS}/>
                  </div>)}
              </CrashFreeWrapper>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
          </SectionContent>)}
      </CrashFreeSection>

      <AdoptionSection>
        <SectionHeading>
          {t('Adoption')}
          <QuestionTooltip position="top" title={getSessionTermDescription(SessionTerm.ADOPTION, project.platform)} size="sm"/>
        </SectionHeading>
        {isHealthLoading ? (<Placeholder height="88px"/>) : (<SectionContent>
            {get24hSessionCountByProject || get24hUserCountByProject ? (<AdoptionWrapper>
                {defined(get24hSessionCountByProject) &&
                    get24hSessionCountByProject > 0 && (<ReleaseAdoption releaseCount={get24hSessionCountByRelease !== null && get24hSessionCountByRelease !== void 0 ? get24hSessionCountByRelease : 0} projectCount={get24hSessionCountByProject !== null && get24hSessionCountByProject !== void 0 ? get24hSessionCountByProject : 0} adoption={sessionAdoption !== null && sessionAdoption !== void 0 ? sessionAdoption : 0} displayOption={DisplayOption.SESSIONS} withLabels/>)}

                {defined(get24hUserCountByProject) && get24hUserCountByProject > 0 && (<ReleaseAdoption releaseCount={get24hUserCountByRelease !== null && get24hUserCountByRelease !== void 0 ? get24hUserCountByRelease : 0} projectCount={get24hUserCountByProject !== null && get24hUserCountByProject !== void 0 ? get24hUserCountByProject : 0} adoption={userAdoption !== null && userAdoption !== void 0 ? userAdoption : 0} displayOption={DisplayOption.USERS} withLabels/>)}
              </AdoptionWrapper>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
          </SectionContent>)}
      </AdoptionSection>

      <LinkedStatsSection>
        <div>
          <SectionHeading>{t('New Issues')}</SectionHeading>
          <SectionContent>
            <Tooltip title={t('Open in Issues')}>
              <GlobalSelectionLink to={getReleaseNewIssuesUrl(organization.slug, project.id, version)}>
                <Count value={newGroups}/>
              </GlobalSelectionLink>
            </Tooltip>
          </SectionContent>
        </div>

        <div>
          <SectionHeading>
            {sessionTerm.crashes}
            <QuestionTooltip position="top" title={getSessionTermDescription(SessionTerm.CRASHES, project.platform)} size="sm"/>
          </SectionHeading>
          {isHealthLoading ? (<Placeholder height="24px"/>) : (<SectionContent>
              {hasHealthData ? (<Tooltip title={t('Open in Issues')}>
                  <GlobalSelectionLink to={getReleaseUnhandledIssuesUrl(organization.slug, project.id, version)}>
                    <Count value={crashCount !== null && crashCount !== void 0 ? crashCount : 0}/>
                  </GlobalSelectionLink>
                </Tooltip>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.releaseHealth}/>)}
            </SectionContent>)}
        </div>

        <div>
          <SectionHeading>
            {t('Apdex')}
            <QuestionTooltip position="top" title={getTermHelp(organization, PERFORMANCE_TERM.APDEX)} size="sm"/>
          </SectionHeading>
          <SectionContent>
            <Feature features={['performance-view']}>
              {function (hasFeature) {
            return hasFeature ? (<DiscoverQuery eventView={getReleaseEventView(selection, release === null || release === void 0 ? void 0 : release.version, organization)} location={location} orgSlug={organization.slug}>
                    {function (_a) {
                    var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
                    if (isLoading) {
                        return <Placeholder height="24px"/>;
                    }
                    if (error || !tableData || tableData.data.length === 0) {
                        return <NotAvailable />;
                    }
                    return (<GlobalSelectionLink to={{
                            pathname: "/organizations/" + organization.slug + "/performance/",
                            query: {
                                query: "release:" + (release === null || release === void 0 ? void 0 : release.version),
                            },
                        }}>
                          <Tooltip title={t('Open in Performance')}>
                            <Count value={tableData.data[0][getAggregateAlias("apdex(" + organization.apdexThreshold + ")")]}/>
                          </Tooltip>
                        </GlobalSelectionLink>);
                }}
                  </DiscoverQuery>) : (<NotAvailable tooltip={NOT_AVAILABLE_MESSAGES.performance}/>);
        }}
            </Feature>
          </SectionContent>
        </div>
      </LinkedStatsSection>
    </Container>);
}
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: ", ";\n  margin-bottom: ", ";\n"])), space(2), space(3));
var SectionContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject([""], [""])));
var CrashFreeSection = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-column: 1/3;\n"], ["\n  grid-column: 1/3;\n"])));
var CrashFreeWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1));
var AdoptionSection = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-column: 1/3;\n  margin-bottom: ", ";\n"], ["\n  grid-column: 1/3;\n  margin-bottom: ", ";\n"])), space(1));
var AdoptionWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
var LinkedStatsSection = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-column: 1/3;\n  display: flex;\n  justify-content: space-between;\n"], ["\n  grid-column: 1/3;\n  display: flex;\n  justify-content: space-between;\n"])));
export default ReleaseStats;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=releaseStats.jsx.map
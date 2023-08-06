import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import Collapsible from 'app/components/collapsible';
import Count from 'app/components/count';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import NotAvailable from 'app/components/notAvailable';
import { PanelItem } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import Tooltip from 'app/components/tooltip';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { getReleaseNewIssuesUrl, getReleaseUnhandledIssuesUrl } from '../../utils';
import CrashFree from '../crashFree';
import HealthStatsChart from '../healthStatsChart';
import HealthStatsPeriod from '../healthStatsPeriod';
import ReleaseAdoption from '../releaseAdoption';
import { DisplayOption } from '../utils';
import Header from './header';
import ProjectLink from './projectLink';
var Content = function (_a) {
    var projects = _a.projects, releaseVersion = _a.releaseVersion, location = _a.location, organization = _a.organization, activeDisplay = _a.activeDisplay, showPlaceholders = _a.showPlaceholders, isTopRelease = _a.isTopRelease, getHealthData = _a.getHealthData;
    return (<React.Fragment>
      <Header>
        <Layout>
          <Column>{t('Project Name')}</Column>
          <AdoptionColumn>
            <GuideAnchor target="release_adoption" position="bottom" disabled={!(isTopRelease && window.innerWidth >= 800)}>
              {t('Adoption')}
            </GuideAnchor>
          </AdoptionColumn>
          <CrashFreeRateColumn>{t('Crash Free Rate')}</CrashFreeRateColumn>
          <CountColumn>
            <span>{t('Count')}</span>
            <HealthStatsPeriod location={location}/>
          </CountColumn>
          <CrashesColumn>{t('Crashes')}</CrashesColumn>
          <NewIssuesColumn>{t('New Issues')}</NewIssuesColumn>
          <ViewColumn />
        </Layout>
      </Header>

      <ProjectRows>
        <Collapsible expandButton={function (_a) {
            var onExpand = _a.onExpand, numberOfCollapsedItems = _a.numberOfCollapsedItems;
            return (<ExpandButtonWrapper>
              <Button priority="primary" size="xsmall" onClick={onExpand}>
                {tct('Show [numberOfCollapsedItems] More', {
                    numberOfCollapsedItems: numberOfCollapsedItems,
                })}
              </Button>
            </ExpandButtonWrapper>);
        }} collapseButton={function (_a) {
            var onCollapse = _a.onCollapse;
            return (<CollapseButtonWrapper>
              <Button priority="primary" size="xsmall" onClick={onCollapse}>
                {t('Collapse')}
              </Button>
            </CollapseButtonWrapper>);
        }}>
          {projects.map(function (project, index) {
            var id = project.id, slug = project.slug, newGroups = project.newGroups;
            var crashCount = getHealthData.getCrashCount(releaseVersion, id, DisplayOption.SESSIONS);
            var crashFreeRate = getHealthData.getCrashFreeRate(releaseVersion, id, activeDisplay);
            var get24hCountByRelease = getHealthData.get24hCountByRelease(releaseVersion, id, activeDisplay);
            var get24hCountByProject = getHealthData.get24hCountByProject(id, activeDisplay);
            var timeSeries = getHealthData.getTimeSeries(releaseVersion, id, activeDisplay);
            var adoption = getHealthData.getAdoption(releaseVersion, id, activeDisplay);
            // we currently don't support sub-hour session intervals, we rather hide the count histogram than to show only two bars
            var hasCountHistogram = (timeSeries === null || timeSeries === void 0 ? void 0 : timeSeries[0].data.length) > 7 &&
                timeSeries[0].data.some(function (item) { return item.value > 0; });
            return (<ProjectRow key={releaseVersion + "-" + slug + "-health"}>
                <Layout>
                  <Column>
                    <ProjectBadge project={project} avatarSize={16}/>
                  </Column>

                  <AdoptionColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="150px"/>) : get24hCountByProject ? (<AdoptionWrapper>
                        <ReleaseAdoption adoption={adoption !== null && adoption !== void 0 ? adoption : 0} releaseCount={get24hCountByRelease !== null && get24hCountByRelease !== void 0 ? get24hCountByRelease : 0} projectCount={get24hCountByProject !== null && get24hCountByProject !== void 0 ? get24hCountByProject : 0} displayOption={activeDisplay}/>
                        <Count value={get24hCountByRelease !== null && get24hCountByRelease !== void 0 ? get24hCountByRelease : 0}/>
                      </AdoptionWrapper>) : (<NotAvailable />)}
                  </AdoptionColumn>

                  <CrashFreeRateColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="60px"/>) : defined(crashFreeRate) ? (<CrashFree percent={crashFreeRate}/>) : (<NotAvailable />)}
                  </CrashFreeRateColumn>

                  <CountColumn>
                    {showPlaceholders ? (<StyledPlaceholder />) : hasCountHistogram ? (<ChartWrapper>
                        <HealthStatsChart data={timeSeries} height={20} activeDisplay={activeDisplay}/>
                      </ChartWrapper>) : (<NotAvailable />)}
                  </CountColumn>

                  <CrashesColumn>
                    {showPlaceholders ? (<StyledPlaceholder width="30px"/>) : defined(crashCount) ? (<Tooltip title={t('Open in Issues')}>
                        <GlobalSelectionLink to={getReleaseUnhandledIssuesUrl(organization.slug, project.id, releaseVersion)}>
                          <Count value={crashCount}/>
                        </GlobalSelectionLink>
                      </Tooltip>) : (<NotAvailable />)}
                  </CrashesColumn>

                  <NewIssuesColumn>
                    <Tooltip title={t('Open in Issues')}>
                      <GlobalSelectionLink to={getReleaseNewIssuesUrl(organization.slug, project.id, releaseVersion)}>
                        <Count value={newGroups || 0}/>
                      </GlobalSelectionLink>
                    </Tooltip>
                  </NewIssuesColumn>

                  <ViewColumn>
                    <GuideAnchor disabled={!isTopRelease || index !== 0} target="view_release">
                      <ProjectLink orgSlug={organization.slug} project={project} releaseVersion={releaseVersion} location={location}/>
                    </GuideAnchor>
                  </ViewColumn>
                </Layout>
              </ProjectRow>);
        })}
        </Collapsible>
      </ProjectRows>
    </React.Fragment>);
};
export default Content;
var ProjectRows = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ExpandButtonWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  width: 100%;\n  bottom: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-image: linear-gradient(\n    180deg,\n    hsla(0, 0%, 100%, 0.15) 0,\n    ", "\n  );\n  background-repeat: repeat-x;\n  border-bottom: ", " solid ", ";\n  border-top: ", " solid transparent;\n  border-bottom-right-radius: ", ";\n  @media (max-width: ", ") {\n    border-bottom-left-radius: ", ";\n  }\n"], ["\n  position: absolute;\n  width: 100%;\n  bottom: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background-image: linear-gradient(\n    180deg,\n    hsla(0, 0%, 100%, 0.15) 0,\n    ", "\n  );\n  background-repeat: repeat-x;\n  border-bottom: ", " solid ", ";\n  border-top: ", " solid transparent;\n  border-bottom-right-radius: ", ";\n  @media (max-width: ", ") {\n    border-bottom-left-radius: ", ";\n  }\n"])), function (p) { return p.theme.white; }, space(1), function (p) { return p.theme.white; }, space(1), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.borderRadius; });
var CollapseButtonWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 41px;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  height: 41px;\n"])));
var ProjectRow = styled(PanelItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", " ", ";\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"], ["\n  padding: ", " ", ";\n  @media (min-width: ", ") {\n    font-size: ", ";\n  }\n"])), space(1), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.fontSizeMedium; });
var Layout = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1.4fr 0.6fr 0.7fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  width: 100%;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 0.8fr 1fr 0.5fr 0.5fr 0.6fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 0.8fr 1fr 1fr 0.5fr 0.5fr 0.5fr;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1.4fr 0.6fr 0.7fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  width: 100%;\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 1fr 1fr 0.5fr 0.5fr 0.5fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 0.8fr 1fr 0.5fr 0.5fr 0.6fr;\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr 0.8fr 1fr 1fr 0.5fr 0.5fr 0.5fr;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[3]; });
var Column = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", ";\n  line-height: 20px;\n"], ["\n  ", ";\n  line-height: 20px;\n"])), overflowEllipsis);
var NewIssuesColumn = styled(Column)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    text-align: right;\n  }\n"], ["\n  @media (min-width: ", ") {\n    text-align: right;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var AdoptionColumn = styled(Column)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n"], ["\n  display: none;\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var AdoptionWrapper = styled('span')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: 70px 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  @media (min-width: ", ") {\n    grid-template-columns: 90px 1fr;\n  }\n"], ["\n  display: inline-grid;\n  grid-template-columns: 70px 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  @media (min-width: ", ") {\n    grid-template-columns: 90px 1fr;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[3]; });
var CrashFreeRateColumn = styled(Column)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    text-align: center;\n  }\n"], ["\n  @media (min-width: ", ") {\n    text-align: center;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var CountColumn = styled(Column)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    /* Chart tooltips need overflow */\n    overflow: visible;\n  }\n"])), function (p) { return p.theme.breakpoints[3]; });
var CrashesColumn = styled(Column)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    text-align: right;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    text-align: right;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var ViewColumn = styled(Column)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var ChartWrapper = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  flex: 1;\n  g > .barchart-rect {\n    background: ", ";\n    fill: ", ";\n  }\n"], ["\n  flex: 1;\n  g > .barchart-rect {\n    background: ", ";\n    fill: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray200; });
var StyledPlaceholder = styled(Placeholder)(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  height: 15px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"], ["\n  height: 15px;\n  display: inline-block;\n  position: relative;\n  top: ", ";\n"])), space(0.25));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15;
//# sourceMappingURL=content.jsx.map
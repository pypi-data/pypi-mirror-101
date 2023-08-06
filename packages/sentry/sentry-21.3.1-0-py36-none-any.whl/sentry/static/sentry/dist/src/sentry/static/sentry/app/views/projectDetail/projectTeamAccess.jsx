import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { SectionHeading } from 'app/components/charts/styles';
import Collapsible from 'app/components/collapsible';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import Placeholder from 'app/components/placeholder';
import { IconOpen } from 'app/icons';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
import { SectionHeadingLink, SectionHeadingWrapper, SidebarSection } from './styles';
function ProjectTeamAccess(_a) {
    var organization = _a.organization, project = _a.project;
    var hasEditPermissions = organization.access.includes('project:write');
    var settingsLink = "/settings/" + organization.slug + "/projects/" + (project === null || project === void 0 ? void 0 : project.slug) + "/teams/";
    function renderInnerBody() {
        if (!project) {
            return <Placeholder height="23px"/>;
        }
        if (project.teams.length === 0) {
            return (<Button to={settingsLink} disabled={!hasEditPermissions} title={hasEditPermissions ? undefined : t('You do not have permission to do this')} priority="primary" size="small">
          {t('Assign Team')}
        </Button>);
        }
        return (<Collapsible expandButton={function (_a) {
                var onExpand = _a.onExpand, numberOfCollapsedItems = _a.numberOfCollapsedItems;
                return (<Button priority="link" onClick={onExpand}>
            {tn('Show %s collapsed team', 'Show %s collapsed teams', numberOfCollapsedItems)}
          </Button>);
            }}>
        {project.teams
                .sort(function (a, b) { return a.slug.localeCompare(b.slug); })
                .map(function (team) { return (<StyledLink to={"/settings/" + organization.slug + "/teams/" + team.slug + "/"} key={team.slug}>
              <IdBadge team={team} hideAvatar/>
            </StyledLink>); })}
      </Collapsible>);
    }
    return (<StyledSidebarSection>
      <SectionHeadingWrapper>
        <SectionHeading>{t('Team Access')}</SectionHeading>
        <SectionHeadingLink to={settingsLink}>
          <IconOpen />
        </SectionHeadingLink>
      </SectionHeadingWrapper>

      <div>{renderInnerBody()}</div>
    </StyledSidebarSection>);
}
var StyledSidebarSection = styled(SidebarSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledLink = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  margin-bottom: ", ";\n"], ["\n  display: block;\n  margin-bottom: ", ";\n"])), space(0.5));
export default ProjectTeamAccess;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectTeamAccess.jsx.map
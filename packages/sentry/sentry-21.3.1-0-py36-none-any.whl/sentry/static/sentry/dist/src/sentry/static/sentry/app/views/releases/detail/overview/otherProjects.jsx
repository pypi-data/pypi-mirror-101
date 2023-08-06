import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import Collapsible from 'app/components/collapsible';
import IdBadge from 'app/components/idBadge';
import { tn } from 'app/locale';
import space from 'app/styles/space';
import ProjectLink from '../../list/releaseHealth/projectLink';
import { SectionHeading, Wrapper } from './styles';
function OtherProjects(_a) {
    var projects = _a.projects, location = _a.location, version = _a.version, organization = _a.organization;
    return (<Wrapper>
      <SectionHeading>
        {tn('Other Project for This Release', 'Other Projects for This Release', projects.length)}
      </SectionHeading>

      <Collapsible expandButton={function (_a) {
            var onExpand = _a.onExpand, numberOfCollapsedItems = _a.numberOfCollapsedItems;
            return (<Button priority="link" onClick={onExpand}>
            {tn('Show %s collapsed project', 'Show %s collapsed projects', numberOfCollapsedItems)}
          </Button>);
        }}>
        {projects.map(function (project) { return (<Row key={project.id}>
            <IdBadge project={project} avatarSize={16}/>
            <ProjectLink location={location} orgSlug={organization.slug} releaseVersion={version} project={project}/>
          </Row>); })}
      </Collapsible>
    </Wrapper>);
}
var Row = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n\n  @media (min-width: ", ") and (max-width: ", ") {\n    grid-template-columns: 200px max-content;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  font-size: ", ";\n\n  @media (min-width: ", ") and (max-width: ",
    ") {\n    grid-template-columns: 200px max-content;\n  }\n"])), space(0.75), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.breakpoints[1]; }, function (p) {
    return p.theme.breakpoints[2];
});
export default OtherProjects;
var templateObject_1;
//# sourceMappingURL=otherProjects.jsx.map
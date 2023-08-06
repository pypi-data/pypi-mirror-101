import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import ProjectApdexScoreCard from './projectApdexScoreCard';
import ProjectStabilityScoreCard from './projectStabilityScoreCard';
import ProjectVelocityScoreCard from './projectVelocityScoreCard';
function ProjectScoreCards(_a) {
    var organization = _a.organization, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasSessions = _a.hasSessions, hasTransactions = _a.hasTransactions;
    return (<CardWrapper>
      <ProjectStabilityScoreCard organization={organization} selection={selection} isProjectStabilized={isProjectStabilized} hasSessions={hasSessions}/>

      <ProjectVelocityScoreCard organization={organization} selection={selection} isProjectStabilized={isProjectStabilized}/>

      <ProjectApdexScoreCard organization={organization} selection={selection} isProjectStabilized={isProjectStabilized} hasTransactions={hasTransactions}/>
    </CardWrapper>);
}
var CardWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  grid-column-gap: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n    grid-template-rows: repeat(3, 1fr);\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  grid-column-gap: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n    grid-template-rows: repeat(3, 1fr);\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
export default ProjectScoreCards;
var templateObject_1;
//# sourceMappingURL=projectScoreCards.jsx.map
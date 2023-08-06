import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import BadgeDisplayName from 'app/components/idBadge/badgeDisplayName';
import BaseBadge from 'app/components/idBadge/baseBadge';
import Link from 'app/components/links/link';
import withOrganization from 'app/utils/withOrganization';
var ProjectBadge = function (_a) {
    var project = _a.project, organization = _a.organization, _b = _a.hideOverflow, hideOverflow = _b === void 0 ? true : _b, _c = _a.disableLink, disableLink = _c === void 0 ? false : _c, props = __rest(_a, ["project", "organization", "hideOverflow", "disableLink"]);
    var slug = project.slug, id = project.id;
    var badge = (<BaseBadge displayName={<BadgeDisplayName hideOverflow={hideOverflow}>{slug}</BadgeDisplayName>} project={project} {...props}/>);
    if (!disableLink &&
        (organization === null || organization === void 0 ? void 0 : organization.features.includes('project-detail')) &&
        (organization === null || organization === void 0 ? void 0 : organization.features.includes('project-detail-links'))) {
        return (<StyledLink to={"/organizations/" + organization.slug + "/projects/" + slug + "/" + (id ? "?project=" + id : '')}>
        {badge}
      </StyledLink>);
    }
    return badge;
};
var StyledLink = styled(Link)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex-shrink: 0;\n\n  img:hover {\n    cursor: pointer;\n  }\n"], ["\n  flex-shrink: 0;\n\n  img:hover {\n    cursor: pointer;\n  }\n"])));
export default withOrganization(ProjectBadge);
var templateObject_1;
//# sourceMappingURL=projectBadge.jsx.map
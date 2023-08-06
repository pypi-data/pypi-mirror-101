import { __assign } from "tslib";
import React from 'react';
import Button from 'app/components/button';
import { extractSelectionParameters } from 'app/components/organizations/globalSelectionHeader/utils';
import { t } from 'app/locale';
var ProjectLink = function (_a) {
    var orgSlug = _a.orgSlug, releaseVersion = _a.releaseVersion, project = _a.project, location = _a.location;
    return (<Button size="xsmall" to={{
            pathname: "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(releaseVersion) + "/",
            query: __assign(__assign({}, extractSelectionParameters(location.query)), { project: project.id, yAxis: undefined }),
        }}>
    {t('View')}
  </Button>);
};
export default ProjectLink;
//# sourceMappingURL=projectLink.jsx.map
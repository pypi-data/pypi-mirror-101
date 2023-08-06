import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import { Panel } from 'app/components/panels';
import ReleaseStats from 'app/components/releaseStats';
import TextOverflow from 'app/components/textOverflow';
import TimeSince from 'app/components/timeSince';
import Version from 'app/components/version';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import ReleaseHealth from './releaseHealth';
function getReleaseProjectId(release, selection) {
    // if a release has only one project
    if (release.projects.length === 1) {
        return release.projects[0].id;
    }
    // if only one project is selected in global header and release has it (second condition will prevent false positives like -1)
    if (selection.projects.length === 1 &&
        release.projects.map(function (p) { return p.id; }).includes(selection.projects[0])) {
        return selection.projects[0];
    }
    // project selector on release detail page will pick it up
    return undefined;
}
var ReleaseCard = function (_a) {
    var release = _a.release, organization = _a.organization, activeDisplay = _a.activeDisplay, location = _a.location, reloading = _a.reloading, selection = _a.selection, showHealthPlaceholders = _a.showHealthPlaceholders, isTopRelease = _a.isTopRelease, getHealthData = _a.getHealthData;
    var version = release.version, commitCount = release.commitCount, lastDeploy = release.lastDeploy, dateCreated = release.dateCreated, versionInfo = release.versionInfo;
    return (<StyledPanel reloading={reloading ? 1 : 0}>
      <ReleaseInfo>
        <ReleaseInfoHeader>
          <GlobalSelectionLink to={{
            pathname: "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(version) + "/",
            query: { project: getReleaseProjectId(release, selection) },
        }}>
            <GuideAnchor disabled={!isTopRelease} target="release_version">
              <VersionWrapper>
                <StyledVersion version={version} tooltipRawVersion anchor={false}/>
              </VersionWrapper>
            </GuideAnchor>
          </GlobalSelectionLink>
          {commitCount > 0 && <ReleaseStats release={release} withHeading={false}/>}
        </ReleaseInfoHeader>
        <ReleaseInfoSubheader>
          {(versionInfo === null || versionInfo === void 0 ? void 0 : versionInfo.package) && (<PackageName ellipsisDirection="left">{versionInfo.package}</PackageName>)}
          <TimeSince date={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) || dateCreated}/>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) && " | " + lastDeploy.environment}
        </ReleaseInfoSubheader>
      </ReleaseInfo>

      <ReleaseProjects>
        <ReleaseHealth release={release} organization={organization} activeDisplay={activeDisplay} location={location} showPlaceholders={showHealthPlaceholders} reloading={reloading} selection={selection} isTopRelease={isTopRelease} getHealthData={getHealthData}/>
      </ReleaseProjects>
    </StyledPanel>);
};
var VersionWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledVersion = styled(Version)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var StyledPanel = styled(Panel)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  opacity: ", ";\n  pointer-events: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n  }\n"], ["\n  opacity: ", ";\n  pointer-events: ", ";\n\n  @media (min-width: ", ") {\n    display: flex;\n  }\n"])), function (p) { return (p.reloading ? 0.5 : 1); }, function (p) { return (p.reloading ? 'none' : 'auto'); }, function (p) { return p.theme.breakpoints[1]; });
var ReleaseInfo = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: ", " ", ";\n  flex-shrink: 0;\n\n  @media (min-width: ", ") {\n    border-right: 1px solid ", ";\n    min-width: 260px;\n    width: 22%;\n    max-width: 300px;\n  }\n"], ["\n  padding: ", " ", ";\n  flex-shrink: 0;\n\n  @media (min-width: ", ") {\n    border-right: 1px solid ", ";\n    min-width: 260px;\n    width: 22%;\n    max-width: 300px;\n  }\n"])), space(1.5), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.border; });
var ReleaseInfoSubheader = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray400; });
var PackageName = styled(TextOverflow)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.textColor; });
var ReleaseProjects = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  flex-grow: 1;\n  display: grid;\n\n  @media (min-width: ", ") {\n    border-top: none;\n  }\n"], ["\n  border-top: 1px solid ", ";\n  flex-grow: 1;\n  display: grid;\n\n  @media (min-width: ", ") {\n    border-top: none;\n  }\n"])), function (p) { return p.theme.border; }, function (p) { return p.theme.breakpoints[1]; });
var ReleaseInfoHeader = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  display: grid;\n  grid-template-columns: minmax(0, 1fr) max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  font-size: ", ";\n  display: grid;\n  grid-template-columns: minmax(0, 1fr) max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(2));
export default ReleaseCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=releaseCard.jsx.map
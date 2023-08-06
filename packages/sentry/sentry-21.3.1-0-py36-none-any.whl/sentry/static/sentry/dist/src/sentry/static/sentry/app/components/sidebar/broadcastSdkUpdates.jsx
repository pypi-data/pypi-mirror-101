import { __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import groupBy from 'lodash/groupBy';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import { t } from 'app/locale';
import space from 'app/styles/space';
import getSdkUpdateSuggestion from 'app/utils/getSdkUpdateSuggestion';
import withProjects from 'app/utils/withProjects';
import withSdkUpdates from 'app/utils/withSdkUpdates';
import Collapsible from '../collapsible';
import List from '../list';
import ListItem from '../list/listItem';
import SidebarPanelItem from './sidebarPanelItem';
var flattenSuggestions = function (list) {
    return list.reduce(function (suggestions, sdk) { return __spreadArray(__spreadArray([], __read(suggestions)), __read(sdk.suggestions)); }, []);
};
var BroadcastSdkUpdates = function (_a) {
    var projects = _a.projects, sdkUpdates = _a.sdkUpdates;
    if (!sdkUpdates) {
        return null;
    }
    // Are there any updates?
    if (flattenSuggestions(sdkUpdates).length === 0) {
        return null;
    }
    // Group SDK updates by project
    var items = Object.entries(groupBy(sdkUpdates, 'projectId'));
    return (<SidebarPanelItem hasSeen title={t('Update your SDKs')} message={t('Seems like your SDKs could use a refresh. We recommend updating these SDKs to make sure you’re getting all the data you need.')}>
      <UpdatesList>
        <Collapsible>
          {items.map(function (_a) {
            var _b = __read(_a, 2), projectId = _b[0], updates = _b[1];
            var project = projects.find(function (p) { return p.id === projectId; });
            if (project === undefined) {
                return null;
            }
            return (<div key={project.id}>
                <SdkProjectBadge project={project}/>
                <Suggestions>
                  {updates.map(function (sdkUpdate) { return (<div key={sdkUpdate.sdkName}>
                      <SdkName>
                        {sdkUpdate.sdkName}{' '}
                        <SdkOutdatedVersion>@v{sdkUpdate.sdkVersion}</SdkOutdatedVersion>
                      </SdkName>
                      <List>
                        {sdkUpdate.suggestions.map(function (suggestion, i) { return (<ListItem key={i}>
                            {getSdkUpdateSuggestion({
                            sdk: {
                                name: sdkUpdate.sdkName,
                                version: sdkUpdate.sdkVersion,
                            },
                            suggestion: suggestion,
                            shortStyle: true,
                        })}
                          </ListItem>); })}
                      </List>
                    </div>); })}
                </Suggestions>
              </div>);
        })}
        </Collapsible>
      </UpdatesList>
    </SidebarPanelItem>);
};
var UpdatesList = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n"], ["\n  margin-top: ", ";\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n"])), space(3), space(2));
var Suggestions = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n  margin-left: calc(", " + ", ");\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n"], ["\n  margin-top: ", ";\n  margin-left: calc(", " + ", ");\n  display: grid;\n  grid-auto-flow: row;\n  grid-gap: ", ";\n"])), space(1), space(4), space(0.25), space(1.5));
var SdkProjectBadge = styled(ProjectBadge)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var SdkName = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-family: ", ";\n  font-weight: bold;\n"], ["\n  font-family: ", ";\n  font-weight: bold;\n"])), function (p) { return p.theme.text.familyMono; });
var SdkOutdatedVersion = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
export default withSdkUpdates(withProjects(BroadcastSdkUpdates));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=broadcastSdkUpdates.jsx.map
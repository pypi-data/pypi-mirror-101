import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var IntegrationAlertRules = function (_a) {
    var projects = _a.projects, organization = _a.organization;
    return (<Panel>
    <PanelHeader>{t('Project Configuration')}</PanelHeader>
    <PanelBody>
      {projects.length === 0 && (<EmptyMessage size="large">
          {t('You have no projects to add Alert Rules to')}
        </EmptyMessage>)}
      {projects.map(function (project) { return (<ProjectItem key={project.slug}>
          <ProjectBadge project={project} avatarSize={16}/>
          <Button to={"/organizations/" + organization.slug + "/alerts/" + project.slug + "/new/"} size="xsmall">
            {t('Add Alert Rule')}
          </Button>
        </ProjectItem>); })}
    </PanelBody>
  </Panel>);
};
var ProjectItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  align-items: center;\n  justify-content: space-between;\n"])));
export default withOrganization(withProjects(IntegrationAlertRules));
var templateObject_1;
//# sourceMappingURL=integrationAlertRules.jsx.map
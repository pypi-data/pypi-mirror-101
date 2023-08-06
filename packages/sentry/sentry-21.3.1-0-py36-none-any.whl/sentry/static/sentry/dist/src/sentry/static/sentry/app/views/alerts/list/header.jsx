import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { navigateTo } from 'app/actionCreators/navigation';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import CreateAlertButton from 'app/components/createAlertButton';
import GlobalSelectionLink from 'app/components/globalSelectionLink';
import * as Layout from 'app/components/layouts/thirds';
import { IconSettings } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var AlertHeader = function (_a) {
    var router = _a.router, organization = _a.organization, activeTab = _a.activeTab;
    /**
     * Incidents list is currently at the organization level, but the link needs to
     * go down to a specific project scope.
     */
    var handleNavigateToSettings = function (e) {
        e.preventDefault();
        navigateTo("/settings/" + organization.slug + "/projects/:projectId/alerts/", router);
    };
    return (<React.Fragment>
      <BorderlessHeader>
        <StyledLayoutHeaderContent>
          <StyledLayoutTitle>{t('Alerts')}</StyledLayoutTitle>
        </StyledLayoutHeaderContent>
        <Layout.HeaderActions>
          <Actions gap={1}>
            <CreateAlertButton organization={organization} iconProps={{ size: 'sm' }} priority="primary" referrer="alert_stream" showPermissionGuide>
              {t('Create Alert Rule')}
            </CreateAlertButton>
            <Button onClick={handleNavigateToSettings} href="#" icon={<IconSettings size="sm"/>} aria-label="Settings"/>
          </Actions>
        </Layout.HeaderActions>
      </BorderlessHeader>
      <TabLayoutHeader>
        <Layout.HeaderNavTabs underlined>
          <Feature features={['incidents']} organization={organization}>
            <li className={activeTab === 'stream' ? 'active' : ''}>
              <GlobalSelectionLink to={"/organizations/" + organization.slug + "/alerts/"}>
                {t('Metric Alerts')}
              </GlobalSelectionLink>
            </li>
          </Feature>
          <li className={activeTab === 'rules' ? 'active' : ''}>
            <GlobalSelectionLink to={"/organizations/" + organization.slug + "/alerts/rules/"}>
              {t('Alert Rules')}
            </GlobalSelectionLink>
          </li>
        </Layout.HeaderNavTabs>
      </TabLayoutHeader>
    </React.Fragment>);
};
export default AlertHeader;
var BorderlessHeader = styled(Layout.Header)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for mobile view */\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"], ["\n  border-bottom: 0;\n\n  /* Not enough buttons to change direction for mobile view */\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledLayoutHeaderContent = styled(Layout.HeaderContent)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: 0;\n  margin-right: ", ";\n"], ["\n  margin-bottom: 0;\n  margin-right: ", ";\n"])), space(2));
var StyledLayoutTitle = styled(Layout.Title)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(0.5));
var TabLayoutHeader = styled(Layout.Header)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding-top: ", ";\n\n  @media (max-width: ", ") {\n    padding-top: ", ";\n  }\n"], ["\n  padding-top: ", ";\n\n  @media (max-width: ", ") {\n    padding-top: ", ";\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[1]; }, space(1));
var Actions = styled(ButtonBar)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  height: 32px;\n"], ["\n  height: 32px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=header.jsx.map
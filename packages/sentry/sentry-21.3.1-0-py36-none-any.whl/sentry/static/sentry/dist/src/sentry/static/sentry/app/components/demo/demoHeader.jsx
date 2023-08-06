import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import ExternalLink from 'app/components/links/externalLink';
import { IconSentryFull } from 'app/icons';
import { t } from 'app/locale';
import OrganizationStore from 'app/stores/organizationStore';
import space from 'app/styles/space';
import { trackAdvancedAnalyticsEvent } from 'app/utils/advancedAnalytics';
function DemoHeader(_a) {
    var organization = _a.organization;
    return (<Wrapper>
      <LogoSvg />
      <ButtonBar gap={4}>
        <StyledExternalLink href="https://docs.sentry.io">
          {t('Documentation')}
        </StyledExternalLink>
        <GetStarted onClick={function () {
            return trackAdvancedAnalyticsEvent('growth.demo_click_get_started', {}, organization);
        }} href="https://sentry.io/signup/">
          {t('Sign Up')}
        </GetStarted>
      </ButtonBar>
    </Wrapper>);
}
//can't use withOrganization here since we aren't within the OrganizationContext
export default createReactClass({
    displayName: 'DemoHeader',
    mixins: [Reflux.connect(OrganizationStore, 'organization')],
    render: function () {
        var _a;
        var organization = (_a = this.state.organization) === null || _a === void 0 ? void 0 : _a.organization;
        return <DemoHeader organization={organization}/>;
    },
});
//Note many of the colors don't come from the theme as they come from the marketing site
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-right: ", ";\n  background-color: ", ";\n  height: ", ";\n  display: flex;\n  justify-content: space-between;\n  text-transform: uppercase;\n  margin-left: calc(-1 * ", ");\n  position: fixed;\n  width: 100%;\n  border-bottom: 1px solid ", ";\n  z-index: ", ";\n\n  @media (max-width: ", ") {\n    height: ", ";\n    margin-left: 0;\n  }\n"], ["\n  padding-right: ", ";\n  background-color: ", ";\n  height: ", ";\n  display: flex;\n  justify-content: space-between;\n  text-transform: uppercase;\n  margin-left: calc(-1 * ", ");\n  position: fixed;\n  width: 100%;\n  border-bottom: 1px solid ", ";\n  z-index: ", ";\n\n  @media (max-width: ", ") {\n    height: ", ";\n    margin-left: 0;\n  }\n"])), space(3), function (p) { return p.theme.white; }, function (p) { return p.theme.demo.headerSize; }, function (p) { return p.theme.sidebar.expandedWidth; }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.settingsSidebarNav; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.sidebar.mobileHeight; });
var LogoSvg = styled(IconSentryFull)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: auto;\n  margin-bottom: auto;\n  margin-left: 20px;\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"], ["\n  margin-top: auto;\n  margin-bottom: auto;\n  margin-left: 20px;\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var GetStarted = styled(Button)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background-color: #e1567c;\n  color: #fff;\n  box-shadow: 0 2px 0 rgb(54 45 89 / 10%);\n  border-color: transparent;\n  border-radius: 2rem;\n  text-transform: uppercase;\n"], ["\n  background-color: #e1567c;\n  color: #fff;\n  box-shadow: 0 2px 0 rgb(54 45 89 / 10%);\n  border-color: transparent;\n  border-radius: 2rem;\n  text-transform: uppercase;\n"])));
var StyledExternalLink = styled(ExternalLink)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: #584774;\n"], ["\n  color: #584774;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=demoHeader.jsx.map
import { __assign, __extends, __makeTemplateObject } from "tslib";
import 'prism-sentry/index.css';
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import platforms from 'app/data/platforms';
import { t } from 'app/locale';
import { PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import withOrganization from 'app/utils/withOrganization';
import FirstEventFooter from 'app/views/onboarding/components/firstEventFooter';
import AddInstallationInstructions from 'app/views/onboarding/components/integrations/addInstallationInstructions';
import PostInstallCodeSnippet from 'app/views/onboarding/components/integrations/postInstallCodeSnippet';
import AddIntegrationButton from 'app/views/organizationIntegrations/addIntegrationButton';
import PlatformHeaderButtonBar from './components/platformHeaderButtonBar';
var PlatformIntegrationSetup = /** @class */ (function (_super) {
    __extends(PlatformIntegrationSetup, _super);
    function PlatformIntegrationSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAddIntegration = function () {
            _this.setState({ installed: true });
        };
        _this.trackSwitchToManual = function () {
            var _a = _this.props, organization = _a.organization, integrationSlug = _a.integrationSlug;
            trackIntegrationEvent('integrations.switch_manual_sdk_setup', {
                integration_type: 'first_party',
                integration: integrationSlug,
                view: 'project_creation',
            }, organization);
        };
        return _this;
    }
    PlatformIntegrationSetup.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { installed: false, integrations: { providers: [] }, project: null });
    };
    PlatformIntegrationSetup.prototype.componentDidMount = function () {
        window.scrollTo(0, 0);
        var platform = this.props.params.platform;
        //redirect if platform is not known.
        if (!platform || platform === 'other') {
            this.redirectToNeutralDocs();
        }
    };
    Object.defineProperty(PlatformIntegrationSetup.prototype, "provider", {
        get: function () {
            var providers = this.state.integrations.providers;
            return providers.length ? providers[0] : null;
        },
        enumerable: false,
        configurable: true
    });
    PlatformIntegrationSetup.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, integrationSlug = _a.integrationSlug, params = _a.params;
        if (!integrationSlug) {
            return [];
        }
        return [
            [
                'integrations',
                "/organizations/" + organization.slug + "/config/integrations/?provider_key=" + integrationSlug,
            ],
            ['project', "/projects/" + organization.slug + "/" + params.projectId + "/"],
        ];
    };
    PlatformIntegrationSetup.prototype.redirectToNeutralDocs = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        var url = "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/";
        browserHistory.push(url);
    };
    PlatformIntegrationSetup.prototype.render = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        var _b = this.state, installed = _b.installed, project = _b.project;
        var projectId = params.projectId, orgId = params.orgId, platform = params.platform;
        var provider = this.provider;
        var platformIntegration = platforms.find(function (p) { return p.id === platform; });
        if (!provider || !platformIntegration || !project) {
            return null;
        }
        var gettingStartedLink = "/organizations/" + orgId + "/projects/" + projectId + "/getting-started/";
        //TODO: make dynamic when adding more integrations
        var docsLink = 'https://docs.sentry.io/product/integrations/aws-lambda/';
        return (<OuterWrapper>
        <StyledPageHeader>
          <StyledTitle>
            {t('Automatically instrument %s', platformIntegration.name)}
          </StyledTitle>
          <PlatformHeaderButtonBar gettingStartedLink={gettingStartedLink} docsLink={docsLink}/>
        </StyledPageHeader>
        <InnerWrapper>
          {!installed ? (<React.Fragment>
              <AddInstallationInstructions />
              <StyledButtonBar gap={1}>
                <AddIntegrationButton provider={provider} onAddIntegration={this.handleAddIntegration} organization={organization} priority="primary" size="small" analyticsParams={{ view: 'project_creation', already_installed: false }} modalParams={{ projectId: project.id }}/>
                <Button size="small" to={{
                    pathname: window.location.pathname,
                    query: { manual: '1' },
                }} onClick={this.trackSwitchToManual}>
                  {t('Manual Setup')}
                </Button>
              </StyledButtonBar>
            </React.Fragment>) : (<React.Fragment>
              <PostInstallCodeSnippet provider={provider}/>
              <FirstEventFooter project={project} organization={organization} docsLink={docsLink}/>
            </React.Fragment>)}
        </InnerWrapper>
      </OuterWrapper>);
    };
    return PlatformIntegrationSetup;
}(AsyncComponent));
var StyledButtonBar = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"])), space(3), function (p) { return p.theme.breakpoints[0]; }, space(1));
var InnerWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 850px;\n"], ["\n  width: 850px;\n"])));
var OuterWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-top: 50px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-top: 50px;\n"])));
var StyledPageHeader = styled(PageHeader)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
var StyledTitle = styled('h2')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: 0 ", " 0 0;\n"], ["\n  margin: 0 ", " 0 0;\n"])), space(3));
export default withOrganization(PlatformIntegrationSetup);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=platformIntegrationSetup.jsx.map
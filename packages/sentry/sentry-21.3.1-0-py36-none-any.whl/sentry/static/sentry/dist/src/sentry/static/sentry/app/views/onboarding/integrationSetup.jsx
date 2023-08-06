import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import 'prism-sentry/index.css';
import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import LoadingError from 'app/components/loadingError';
import platforms from 'app/data/platforms';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import getDynamicText from 'app/utils/getDynamicText';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import AddIntegrationButton from 'app/views/organizationIntegrations/addIntegrationButton';
import FirstEventFooter from './components/firstEventFooter';
import AddInstallationInstructions from './components/integrations/addInstallationInstructions';
import PostInstallCodeSnippet from './components/integrations/postInstallCodeSnippet';
import SetupIntroduction from './components/setupIntroduction';
var recordAnalyticsDocsClicked = function (_a) {
    var organization = _a.organization, project = _a.project, platform = _a.platform;
    return analytics('onboarding_v2.full_docs_clicked', {
        org_id: organization.id,
        project: project === null || project === void 0 ? void 0 : project.slug,
        platform: platform,
    });
};
var IntegrationSetup = /** @class */ (function (_super) {
    __extends(IntegrationSetup, _super);
    function IntegrationSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loadedPlatform: null,
            hasError: false,
            provider: null,
            installed: false,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, platform, integrationSlug, endpoint, integrations, provider, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization, platform = _a.platform, integrationSlug = _a.integrationSlug;
                        if (!integrationSlug) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        endpoint = "/organizations/" + organization.slug + "/config/integrations/?provider_key=" + integrationSlug;
                        return [4 /*yield*/, api.requestPromise(endpoint)];
                    case 2:
                        integrations = _b.sent();
                        provider = integrations.providers[0];
                        this.setState({ provider: provider, loadedPlatform: platform, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({ hasError: error_1 });
                        throw error_1;
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleFullDocsClick = function () {
            var _a = _this.props, organization = _a.organization, project = _a.project, platform = _a.platform;
            recordAnalyticsDocsClicked({ organization: organization, project: project, platform: platform });
        };
        _this.trackSwitchToManual = function () {
            var _a = _this.props, organization = _a.organization, integrationSlug = _a.integrationSlug;
            trackIntegrationEvent('integrations.switch_manual_sdk_setup', {
                integration_type: 'first_party',
                integration: integrationSlug,
                view: 'onboarding',
            }, organization);
        };
        _this.handleAddIntegration = function () {
            _this.setState({ installed: true });
        };
        _this.renderSetupInstructions = function () {
            var _a, _b, _c;
            var platform = _this.props.platform;
            var loadedPlatform = _this.state.loadedPlatform;
            var currentPlatform = (_a = loadedPlatform !== null && loadedPlatform !== void 0 ? loadedPlatform : platform) !== null && _a !== void 0 ? _a : 'other';
            return (<SetupIntroduction stepHeaderText={t('Automatically instrument %s', (_c = (_b = platforms.find(function (p) { return p.id === currentPlatform; })) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '')} platform={currentPlatform}/>);
        };
        return _this;
    }
    IntegrationSetup.prototype.componentDidMount = function () {
        this.fetchData();
    };
    IntegrationSetup.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.platform !== this.props.platform ||
            nextProps.project !== this.props.project) {
            this.fetchData();
        }
    };
    Object.defineProperty(IntegrationSetup.prototype, "manualSetupUrl", {
        get: function () {
            var search = window.location.search;
            // honor any existing query params
            var separator = search.includes('?') ? '&' : '?';
            return "" + search + separator + "manual=1";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationSetup.prototype, "platformDocs", {
        get: function () {
            // TODO: make dynamic based on the integration
            return 'https://docs.sentry.io/product/integrations/aws-lambda/';
        },
        enumerable: false,
        configurable: true
    });
    IntegrationSetup.prototype.renderIntegrationInstructions = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var provider = this.state.provider;
        if (!provider || !project) {
            return null;
        }
        return (<React.Fragment>
        {this.renderSetupInstructions()}
        <motion.p variants={{
                initial: { opacity: 0 },
                animate: { opacity: 1 },
                exit: { opacity: 0 },
            }}>
          {tct("Don't have have permissions to create a Cloudformation stack? [link:Invite your team instead].", {
                link: <Button priority="link" onClick={openInviteMembersModal}/>,
            })}
        </motion.p>
        <motion.div variants={{
                initial: { opacity: 0 },
                animate: { opacity: 1 },
                exit: { opacity: 0 },
            }}>
          <AddInstallationInstructions />
        </motion.div>

        <DocsWrapper>
          <StyledButtonBar gap={1}>
            <AddIntegrationButton provider={provider} onAddIntegration={this.handleAddIntegration} organization={organization} priority="primary" size="small" analyticsParams={{ view: 'onboarding', already_installed: false }} modalParams={{ projectId: project.id }}/>
            <Button size="small" to={{
                pathname: window.location.pathname,
                query: { manual: '1' },
            }} onClick={this.trackSwitchToManual}>
              {t('Manual Setup')}
            </Button>
          </StyledButtonBar>
        </DocsWrapper>
      </React.Fragment>);
    };
    IntegrationSetup.prototype.renderPostInstallInstructions = function () {
        var _a = this.props, organization = _a.organization, project = _a.project, platform = _a.platform;
        var provider = this.state.provider;
        if (!project || !provider || !platform) {
            return null;
        }
        return (<React.Fragment>
        {this.renderSetupInstructions()}
        <PostInstallCodeSnippet provider={provider} platform={platform} isOnboarding/>
        <FirstEventFooter project={project} organization={organization} docsLink={this.platformDocs} docsOnClick={this.handleFullDocsClick}/>
      </React.Fragment>);
    };
    IntegrationSetup.prototype.render = function () {
        var platform = this.props.platform;
        var hasError = this.state.hasError;
        var loadingError = (<LoadingError message={t('Failed to load the integration for the %s platform.', platform)} onRetry={this.fetchData}/>);
        var testOnlyAlert = (<Alert type="warning">
        Platform documentation is not rendered in for tests in CI
      </Alert>);
        return (<React.Fragment>
        {this.state.installed
                ? this.renderPostInstallInstructions()
                : this.renderIntegrationInstructions()}
        {getDynamicText({
                value: !hasError ? null : loadingError,
                fixed: testOnlyAlert,
            })}
      </React.Fragment>);
    };
    return IntegrationSetup;
}(React.Component));
var DocsWrapper = styled(motion.div)(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
var StyledButtonBar = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-top: ", ";\n  width: max-content;\n\n  @media (max-width: ", ") {\n    width: auto;\n    grid-row-gap: ", ";\n    grid-auto-flow: row;\n  }\n"])), space(3), function (p) { return p.theme.breakpoints[0]; }, space(1));
export default withOrganization(withApi(IntegrationSetup));
var templateObject_1, templateObject_2;
//# sourceMappingURL=integrationSetup.jsx.map
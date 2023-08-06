import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import sortBy from 'lodash/sortBy';
import * as qs from 'query-string';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import Alert from 'app/components/alert';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import RepositoryProjectPathConfigForm from 'app/components/repositoryProjectPathConfigForm';
import RepositoryProjectPathConfigRow, { ButtonColumn, InputPathColumn, NameRepoColumn, OutputPathColumn, } from 'app/components/repositoryProjectPathConfigRow';
import { IconAdd, IconInfo } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { getIntegrationIcon, trackIntegrationEvent } from 'app/utils/integrationUtil';
import withOrganization from 'app/utils/withOrganization';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import TextBlock from 'app/views/settings/components/text/textBlock';
var IntegrationCodeMappings = /** @class */ (function (_super) {
    __extends(IntegrationCodeMappings, _super);
    function IntegrationCodeMappings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (pathConfig) { return __awaiter(_this, void 0, void 0, function () {
            var organization, endpoint, pathConfigs, _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        organization = this.props.organization;
                        endpoint = "/organizations/" + organization.slug + "/code-mappings/" + pathConfig.id + "/";
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(endpoint, {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        pathConfigs = this.state.pathConfigs;
                        pathConfigs = pathConfigs.filter(function (config) { return config.id !== pathConfig.id; });
                        this.setState({ pathConfigs: pathConfigs });
                        addSuccessMessage(t('Deletion successful'));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        //no 4xx errors should happen on delete
                        addErrorMessage(t('An error occurred'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubmitSuccess = function (pathConfig) {
            trackIntegrationEvent('integrations.stacktrace_complete_setup', {
                setup_type: 'manual',
                view: 'integration_configuration_detail',
                provider: _this.props.integration.provider.key,
            }, _this.props.organization);
            var pathConfigs = _this.state.pathConfigs;
            pathConfigs = pathConfigs.filter(function (config) { return config.id !== pathConfig.id; });
            // our getter handles the order of the configs
            pathConfigs = pathConfigs.concat([pathConfig]);
            _this.setState({ pathConfigs: pathConfigs });
            _this.setState({ pathConfig: undefined });
        };
        _this.openModal = function (pathConfig) {
            var _a = _this.props, organization = _a.organization, integration = _a.integration;
            trackIntegrationEvent('integrations.stacktrace_start_setup', {
                setup_type: 'manual',
                view: 'integration_configuration_detail',
                provider: _this.props.integration.provider.key,
            }, _this.props.organization);
            openModal(function (_a) {
                var Body = _a.Body, Header = _a.Header, closeModal = _a.closeModal;
                return (<React.Fragment>
        <Header closeButton>{t('Configure code path mapping')}</Header>
        <Body>
          <RepositoryProjectPathConfigForm organization={organization} integration={integration} projects={_this.projects} repos={_this.repos} onSubmitSuccess={function (config) {
                        _this.handleSubmitSuccess(config);
                        closeModal();
                    }} existingConfig={pathConfig} onCancel={closeModal}/>
        </Body>
      </React.Fragment>);
            });
        };
        return _this;
    }
    IntegrationCodeMappings.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { pathConfigs: [], repos: [] });
    };
    Object.defineProperty(IntegrationCodeMappings.prototype, "integrationId", {
        get: function () {
            return this.props.integration.id;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "projects", {
        get: function () {
            return this.props.organization.projects;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "pathConfigs", {
        get: function () {
            // we want to sort by the project slug and the
            // id of the config
            return sortBy(this.state.pathConfigs, [
                function (_a) {
                    var projectSlug = _a.projectSlug;
                    return projectSlug;
                },
                function (_a) {
                    var id = _a.id;
                    return parseInt(id, 10);
                },
            ]);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationCodeMappings.prototype, "repos", {
        get: function () {
            var _this = this;
            //endpoint doesn't support loading only the repos for this integration
            //but most people only have one source code repo so this should be fine
            return this.state.repos.filter(function (repo) { return repo.integrationId === _this.integrationId; });
        },
        enumerable: false,
        configurable: true
    });
    IntegrationCodeMappings.prototype.getEndpoints = function () {
        var orgSlug = this.props.organization.slug;
        return [
            [
                'pathConfigs',
                "/organizations/" + orgSlug + "/code-mappings/",
                { query: { integrationId: this.integrationId } },
            ],
            ['repos', "/organizations/" + orgSlug + "/repos/", { query: { status: 'active' } }],
        ];
    };
    IntegrationCodeMappings.prototype.getMatchingProject = function (pathConfig) {
        return this.projects.find(function (project) { return project.id === pathConfig.projectId; });
    };
    IntegrationCodeMappings.prototype.componentDidMount = function () {
        var referrer = (qs.parse(window.location.search) || {}).referrer;
        // We don't start new session if the user was coming from choosing
        // the manual setup option flow from the issue details page
        var startSession = referrer === 'stacktrace-issue-details' ? false : true;
        trackIntegrationEvent('integrations.code_mappings_viewed', {
            integration: this.props.integration.provider.key,
            integration_type: 'first_party',
        }, this.props.organization, { startSession: startSession });
    };
    IntegrationCodeMappings.prototype.renderBody = function () {
        var _this = this;
        var pathConfigs = this.pathConfigs;
        var integration = this.props.integration;
        return (<React.Fragment>
        <Alert type="info" icon={<IconInfo />}>
          {tct('Got feedback? Email [email:ecosystem-feedback@sentry.io].', {
                email: <a href="mailto:ecosystem-feedback@sentry.io"/>,
            })}
        </Alert>
        <TextBlock>
          {tct("Code Mappings are used to map stack trace file paths to source code file paths. These mappings are the basis for features like Stack Trace Linking. To learn more, [link: read the docs].", {
                link: (<ExternalLink href="https://docs.sentry.io/product/integrations/gitlab/#stack-trace-linking"/>),
            })}
        </TextBlock>

        <Panel>
          <PanelHeader disablePadding hasButtons>
            <HeaderLayout>
              <NameRepoColumn>{t('Code Mappings')}</NameRepoColumn>
              <InputPathColumn>{t('Stack Trace Root')}</InputPathColumn>
              <OutputPathColumn>{t('Source Code Root')}</OutputPathColumn>
              <ButtonColumn>
                <AddButton onClick={function () { return _this.openModal(); }} size="xsmall" icon={<IconAdd size="xs" isCircled/>}>
                  {t('Add Mapping')}
                </AddButton>
              </ButtonColumn>
            </HeaderLayout>
          </PanelHeader>
          <PanelBody>
            {pathConfigs.length === 0 && (<EmptyMessage icon={getIntegrationIcon(integration.provider.key, 'lg')} action={<Button href={"https://docs.sentry.io/product/integrations/" + integration.provider.key + "/#stack-trace-linking"} size="small" onClick={function () {
                        trackIntegrationEvent('integrations.stacktrace_docs_clicked', {
                            view: 'integration_configuration_detail',
                            provider: _this.props.integration.provider.key,
                        }, _this.props.organization);
                    }}>
                    View Documentation
                  </Button>}>
                Set up stack trace linking by adding a code mapping.
              </EmptyMessage>)}
            {pathConfigs
                .map(function (pathConfig) {
                var project = _this.getMatchingProject(pathConfig);
                // this should never happen since our pathConfig would be deleted
                // if project was deleted
                if (!project) {
                    return null;
                }
                return (<ConfigPanelItem key={pathConfig.id}>
                    <Layout>
                      <RepositoryProjectPathConfigRow pathConfig={pathConfig} project={project} onEdit={_this.openModal} onDelete={_this.handleDelete}/>
                    </Layout>
                  </ConfigPanelItem>);
            })
                .filter(function (item) { return !!item; })}
          </PanelBody>
        </Panel>
      </React.Fragment>);
    };
    return IntegrationCodeMappings;
}(AsyncComponent));
export default withOrganization(IntegrationCodeMappings);
var AddButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var Layout = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 4.5fr 2.5fr 2.5fr 1.6fr;\n  grid-template-areas: 'name-repo input-path output-path button';\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n  width: 100%;\n  align-items: center;\n  grid-template-columns: 4.5fr 2.5fr 2.5fr 1.6fr;\n  grid-template-areas: 'name-repo input-path output-path button';\n"])), space(1));
var HeaderLayout = styled(Layout)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  align-items: center;\n  margin: 0;\n  margin-left: ", ";\n"], ["\n  align-items: center;\n  margin: 0;\n  margin-left: ", ";\n"])), space(2));
var ConfigPanelItem = styled(PanelItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject([""], [""])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=integrationCodeMappings.jsx.map
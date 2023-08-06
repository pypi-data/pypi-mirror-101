import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { IconInfo } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { getIntegrationIcon, trackIntegrationEvent } from 'app/utils/integrationUtil';
import withApi from 'app/utils/withApi';
import InputField from 'app/views/settings/components/forms/inputField';
var StacktraceLinkModal = /** @class */ (function (_super) {
    __extends(StacktraceLinkModal, _super);
    function StacktraceLinkModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            sourceCodeInput: '',
        };
        _this.handleSubmit = function () { return __awaiter(_this, void 0, void 0, function () {
            var sourceCodeInput, _a, api, closeModal, filename, onSubmit, organization, project, parsingEndpoint, configData, configEndpoint, err_1, errors, apiErrors;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        sourceCodeInput = this.state.sourceCodeInput;
                        _a = this.props, api = _a.api, closeModal = _a.closeModal, filename = _a.filename, onSubmit = _a.onSubmit, organization = _a.organization, project = _a.project;
                        trackIntegrationEvent('integrations.stacktrace_submit_config', {
                            setup_type: 'automatic',
                            view: 'stacktrace_issue_details',
                        }, organization);
                        parsingEndpoint = "/projects/" + organization.slug + "/" + project.slug + "/repo-path-parsing/";
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 4, , 5]);
                        return [4 /*yield*/, api.requestPromise(parsingEndpoint, {
                                method: 'POST',
                                data: {
                                    sourceUrl: sourceCodeInput,
                                    stackPath: filename,
                                },
                            })];
                    case 2:
                        configData = _c.sent();
                        configEndpoint = "/organizations/" + organization.slug + "/code-mappings/";
                        return [4 /*yield*/, api.requestPromise(configEndpoint, {
                                method: 'POST',
                                data: __assign(__assign({}, configData), { projectId: project.id, integrationId: configData.integrationId }),
                            })];
                    case 3:
                        _c.sent();
                        addSuccessMessage(t('Stack trace configuration saved.'));
                        trackIntegrationEvent('integrations.stacktrace_complete_setup', {
                            setup_type: 'automatic',
                            provider: (_b = configData.config) === null || _b === void 0 ? void 0 : _b.provider.key,
                            view: 'stacktrace_issue_details',
                        }, organization);
                        closeModal();
                        onSubmit();
                        return [3 /*break*/, 5];
                    case 4:
                        err_1 = _c.sent();
                        errors = (err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            ? Array.isArray(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                                ? err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON
                                : Object.values(err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON)
                            : [];
                        apiErrors = errors.length > 0 ? ": " + errors.join(', ') : '';
                        addErrorMessage(t('Something went wrong%s', apiErrors));
                        return [3 /*break*/, 5];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    StacktraceLinkModal.prototype.onHandleChange = function (sourceCodeInput) {
        this.setState({
            sourceCodeInput: sourceCodeInput,
        });
    };
    StacktraceLinkModal.prototype.onManualSetup = function (provider) {
        trackIntegrationEvent('integrations.stacktrace_manual_option_clicked', {
            view: 'stacktrace_issue_details',
            setup_type: 'manual',
            provider: provider,
        }, this.props.organization);
    };
    StacktraceLinkModal.prototype.render = function () {
        var _this = this;
        var sourceCodeInput = this.state.sourceCodeInput;
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, filename = _a.filename, integrations = _a.integrations, organization = _a.organization;
        var baseUrl = "/settings/" + organization.slug + "/integrations";
        return (<React.Fragment>
        <Header closeButton>{t('Link Stack Trace To Source Code')}</Header>
        <Body>
          <ModalContainer>
            <div>
              <h6>{t('Automatic Setup')}</h6>
              {tct('Enter the source code URL corresponding to stack trace filename [filename] so we can automatically set up stack trace linking for this project.', {
                filename: <code>{filename}</code>,
            })}
            </div>
            <SourceCodeInput>
              <StyledInputField inline={false} flexibleControlStateSize stacked name="source-code-input" type="text" value={sourceCodeInput} onChange={function (val) { return _this.onHandleChange(val); }} placeholder={t("https://github.com/helloworld/Hello-World/blob/master/" + filename)}/>
              <ButtonBar>
                <Button data-test-id="quick-setup-button" type="button" onClick={function () { return _this.handleSubmit(); }}>
                  {t('Submit')}
                </Button>
              </ButtonBar>
            </SourceCodeInput>
            <div>
              <h6>{t('Manual Setup')}</h6>
              <Alert type="warning">
                {t('We recommend this for more complicated configurations, like projects with multiple repositories.')}
              </Alert>
              {t("To manually configure stack trace linking, select the integration you'd like to use for mapping:")}
            </div>
            <ManualSetup>
              {integrations.map(function (integration) { return (<Button key={integration.id} type="button" onClick={function () { return _this.onManualSetup(integration.provider.key); }} to={baseUrl + "/" + integration.provider.key + "/" + integration.id + "/?tab=codeMappings&referrer=stacktrace-issue-details"}>
                  {getIntegrationIcon(integration.provider.key)}
                  <IntegrationName>{integration.name}</IntegrationName>
                </Button>); })}
            </ManualSetup>
          </ModalContainer>
        </Body>
        <Footer>
          <Alert type="info" icon={<IconInfo />}>
            {tct('Got feedback? Email [email:ecosystem-feedback@sentry.io].', {
                email: <a href="mailto:ecosystem-feedback@sentry.io"/>,
            })}
          </Alert>
        </Footer>
      </React.Fragment>);
    };
    return StacktraceLinkModal;
}(React.Component));
var SourceCodeInput = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 5fr 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 5fr 1fr;\n  grid-gap: ", ";\n"])), space(1));
var ManualSetup = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  justify-items: center;\n"])), space(1));
var ModalContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"])), space(3));
var StyledInputField = styled(InputField)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: 0px;\n"], ["\n  padding: 0px;\n"])));
var IntegrationName = styled('p')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding-left: 10px;\n"], ["\n  padding-left: 10px;\n"])));
export default withApi(StacktraceLinkModal);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=stacktraceLinkModal.jsx.map
import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { openModal } from 'app/actionCreators/modal';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import Access from 'app/components/acl/access';
import AsyncComponent from 'app/components/asyncComponent';
import { Body, Header, Hovercard } from 'app/components/hovercard';
import { IconInfo } from 'app/icons';
import { IconClose } from 'app/icons/iconClose';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { getIntegrationIcon, trackIntegrationEvent } from 'app/utils/integrationUtil';
import { promptIsDismissed } from 'app/utils/promptIsDismissed';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { OpenInContainer, OpenInLink, OpenInName } from './openInContextLine';
import StacktraceLinkModal from './stacktraceLinkModal';
var StacktraceLink = /** @class */ (function (_super) {
    __extends(StacktraceLink, _super);
    function StacktraceLink() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmit = function () {
            _this.reloadData();
        };
        return _this;
    }
    Object.defineProperty(StacktraceLink.prototype, "project", {
        get: function () {
            // we can't use the withProject HoC on an the issue page
            // so we ge around that by using the withProjects HoC
            // and look up the project from the list
            var _a = this.props, projects = _a.projects, event = _a.event;
            return projects.find(function (project) { return project.id === event.projectID; });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "match", {
        get: function () {
            return this.state.match;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "config", {
        get: function () {
            return this.match.config;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "integrations", {
        get: function () {
            return this.match.integrations;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(StacktraceLink.prototype, "errorText", {
        get: function () {
            var error = this.match.error;
            switch (error) {
                case 'stack_root_mismatch':
                    return t('Error matching your configuration.');
                case 'file_not_found':
                    return t('Source file not found.');
                default:
                    return t('There was an error encountered with the code mapping for this project');
            }
        },
        enumerable: false,
        configurable: true
    });
    StacktraceLink.prototype.componentDidMount = function () {
        this.promptsCheck();
    };
    StacktraceLink.prototype.promptsCheck = function () {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            var organization, prompt;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        organization = this.props.organization;
                        return [4 /*yield*/, promptsCheck(this.api, {
                                organizationId: organization.id,
                                projectId: (_a = this.project) === null || _a === void 0 ? void 0 : _a.id,
                                feature: 'stacktrace_link',
                            })];
                    case 1:
                        prompt = _b.sent();
                        this.setState({
                            isDismissed: promptIsDismissed(prompt),
                            promptLoaded: true,
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    StacktraceLink.prototype.dismissPrompt = function () {
        var _a;
        var organization = this.props.organization;
        promptsUpdate(this.api, {
            organizationId: organization.id,
            projectId: (_a = this.project) === null || _a === void 0 ? void 0 : _a.id,
            feature: 'stacktrace_link',
            status: 'dismissed',
        });
        trackIntegrationEvent('integrations.stacktrace_link_cta_dismissed', {
            view: 'stacktrace_issue_details',
        }, this.props.organization);
        this.setState({ isDismissed: true });
    };
    StacktraceLink.prototype.getEndpoints = function () {
        var _a, _b;
        var _c = this.props, organization = _c.organization, frame = _c.frame, event = _c.event;
        var project = this.project;
        if (!project) {
            throw new Error('Unable to find project');
        }
        var commitId = (_b = (_a = event.release) === null || _a === void 0 ? void 0 : _a.lastCommit) === null || _b === void 0 ? void 0 : _b.id;
        var platform = event.platform;
        return [
            [
                'match',
                "/projects/" + organization.slug + "/" + project.slug + "/stacktrace-link/",
                { query: { file: frame.filename, platform: platform, commitId: commitId } },
            ],
        ];
    };
    StacktraceLink.prototype.onRequestError = function (error, args) {
        Sentry.withScope(function (scope) {
            scope.setExtra('errorInfo', args);
            Sentry.captureException(new Error(error));
        });
    };
    StacktraceLink.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { showModal: false, sourceCodeInput: '', match: { integrations: [] }, isDismissed: false, promptLoaded: false });
    };
    StacktraceLink.prototype.onOpenLink = function () {
        var _a;
        var provider = (_a = this.config) === null || _a === void 0 ? void 0 : _a.provider;
        if (provider) {
            trackIntegrationEvent('integrations.stacktrace_link_clicked', {
                view: 'stacktrace_issue_details',
                provider: provider.key,
            }, this.props.organization, { startSession: true });
        }
    };
    StacktraceLink.prototype.onReconfigureMapping = function () {
        var _a;
        var provider = (_a = this.config) === null || _a === void 0 ? void 0 : _a.provider;
        var error = this.match.error;
        if (provider) {
            trackIntegrationEvent('integrations.reconfigure_stacktrace_setup', {
                view: 'stacktrace_issue_details',
                provider: provider.key,
                error_reason: error,
            }, this.props.organization, { startSession: true });
        }
    };
    // don't show the error boundary if the component fails.
    // capture the endpoint error on onRequestError
    StacktraceLink.prototype.renderError = function () {
        return null;
    };
    StacktraceLink.prototype.renderLoading = function () {
        //TODO: Add loading
        return null;
    };
    StacktraceLink.prototype.renderNoMatch = function () {
        var _this = this;
        var organization = this.props.organization;
        var filename = this.props.frame.filename;
        var platform = this.props.event.platform;
        if (this.project && this.integrations.length > 0 && filename) {
            return (<Access organization={organization} access={['org:integrations']}>
          {function (_a) {
                    var hasAccess = _a.hasAccess;
                    return hasAccess && (<CodeMappingButtonContainer columnQuantity={2}>
                {tct('[link:Link your stack trace to your source code.]', {
                            link: (<a onClick={function () {
                                    trackIntegrationEvent('integrations.stacktrace_start_setup', {
                                        view: 'stacktrace_issue_details',
                                        platform: platform,
                                    }, _this.props.organization, { startSession: true });
                                    openModal(function (deps) {
                                        return _this.project && (<StacktraceLinkModal onSubmit={_this.handleSubmit} filename={filename} project={_this.project} organization={organization} integrations={_this.integrations} {...deps}/>);
                                    });
                                }}/>),
                        })}
                <StyledIconClose size="xs" onClick={function () { return _this.dismissPrompt(); }}/>
              </CodeMappingButtonContainer>);
                }}
        </Access>);
        }
        return null;
    };
    StacktraceLink.prototype.renderHovercard = function () {
        var error = this.match.error;
        var url = this.match.attemptedUrl;
        var frame = this.props.frame;
        var config = this.match.config;
        return (<React.Fragment>
        <StyledHovercard header={error === 'stack_root_mismatch' ? (<span>{t('Mismatch between filename and stack root')}</span>) : (<span>{t('Unable to find source code url')}</span>)} body={error === 'stack_root_mismatch' ? (<HeaderContainer>
                <HovercardLine>
                  filename: <code>{"" + frame.filename}</code>
                </HovercardLine>
                <HovercardLine>
                  stack root: <code>{"" + (config === null || config === void 0 ? void 0 : config.stackRoot)}</code>
                </HovercardLine>
              </HeaderContainer>) : (<HeaderContainer>
                <HovercardLine>{url}</HovercardLine>
              </HeaderContainer>)}>
          <StyledIconInfo size="xs"/>
        </StyledHovercard>
      </React.Fragment>);
    };
    StacktraceLink.prototype.renderMatchNoUrl = function () {
        var _this = this;
        var _a = this.match, config = _a.config, error = _a.error;
        var organization = this.props.organization;
        var url = "/settings/" + organization.slug + "/integrations/" + (config === null || config === void 0 ? void 0 : config.provider.key) + "/" + (config === null || config === void 0 ? void 0 : config.integrationId) + "/?tab=codeMappings";
        return (<CodeMappingButtonContainer columnQuantity={2}>
        <ErrorInformation>
          {error && this.renderHovercard()}
          <ErrorText>{this.errorText}</ErrorText>
          {tct('[link:Configure Stack Trace Linking] to fix this problem.', {
                link: (<a onClick={function () {
                        _this.onReconfigureMapping();
                    }} href={url}/>),
            })}
        </ErrorInformation>
      </CodeMappingButtonContainer>);
    };
    StacktraceLink.prototype.renderMatchWithUrl = function (config, url) {
        var _this = this;
        url = url + "#L" + this.props.frame.lineNo;
        return (<OpenInContainer columnQuantity={2}>
        <div>{t('Open this line in')}</div>
        <OpenInLink onClick={function () { return _this.onOpenLink(); }} href={url} openInNewTab>
          {getIntegrationIcon(config.provider.key)}
          <OpenInName>{config.provider.name}</OpenInName>
        </OpenInLink>
      </OpenInContainer>);
    };
    StacktraceLink.prototype.renderBody = function () {
        var _a = this.match || {}, config = _a.config, sourceUrl = _a.sourceUrl;
        var _b = this.state, isDismissed = _b.isDismissed, promptLoaded = _b.promptLoaded;
        if (config && sourceUrl) {
            return this.renderMatchWithUrl(config, sourceUrl);
        }
        if (config) {
            return this.renderMatchNoUrl();
        }
        if (!promptLoaded || (promptLoaded && isDismissed)) {
            return null;
        }
        return this.renderNoMatch();
    };
    return StacktraceLink;
}(AsyncComponent));
export default withProjects(withOrganization(StacktraceLink));
export { StacktraceLink };
export var CodeMappingButtonContainer = styled(OpenInContainer)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: space-between;\n"], ["\n  justify-content: space-between;\n"])));
var StyledIconClose = styled(IconClose)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: auto;\n  cursor: pointer;\n"], ["\n  margin: auto;\n  cursor: pointer;\n"])));
var StyledIconInfo = styled(IconInfo)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n  margin-bottom: -2px;\n  cursor: pointer;\n  line-height: 0;\n"], ["\n  margin-right: ", ";\n  margin-bottom: -2px;\n  cursor: pointer;\n  line-height: 0;\n"])), space(0.5));
var StyledHovercard = styled(Hovercard)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: normal;\n  width: inherit;\n  line-height: 0;\n  ", " {\n    font-weight: strong;\n    font-size: ", ";\n    color: ", ";\n  }\n  ", " {\n    font-weight: normal;\n    font-size: ", ";\n  }\n"], ["\n  font-weight: normal;\n  width: inherit;\n  line-height: 0;\n  ", " {\n    font-weight: strong;\n    font-size: ", ";\n    color: ", ";\n  }\n  ", " {\n    font-weight: normal;\n    font-size: ", ";\n  }\n"])), Header, function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; }, Body, function (p) { return p.theme.fontSizeSmall; });
var HeaderContainer = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  width: 100%;\n  display: flex;\n  justify-content: space-between;\n"], ["\n  width: 100%;\n  display: flex;\n  justify-content: space-between;\n"])));
var HovercardLine = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding-bottom: 3px;\n"], ["\n  padding-bottom: 3px;\n"])));
var ErrorInformation = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  padding-right: 5px;\n  margin-right: ", ";\n"], ["\n  padding-right: 5px;\n  margin-right: ", ";\n"])), space(1));
var ErrorText = styled('span')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=stacktraceLink.jsx.map
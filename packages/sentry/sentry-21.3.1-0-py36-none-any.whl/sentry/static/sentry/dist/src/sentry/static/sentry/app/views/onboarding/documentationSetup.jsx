import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import 'prism-sentry/index.css';
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import { loadDocs } from 'app/actionCreators/projects';
import Alert, { alertStyles } from 'app/components/alert';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import LoadingError from 'app/components/loadingError';
import platforms from 'app/data/platforms';
import { IconInfo } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import getDynamicText from 'app/utils/getDynamicText';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import FirstEventFooter from './components/firstEventFooter';
import SetupIntroduction from './components/setupIntroduction';
/**
 * The documentation will include the following string should it be missing the
 * verification example, which currently a lot of docs are.
 */
var INCOMPLETE_DOC_FLAG = 'TODO-ADD-VERIFICATION-EXAMPLE';
var recordAnalyticsDocsClicked = function (_a) {
    var organization = _a.organization, project = _a.project, platform = _a.platform;
    return analytics('onboarding_v2.full_docs_clicked', {
        org_id: organization.id,
        project: project === null || project === void 0 ? void 0 : project.slug,
        platform: platform,
    });
};
var DocumentationSetup = /** @class */ (function (_super) {
    __extends(DocumentationSetup, _super);
    function DocumentationSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            platformDocs: null,
            loadedPlatform: null,
            hasError: false,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, project, organization, platform, platformDocs, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, project = _a.project, organization = _a.organization, platform = _a.platform;
                        if (!project || !platform) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, loadDocs(api, organization.slug, project.slug, platform)];
                    case 2:
                        platformDocs = _b.sent();
                        this.setState({ platformDocs: platformDocs, loadedPlatform: platform, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        if (platform === 'other') {
                            // TODO(epurkhiser): There are currently no docs for the other
                            // platform. We should add generic documentation, in which case, this
                            // check should go away.
                            return [2 /*return*/];
                        }
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
        return _this;
    }
    DocumentationSetup.prototype.componentDidMount = function () {
        this.fetchData();
    };
    DocumentationSetup.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.platform !== this.props.platform ||
            nextProps.project !== this.props.project) {
            this.fetchData();
        }
    };
    Object.defineProperty(DocumentationSetup.prototype, "missingExampleWarning", {
        /**
         * TODO(epurkhiser): This can be removed once all documentation has an
         * example for sending the users first event.
         */
        get: function () {
            var _a;
            var _b = this.state, loadedPlatform = _b.loadedPlatform, platformDocs = _b.platformDocs;
            var missingExample = platformDocs && platformDocs.html.includes(INCOMPLETE_DOC_FLAG);
            if (!missingExample) {
                return null;
            }
            return (<Alert type="warning" icon={<IconInfo size="md"/>}>
        {tct("Looks like this getting started example is still undergoing some\n           work and doesn't include an example for triggering an event quite\n           yet. If you have trouble sending your first event be sure to consult\n           the [docsLink:full documentation] for [platform].", {
                    docsLink: <ExternalLink href={platformDocs === null || platformDocs === void 0 ? void 0 : platformDocs.link}/>,
                    platform: (_a = platforms.find(function (p) { return p.id === loadedPlatform; })) === null || _a === void 0 ? void 0 : _a.name,
                })}
      </Alert>);
        },
        enumerable: false,
        configurable: true
    });
    DocumentationSetup.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, organization = _d.organization, project = _d.project, platform = _d.platform;
        var _e = this.state, loadedPlatform = _e.loadedPlatform, platformDocs = _e.platformDocs, hasError = _e.hasError;
        var currentPlatform = (_a = loadedPlatform !== null && loadedPlatform !== void 0 ? loadedPlatform : platform) !== null && _a !== void 0 ? _a : 'other';
        var introduction = (<React.Fragment>
        <SetupIntroduction stepHeaderText={t('Prepare the %s SDK', (_c = (_b = platforms.find(function (p) { return p.id === currentPlatform; })) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '')} platform={currentPlatform}/>
        <motion.p variants={{
                initial: { opacity: 0 },
                animate: { opacity: 1 },
                exit: { opacity: 0 },
            }}>
          {tct("Don't have a relationship with your terminal? [link:Invite your team instead].", {
                link: (<Button priority="link" data-test-id="onboarding-getting-started-invite-members" onClick={openInviteMembersModal}/>),
            })}
        </motion.p>
      </React.Fragment>);
        var docs = platformDocs !== null && (<DocsWrapper key={platformDocs.html}>
        <Content dangerouslySetInnerHTML={{ __html: platformDocs.html }}/>
        {this.missingExampleWarning}

        {project && (<FirstEventFooter project={project} organization={organization} docsLink={platformDocs === null || platformDocs === void 0 ? void 0 : platformDocs.link} docsOnClick={this.handleFullDocsClick}/>)}
      </DocsWrapper>);
        var loadingError = (<LoadingError message={t('Failed to load documentation for the %s platform.', platform)} onRetry={this.fetchData}/>);
        var testOnlyAlert = (<Alert type="warning">
        Platform documentation is not rendered in for tests in CI
      </Alert>);
        return (<React.Fragment>
        {introduction}
        {getDynamicText({
                value: !hasError ? docs : loadingError,
                fixed: testOnlyAlert,
            })}
      </React.Fragment>);
    };
    return DocumentationSetup;
}(React.Component));
var getAlertSelector = function (type) {
    return type === 'muted' ? null : ".alert[level=\"" + type + "\"], .alert-" + type;
};
var mapAlertStyles = function (p, type) {
    return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n    ", " {\n      ", ";\n      display: block;\n    }\n  "], ["\n    ", " {\n      ", ";\n      display: block;\n    }\n  "])), getAlertSelector(type), alertStyles({ theme: p.theme, type: type }));
};
var Content = styled(motion.div)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6,\n  p {\n    margin-bottom: 18px;\n  }\n\n  div[data-language] {\n    margin-bottom: ", ";\n  }\n\n  code {\n    font-size: 87.5%;\n    color: ", ";\n  }\n\n  pre code {\n    color: inherit;\n    font-size: inherit;\n    white-space: pre;\n  }\n\n  h2 {\n    font-size: 1.4em;\n  }\n\n  .alert h5 {\n    font-size: 1em;\n    margin-bottom: 1rem;\n  }\n\n  /**\n   * XXX(epurkhiser): This comes from the doc styles and avoids bottom margin issues in alerts\n   */\n  .content-flush-bottom *:last-child {\n    margin-bottom: 0;\n  }\n\n  ", "\n"], ["\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6,\n  p {\n    margin-bottom: 18px;\n  }\n\n  div[data-language] {\n    margin-bottom: ", ";\n  }\n\n  code {\n    font-size: 87.5%;\n    color: ", ";\n  }\n\n  pre code {\n    color: inherit;\n    font-size: inherit;\n    white-space: pre;\n  }\n\n  h2 {\n    font-size: 1.4em;\n  }\n\n  .alert h5 {\n    font-size: 1em;\n    margin-bottom: 1rem;\n  }\n\n  /**\n   * XXX(epurkhiser): This comes from the doc styles and avoids bottom margin issues in alerts\n   */\n  .content-flush-bottom *:last-child {\n    margin-bottom: 0;\n  }\n\n  ", "\n"])), space(2), function (p) { return p.theme.pink300; }, function (p) { return Object.keys(p.theme.alert).map(function (type) { return mapAlertStyles(p, type); }); });
var DocsWrapper = styled(motion.div)(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
export default withOrganization(withApi(DocumentationSetup));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=documentationSetup.jsx.map
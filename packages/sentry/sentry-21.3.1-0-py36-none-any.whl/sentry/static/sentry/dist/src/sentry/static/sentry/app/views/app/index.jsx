import { __decorate, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import keydown from 'react-keydown';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import PropTypes from 'prop-types';
import { displayDeployPreviewAlert, displayExperimentalSpaAlert, } from 'app/actionCreators/deployPreview';
import { fetchGuides } from 'app/actionCreators/guides';
import { openCommandPalette } from 'app/actionCreators/modal';
import AlertActions from 'app/actions/alertActions';
import { initApiClientErrorHandling } from 'app/api';
import ErrorBoundary from 'app/components/errorBoundary';
import GlobalModal from 'app/components/globalModal';
import Indicators from 'app/components/indicators';
import LoadingIndicator from 'app/components/loadingIndicator';
import { DEPLOY_PREVIEW_CONFIG, EXPERIMENTAL_SPA } from 'app/constants';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import HookStore from 'app/stores/hookStore';
import OrganizationsStore from 'app/stores/organizationsStore';
import withApi from 'app/utils/withApi';
import withConfig from 'app/utils/withConfig';
import NewsletterConsent from 'app/views/newsletterConsent';
import SystemAlerts from './systemAlerts';
function getAlertTypeForProblem(problem) {
    switch (problem.severity) {
        case 'critical':
            return 'error';
        default:
            return 'warning';
    }
}
var App = /** @class */ (function (_super) {
    __extends(App, _super);
    function App() {
        var _a, _b, _c;
        var _this = _super.apply(this, __spreadArray([], __read(arguments))) || this;
        _this.state = {
            loading: false,
            error: false,
            needsUpgrade: ((_a = ConfigStore.get('user')) === null || _a === void 0 ? void 0 : _a.isSuperuser) && ConfigStore.get('needsUpgrade'),
            newsletterConsentPrompt: (_c = (_b = ConfigStore.get('user')) === null || _b === void 0 ? void 0 : _b.flags) === null || _c === void 0 ? void 0 : _c.newsletter_consent_prompt,
        };
        _this.mainContainerRef = React.createRef();
        _this.onConfigured = function () { return _this.setState({ needsUpgrade: false }); };
        // this is somewhat hackish
        _this.handleNewsletterConsent = function () {
            return _this.setState({
                newsletterConsentPrompt: false,
            });
        };
        _this.handleGlobalModalClose = function () {
            var _a;
            if (typeof ((_a = _this.mainContainerRef.current) === null || _a === void 0 ? void 0 : _a.focus) === 'function') {
                // Focus the main container to get hotkeys to keep working after modal closes
                _this.mainContainerRef.current.focus();
            }
        };
        return _this;
    }
    App.prototype.getChildContext = function () {
        return {
            location: this.props.location,
        };
    };
    App.prototype.componentDidMount = function () {
        var _this = this;
        this.props.api.request('/organizations/', {
            query: {
                member: '1',
            },
            success: function (data) {
                OrganizationsStore.load(data);
                _this.setState({
                    loading: false,
                });
            },
            error: function () {
                _this.setState({
                    loading: false,
                    error: true,
                });
            },
        });
        this.props.api.request('/internal/health/', {
            success: function (data) {
                if (data && data.problems) {
                    data.problems.forEach(function (problem) {
                        AlertActions.addAlert({
                            id: problem.id,
                            message: problem.message,
                            type: getAlertTypeForProblem(problem),
                            url: problem.url,
                        });
                    });
                }
            },
            error: function () { }, // TODO: do something?
        });
        ConfigStore.get('messages').forEach(function (msg) {
            AlertActions.addAlert({
                message: msg.message,
                type: msg.level,
                neverExpire: true,
            });
        });
        if (DEPLOY_PREVIEW_CONFIG) {
            displayDeployPreviewAlert();
        }
        else if (EXPERIMENTAL_SPA) {
            displayExperimentalSpaAlert();
        }
        initApiClientErrorHandling();
        var user = ConfigStore.get('user');
        if (user) {
            HookStore.get('analytics:init-user').map(function (cb) { return cb(user); });
        }
        fetchGuides();
    };
    App.prototype.componentDidUpdate = function (prevProps) {
        var config = this.props.config;
        if (!isEqual(config, prevProps.config)) {
            this.handleConfigStoreChange(config);
        }
    };
    App.prototype.componentWillUnmount = function () {
        OrganizationsStore.load([]);
    };
    App.prototype.handleConfigStoreChange = function (config) {
        var newState = {};
        if (config.needsUpgrade !== undefined) {
            newState.needsUpgrade = config.needsUpgrade;
        }
        if (config.user !== undefined) {
            newState.user = config.user;
        }
        if (Object.keys(newState).length > 0) {
            this.setState(newState);
        }
    };
    App.prototype.openCommandPalette = function (e) {
        openCommandPalette();
        e.preventDefault();
        e.stopPropagation();
    };
    App.prototype.toggleDarkMode = function () {
        ConfigStore.set('theme', ConfigStore.get('theme') === 'light' ? 'dark' : 'light');
    };
    App.prototype.renderBody = function () {
        var _a = this.state, needsUpgrade = _a.needsUpgrade, newsletterConsentPrompt = _a.newsletterConsentPrompt;
        if (needsUpgrade) {
            var InstallWizard = React.lazy(function () {
                return import(/* webpackChunkName: "InstallWizard" */ 'app/views/admin/installWizard');
            });
            return (<React.Suspense fallback={null}>
          <InstallWizard onConfigured={this.onConfigured}/>;
        </React.Suspense>);
        }
        if (newsletterConsentPrompt) {
            return <NewsletterConsent onSubmitSuccess={this.handleNewsletterConsent}/>;
        }
        return this.props.children;
    };
    App.prototype.render = function () {
        if (this.state.loading) {
            return (<LoadingIndicator triangle>
          {t('Getting a list of all of your organizations.')}
        </LoadingIndicator>);
        }
        return (<MainContainer tabIndex={-1} ref={this.mainContainerRef}>
        <GlobalModal onClose={this.handleGlobalModalClose}/>
        <SystemAlerts className="messages-container"/>
        <Indicators className="indicators-container"/>
        <ErrorBoundary>{this.renderBody()}</ErrorBoundary>
      </MainContainer>);
    };
    App.childContextTypes = {
        location: PropTypes.object,
    };
    __decorate([
        keydown('meta+shift+p', 'meta+k', 'ctrl+shift+p', 'ctrl+k')
    ], App.prototype, "openCommandPalette", null);
    __decorate([
        keydown('meta+shift+l', 'ctrl+shift+l')
    ], App.prototype, "toggleDarkMode", null);
    return App;
}(React.Component));
export default withApi(withConfig(App));
var MainContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  min-height: 100vh;\n  outline: none;\n  padding-top: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  min-height: 100vh;\n  outline: none;\n  padding-top: ", ";\n"])), function (p) { return (ConfigStore.get('demoMode') ? p.theme.demo.headerSize : 0); });
var templateObject_1;
//# sourceMappingURL=index.jsx.map
import { __awaiter, __extends, __generator, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import Alert from 'app/components/alert';
import SuggestProjectModal from 'app/components/modals/suggestProjectModal';
import { IconClose } from 'app/icons';
import { tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAdvancedAnalyticsEvent } from 'app/utils/advancedAnalytics';
import { promptIsDismissed } from 'app/utils/promptIsDismissed';
import withApi from 'app/utils/withApi';
import withProjects from 'app/utils/withProjects';
var MOBILE_PLATFORMS = [
    'react-native',
    'android',
    'cordova',
    'cocoa',
    'cocoa-swift',
    'apple-ios',
    'swift',
    'flutter',
    'xamarin',
    'dotnet-xamarin',
];
var MOBILE_USER_AGENTS = ['okhttp', 'CFNetwork', 'Alamofire', 'Dalvik'];
var SuggestProjectCTA = /** @class */ (function (_super) {
    __extends(SuggestProjectCTA, _super);
    function SuggestProjectCTA() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleCTAClose = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            trackAdvancedAnalyticsEvent('growth.dismissed_mobile_prompt_banner', {
                matchedUserAgentString: _this.matchedUserAgentString,
            }, _this.props.organization);
            promptsUpdate(api, {
                organizationId: organization.id,
                feature: 'suggest_mobile_project',
                status: 'dismissed',
            });
            _this.setState({ isDismissed: true });
        };
        _this.openModal = function () {
            trackAdvancedAnalyticsEvent('growth.opened_mobile_project_suggest_modal', {
                matchedUserAgentString: _this.matchedUserAgentString,
            }, _this.props.organization);
            openModal(function (deps) { return (<SuggestProjectModal organization={_this.props.organization} matchedUserAgentString={_this.matchedUserAgentString} {...deps}/>); });
        };
        return _this;
    }
    SuggestProjectCTA.prototype.componentDidMount = function () {
        this.fetchData();
    };
    Object.defineProperty(SuggestProjectCTA.prototype, "matchedUserAgentString", {
        //Returns the matched user agent string
        //otherwise, returns an empty string
        get: function () {
            var _a, _b, _c, _d;
            var entries = this.props.event.entries;
            var requestEntry = entries.find(function (item) { return item.type === 'request'; });
            if (!requestEntry) {
                return '';
            }
            //find the user agent header out of our list of headers
            var userAgent = (_c = (_b = (_a = requestEntry) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.headers) === null || _c === void 0 ? void 0 : _c.find(function (item) { return item[0].toLowerCase() === 'user-agent'; });
            if (!userAgent) {
                return '';
            }
            //check if any of our mobile agent headers matches the event mobile agent
            return ((_d = MOBILE_USER_AGENTS.find(function (mobileAgent) { var _a; return (_a = userAgent[1]) === null || _a === void 0 ? void 0 : _a.toLowerCase().includes(mobileAgent.toLowerCase()); })) !== null && _d !== void 0 ? _d : '');
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SuggestProjectCTA.prototype, "hasMobileProject", {
        //check our projects to see if there is a mobile project
        get: function () {
            return this.props.projects.some(function (project) {
                return MOBILE_PLATFORMS.includes(project.platform || '');
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SuggestProjectCTA.prototype, "hasMobileEvent", {
        //returns true if the current event is mobile from the user agent
        //or if we found a mobile event with the API
        get: function () {
            var mobileEventResult = this.state.mobileEventResult;
            return !!this.matchedUserAgentString || !!mobileEventResult;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SuggestProjectCTA.prototype, "showCTA", {
        /**
         * conditions to show prompt:
         * 1. Have a mobile event
         * 2. No mobile project
         * 3. CTA is not dimissed
         * 4. We've loaded the data from the backend for the prompt
         */
        get: function () {
            var _a = this.state, loaded = _a.loaded, isDismissed = _a.isDismissed;
            return !!(this.hasMobileEvent && !this.hasMobileProject && !isDismissed && loaded);
        },
        enumerable: false,
        configurable: true
    });
    SuggestProjectCTA.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, isDismissed, mobileEventResult;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, Promise.all([
                            this.checkMobilePrompt(),
                            this.checkOrgHasMobileEvent(),
                        ])];
                    case 1:
                        _a = __read.apply(void 0, [_b.sent(), 2]), isDismissed = _a[0], mobileEventResult = _a[1];
                        //set the new state
                        this.setState({
                            isDismissed: isDismissed,
                            mobileEventResult: mobileEventResult,
                            loaded: true,
                        }, function () {
                            var matchedUserAgentString = _this.matchedUserAgentString;
                            //now record the results
                            trackAdvancedAnalyticsEvent('growth.check_show_mobile_prompt_banner', {
                                matchedUserAgentString: matchedUserAgentString,
                                userAgentMatches: !!matchedUserAgentString,
                                hasMobileProject: _this.hasMobileProject,
                                snoozedOrDismissed: isDismissed,
                                mobileEventBrowserName: (mobileEventResult === null || mobileEventResult === void 0 ? void 0 : mobileEventResult.browserName) || '',
                                mobileEventClientOsName: (mobileEventResult === null || mobileEventResult === void 0 ? void 0 : mobileEventResult.clientOsName) || '',
                                showCTA: _this.showCTA,
                            }, _this.props.organization, { startSession: true });
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    SuggestProjectCTA.prototype.checkOrgHasMobileEvent = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization;
            return __generator(this, function (_b) {
                _a = this.props, api = _a.api, organization = _a.organization;
                return [2 /*return*/, api.requestPromise("/organizations/" + organization.slug + "/has-mobile-app-events/", {
                        query: {
                            userAgents: MOBILE_USER_AGENTS,
                        },
                    })];
            });
        });
    };
    SuggestProjectCTA.prototype.checkMobilePrompt = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, promptData;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, promptsCheck(api, {
                                organizationId: organization.id,
                                feature: 'suggest_mobile_project',
                            })];
                    case 1:
                        promptData = _b.sent();
                        return [2 /*return*/, promptIsDismissed(promptData)];
                }
            });
        });
    };
    SuggestProjectCTA.prototype.renderCTA = function () {
        return (<Alert type="info">
        <Content>
          <span>
            {tct('We have a sneaking suspicion you have a mobile app that doesn’t use Sentry. [link:Start Monitoring]', { link: <a onClick={this.openModal}/> })}
          </span>
          <StyledIconClose onClick={this.handleCTAClose}/>
        </Content>
      </Alert>);
    };
    SuggestProjectCTA.prototype.render = function () {
        return this.showCTA ? this.renderCTA() : null;
    };
    return SuggestProjectCTA;
}(React.Component));
export default withApi(withProjects(SuggestProjectCTA));
var Content = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n"])), space(1));
var StyledIconClose = styled(IconClose)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: auto;\n  cursor: pointer;\n"], ["\n  margin: auto;\n  cursor: pointer;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=suggestProjectCTA.jsx.map
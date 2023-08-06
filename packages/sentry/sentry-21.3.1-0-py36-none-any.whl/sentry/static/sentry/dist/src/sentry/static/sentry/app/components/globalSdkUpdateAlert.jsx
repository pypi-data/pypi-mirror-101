import { __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { promptsCheck, promptsUpdate } from 'app/actionCreators/prompts';
import SidebarPanelActions from 'app/actions/sidebarPanelActions';
import Alert from 'app/components/alert';
import { ALL_ACCESS_PROJECTS } from 'app/constants/globalSelectionHeader';
import { IconUpgrade } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { promptIsDismissed } from 'app/utils/promptIsDismissed';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withSdkUpdates from 'app/utils/withSdkUpdates';
import { SidebarPanelKey } from './sidebar/types';
import Button from './button';
var recordAnalyticsSeen = function (_a) {
    var organization = _a.organization;
    return trackAnalyticsEvent({
        eventKey: 'sdk_updates.seen',
        eventName: 'SDK Updates: Seen',
        organizationId: organization.id,
    });
};
var recordAnalyticsSnoozed = function (_a) {
    var organization = _a.organization;
    return trackAnalyticsEvent({
        eventKey: 'sdk_updates.snoozed',
        eventName: 'SDK Updates: Snoozed',
        organizationId: organization.id,
    });
};
var recordAnalyticsClicked = function (_a) {
    var organization = _a.organization;
    return trackAnalyticsEvent({
        eventKey: 'sdk_updates.clicked',
        eventName: 'SDK Updates: Clicked',
        organizationId: organization.id,
    });
};
var flattenSuggestions = function (list) {
    return list.reduce(function (suggestions, sdk) { return __spreadArray(__spreadArray([], __read(suggestions)), __read(sdk.suggestions)); }, []);
};
var InnerGlobalSdkSuggestions = /** @class */ (function (_super) {
    __extends(InnerGlobalSdkSuggestions, _super);
    function InnerGlobalSdkSuggestions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isDismissed: null,
        };
        _this.snoozePrompt = function () {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            promptsUpdate(api, {
                organizationId: organization.id,
                feature: 'sdk_updates',
                status: 'snoozed',
            });
            _this.setState({ isDismissed: true });
            recordAnalyticsSnoozed({ organization: _this.props.organization });
        };
        return _this;
    }
    InnerGlobalSdkSuggestions.prototype.componentDidMount = function () {
        this.promptsCheck();
        recordAnalyticsSeen({ organization: this.props.organization });
    };
    InnerGlobalSdkSuggestions.prototype.promptsCheck = function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, organization, prompt;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, promptsCheck(api, {
                                organizationId: organization.id,
                                feature: 'sdk_updates',
                            })];
                    case 1:
                        prompt = _b.sent();
                        this.setState({
                            isDismissed: promptIsDismissed(prompt),
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    InnerGlobalSdkSuggestions.prototype.render = function () {
        var _a = this.props, _api = _a.api, selection = _a.selection, sdkUpdates = _a.sdkUpdates, organization = _a.organization, Wrapper = _a.Wrapper, props = __rest(_a, ["api", "selection", "sdkUpdates", "organization", "Wrapper"]);
        var isDismissed = this.state.isDismissed;
        if (!sdkUpdates || isDismissed === null || isDismissed) {
            return null;
        }
        // withSdkUpdates explicitly only queries My Projects. This means that when
        // looking at any projects outside of My Projects (like All Projects), this
        // will only show the updates relevant to the to user.
        var projectSpecificUpdates = (selection === null || selection === void 0 ? void 0 : selection.projects.length) === 0 || (selection === null || selection === void 0 ? void 0 : selection.projects) === [ALL_ACCESS_PROJECTS]
            ? sdkUpdates
            : sdkUpdates.filter(function (update) { var _a; return (_a = selection === null || selection === void 0 ? void 0 : selection.projects) === null || _a === void 0 ? void 0 : _a.includes(parseInt(update.projectId, 10)); });
        // Are there any updates?
        if (flattenSuggestions(projectSpecificUpdates).length === 0) {
            return null;
        }
        var showBroadcastsPanel = (<Button priority="link" onClick={function () {
                SidebarPanelActions.activatePanel(SidebarPanelKey.Broadcasts);
                recordAnalyticsClicked({ organization: organization });
            }}/>);
        var notice = (<Alert type="info" icon={<IconUpgrade />} {...props}>
        <Content>
          {tct("Looks like some SDKs configured for the selected projects are out of date.\n             [showBroadcastsPanel:View upgrade suggestions]", { showBroadcastsPanel: showBroadcastsPanel })}
          <Button priority="link" title={t('Dismiss SDK update notifications for the next two weeks')} onClick={this.snoozePrompt}>
            {t('Remind me later')}
          </Button>
        </Content>
      </Alert>);
        return Wrapper ? <Wrapper>{notice}</Wrapper> : notice;
    };
    return InnerGlobalSdkSuggestions;
}(React.Component));
var Content = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n"])), space(1));
var GlobalSdkSuggestions = withOrganization(withSdkUpdates(withGlobalSelection(withApi(InnerGlobalSdkSuggestions))));
export default GlobalSdkSuggestions;
var templateObject_1;
//# sourceMappingURL=globalSdkUpdateAlert.jsx.map
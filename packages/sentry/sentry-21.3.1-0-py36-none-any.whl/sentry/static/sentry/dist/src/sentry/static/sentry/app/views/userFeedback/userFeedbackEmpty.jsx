import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import emptyStateImg from 'sentry-images/spot/feedback-empty-state.svg';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import OnboardingPanel from 'app/components/onboardingPanel';
import { t } from 'app/locale';
import { trackAdhocEvent, trackAnalyticsEvent } from 'app/utils/analytics';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
var UserFeedbackEmpty = /** @class */ (function (_super) {
    __extends(UserFeedbackEmpty, _super);
    function UserFeedbackEmpty() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UserFeedbackEmpty.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, projectIds = _a.projectIds;
        window.sentryEmbedCallback = function (embed) {
            // Mock the embed's submit xhr to always be successful
            // NOTE: this will not have errors if the form is empty
            embed.submit = function (_body) {
                var _this = this;
                this._submitInProgress = true;
                setTimeout(function () {
                    _this._submitInProgress = false;
                    _this.onSuccess();
                }, 500);
            };
        };
        if (this.hasAnyFeedback === false) {
            // send to reload only due to higher event volume
            trackAdhocEvent({
                eventKey: 'user_feedback.viewed',
                org_id: parseInt(organization.id, 10),
                projects: projectIds,
            });
        }
    };
    UserFeedbackEmpty.prototype.componentWillUnmount = function () {
        window.sentryEmbedCallback = null;
    };
    Object.defineProperty(UserFeedbackEmpty.prototype, "selectedProjects", {
        get: function () {
            var _a = this.props, projects = _a.projects, projectIds = _a.projectIds;
            return projectIds && projectIds.length
                ? projects.filter(function (_a) {
                    var id = _a.id;
                    return projectIds.includes(id);
                })
                : projects;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(UserFeedbackEmpty.prototype, "hasAnyFeedback", {
        get: function () {
            return this.selectedProjects.some(function (_a) {
                var hasUserReports = _a.hasUserReports;
                return hasUserReports;
            });
        },
        enumerable: false,
        configurable: true
    });
    UserFeedbackEmpty.prototype.trackAnalytics = function (_a) {
        var eventKey = _a.eventKey, eventName = _a.eventName;
        var _b = this.props, organization = _b.organization, projectIds = _b.projectIds;
        trackAnalyticsEvent({
            eventKey: eventKey,
            eventName: eventName,
            organization_id: organization.id,
            projects: projectIds,
        });
    };
    UserFeedbackEmpty.prototype.render = function () {
        var _this = this;
        var _a;
        // Show no user reports if waiting for projects to load or if there is no feedback
        if (this.props.loadingProjects || this.hasAnyFeedback !== false) {
            return (<EmptyStateWarning>
          <p>{t('Sorry, no user reports match your filters.')}</p>
        </EmptyStateWarning>);
        }
        // Show landing page after projects have loaded and it is confirmed no projects have feedback
        return (<OnboardingPanel image={<img src={emptyStateImg}/>}>
        <h3>{t('What do users think?')}</h3>
        <p>
          {t("You can't read minds. At least we hope not. Ask users for feedback on the impact of their crashes or bugs and you shall receive.")}
        </p>
        <ButtonList gap={1}>
          <Button external onClick={function () {
                return _this.trackAnalytics({
                    eventKey: 'user_feedback.docs_clicked',
                    eventName: 'User Feedback Docs Clicked',
                });
            }} href={"https://docs.sentry.io/platforms/" + (((_a = this.selectedProjects[0]) === null || _a === void 0 ? void 0 : _a.platform) || 'javascript') + "/enriching-events/user-feedback/"}>
            {t('Read the docs')}
          </Button>
          <Button priority="primary" onClick={function () {
                Sentry.showReportDialog({
                    // should never make it to the Sentry API, but just in case, use throwaway id
                    eventId: '00000000000000000000000000000000',
                });
                _this.trackAnalytics({
                    eventKey: 'user_feedback.dialog_opened',
                    eventName: 'User Feedback Dialog Opened',
                });
            }}>
            {t('Open Dialog')}
          </Button>
        </ButtonList>
      </OnboardingPanel>);
    };
    return UserFeedbackEmpty;
}(React.Component));
var ButtonList = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"], ["\n  grid-template-columns: repeat(auto-fit, minmax(130px, max-content));\n"])));
export { UserFeedbackEmpty };
export default withOrganization(withProjects(UserFeedbackEmpty));
var templateObject_1;
//# sourceMappingURL=userFeedbackEmpty.jsx.map
import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as qs from 'query-string';
import bgPattern from 'sentry-images/spot/mobile-hero.jpg';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAdvancedAnalyticsEvent } from 'app/utils/advancedAnalytics';
import withApi from 'app/utils/withApi';
import EmailField from 'app/views/settings/components/forms/emailField';
import Form from 'app/views/settings/components/forms/form';
var SuggestProjectModal = /** @class */ (function (_super) {
    __extends(SuggestProjectModal, _super);
    function SuggestProjectModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            askTeammate: false,
        };
        _this.handleGetStartedClick = function () {
            var _a = _this.props, matchedUserAgentString = _a.matchedUserAgentString, organization = _a.organization;
            trackAdvancedAnalyticsEvent('growth.clicked_mobile_prompt_setup_project', { matchedUserAgentString: matchedUserAgentString }, organization);
        };
        _this.handleAskTeammate = function () {
            var _a = _this.props, matchedUserAgentString = _a.matchedUserAgentString, organization = _a.organization;
            _this.setState({ askTeammate: true });
            trackAdvancedAnalyticsEvent('growth.clicked_mobile_prompt_ask_teammate', { matchedUserAgentString: matchedUserAgentString }, organization);
        };
        _this.goBack = function () {
            _this.setState({ askTeammate: false });
        };
        _this.handleSubmitSuccess = function () {
            var _a = _this.props, matchedUserAgentString = _a.matchedUserAgentString, organization = _a.organization, closeModal = _a.closeModal;
            addSuccessMessage('Notified teammate successfully');
            trackAdvancedAnalyticsEvent('growth.submitted_mobile_prompt_ask_teammate', { matchedUserAgentString: matchedUserAgentString }, organization);
            closeModal();
        };
        _this.handlePreSubmit = function () {
            addLoadingMessage(t('Submitting\u2026'));
        };
        _this.handleSubmitError = function () {
            addErrorMessage(t('Error notifying teammate'));
        };
        return _this;
    }
    SuggestProjectModal.prototype.renderAskTeammate = function () {
        var _a = this.props, Body = _a.Body, organization = _a.organization;
        return (<Body>
        <Form apiEndpoint={"/organizations/" + organization.slug + "/request-project-creation/"} apiMethod="POST" submitLabel={t('Send')} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onPreSubmit={this.handlePreSubmit} extraButton={<BackWrapper>
              <StyledBackButton onClick={this.goBack}>{t('Back')}</StyledBackButton>
            </BackWrapper>}>
          <p>
            {t('Let the right folks know about Sentry Mobile Application Monitoring.')}
          </p>
          <EmailField required name="targetUserEmail" inline={false} label={t('Email Address')} placeholder="name@example.com" stacked/>
        </Form>
      </Body>);
    };
    SuggestProjectModal.prototype.renderMain = function () {
        var _this = this;
        var _a = this.props, Body = _a.Body, Footer = _a.Footer, organization = _a.organization;
        var paramString = qs.stringify({
            referrer: 'suggest_project',
            category: 'mobile',
        });
        var newProjectLink = "/organizations/" + organization.slug + "/projects/new/?" + paramString;
        return (<React.Fragment>
        <Body>
          <ModalContainer>
            <SmallP>
              {t("Sentry for Mobile shows a holistic overview of your application's health in real time. So you can correlate errors with releases, tags, and devices to solve problems quickly, decrease churn, and improve user retention.")}
            </SmallP>

            <StyledList symbol="bullet">
              <ListItem>
                {tct('[see:See] session data, version adoption, and user impact by every release.', {
                see: <strong />,
            })}
              </ListItem>
              <ListItem>
                {tct('[solve:Solve] issues quickly with full context: contextualized stack traces, events that lead to the error, client, hardware information, and the very commit that introduced the error.', {
                solve: <strong />,
            })}
              </ListItem>
              <ListItem>
                {tct('[learn:Learn] and analyze event data to reduce regressions and ultimately improve user adoption and engagement.', {
                learn: <strong />,
            })}
              </ListItem>
            </StyledList>

            <SmallP>{t('And guess what? Setup takes less than five minutes.')}</SmallP>
          </ModalContainer>
        </Body>
        <Footer>
          <Access organization={organization} access={['project:write']}>
            {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<ButtonBar gap={1}>
                <Button priority={hasAccess ? 'default' : 'primary'} onClick={_this.handleAskTeammate}>
                  {t('Tell a Teammate')}
                </Button>
                {hasAccess && (<Button href={newProjectLink} onClick={_this.handleGetStartedClick} priority="primary">
                    {t('Get Started')}
                  </Button>)}
              </ButtonBar>);
            }}
          </Access>
        </Footer>
      </React.Fragment>);
    };
    SuggestProjectModal.prototype.render = function () {
        var Header = this.props.Header;
        var askTeammate = this.state.askTeammate;
        var header = askTeammate ? t('Tell a Teammate') : t('Try Sentry for Mobile');
        return (<React.Fragment>
        <Header>
          <PatternHeader />
          <Title>{header}</Title>
        </Header>
        {this.state.askTeammate ? this.renderAskTeammate() : this.renderMain()}
      </React.Fragment>);
    };
    return SuggestProjectModal;
}(React.Component));
var ModalContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n\n  code {\n    word-break: break-word;\n  }\n"])), space(3));
var Title = styled('h3')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n  margin-bottom: ", ";\n"], ["\n  margin-top: ", ";\n  margin-bottom: ", ";\n"])), space(2), space(3));
var SmallP = styled('p')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var PatternHeader = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: -", " -", " 0 -", ";\n  border-radius: 7px 7px 0 0;\n  background-image: url(", ");\n  background-size: 475px;\n  background-color: black;\n  background-repeat: no-repeat;\n  overflow: hidden;\n  background-position: center bottom;\n  height: 156px;\n"], ["\n  margin: -", " -", " 0 -", ";\n  border-radius: 7px 7px 0 0;\n  background-image: url(", ");\n  background-size: 475px;\n  background-color: black;\n  background-repeat: no-repeat;\n  overflow: hidden;\n  background-position: center bottom;\n  height: 156px;\n"])), space(4), space(4), space(4), bgPattern);
var StyledList = styled(List)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  li {\n    padding-left: ", ";\n    :before {\n      top: 7px;\n    }\n  }\n"], ["\n  li {\n    padding-left: ", ";\n    :before {\n      top: 7px;\n    }\n  }\n"])), space(3));
var BackWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  width: 100%;\n  margin-right: ", ";\n"], ["\n  width: 100%;\n  margin-right: ", ";\n"])), space(1));
var StyledBackButton = styled(Button)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  float: right;\n"], ["\n  float: right;\n"])));
export default withApi(SuggestProjectModal);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=suggestProjectModal.jsx.map
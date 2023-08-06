import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { closeGuide, dismissGuide, nextStep, recordFinish, registerAnchor, unregisterAnchor, } from 'app/actionCreators/guides';
import Button from 'app/components/button';
import Hovercard, { Body as HovercardBody } from 'app/components/hovercard';
import { t, tct } from 'app/locale';
import GuideStore from 'app/stores/guideStore';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
/**
 * A GuideAnchor puts an informative hovercard around an element.
 * Guide anchors register with the GuideStore, which uses registrations
 * from one or more anchors on the page to determine which guides can
 * be shown on the page.
 */
export var GuideAnchor = createReactClass({
    mixins: [Reflux.listenTo(GuideStore, 'onGuideStateChange')],
    getInitialState: function () {
        return {
            active: false,
            orgId: null,
        };
    },
    componentDidMount: function () {
        var target = this.props.target;
        target && registerAnchor(target);
    },
    componentDidUpdate: function (_prevProps, prevState) {
        if (this.containerElement && !prevState.active && this.state.active) {
            try {
                var top_1 = this.containerElement.getBoundingClientRect().top;
                var scrollTop = window.pageYOffset;
                var centerElement = top_1 + scrollTop - window.innerHeight / 2;
                window.scrollTo({ top: centerElement });
            }
            catch (err) {
                Sentry.captureException(err);
            }
        }
    },
    componentWillUnmount: function () {
        var target = this.props.target;
        target && unregisterAnchor(target);
    },
    onGuideStateChange: function (data) {
        var _a;
        var active = data.currentGuide &&
            ((_a = data.currentGuide.steps[data.currentStep]) === null || _a === void 0 ? void 0 : _a.target) === this.props.target;
        this.setState({
            active: active,
            currentGuide: data.currentGuide,
            step: data.currentStep,
            orgId: data.orgId,
        });
    },
    /**
     * Terminology:
     *
     *  - A guide can be FINISHED by clicking one of the buttons in the last step
     *  - A guide can be DISMISSED by x-ing out of it at any step except the last (where there is no x)
     *  - In both cases we consider it CLOSED
     */
    handleFinish: function (e) {
        e.stopPropagation();
        var onFinish = this.props.onFinish;
        if (onFinish) {
            onFinish();
        }
        var _a = this.state, currentGuide = _a.currentGuide, orgId = _a.orgId;
        recordFinish(currentGuide.guide, orgId);
        closeGuide();
    },
    handleNextStep: function (e) {
        e.stopPropagation();
        nextStep();
    },
    handleDismiss: function (e) {
        e.stopPropagation();
        var _a = this.state, currentGuide = _a.currentGuide, step = _a.step, orgId = _a.orgId;
        dismissGuide(currentGuide.guide, step, orgId);
    },
    getHovercardBody: function () {
        var to = this.props.to;
        var _a = this.state, currentGuide = _a.currentGuide, step = _a.step;
        var totalStepCount = currentGuide.steps.length;
        var currentStepCount = step + 1;
        var currentStep = currentGuide.steps[step];
        var lastStep = currentStepCount === totalStepCount;
        var hasManySteps = totalStepCount > 1;
        var dismissButton = (<DismissButton size="small" href="#" // to clear `#assistant` from the url
         onClick={this.handleDismiss} priority="link">
        {currentStep.dismissText || t('Dismiss')}
      </DismissButton>);
        return (<GuideContainer>
        <GuideContent>
          {currentStep.title && <GuideTitle>{currentStep.title}</GuideTitle>}
          <GuideDescription>{currentStep.description}</GuideDescription>
        </GuideContent>
        <GuideAction>
          <div>
            {lastStep ? (<React.Fragment>
                <StyledButton size="small" to={to} onClick={this.handleFinish}>
                  {currentStep.nextText ||
                    (hasManySteps ? t('Enough Already') : t('Got It'))}
                </StyledButton>
                {currentStep.hasNextGuide && dismissButton}
              </React.Fragment>) : (<React.Fragment>
                <StyledButton size="small" onClick={this.handleNextStep} to={to}>
                  {currentStep.nextText || t('Next')}
                </StyledButton>
                {!currentStep.cantDismiss && dismissButton}
              </React.Fragment>)}
          </div>

          {hasManySteps && (<StepCount>
              {tct('[currentStepCount] of [totalStepCount]', {
                    currentStepCount: currentStepCount,
                    totalStepCount: totalStepCount,
                })}
            </StepCount>)}
        </GuideAction>
      </GuideContainer>);
    },
    render: function () {
        var _this = this;
        var _a = this.props, children = _a.children, position = _a.position, offset = _a.offset, containerClassName = _a.containerClassName;
        var active = this.state.active;
        if (!active) {
            return children ? children : null;
        }
        return (<StyledHovercard show body={this.getHovercardBody()} tipColor={theme.purple300} position={position} offset={offset} containerClassName={containerClassName}>
        <span ref={function (el) { return (_this.containerElement = el); }}>{children}</span>
      </StyledHovercard>);
    },
});
var GuideAnchorWrapper = /** @class */ (function (_super) {
    __extends(GuideAnchorWrapper, _super);
    function GuideAnchorWrapper() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    GuideAnchorWrapper.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, children = _a.children, rest = __rest(_a, ["disabled", "children"]);
        if (disabled || window.localStorage.getItem('hide_anchors') === '1') {
            return children || null;
        }
        return <GuideAnchor {...rest}>{children}</GuideAnchor>;
    };
    return GuideAnchorWrapper;
}(React.Component));
export default GuideAnchorWrapper;
var GuideContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  text-align: center;\n  line-height: 1.5;\n  background-color: ", ";\n  border-color: ", ";\n  color: ", ";\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n  text-align: center;\n  line-height: 1.5;\n  background-color: ", ";\n  border-color: ", ";\n  color: ", ";\n"])), space(2), function (p) { return p.theme.purple300; }, function (p) { return p.theme.purple300; }, function (p) { return p.theme.white; });
var GuideContent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n\n  a {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n\n  a {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space(1), function (p) { return p.theme.white; });
var GuideTitle = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-weight: bold;\n  font-size: ", ";\n"], ["\n  font-weight: bold;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var GuideDescription = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var GuideAction = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-rows: repeat(2, auto);\n  grid-gap: ", ";\n"])), space(1));
var StyledButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  min-width: 40%;\n"], ["\n  font-size: ", ";\n  min-width: 40%;\n"])), function (p) { return p.theme.fontSizeMedium; });
var DismissButton = styled(StyledButton)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-left: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n  color: ", ";\n"], ["\n  margin-left: ", ";\n\n  &:hover,\n  &:focus,\n  &:active {\n    color: ", ";\n  }\n  color: ", ";\n"])), space(1), function (p) { return p.theme.white; }, function (p) { return p.theme.white; });
var StepCount = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n  text-transform: uppercase;\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n  text-transform: uppercase;\n"])), function (p) { return p.theme.fontSizeSmall; });
var StyledHovercard = styled(Hovercard)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  ", " {\n    background-color: ", ";\n    margin: -1px;\n    border-radius: ", ";\n    width: 300px;\n  }\n"], ["\n  ", " {\n    background-color: ", ";\n    margin: -1px;\n    border-radius: ", ";\n    width: 300px;\n  }\n"])), HovercardBody, theme.purple300, theme.borderRadius);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=guideAnchor.jsx.map
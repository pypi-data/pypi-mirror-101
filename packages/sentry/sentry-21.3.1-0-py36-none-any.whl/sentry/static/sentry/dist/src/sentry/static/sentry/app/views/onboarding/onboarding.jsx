import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { AnimatePresence, motion, useAnimation } from 'framer-motion';
import Button from 'app/components/button';
import Hook from 'app/components/hook';
import { IconChevron, IconSentryFull } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import testableTransition from 'app/utils/testableTransition';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import PageCorners from './components/pageCorners';
import OnboardingPlatform from './platform';
import SdkConfiguration from './sdkConfiguration';
import OnboardingWelcome from './welcome';
var recordAnalyticStepComplete = function (_a) {
    var organization = _a.organization, project = _a.project, step = _a.step;
    return analytics('onboarding_v2.step_compete', {
        org_id: parseInt(organization.id, 10),
        project: project ? project.slug : null,
        step: step.id,
    });
};
var ONBOARDING_STEPS = [
    {
        id: 'welcome',
        title: t('Welcome to Sentry'),
        Component: OnboardingWelcome,
        centered: true,
    },
    {
        id: 'select-platform',
        title: t('Select a platform'),
        Component: OnboardingPlatform,
    },
    {
        id: 'get-started',
        title: t('Install the Sentry SDK'),
        Component: SdkConfiguration,
    },
];
var Onboarding = /** @class */ (function (_super) {
    __extends(Onboarding, _super);
    function Onboarding() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleUpdate = function (data) {
            _this.setState(data);
        };
        _this.handleGoBack = function () {
            var previousStep = _this.props.steps[_this.activeStepIndex - 1];
            browserHistory.replace("/onboarding/" + _this.props.params.orgId + "/" + previousStep.id + "/");
        };
        _this.Contents = function () {
            var cornerVariantControl = useAnimation();
            var updateCornerVariant = function () {
                cornerVariantControl.start(_this.activeStepIndex === 0 ? 'top-right' : 'top-left');
            };
            // XXX(epurkhiser): We're using a react hook here becuase there's no other
            // way to create framer-motion controls than by using the `useAnimation`
            // hook.
            // eslint-disable-next-line sentry/no-react-hooks
            React.useEffect(updateCornerVariant, []);
            return (<Container>
        <Back animate={_this.activeStepIndex > 0 ? 'visible' : 'hidden'} onClick={_this.handleGoBack}/>
        <AnimatePresence exitBeforeEnter onExitComplete={updateCornerVariant}>
          {_this.renderOnboardingStep()}
        </AnimatePresence>
        <PageCorners animateVariant={cornerVariantControl}/>
      </Container>);
        };
        return _this;
    }
    Onboarding.prototype.componentDidMount = function () {
        this.validateActiveStep();
    };
    Onboarding.prototype.componentDidUpdate = function () {
        this.validateActiveStep();
    };
    Onboarding.prototype.validateActiveStep = function () {
        if (this.activeStepIndex === -1) {
            var firstStep = this.props.steps[0].id;
            browserHistory.replace("/onboarding/" + this.props.params.orgId + "/" + firstStep + "/");
        }
    };
    Object.defineProperty(Onboarding.prototype, "activeStepIndex", {
        get: function () {
            var _this = this;
            return this.props.steps.findIndex(function (_a) {
                var id = _a.id;
                return _this.props.params.step === id;
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "activeStep", {
        get: function () {
            return this.props.steps[this.activeStepIndex];
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "firstProject", {
        get: function () {
            var sortedProjects = this.props.projects.sort(function (a, b) { return new Date(a.dateCreated).getTime() - new Date(b.dateCreated).getTime(); });
            return sortedProjects.length > 0 ? sortedProjects[0] : null;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(Onboarding.prototype, "projectPlatform", {
        get: function () {
            var _a, _b, _c;
            return (_c = (_a = this.state.platform) !== null && _a !== void 0 ? _a : (_b = this.firstProject) === null || _b === void 0 ? void 0 : _b.platform) !== null && _c !== void 0 ? _c : null;
        },
        enumerable: false,
        configurable: true
    });
    Onboarding.prototype.handleNextStep = function (step, data) {
        this.handleUpdate(data);
        if (step !== this.activeStep) {
            return;
        }
        var orgId = this.props.params.orgId;
        var nextStep = this.props.steps[this.activeStepIndex + 1];
        recordAnalyticStepComplete({
            organization: this.props.organization,
            project: this.firstProject,
            step: nextStep,
        });
        browserHistory.push("/onboarding/" + orgId + "/" + nextStep.id + "/");
    };
    Onboarding.prototype.renderProgressBar = function () {
        var activeStepIndex = this.activeStepIndex;
        return (<ProgressBar>
        {this.props.steps.map(function (step, index) { return (<ProgressStep active={activeStepIndex === index} key={step.id}/>); })}
      </ProgressBar>);
    };
    Onboarding.prototype.renderOnboardingStep = function () {
        var _this = this;
        var orgId = this.props.params.orgId;
        var step = this.activeStep;
        return (<OnboardingStep centered={step.centered} key={step.id} data-test-id={"onboarding-step-" + step.id}>
        <step.Component active orgId={orgId} project={this.firstProject} platform={this.projectPlatform} onComplete={function (data) { return _this.handleNextStep(step, data); }} onUpdate={this.handleUpdate}/>
      </OnboardingStep>);
    };
    Onboarding.prototype.render = function () {
        if (this.activeStepIndex === -1) {
            return null;
        }
        return (<OnboardingWrapper>
        <DocumentTitle title={this.activeStep.title}/>
        <Header>
          <LogoSvg />
          <HeaderRight>
            {this.renderProgressBar()}
            <Hook name="onboarding:extra-chrome"/>
          </HeaderRight>
        </Header>
        <this.Contents />
      </OnboardingWrapper>);
    };
    Onboarding.defaultProps = {
        steps: ONBOARDING_STEPS,
    };
    return Onboarding;
}(React.Component));
var OnboardingWrapper = styled('main')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  overflow: hidden;\n  display: flex;\n  flex-direction: column;\n  flex-grow: 1;\n"], ["\n  overflow: hidden;\n  display: flex;\n  flex-direction: column;\n  flex-grow: 1;\n"])));
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  position: relative;\n  background: ", ";\n  padding: 120px ", ";\n  padding-top: 12vh;\n  width: 100%;\n  margin: 0 auto;\n  flex-grow: 1;\n"], ["\n  display: flex;\n  justify-content: center;\n  position: relative;\n  background: ", ";\n  padding: 120px ", ";\n  padding-top: 12vh;\n  width: 100%;\n  margin: 0 auto;\n  flex-grow: 1;\n"])), function (p) { return p.theme.background; }, space(3));
var Header = styled('header')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: ", ";\n  padding: ", ";\n  position: sticky;\n  top: 0;\n  z-index: 100;\n  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.05);\n  display: flex;\n  justify-content: space-between;\n"], ["\n  background: ", ";\n  padding: ", ";\n  position: sticky;\n  top: 0;\n  z-index: 100;\n  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.05);\n  display: flex;\n  justify-content: space-between;\n"])), function (p) { return p.theme.background; }, space(4));
var LogoSvg = styled(IconSentryFull)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"], ["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var ProgressBar = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: 0 ", ";\n  position: relative;\n  display: flex;\n  align-items: center;\n  min-width: 120px;\n  justify-content: space-between;\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    height: 4px;\n    background: ", ";\n    left: 2px;\n    right: 2px;\n    top: 50%;\n    margin-top: -2px;\n  }\n"], ["\n  margin: 0 ", ";\n  position: relative;\n  display: flex;\n  align-items: center;\n  min-width: 120px;\n  justify-content: space-between;\n\n  &:before {\n    position: absolute;\n    display: block;\n    content: '';\n    height: 4px;\n    background: ", ";\n    left: 2px;\n    right: 2px;\n    top: 50%;\n    margin-top: -2px;\n  }\n"])), space(4), function (p) { return p.theme.inactive; });
var ProgressStep = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: relative;\n  width: 16px;\n  height: 16px;\n  border-radius: 50%;\n  border: 4px solid ", ";\n  background: ", ";\n"], ["\n  position: relative;\n  width: 16px;\n  height: 16px;\n  border-radius: 50%;\n  border: 4px solid ", ";\n  background: ", ";\n"])), function (p) { return (p.active ? p.theme.active : p.theme.inactive); }, function (p) { return p.theme.background; });
var ProgressStatus = styled(motion.div)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  text-align: right;\n  grid-column: 3;\n  grid-row: 1;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  text-align: right;\n  grid-column: 3;\n  grid-row: 1;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
var HeaderRight = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n"])), space(1));
ProgressStatus.defaultProps = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
    transition: testableTransition(),
};
var Back = styled(function (_a) {
    var className = _a.className, animate = _a.animate, props = __rest(_a, ["className", "animate"]);
    return (<motion.div className={className} animate={animate} transition={testableTransition()} variants={{
            initial: { opacity: 0 },
            visible: { opacity: 1, transition: testableTransition({ delay: 1 }) },
            hidden: { opacity: 0 },
        }}>
    <Button {...props} icon={<IconChevron direction="left" size="sm"/>} priority="link">
      {t('Go back')}
    </Button>
  </motion.div>);
})(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  position: absolute;\n  top: 40px;\n  left: 20px;\n\n  button {\n    font-size: ", ";\n    color: ", ";\n  }\n"], ["\n  position: absolute;\n  top: 40px;\n  left: 20px;\n\n  button {\n    font-size: ", ";\n    color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; });
var OnboardingStep = styled(motion.div)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  width: 850px;\n  display: flex;\n  flex-direction: column;\n  ", ";\n"], ["\n  width: 850px;\n  display: flex;\n  flex-direction: column;\n  ",
    ";\n"])), function (p) {
    return p.centered &&
        "justify-content: center;\n     align-items: center;";
});
OnboardingStep.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    variants: { animate: {} },
    transition: testableTransition({
        staggerChildren: 0.2,
    }),
};
export default withOrganization(withProjects(Onboarding));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=onboarding.jsx.map
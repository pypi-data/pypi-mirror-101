import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { preloadIcons } from 'platformicons';
import Button from 'app/components/button';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import testableTransition from 'app/utils/testableTransition';
import withOrganization from 'app/utils/withOrganization';
import FallingError from './components/fallingError';
import WelcomeBackground from './components/welcomeBackground';
var recordAnalyticsOnboardingSkipped = function (_a) {
    var organization = _a.organization;
    return analytics('onboarding_v2.skipped', { org_id: organization.id });
};
var easterEggText = [
    t('Be careful. She’s barely hanging on as it is.'),
    t("You know this error's not real, right?"),
    t("It's that big button, right up there."),
    t('You could do this all day. But you really shouldn’t.'),
    tct("Ok, really, that's enough. Click [ready:I'm Ready].", { ready: <em /> }),
    tct("Next time you do that, [bold:we're starting].", { bold: <strong /> }),
    t("We weren't kidding, let's get going."),
];
var fadeAway = {
    variants: {
        initial: { opacity: 0 },
        animate: { opacity: 1, filter: 'blur(0px)' },
        exit: { opacity: 0, filter: 'blur(1px)' },
    },
    transition: testableTransition({ duration: 0.8 }),
};
var OnboardingWelcome = /** @class */ (function (_super) {
    __extends(OnboardingWelcome, _super);
    function OnboardingWelcome() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OnboardingWelcome.prototype.componentDidMount = function () {
        // Next step will render the platform picker (using both large and small
        // icons). Keep things smooth by prefetching them. Preload a bit late to
        // avoid jank on welcome animations.
        setTimeout(preloadIcons, 1500);
    };
    OnboardingWelcome.prototype.render = function () {
        var _a = this.props, organization = _a.organization, onComplete = _a.onComplete, active = _a.active;
        var skipOnboarding = function () { return recordAnalyticsOnboardingSkipped({ organization: organization }); };
        return (<FallingError onFall={function (fallCount) { return fallCount >= easterEggText.length && onComplete({}); }}>
        {function (_a) {
                var fallingError = _a.fallingError, fallCount = _a.fallCount, triggerFall = _a.triggerFall;
                return (<Wrapper>
            <WelcomeBackground />
            <motion.h1 {...fadeAway}>{t('Welcome to Sentry')}</motion.h1>
            <motion.p {...fadeAway}>
              {t('Find the errors and performance slowdowns that keep you up at night. In two steps.')}
            </motion.p>
            <CTAContainer {...fadeAway}>
              <Button data-test-id="welcome-next" disabled={!active} priority="primary" onClick={function () {
                        triggerFall();
                        onComplete({});
                    }}>
                {t("I'm Ready")}
              </Button>
              <PositionedFallingError>{fallingError}</PositionedFallingError>
            </CTAContainer>
            <SecondaryAction {...fadeAway}>
              {tct('[flavorText][br][exitLink:Skip onboarding].', {
                        br: <br />,
                        exitLink: <Button priority="link" onClick={skipOnboarding} href="/"/>,
                        flavorText: fallCount > 0
                            ? easterEggText[fallCount - 1]
                            : t("Really, this again? I've used Sentry before."),
                    })}
            </SecondaryAction>
          </Wrapper>);
            }}
      </FallingError>);
    };
    return OnboardingWelcome;
}(React.Component));
var CTAContainer = styled(motion.div)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  position: relative;\n\n  button {\n    position: relative;\n    z-index: 2;\n  }\n"], ["\n  margin-bottom: ", ";\n  position: relative;\n\n  button {\n    position: relative;\n    z-index: 2;\n  }\n"])), space(2));
var PositionedFallingError = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  position: absolute;\n  top: 30px;\n  right: -5px;\n  z-index: 0;\n"], ["\n  display: block;\n  position: absolute;\n  top: 30px;\n  right: -5px;\n  z-index: 0;\n"])));
var SecondaryAction = styled(motion.small)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  margin-top: 100px;\n"], ["\n  color: ", ";\n  margin-top: 100px;\n"])), function (p) { return p.theme.subText; });
var Wrapper = styled(motion.div)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  max-width: 400px;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  text-align: center;\n  padding-top: 100px;\n\n  h1 {\n    font-size: 42px;\n  }\n"], ["\n  max-width: 400px;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  text-align: center;\n  padding-top: 100px;\n\n  h1 {\n    font-size: 42px;\n  }\n"])));
Wrapper.defaultProps = {
    variants: { exit: { x: 0 } },
    transition: testableTransition({
        staggerChildren: 0.2,
    }),
};
export default withOrganization(OnboardingWelcome);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=welcome.jsx.map
import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { AnimatePresence, motion } from 'framer-motion';
import Button from 'app/components/button';
import { IconCheckmark } from 'app/icons';
import { t } from 'app/locale';
import pulsingIndicatorStyles from 'app/styles/pulsingIndicator';
import space from 'app/styles/space';
import EventWaiter from 'app/utils/eventWaiter';
import testableTransition from 'app/utils/testableTransition';
var FirstEventIndicator = function (_a) {
    var children = _a.children, props = __rest(_a, ["children"]);
    return (<EventWaiter {...props}>
    {function (_a) {
            var firstIssue = _a.firstIssue;
            return children({
                indicator: <Indicator firstIssue={firstIssue} {...props}/>,
                firstEventButton: (<Button title={t("You'll need to send your first error to continue")} tooltipProps={{ disabled: !!firstIssue }} disabled={!firstIssue} priority="primary" to={"/organizations/" + props.organization.slug + "/issues/" + (firstIssue !== true && firstIssue !== null ? firstIssue.id + "/" : '')}>
            {t('Take me to my error')}
          </Button>),
            });
        }}
  </EventWaiter>);
};
var Indicator = function (_a) {
    var firstIssue = _a.firstIssue;
    return (<Container>
    <AnimatePresence>
      {!firstIssue ? <Waiting key="waiting"/> : <Success key="received"/>}
    </AnimatePresence>
  </Container>);
};
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  justify-content: right;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  justify-content: right;\n"])));
var StatusWrapper = styled(motion.div)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  /* Keep the wrapper in the parent grids first cell for transitions */\n  grid-column: 1;\n  grid-row: 1;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  /* Keep the wrapper in the parent grids first cell for transitions */\n  grid-column: 1;\n  grid-row: 1;\n"])), space(1), function (p) { return p.theme.fontSizeMedium; });
StatusWrapper.defaultProps = {
    initial: 'initial',
    animate: 'animate',
    exit: 'exit',
    variants: {
        initial: { opacity: 0, y: -10 },
        animate: {
            opacity: 1,
            y: 0,
            transition: testableTransition({ when: 'beforeChildren', staggerChildren: 0.35 }),
        },
        exit: { opacity: 0, y: 10 },
    },
};
var Waiting = function (props) { return (<StatusWrapper {...props}>
    <AnimatedText>{t('Waiting to receive first event to continue')}</AnimatedText>
    <WaitingIndicator />
  </StatusWrapper>); };
var Success = function (props) { return (<StatusWrapper {...props}>
    <AnimatedText>{t('Event was received!')}</AnimatedText>
    <ReceivedIndicator />
  </StatusWrapper>); };
var indicatorAnimation = {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: 10 },
};
var AnimatedText = styled(motion.div)(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
AnimatedText.defaultProps = {
    variants: indicatorAnimation,
    transition: testableTransition(),
};
var WaitingIndicator = styled(motion.div)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0 6px;\n  ", ";\n"], ["\n  margin: 0 6px;\n  ", ";\n"])), pulsingIndicatorStyles);
WaitingIndicator.defaultProps = {
    variants: indicatorAnimation,
    transition: testableTransition(),
};
var ReceivedIndicator = styled(IconCheckmark)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: #fff;\n  background: ", ";\n  border-radius: 50%;\n  padding: 3px;\n  margin: 0 ", ";\n"], ["\n  color: #fff;\n  background: ", ";\n  border-radius: 50%;\n  padding: 3px;\n  margin: 0 ", ";\n"])), function (p) { return p.theme.green300; }, space(0.25));
ReceivedIndicator.defaultProps = {
    size: 'sm',
};
export { Indicator };
export default FirstEventIndicator;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=firstEventIndicator.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import testableTransition from 'app/utils/testableTransition';
var PageCorners = function (_a) {
    var animateVariant = _a.animateVariant;
    return (<Container>
    <TopRight key="tr" width="874" height="203" viewBox="0 0 874 203" fill="none" xmlns="http://www.w3.org/2000/svg" animate={animateVariant}>
      <path d="M36.5 0H874v203l-288.7-10-7-114-180.2-4.8-3.6-35.2-351.1 2.5L36.5 0z" fill="currentColor"/>
      <path d="M535.5 111.5v-22l31.8 1 .7 21.5-32.5-.5zM4 43.5L0 21.6 28.5 18l4.2 24.7-28.7.8z" fill="currentColor"/>
    </TopRight>
    <BottomLeft key="bl" width="494" height="141" viewBox="0 0 494 141" fill="none" xmlns="http://www.w3.org/2000/svg" animate={animateVariant}>
      <path d="M494 141H-1V7l140-7v19h33l5 82 308 4 9 36z" fill="currentColor"/>
      <path d="M219 88h-30l-1-19 31 3v16z" fill="currentColor"/>
    </BottomLeft>
    <TopLeft key="tl" width="414" height="118" fill="none" xmlns="http://www.w3.org/2000/svg" animate={animateVariant}>
      <path fillRule="evenodd" clipRule="evenodd" d="M414 0H0v102h144l5-69 257-3 8-30zM0 112v-10h117v16L0 112z" fill="currentColor"/>
      <path d="M184 44h-25l-1 16 26-2V44z" fill="currentColor"/>
    </TopLeft>
    <BottomRight key="br" width="650" height="151" fill="none" xmlns="http://www.w3.org/2000/svg" animate={animateVariant}>
      <path fillRule="evenodd" clipRule="evenodd" d="M27 151h623V0L435 7l-5 85-134 4-3 26-261-2-5 31z" fill="currentColor"/>
      <path d="M398 68v16h24l1-16h-25zM3 119l-3 16 21 3 3-19H3z" fill="currentColor"/>
    </BottomRight>
  </Container>);
};
export default PageCorners;
var transition = testableTransition({
    type: 'spring',
    duration: 0.8,
});
var TopLeft = styled(motion.svg)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  left: 0;\n"], ["\n  position: absolute;\n  top: 0;\n  left: 0;\n"])));
TopLeft.defaultProps = {
    initial: { x: '-40px', opacity: 0 },
    variants: {
        'top-right': { x: '-40px', opacity: 0 },
        'top-left': { x: 0, opacity: 1 },
    },
    transition: transition,
};
var TopRight = styled(motion.svg)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: 0;\n  right: 0;\n"], ["\n  position: absolute;\n  top: 0;\n  right: 0;\n"])));
TopRight.defaultProps = {
    initial: { x: '40px', opacity: 0 },
    variants: {
        'top-left': { x: '40px', opacity: 0 },
        'top-right': { x: 0, opacity: 1 },
    },
    transition: transition,
};
var BottomLeft = styled(motion.svg)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: absolute;\n  bottom: 0;\n  left: 0;\n"], ["\n  position: absolute;\n  bottom: 0;\n  left: 0;\n"])));
BottomLeft.defaultProps = {
    initial: { x: '-40px', opacity: 0 },
    variants: {
        'top-left': { x: '-40px', opacity: 0 },
        'top-right': { x: 0, opacity: 1 },
    },
    transition: transition,
};
var BottomRight = styled(motion.svg)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: absolute;\n  bottom: 0;\n  right: 0;\n"], ["\n  position: absolute;\n  bottom: 0;\n  right: 0;\n"])));
BottomRight.defaultProps = {
    initial: { x: '40px', opacity: 0 },
    variants: {
        'top-right': { x: '40px', opacity: 0 },
        'top-left': { x: 0, opacity: 1 },
    },
    transition: transition,
};
var Container = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  pointer-events: none;\n  position: absolute;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  color: ", ";\n  opacity: 0.4;\n"], ["\n  pointer-events: none;\n  position: absolute;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n  color: ", ";\n  opacity: 0.4;\n"])), function (p) { return p.theme.purple200; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=pageCorners.jsx.map
import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import space from 'app/styles/space';
import testableTransition from 'app/utils/testableTransition';
var StepHeading = styled(motion.h2)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: calc(-", " - 30px);\n  position: relative;\n  display: inline-grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n\n  &:before {\n    content: '", "';\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 30px;\n    height: 30px;\n    background-color: ", ";\n    border-radius: 50%;\n    color: ", ";\n    font-size: 1.5rem;\n  }\n"], ["\n  margin-left: calc(-", " - 30px);\n  position: relative;\n  display: inline-grid;\n  grid-template-columns: max-content max-content;\n  grid-gap: ", ";\n  align-items: center;\n\n  &:before {\n    content: '", "';\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    width: 30px;\n    height: 30px;\n    background-color: ", ";\n    border-radius: 50%;\n    color: ", ";\n    font-size: 1.5rem;\n  }\n"])), space(2), space(2), function (p) { return p.step; }, function (p) { return p.theme.yellow300; }, function (p) { return p.theme.textColor; });
StepHeading.defaultProps = {
    variants: {
        initial: { clipPath: 'inset(0% 100% 0% 0%)', opacity: 1 },
        animate: { clipPath: 'inset(0% 0% 0% 0%)', opacity: 1 },
        exit: { opacity: 0 },
    },
    transition: testableTransition({
        duration: 0.3,
    }),
};
export default StepHeading;
var templateObject_1;
//# sourceMappingURL=stepHeading.jsx.map
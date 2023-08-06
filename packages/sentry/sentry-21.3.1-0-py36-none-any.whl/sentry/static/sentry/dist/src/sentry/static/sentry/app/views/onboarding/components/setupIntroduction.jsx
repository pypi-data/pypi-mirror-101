import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { PlatformIcon } from 'platformicons';
import space from 'app/styles/space';
import StepHeading from './stepHeading';
export default function SetupIntroduction(_a) {
    var stepHeaderText = _a.stepHeaderText, platform = _a.platform;
    return (<TitleContainer>
      <StepHeading step={2}>{stepHeaderText}</StepHeading>
      <motion.div variants={{
            initial: { opacity: 0, x: 20 },
            animate: { opacity: 1, x: 0 },
            exit: { opacity: 0 },
        }}>
        <PlatformIcon size={48} format="lg" platform={platform}/>
      </motion.div>
    </TitleContainer>);
}
var TitleContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  justify-items: end;\n\n  ", " {\n    margin-bottom: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  justify-items: end;\n\n  ", " {\n    margin-bottom: 0;\n  }\n"])), space(2), StepHeading);
var templateObject_1;
//# sourceMappingURL=setupIntroduction.jsx.map
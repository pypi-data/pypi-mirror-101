import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
var WidgetWrapper = styled(motion.div)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  touch-action: manipulation;\n\n  ", ";\n"], ["\n  position: relative;\n  touch-action: manipulation;\n\n  ",
    ";\n"])), function (p) {
    switch (p.displayType) {
        case 'big_number':
            return "\n          /* 2 cols */\n          grid-area: span 1 / span 2;\n\n          @media (min-width: " + p.theme.breakpoints[0] + ") {\n            /* 4 cols */\n            grid-area: span 1 / span 1;\n          }\n\n          @media (min-width: " + p.theme.breakpoints[3] + ") {\n            /* 6 and 8 cols */\n            grid-area: span 1 / span 2;\n          }\n        ";
        default:
            return "\n          /* 2, 4, 6 and 8 cols */\n          grid-area: span 2 / span 2;\n        ";
    }
});
export default WidgetWrapper;
var templateObject_1;
//# sourceMappingURL=widgetWrapper.jsx.map
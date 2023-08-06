import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
var defaultProps = {
    enabled: true,
    size: 14,
};
var getBackgroundColor = function (p) {
    if (p.color) {
        return "background: " + p.color + ";";
    }
    return "background: " + (p.enabled ? p.theme.success : p.theme.error) + ";";
};
var getSize = function (p) { return "\n  height: " + p.size + "px;\n  width: " + p.size + "px;\n"; };
var CircleIndicator = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n  border-radius: 50%;\n  ", ";\n  ", ";\n"], ["\n  display: inline-block;\n  position: relative;\n  border-radius: 50%;\n  ", ";\n  ", ";\n"])), getSize, getBackgroundColor);
CircleIndicator.defaultProps = defaultProps;
export default CircleIndicator;
var templateObject_1;
//# sourceMappingURL=circleIndicator.jsx.map
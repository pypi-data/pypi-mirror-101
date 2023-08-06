import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconChevron } from 'app/icons';
import space from 'app/styles/space';
var DropdownButton = function (_a) {
    var children = _a.children, forwardedRef = _a.forwardedRef, prefix = _a.prefix, _b = _a.isOpen, isOpen = _b === void 0 ? false : _b, _c = _a.showChevron, showChevron = _c === void 0 ? false : _c, _d = _a.hideBottomBorder, hideBottomBorder = _d === void 0 ? true : _d, _e = _a.disabled, disabled = _e === void 0 ? false : _e, _f = _a.priority, priority = _f === void 0 ? 'form' : _f, props = __rest(_a, ["children", "forwardedRef", "prefix", "isOpen", "showChevron", "hideBottomBorder", "disabled", "priority"]);
    return (<StyledButton {...props} type="button" disabled={disabled} priority={priority} isOpen={isOpen} hideBottomBorder={hideBottomBorder} ref={forwardedRef}>
      {prefix && <LabelText>{prefix}</LabelText>}
      {children}
      {showChevron && <StyledChevron size="10px" direction={isOpen ? 'up' : 'down'}/>}
    </StyledButton>);
};
DropdownButton.defaultProps = {
    showChevron: true,
};
var StyledChevron = styled(IconChevron)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: 0.33em;\n"], ["\n  margin-left: 0.33em;\n"])));
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom-right-radius: ", ";\n  border-bottom-left-radius: ", ";\n  position: relative;\n  z-index: 2;\n  box-shadow: ", ";\n  &,\n  &:active,\n  &:focus,\n  &:hover {\n    border-bottom-color: ", ";\n  }\n"], ["\n  border-bottom-right-radius: ", ";\n  border-bottom-left-radius: ", ";\n  position: relative;\n  z-index: 2;\n  box-shadow: ", ";\n  &,\n  &:active,\n  &:focus,\n  &:hover {\n    border-bottom-color: ",
    ";\n  }\n"])), function (p) { return (p.isOpen ? 0 : p.theme.borderRadius); }, function (p) { return (p.isOpen ? 0 : p.theme.borderRadius); }, function (p) { return (p.isOpen || p.disabled ? 'none' : p.theme.dropShadowLight); }, function (p) {
    return p.isOpen && p.hideBottomBorder
        ? 'transparent'
        : p.theme.button[p.priority].borderActive;
});
var LabelText = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  &:after {\n    content: ':';\n  }\n\n  font-weight: 400;\n  padding-right: ", ";\n"], ["\n  &:after {\n    content: ':';\n  }\n\n  font-weight: 400;\n  padding-right: ", ";\n"])), space(0.75));
export default React.forwardRef(function (props, ref) { return (<DropdownButton forwardedRef={ref} {...props}/>); });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=dropdownButton.jsx.map
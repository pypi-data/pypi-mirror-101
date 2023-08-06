import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/actions/button';
import space from 'app/styles/space';
export default function FooterWithButtons(_a) {
    var buttonText = _a.buttonText, rest = __rest(_a, ["buttonText"]);
    return (<Footer>
      <Button priority="primary" type="submit" size="xsmall" {...rest}>
        {buttonText}
      </Button>
    </Footer>);
}
//wrap in form so we can keep form submission behavior
var Footer = styled('form')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  position: fixed;\n  display: flex;\n  justify-content: flex-end;\n  bottom: 0;\n  z-index: 100;\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n"], ["\n  width: 100%;\n  position: fixed;\n  display: flex;\n  justify-content: flex-end;\n  bottom: 0;\n  z-index: 100;\n  background-color: ", ";\n  border-top: 1px solid ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.bodyBackground; }, function (p) { return p.theme.innerBorder; }, space(2));
var templateObject_1;
//# sourceMappingURL=footerWithButtons.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import space from 'app/styles/space';
var BaseButton = function (props) { return (<Button size="zero" {...props}/>); };
var ActionButton = styled(BaseButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  font-size: ", ";\n"], ["\n  padding: ", " ", ";\n  font-size: ", ";\n"])), function (p) { return (p.icon ? space(0.75) : '7px'); }, space(1), function (p) { return p.theme.fontSizeSmall; });
export default ActionButton;
var templateObject_1;
//# sourceMappingURL=button.jsx.map
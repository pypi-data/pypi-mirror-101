import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import MenuItem from 'app/components/menuItem';
import space from 'app/styles/space';
function MenuHeaderBase(_a) {
    var children = _a.children, className = _a.className;
    return (<MenuItem header className={className}>
      {children}
    </MenuItem>);
}
var MenuHeader = styled(MenuHeaderBase)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-transform: uppercase;\n  font-weight: 600;\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  padding-bottom: ", ";\n"], ["\n  text-transform: uppercase;\n  font-weight: 600;\n  color: ", ";\n  border-bottom: 1px solid ", ";\n  padding-bottom: ", ";\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.innerBorder; }, space(0.5));
export default MenuHeader;
var templateObject_1;
//# sourceMappingURL=menuHeader.jsx.map
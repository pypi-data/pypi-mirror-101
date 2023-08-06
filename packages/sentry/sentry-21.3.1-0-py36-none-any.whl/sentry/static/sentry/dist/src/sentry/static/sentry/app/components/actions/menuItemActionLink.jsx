import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ActionLink from 'app/components/actions/actionLink';
import MenuItem from 'app/components/menuItem';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
function MenuItemActionLinkBase(_a) {
    var className = _a.className, props = __rest(_a, ["className"]);
    return (<MenuItem noAnchor disabled={props.disabled} className={className}>
      <StyledActionLink {...props}/>
    </MenuItem>);
}
var StyledActionLink = styled(ActionLink)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  ", "\n  &:hover {\n    color: ", ";\n  }\n\n  .dropdown-menu > li > &,\n  .dropdown-menu > span > li > & {\n    padding: ", ";\n\n    &.disabled:hover {\n      background: ", ";\n      color: #7a8188;\n    }\n  }\n"], ["\n  color: ", ";\n  ", "\n  &:hover {\n    color: ", ";\n  }\n\n  .dropdown-menu > li > &,\n  .dropdown-menu > span > li > & {\n    padding: ", ";\n\n    &.disabled:hover {\n      background: ", ";\n      color: #7a8188;\n    }\n  }\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis, function (p) { return p.theme.textColor; }, space(1), function (p) { return p.theme.white; });
var MenuItemActionLink = styled(MenuItemActionLinkBase)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  padding: 0;\n\n  &:last-child {\n    border-bottom: none;\n  }\n"], ["\n  border-bottom: 1px solid ", ";\n  padding: 0;\n\n  &:last-child {\n    border-bottom: none;\n  }\n"])), function (p) { return p.theme.innerBorder; });
export default MenuItemActionLink;
var templateObject_1, templateObject_2;
//# sourceMappingURL=menuItemActionLink.jsx.map
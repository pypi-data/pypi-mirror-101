import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import classNames from 'classnames';
import { withTheme } from 'emotion-theming';
import DropdownMenu from 'app/components/dropdownMenu';
import { IconChevron } from 'app/icons';
var getRootCss = function (theme) { return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  .dropdown-menu {\n    & > li > a {\n      color: ", ";\n\n      &:hover,\n      &:focus {\n        color: inherit;\n        background-color: ", ";\n      }\n    }\n\n    & .disabled {\n      cursor: not-allowed;\n      &:hover {\n        background: inherit;\n        color: inherit;\n      }\n    }\n  }\n\n  .dropdown-submenu:hover > span {\n    color: ", ";\n    background: ", ";\n  }\n"], ["\n  .dropdown-menu {\n    & > li > a {\n      color: ", ";\n\n      &:hover,\n      &:focus {\n        color: inherit;\n        background-color: ", ";\n      }\n    }\n\n    & .disabled {\n      cursor: not-allowed;\n      &:hover {\n        background: inherit;\n        color: inherit;\n      }\n    }\n  }\n\n  .dropdown-submenu:hover > span {\n    color: ", ";\n    background: ", ";\n  }\n"])), theme.textColor, theme.focus, theme.textColor, theme.focus); };
var DropdownLink = withTheme(function (_a) {
    var anchorRight = _a.anchorRight, anchorMiddle = _a.anchorMiddle, disabled = _a.disabled, title = _a.title, customTitle = _a.customTitle, caret = _a.caret, children = _a.children, menuClasses = _a.menuClasses, className = _a.className, alwaysRenderMenu = _a.alwaysRenderMenu, topLevelClasses = _a.topLevelClasses, theme = _a.theme, otherProps = __rest(_a, ["anchorRight", "anchorMiddle", "disabled", "title", "customTitle", "caret", "children", "menuClasses", "className", "alwaysRenderMenu", "topLevelClasses", "theme"]);
    return (<DropdownMenu alwaysRenderMenu={alwaysRenderMenu} {...otherProps}>
      {function (_a) {
            var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
            var shouldRenderMenu = alwaysRenderMenu || isOpen;
            var cx = classNames('dropdown-actor', className, {
                'dropdown-menu-right': anchorRight,
                'dropdown-toggle': true,
                hover: isOpen,
                disabled: disabled,
            });
            var topLevelCx = classNames('dropdown', topLevelClasses, {
                'pull-right': anchorRight,
                'anchor-right': anchorRight,
                'anchor-middle': anchorMiddle,
                open: isOpen,
            });
            return (<span css={getRootCss(theme)} {...getRootProps({
                className: topLevelCx,
            })}>
            <a {...getActorProps({
                className: cx,
            })}>
              {customTitle || (<div className="dropdown-actor-title">
                  {title}
                  {caret && <IconChevron direction={isOpen ? 'up' : 'down'} size="xs"/>}
                </div>)}
            </a>

            {shouldRenderMenu && (<ul {...getMenuProps({
                    className: classNames(menuClasses, 'dropdown-menu'),
                })}>
                {children}
              </ul>)}
          </span>);
        }}
    </DropdownMenu>);
});
DropdownLink.defaultProps = {
    alwaysRenderMenu: true,
    disabled: false,
    anchorRight: false,
    caret: true,
};
DropdownLink.displayName = 'DropdownLink';
export default DropdownLink;
var templateObject_1;
//# sourceMappingURL=dropdownLink.jsx.map
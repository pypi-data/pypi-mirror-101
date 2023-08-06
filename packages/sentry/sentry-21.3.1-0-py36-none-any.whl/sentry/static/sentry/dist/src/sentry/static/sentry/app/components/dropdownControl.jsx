import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownBubble from 'app/components/dropdownBubble';
import DropdownButton from 'app/components/dropdownButton';
import DropdownMenu from 'app/components/dropdownMenu';
import MenuItem from 'app/components/menuItem';
/*
 * A higher level dropdown component that helps with building complete dropdowns
 * including the button + menu options. Use the `button` or `label` prop to set
 * the button content and `children` to provide menu options.
 */
var DropdownControl = /** @class */ (function (_super) {
    __extends(DropdownControl, _super);
    function DropdownControl() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DropdownControl.prototype.renderButton = function (isOpen, getActorProps) {
        var _a = this.props, label = _a.label, button = _a.button, buttonProps = _a.buttonProps, priority = _a.priority;
        if (button) {
            return button({ isOpen: isOpen, getActorProps: getActorProps });
        }
        return (<StyledDropdownButton priority={priority} {...getActorProps(buttonProps)} isOpen={isOpen}>
        {label}
      </StyledDropdownButton>);
    };
    DropdownControl.prototype.renderChildren = function (isOpen, getMenuProps) {
        var _a = this.props, children = _a.children, alignRight = _a.alignRight, menuWidth = _a.menuWidth, blendWithActor = _a.blendWithActor, priority = _a.priority;
        if (typeof children === 'function') {
            return children({ isOpen: isOpen, getMenuProps: getMenuProps });
        }
        var alignMenu = alignRight ? 'right' : 'left';
        return (<Content {...getMenuProps()} priority={priority} alignMenu={alignMenu} width={menuWidth} isOpen={isOpen} blendWithActor={blendWithActor} blendCorner>
        {children}
      </Content>);
    };
    DropdownControl.prototype.render = function () {
        var _this = this;
        var _a = this.props, alwaysRenderMenu = _a.alwaysRenderMenu, className = _a.className;
        return (<Container className={className}>
        <DropdownMenu alwaysRenderMenu={alwaysRenderMenu}>
          {function (_a) {
                var isOpen = _a.isOpen, getMenuProps = _a.getMenuProps, getActorProps = _a.getActorProps;
                return (<React.Fragment>
              {_this.renderButton(isOpen, getActorProps)}
              {_this.renderChildren(isOpen, getMenuProps)}
            </React.Fragment>);
            }}
        </DropdownMenu>
      </Container>);
    };
    DropdownControl.defaultProps = {
        alwaysRenderMenu: true,
        menuWidth: '100%',
    };
    return DropdownControl;
}(React.Component));
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-block;\n  position: relative;\n"], ["\n  display: inline-block;\n  position: relative;\n"])));
var StyledDropdownButton = styled(DropdownButton)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  z-index: ", ";\n  white-space: nowrap;\n"], ["\n  z-index: ", ";\n  white-space: nowrap;\n"])), function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; });
var Content = styled(DropdownBubble)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: ", ";\n  border-color: ", ";\n"], ["\n  display: ", ";\n  border-color: ", ";\n"])), function (p) { return (p.isOpen ? 'block' : 'none'); }, function (p) { return p.theme.button[p.priority || 'form'].border; });
var DropdownItem = styled(MenuItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
export default DropdownControl;
export { DropdownItem, Content };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=dropdownControl.jsx.map
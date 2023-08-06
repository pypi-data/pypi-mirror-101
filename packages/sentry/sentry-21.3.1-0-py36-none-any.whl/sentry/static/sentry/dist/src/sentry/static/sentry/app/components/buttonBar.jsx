import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import classNames from 'classnames';
import { StyledButton } from 'app/components/button';
import space from 'app/styles/space';
function ButtonBar(_a) {
    var children = _a.children, className = _a.className, active = _a.active, _b = _a.merged, merged = _b === void 0 ? false : _b, _c = _a.gap, gap = _c === void 0 ? 0 : _c;
    var shouldCheckActive = typeof active !== 'undefined';
    return (<ButtonGrid merged={merged} gap={gap} className={className}>
      {!shouldCheckActive
            ? children
            : React.Children.map(children, function (child) {
                if (!React.isValidElement(child)) {
                    return child;
                }
                var childProps = child.props, childWithoutProps = __rest(child, ["props"]);
                // We do not want to pass `barId` to <Button>`
                var barId = childProps.barId, props = __rest(childProps, ["barId"]);
                var isActive = active === barId;
                // This ["primary"] could be customizable with a prop,
                // but let's just enforce one "active" type for now
                var priority = isActive ? 'primary' : childProps.priority || 'default';
                return React.cloneElement(childWithoutProps, __assign(__assign({}, props), { className: classNames(className, { active: isActive }), priority: priority }));
            })}
    </ButtonGrid>);
}
var MergedStyles = function () { return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* Raised buttons show borders on both sides. Useful to create pill bars */\n  & > .active {\n    z-index: 2;\n  }\n\n  & > .dropdown,\n  & > button,\n  & > a {\n    position: relative;\n\n    /* First button is square on the right side */\n    &:first-child:not(:last-child) {\n      border-top-right-radius: 0;\n      border-bottom-right-radius: 0;\n\n      & > .dropdown-actor > ", " {\n        border-top-right-radius: 0;\n        border-bottom-right-radius: 0;\n      }\n    }\n\n    /* Middle buttons are square */\n    &:not(:last-child):not(:first-child) {\n      border-radius: 0;\n\n      & > .dropdown-actor > ", " {\n        border-radius: 0;\n      }\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    &:first-child {\n      & + .dropdown:not(:last-child),\n      & + a:not(:last-child),\n      & + button:not(:last-child) {\n        margin-left: -1px;\n      }\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    /* stylelint-disable-next-line no-duplicate-selectors */\n    &:not(:last-child):not(:first-child) {\n      & + .dropdown,\n      & + button,\n      & + a {\n        margin-left: -1px;\n      }\n    }\n\n    /* Last button is square on the left side */\n    &:last-child:not(:first-child) {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n      margin-left: -1px;\n\n      & > .dropdown-actor > ", " {\n        border-top-left-radius: 0;\n        border-bottom-left-radius: 0;\n        margin-left: -1px;\n      }\n    }\n  }\n"], ["\n  /* Raised buttons show borders on both sides. Useful to create pill bars */\n  & > .active {\n    z-index: 2;\n  }\n\n  & > .dropdown,\n  & > button,\n  & > a {\n    position: relative;\n\n    /* First button is square on the right side */\n    &:first-child:not(:last-child) {\n      border-top-right-radius: 0;\n      border-bottom-right-radius: 0;\n\n      & > .dropdown-actor > ", " {\n        border-top-right-radius: 0;\n        border-bottom-right-radius: 0;\n      }\n    }\n\n    /* Middle buttons are square */\n    &:not(:last-child):not(:first-child) {\n      border-radius: 0;\n\n      & > .dropdown-actor > ", " {\n        border-radius: 0;\n      }\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    &:first-child {\n      & + .dropdown:not(:last-child),\n      & + a:not(:last-child),\n      & + button:not(:last-child) {\n        margin-left: -1px;\n      }\n    }\n\n    /* Middle buttons only need one border so we don't get a double line */\n    /* stylelint-disable-next-line no-duplicate-selectors */\n    &:not(:last-child):not(:first-child) {\n      & + .dropdown,\n      & + button,\n      & + a {\n        margin-left: -1px;\n      }\n    }\n\n    /* Last button is square on the left side */\n    &:last-child:not(:first-child) {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n      margin-left: -1px;\n\n      & > .dropdown-actor > ", " {\n        border-top-left-radius: 0;\n        border-bottom-left-radius: 0;\n        margin-left: -1px;\n      }\n    }\n  }\n"])), StyledButton, StyledButton, StyledButton); };
var ButtonGrid = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  ", "\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  ", "\n"])), function (p) { return space(p.gap); }, function (p) { return p.merged && MergedStyles; });
export default ButtonBar;
var templateObject_1, templateObject_2;
//# sourceMappingURL=buttonBar.jsx.map
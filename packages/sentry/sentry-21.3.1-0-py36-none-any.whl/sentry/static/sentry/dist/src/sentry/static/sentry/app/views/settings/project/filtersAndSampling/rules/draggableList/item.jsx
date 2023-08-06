import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
function Item(_a) {
    var value = _a.value, dragging = _a.dragging, index = _a.index, transform = _a.transform, listeners = _a.listeners, sorting = _a.sorting, transition = _a.transition, forwardRef = _a.forwardRef, attributes = _a.attributes, renderItem = _a.renderItem, wrapperStyle = _a.wrapperStyle, innerWrapperStyle = _a.innerWrapperStyle;
    return (<Wrapper ref={forwardRef} style={__assign(__assign({}, wrapperStyle), { transition: transition, '--translate-x': transform ? Math.round(transform.x) + "px" : undefined, '--translate-y': transform ? Math.round(transform.y) + "px" : undefined, '--scale-x': (transform === null || transform === void 0 ? void 0 : transform.scaleX) ? "" + transform.scaleX : undefined, '--scale-y': (transform === null || transform === void 0 ? void 0 : transform.scaleY) ? "" + transform.scaleY : undefined })}>
      <InnerWrapper style={innerWrapperStyle}>
        {renderItem({
            dragging: Boolean(dragging),
            sorting: Boolean(sorting),
            listeners: listeners,
            transform: transform,
            transition: transition,
            value: value,
            index: index,
            attributes: attributes,
        })}
      </InnerWrapper>
    </Wrapper>);
}
export default Item;
var boxShadowBorder = '0 0 0 calc(1px / var(--scale-x, 1)) rgba(63, 63, 68, 0.05)';
var boxShadowCommon = '0 1px calc(3px / var(--scale-x, 1)) 0 rgba(34, 33, 81, 0.15)';
var boxShadow = boxShadowBorder + ", " + boxShadowCommon;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  transform: translate3d(var(--translate-x, 0), var(--translate-y, 0), 0)\n    scaleX(var(--scale-x, 1)) scaleY(var(--scale-y, 1));\n  transform-origin: 0 0;\n  touch-action: manipulation;\n  --box-shadow: ", ";\n  --box-shadow-picked-up: ", ", -1px 0 15px 0 rgba(34, 33, 81, 0.01),\n    0px 15px 15px 0 rgba(34, 33, 81, 0.25);\n"], ["\n  transform: translate3d(var(--translate-x, 0), var(--translate-y, 0), 0)\n    scaleX(var(--scale-x, 1)) scaleY(var(--scale-y, 1));\n  transform-origin: 0 0;\n  touch-action: manipulation;\n  --box-shadow: ", ";\n  --box-shadow-picked-up: ", ", -1px 0 15px 0 rgba(34, 33, 81, 0.01),\n    0px 15px 15px 0 rgba(34, 33, 81, 0.25);\n"])), boxShadow, boxShadowBorder);
var InnerWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background-color: ", ";\n\n  animation: pop 200ms cubic-bezier(0.18, 0.67, 0.6, 1.22);\n  box-shadow: var(--box-shadow-picked-up);\n  opacity: 1;\n\n  :focus {\n    box-shadow: 0 0px 4px 1px rgba(76, 159, 254, 1), ", ";\n  }\n\n  @keyframes pop {\n    0% {\n      transform: scale(1);\n      box-shadow: var(--box-shadow);\n    }\n    100% {\n      box-shadow: var(--box-shadow-picked-up);\n    }\n  }\n"], ["\n  background-color: ", ";\n\n  animation: pop 200ms cubic-bezier(0.18, 0.67, 0.6, 1.22);\n  box-shadow: var(--box-shadow-picked-up);\n  opacity: 1;\n\n  :focus {\n    box-shadow: 0 0px 4px 1px rgba(76, 159, 254, 1), ", ";\n  }\n\n  @keyframes pop {\n    0% {\n      transform: scale(1);\n      box-shadow: var(--box-shadow);\n    }\n    100% {\n      box-shadow: var(--box-shadow-picked-up);\n    }\n  }\n"])), function (p) { return p.theme.white; }, boxShadow);
var templateObject_1, templateObject_2;
//# sourceMappingURL=item.jsx.map
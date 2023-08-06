import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import LoadingMask from 'app/components/loadingMask';
var TransparentLoadingMask = styled(function (_a) {
    var className = _a.className, visible = _a.visible, children = _a.children, props = __rest(_a, ["className", "visible", "children"]);
    var other = visible ? __assign(__assign({}, props), { 'data-test-id': 'loading-placeholder' }) : props;
    return (<LoadingMask className={className} {...other}>
        {children}
      </LoadingMask>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"], ["\n  ", ";\n  opacity: 0.4;\n  z-index: 1;\n"])), function (p) { return !p.visible && 'display: none;'; });
export default TransparentLoadingMask;
var templateObject_1;
//# sourceMappingURL=transparentLoadingMask.jsx.map
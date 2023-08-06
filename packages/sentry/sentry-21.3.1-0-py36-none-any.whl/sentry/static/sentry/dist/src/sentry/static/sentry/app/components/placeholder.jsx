import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var defaultProps = {
    shape: 'rect',
    bottomGutter: 0,
    width: '100%',
    height: '60px',
    testId: 'loading-placeholder',
};
var Placeholder = styled(function (_a) {
    var className = _a.className, children = _a.children, error = _a.error, testId = _a.testId;
    return (<div data-test-id={testId} className={className}>
      {error || children}
    </div>);
})(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  flex-shrink: 0;\n  justify-content: center;\n\n  background-color: ", ";\n  ", "\n  width: ", ";\n  height: ", ";\n  ", "\n  ", "\n"], ["\n  display: flex;\n  flex-direction: column;\n  flex-shrink: 0;\n  justify-content: center;\n\n  background-color: ", ";\n  ", "\n  width: ", ";\n  height: ", ";\n  ", "\n  ",
    "\n"])), function (p) { return (p.error ? p.theme.red100 : p.theme.backgroundSecondary); }, function (p) { return p.error && "color: " + p.theme.red200 + ";"; }, function (p) { return p.width; }, function (p) { return p.height; }, function (p) { return (p.shape === 'circle' ? 'border-radius: 100%;' : ''); }, function (p) {
    return typeof p.bottomGutter === 'number' && p.bottomGutter > 0
        ? "margin-bottom: " + space(p.bottomGutter) + ";"
        : '';
});
Placeholder.defaultProps = defaultProps;
export default Placeholder;
var templateObject_1;
//# sourceMappingURL=placeholder.jsx.map
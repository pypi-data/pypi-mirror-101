import { __makeTemplateObject } from "tslib";
import styled from '@emotion/styled';
import space from 'app/styles/space';
var Panel = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: ", ";\n  border-radius: ", ";\n  border: 1px\n    ", ";\n  box-shadow: ", ";\n  margin-bottom: ", ";\n  position: relative;\n"], ["\n  background: ", ";\n  border-radius: ", ";\n  border: 1px\n    ", ";\n  box-shadow: ", ";\n  margin-bottom: ", ";\n  position: relative;\n"])), function (p) { return (p.dashedBorder ? p.theme.backgroundSecondary : p.theme.background); }, function (p) { return p.theme.borderRadius; }, function (p) { return (p.dashedBorder ? 'dashed' + p.theme.gray300 : 'solid ' + p.theme.border); }, function (p) { return (p.dashedBorder ? 'none' : p.theme.dropShadowLight); }, space(3));
export default Panel;
var templateObject_1;
//# sourceMappingURL=panel.jsx.map
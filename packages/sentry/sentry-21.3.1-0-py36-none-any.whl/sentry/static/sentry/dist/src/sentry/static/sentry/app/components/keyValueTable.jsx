import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
export var KeyValueTable = styled('dl')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 50% 50%;\n"], ["\n  display: grid;\n  grid-template-columns: 50% 50%;\n"])));
export var KeyValueTableRow = function (_a) {
    var keyName = _a.keyName, value = _a.value;
    return (<React.Fragment>
      <Key>{keyName}</Key>
      <Value>{value}</Value>
    </React.Fragment>);
};
var commonStyles = function (_a) {
    var theme = _a.theme;
    return "\nfont-size: " + theme.fontSizeMedium + ";\npadding: " + space(0.5) + " " + space(1) + ";\nfont-weight: normal;\nline-height: inherit;\n" + overflowEllipsis + ";\n&:nth-of-type(2n-1) {\n  background-color: " + theme.backgroundSecondary + ";\n}\n";
};
var Key = styled('dt')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n  color: ", ";\n"], ["\n  ", ";\n  color: ", ";\n"])), commonStyles, function (p) { return p.theme.textColor; });
var Value = styled('dd')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  color: ", ";\n  text-align: right;\n"], ["\n  ", ";\n  color: ", ";\n  text-align: right;\n"])), commonStyles, function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=keyValueTable.jsx.map
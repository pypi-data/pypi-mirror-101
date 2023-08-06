import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
function List(_a) {
    var items = _a.items, className = _a.className;
    if (!items.length) {
        return null;
    }
    return <Wrapper className={className}>{items}</Wrapper>;
}
export default List;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  font-size: ", ";\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=list.jsx.map
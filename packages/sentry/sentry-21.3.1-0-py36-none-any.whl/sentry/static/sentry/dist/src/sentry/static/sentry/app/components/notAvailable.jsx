import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import { defined } from 'app/utils';
function NotAvailable(_a) {
    var tooltip = _a.tooltip;
    return (<Wrapper>
      <Tooltip title={tooltip} disabled={!defined(tooltip)}>
        {'\u2014'}
      </Tooltip>
    </Wrapper>);
}
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.gray200; });
export default NotAvailable;
var templateObject_1;
//# sourceMappingURL=notAvailable.jsx.map
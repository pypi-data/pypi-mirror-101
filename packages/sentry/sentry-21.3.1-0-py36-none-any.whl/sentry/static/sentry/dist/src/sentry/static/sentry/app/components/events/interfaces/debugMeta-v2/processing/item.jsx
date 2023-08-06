import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import space from 'app/styles/space';
function Item(_a) {
    var type = _a.type, icon = _a.icon, className = _a.className;
    function getLabel() {
        switch (type) {
            case 'stack_unwinding':
                return t('Stack Unwinding');
            case 'symbolication':
                return t('Symbolication');
            default: {
                Sentry.captureException(new Error('Unknown Images Loaded processing item type'));
                return null; // This shall not happen
            }
        }
    }
    return (<Wrapper className={className}>
      {icon}
      {getLabel()}
    </Wrapper>);
}
export default Item;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  white-space: nowrap;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  white-space: nowrap;\n"])), space(0.5), function (p) { return p.theme.fontSizeSmall; });
var templateObject_1;
//# sourceMappingURL=item.jsx.map
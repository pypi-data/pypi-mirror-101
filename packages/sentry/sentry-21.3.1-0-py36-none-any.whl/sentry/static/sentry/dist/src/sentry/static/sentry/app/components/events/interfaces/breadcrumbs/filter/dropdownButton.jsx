import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownButton from 'app/components/dropdownButton';
import { t, tn } from 'app/locale';
var DropDownButton = function (_a) {
    var isOpen = _a.isOpen, getActorProps = _a.getActorProps, checkedQuantity = _a.checkedQuantity;
    if (checkedQuantity > 0) {
        return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} size="small" hideBottomBorder={false} priority="primary">
        {tn('%s Active Filter', '%s Active Filters', checkedQuantity)}
      </StyledDropdownButton>);
    }
    return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} size="small" hideBottomBorder={false}>
      {t('Filter By')}
    </StyledDropdownButton>);
};
export default DropDownButton;
var StyledDropdownButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-right: 0;\n  z-index: ", ";\n  max-width: 200px;\n  white-space: nowrap;\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"], ["\n  border-right: 0;\n  z-index: ", ";\n  max-width: 200px;\n  white-space: nowrap;\n  border-top-right-radius: 0;\n  border-bottom-right-radius: 0;\n"])), function (p) { return p.theme.zIndex.dropdown; });
var templateObject_1;
//# sourceMappingURL=dropdownButton.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownButton from 'app/components/dropdownButton';
import { t, tn } from 'app/locale';
function DropDownButton(_a) {
    var isOpen = _a.isOpen, getActorProps = _a.getActorProps, checkedQuantity = _a.checkedQuantity;
    if (checkedQuantity > 0) {
        return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} size="small" hideBottomBorder={isOpen} priority="primary">
        {tn('%s Active Filter', '%s Active Filters', checkedQuantity)}
      </StyledDropdownButton>);
    }
    return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} size="small" hideBottomBorder={isOpen}>
      {t('Filter By')}
    </StyledDropdownButton>);
}
export default DropDownButton;
var StyledDropdownButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  z-index: ", ";\n  border-radius: ", ";\n  max-width: 200px;\n  white-space: nowrap;\n\n  ", "\n\n  @media (min-width: ", ") {\n    border-right: 0;\n    border-top-right-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n"], ["\n  z-index: ", ";\n  border-radius: ", ";\n  max-width: 200px;\n  white-space: nowrap;\n\n  ",
    "\n\n  @media (min-width: ", ") {\n    border-right: 0;\n    border-top-right-radius: 0;\n    border-bottom-right-radius: 0;\n  }\n"])), function (p) { return p.theme.zIndex.dropdown; }, function (p) { return p.theme.borderRadius; }, function (p) {
    return p.isOpen &&
        "\n      border-bottom-left-radius: 0;\n      border-bottom-right-radius: 0;\n    ";
}, function (p) { return p.theme.breakpoints[0]; });
var templateObject_1;
//# sourceMappingURL=dropDownButton.jsx.map
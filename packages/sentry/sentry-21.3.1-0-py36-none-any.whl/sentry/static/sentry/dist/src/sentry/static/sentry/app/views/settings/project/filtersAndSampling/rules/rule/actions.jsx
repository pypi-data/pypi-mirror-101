import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import MenuItemActionLink from 'app/components/actions/menuItemActionLink';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import DropdownLink from 'app/components/dropdownLink';
import Tooltip from 'app/components/tooltip';
import { IconDelete, IconDownload, IconEdit, IconEllipsis } from 'app/icons';
import { t } from 'app/locale';
var deleteRuleConfirmMessage = t('Are you sure you wish to delete this dynamic sampling rule?');
var deleteRuleMessage = t('You do not have permission to delete dynamic sampling rules.');
var editRuleMessage = t('You do not have permission to edit dynamic sampling rules.');
function Actions(_a) {
    var disabled = _a.disabled, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, onOpenMenuActions = _a.onOpenMenuActions, isMenuActionsOpen = _a.isMenuActionsOpen;
    return (<React.Fragment>
      <StyledButtonbar gap={1}>
        <Button label={t('Edit Rule')} size="small" onClick={onEditRule} icon={<IconEdit />} disabled={disabled} title={disabled ? editRuleMessage : undefined}/>
        <Confirm priority="danger" message={deleteRuleConfirmMessage} onConfirm={onDeleteRule} disabled={disabled}>
          <Button label={t('Delete Rule')} size="small" icon={<IconDelete />} title={disabled ? deleteRuleMessage : undefined}/>
        </Confirm>
      </StyledButtonbar>
      <StyledDropdownLink caret={false} customTitle={<Button label={t('Actions')} icon={<IconEllipsis size="sm"/>} size="xsmall" onClick={onOpenMenuActions}/>} isOpen={isMenuActionsOpen} anchorRight>
        <MenuItemActionLink shouldConfirm={false} icon={<IconDownload size="xs"/>} title={t('Edit')} onClick={!disabled
            ? onEditRule
            : function (event) {
                event === null || event === void 0 ? void 0 : event.stopPropagation();
            }} disabled={disabled}>
          <Tooltip disabled={!disabled} title={editRuleMessage} containerDisplayMode="block">
            {t('Edit')}
          </Tooltip>
        </MenuItemActionLink>
        <MenuItemActionLink onAction={onDeleteRule} message={deleteRuleConfirmMessage} icon={<IconDownload size="xs"/>} title={t('Delete')} disabled={disabled} priority="danger" shouldConfirm>
          <Tooltip disabled={!disabled} title={deleteRuleMessage} containerDisplayMode="block">
            {t('Delete')}
          </Tooltip>
        </MenuItemActionLink>
      </StyledDropdownLink>
    </React.Fragment>);
}
export default Actions;
var StyledButtonbar = styled(ButtonBar)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  justify-content: flex-end;\n  flex: 1;\n  display: none;\n  @media (min-width: ", ") {\n    display: grid;\n  }\n"], ["\n  justify-content: flex-end;\n  flex: 1;\n  display: none;\n  @media (min-width: ", ") {\n    display: grid;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var StyledDropdownLink = styled(DropdownLink)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  transition: none;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  transition: none;\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[2]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=actions.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { Panel, PanelFooter } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Rules from './rules';
import { DYNAMIC_SAMPLING_DOC_LINK } from './utils';
function RulesPanel(_a) {
    var rules = _a.rules, onAddRule = _a.onAddRule, onEditRule = _a.onEditRule, onDeleteRule = _a.onDeleteRule, disabled = _a.disabled, onUpdateRules = _a.onUpdateRules, isErrorPanel = _a.isErrorPanel;
    var panelType = isErrorPanel ? t('error') : t('transaction');
    return (<Panel>
      <Rules rules={rules} onEditRule={onEditRule} onDeleteRule={onDeleteRule} disabled={disabled} onUpdateRules={onUpdateRules} emptyMessage={t('There are no %s rules to display', panelType)}/>
      <StyledPanelFooter>
        <ButtonBar gap={1}>
          <Button href={DYNAMIC_SAMPLING_DOC_LINK} external>
            {t('Read the docs')}
          </Button>
          <Button priority="primary" onClick={onAddRule} disabled={disabled} title={disabled
            ? t('You do not have permission to add dynamic sampling rules.')
            : undefined}>
            {t('Add %s rule', panelType)}
          </Button>
        </ButtonBar>
      </StyledPanelFooter>
    </Panel>);
}
export default RulesPanel;
var StyledPanelFooter = styled(PanelFooter)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"], ["\n  padding: ", " ", ";\n  display: flex;\n  align-items: center;\n  justify-content: flex-end;\n"])), space(1), space(2));
var templateObject_1;
//# sourceMappingURL=rulesPanel.jsx.map
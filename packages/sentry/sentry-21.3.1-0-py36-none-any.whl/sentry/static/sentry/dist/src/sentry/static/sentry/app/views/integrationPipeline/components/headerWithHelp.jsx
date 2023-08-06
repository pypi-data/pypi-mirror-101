import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/actions/button';
import { IconSentryFull } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
export default function HeaderWithHelp(_a) {
    var docsUrl = _a.docsUrl;
    return (<Header>
      <StyledIconSentryFull />
      <Button external href={docsUrl} size="xsmall">
        {t('Need Help?')}
      </Button>
    </Header>);
}
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  position: fixed;\n  display: flex;\n  justify-content: space-between;\n  top: 0;\n  z-index: 100;\n  padding: ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  width: 100%;\n  position: fixed;\n  display: flex;\n  justify-content: space-between;\n  top: 0;\n  z-index: 100;\n  padding: ", ";\n  background: ", ";\n  border-bottom: 1px solid ", ";\n"])), space(2), function (p) { return p.theme.background; }, function (p) { return p.theme.innerBorder; });
var StyledIconSentryFull = styled(IconSentryFull)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"], ["\n  width: 130px;\n  height: 30px;\n  color: ", ";\n"])), function (p) { return p.theme.textColor; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=headerWithHelp.jsx.map
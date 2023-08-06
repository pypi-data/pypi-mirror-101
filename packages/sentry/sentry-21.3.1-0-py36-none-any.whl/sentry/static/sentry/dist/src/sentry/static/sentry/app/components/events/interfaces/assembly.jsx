import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
var Assembly = function (_a) {
    var name = _a.name, version = _a.version, culture = _a.culture, publicKeyToken = _a.publicKeyToken, filePath = _a.filePath;
    return (<AssemblyWrapper>
    <AssemblyInfo>
      <Caption>Assembly:</Caption>
      {name || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>{t('Version')}:</Caption>
      {version || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>{t('Culture')}:</Caption>
      {culture || '-'}
    </AssemblyInfo>
    <AssemblyInfo>
      <Caption>PublicKeyToken:</Caption>
      {publicKeyToken || '-'}
    </AssemblyInfo>

    {filePath && (<FilePathInfo>
        <Caption>{t('Path')}:</Caption>
        <Tooltip title={filePath}>
          <TextCopyInput rtl>{filePath}</TextCopyInput>
        </Tooltip>
      </FilePathInfo>)}
  </AssemblyWrapper>);
};
// TODO(ts): we should be able to delete these after disabling react/prop-types rule in tsx functional components
var AssemblyWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 80%;\n  display: flex;\n  flex-wrap: wrap;\n  color: ", ";\n  text-align: center;\n  position: relative;\n  padding: 0 ", " 0 ", ";\n"], ["\n  font-size: 80%;\n  display: flex;\n  flex-wrap: wrap;\n  color: ", ";\n  text-align: center;\n  position: relative;\n  padding: 0 ", " 0 ", ";\n"])), function (p) { return p.theme.textColor; }, space(3), space(3));
var AssemblyInfo = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: 15px;\n  margin-bottom: 5px;\n"], ["\n  margin-right: 15px;\n  margin-bottom: 5px;\n"])));
var Caption = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: 5px;\n  font-weight: bold;\n"], ["\n  margin-right: 5px;\n  font-weight: bold;\n"])));
var FilePathInfo = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin-bottom: 5px;\n  input {\n    width: 300px;\n    height: 20px;\n    padding-top: 0;\n    padding-bottom: 0;\n    line-height: 1.5;\n    @media (max-width: ", ") {\n      width: auto;\n    }\n  }\n  button > span {\n    padding: 2px 5px;\n  }\n  svg {\n    width: 11px;\n    height: 11px;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  margin-bottom: 5px;\n  input {\n    width: 300px;\n    height: 20px;\n    padding-top: 0;\n    padding-bottom: 0;\n    line-height: 1.5;\n    @media (max-width: ", ") {\n      width: auto;\n    }\n  }\n  button > span {\n    padding: 2px 5px;\n  }\n  svg {\n    width: 11px;\n    height: 11px;\n  }\n"])), theme.breakpoints[1]);
export { Assembly };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=assembly.jsx.map
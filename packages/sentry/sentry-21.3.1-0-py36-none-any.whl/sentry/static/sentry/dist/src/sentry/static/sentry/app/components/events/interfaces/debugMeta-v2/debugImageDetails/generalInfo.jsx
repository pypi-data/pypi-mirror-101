import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import NotAvailable from 'app/components/notAvailable';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Processings from '../debugImage/processings';
import { getImageAddress } from '../utils';
function GeneralInfo(_a) {
    var image = _a.image;
    var _b = image !== null && image !== void 0 ? image : {}, debug_id = _b.debug_id, debug_file = _b.debug_file, code_id = _b.code_id, code_file = _b.code_file, arch = _b.arch, unwind_status = _b.unwind_status, debug_status = _b.debug_status;
    var imageAddress = image ? getImageAddress(image) : undefined;
    return (<Wrapper>
      <Label coloredBg>{t('Address Range')}</Label>
      <Value coloredBg>{imageAddress !== null && imageAddress !== void 0 ? imageAddress : <NotAvailable />}</Value>

      <Label>{t('Debug ID')}</Label>
      <Value>{debug_id !== null && debug_id !== void 0 ? debug_id : <NotAvailable />}</Value>

      <Label coloredBg>{t('Debug File')}</Label>
      <Value coloredBg>{debug_file !== null && debug_file !== void 0 ? debug_file : <NotAvailable />}</Value>

      <Label>{t('Code ID')}</Label>
      <Value>{code_id !== null && code_id !== void 0 ? code_id : <NotAvailable />}</Value>

      <Label coloredBg>{t('Code File')}</Label>
      <Value coloredBg>{code_file !== null && code_file !== void 0 ? code_file : <NotAvailable />}</Value>

      <Label>{t('Architecture')}</Label>
      <Value>{arch !== null && arch !== void 0 ? arch : <NotAvailable />}</Value>

      <Label coloredBg>{t('Processing')}</Label>
      <Value coloredBg>
        {unwind_status || debug_status ? (<Processings unwind_status={unwind_status} debug_status={debug_status}/>) : (<NotAvailable />)}
      </Value>
    </Wrapper>);
}
export default GeneralInfo;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n"])));
var Label = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  padding: ", " ", " ", " ", ";\n  ", "\n"], ["\n  color: ", ";\n  padding: ", " ", " ", " ", ";\n  ", "\n"])), function (p) { return p.theme.textColor; }, space(1), space(1.5), space(1), space(1), function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; });
var Value = styled(Label)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-all;\n  color: ", ";\n  padding: ", ";\n  font-family: ", ";\n  ", "\n"], ["\n  white-space: pre-wrap;\n  word-break: break-all;\n  color: ", ";\n  padding: ", ";\n  font-family: ", ";\n  ", "\n"])), function (p) { return p.theme.subText; }, space(1), function (p) { return p.theme.text.familyMono; }, function (p) { return p.coloredBg && "background-color: " + p.theme.backgroundSecondary + ";"; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=generalInfo.jsx.map
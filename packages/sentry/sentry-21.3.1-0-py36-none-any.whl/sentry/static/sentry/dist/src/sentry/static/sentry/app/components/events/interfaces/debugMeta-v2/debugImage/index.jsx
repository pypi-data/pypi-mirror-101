import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import NotAvailable from 'app/components/notAvailable';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import layout from '../layout';
import { getFileName, getImageAddress } from '../utils';
import Processings from './processings';
import Status from './status';
function DebugImage(_a) {
    var image = _a.image, onOpenImageDetailsModal = _a.onOpenImageDetailsModal, style = _a.style;
    var unwind_status = image.unwind_status, debug_status = image.debug_status, debug_file = image.debug_file, debug_id = image.debug_id, code_file = image.code_file, code_id = image.code_id, status = image.status;
    var codeFilename = getFileName(code_file);
    var debugFilename = getFileName(debug_file);
    var imageAddress = getImageAddress(image);
    return (<Wrapper style={style}>
      <StatusColumn>
        <Status status={status}/>
      </StatusColumn>
      <ImageColumn>
        <div>
          {codeFilename && (<FileName>
              <Tooltip title={code_file}>{codeFilename}</Tooltip>
            </FileName>)}
          {codeFilename !== debugFilename && (<CodeFilename>{"(" + debugFilename + ")"}</CodeFilename>)}
        </div>
        {imageAddress && <ImageAddress>{imageAddress}</ImageAddress>}
      </ImageColumn>
      <Column>
        {unwind_status || debug_status ? (<Processings unwind_status={unwind_status} debug_status={debug_status}/>) : (<NotAvailable />)}
      </Column>
      <DebugFilesColumn>
        <Button size="xsmall" onClick={function () { return onOpenImageDetailsModal(code_id, debug_id); }}>
          {t('View')}
        </Button>
      </DebugFilesColumn>
    </Wrapper>);
}
export default DebugImage;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  :not(:last-child) {\n    > * {\n      border-bottom: 1px solid ", ";\n    }\n  }\n  ", ";\n"], ["\n  :not(:last-child) {\n    > * {\n      border-bottom: 1px solid ", ";\n    }\n  }\n  ", ";\n"])), function (p) { return p.theme.border; }, function (p) { return layout(p.theme); });
var Column = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", ";\n  display: flex;\n  align-items: center;\n"], ["\n  padding: ", ";\n  display: flex;\n  align-items: center;\n"])), space(2));
var StatusColumn = styled(Column)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  max-width: 100%;\n  overflow: hidden;\n"], ["\n  max-width: 100%;\n  overflow: hidden;\n"])));
var FileName = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-family: ", ";\n  font-size: ", ";\n  margin-right: ", ";\n  white-space: pre-wrap;\n  word-break: break-all;\n"], ["\n  color: ", ";\n  font-family: ", ";\n  font-size: ", ";\n  margin-right: ", ";\n  white-space: pre-wrap;\n  word-break: break-all;\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.text.family; }, function (p) { return p.theme.fontSizeMedium; }, space(0.5));
var CodeFilename = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var ImageColumn = styled(Column)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-family: ", ";\n  color: ", ";\n  font-size: ", ";\n  overflow: hidden;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"], ["\n  font-family: ", ";\n  color: ", ";\n  font-size: ", ";\n  overflow: hidden;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"])), function (p) { return p.theme.text.familyMono; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeSmall; });
var ImageAddress = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-word;\n"], ["\n  white-space: pre-wrap;\n  word-break: break-word;\n"])));
var DebugFilesColumn = styled(Column)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=index.jsx.map
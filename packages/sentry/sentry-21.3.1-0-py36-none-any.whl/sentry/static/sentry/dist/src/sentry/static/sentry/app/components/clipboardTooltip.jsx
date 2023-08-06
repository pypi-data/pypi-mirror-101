import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Clipboard from 'app/components/clipboard';
import TextOverflow from 'app/components/textOverflow';
import Tooltip from 'app/components/tooltip';
import { IconCopy } from 'app/icons';
import space from 'app/styles/space';
function ClipboardTooltip(_a) {
    var title = _a.title, onSuccess = _a.onSuccess, props = __rest(_a, ["title", "onSuccess"]);
    return (<Tooltip {...props} title={<TooltipClipboardWrapper onClick={function (event) {
                event.stopPropagation();
            }}>
          <TextOverflow>{title}</TextOverflow>
          <Clipboard value={title} onSuccess={onSuccess}>
            <TooltipClipboardIconWrapper>
              <IconCopy size="xs" color="white"/>
            </TooltipClipboardIconWrapper>
          </Clipboard>
        </TooltipClipboardWrapper>} isHoverable/>);
}
export default ClipboardTooltip;
var TooltipClipboardWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(0.5));
var TooltipClipboardIconWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  bottom: -", ";\n  :hover {\n    cursor: pointer;\n  }\n"], ["\n  position: relative;\n  bottom: -", ";\n  :hover {\n    cursor: pointer;\n  }\n"])), space(0.25));
var templateObject_1, templateObject_2;
//# sourceMappingURL=clipboardTooltip.jsx.map
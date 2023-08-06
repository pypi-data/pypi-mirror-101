import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import space from 'app/styles/space';
import { getStatusTooltipDescription } from '../utils';
import Status from '.';
function StatusTooltip(_a) {
    var candidate = _a.candidate, hasReprocessWarning = _a.hasReprocessWarning;
    var download = candidate.download;
    var _b = getStatusTooltipDescription(candidate, hasReprocessWarning), label = _b.label, description = _b.description, disabled = _b.disabled;
    return (<Tooltip title={label && (<Title>
            <Label>{label}</Label>
            {description && <div>{description}</div>}
          </Title>)} disabled={disabled}>
      <Status status={download.status}/>
    </Tooltip>);
}
export default StatusTooltip;
var Title = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var Label = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n  margin-bottom: ", ";\n"], ["\n  display: inline-block;\n  margin-bottom: ", ";\n"])), space(0.25));
var templateObject_1, templateObject_2;
//# sourceMappingURL=statusTooltip.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { IconCheckmark, IconFire, IconWarning } from 'app/icons';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { displayCrashFreePercent, releaseDisplayLabel } from '../utils';
var CRASH_FREE_DANGER_THRESHOLD = 98;
var CRASH_FREE_WARNING_THRESHOLD = 99.5;
var getIcon = function (percent, iconSize) {
    if (percent < CRASH_FREE_DANGER_THRESHOLD) {
        return <IconFire color="red300" size={iconSize}/>;
    }
    if (percent < CRASH_FREE_WARNING_THRESHOLD) {
        return <IconWarning color="yellow300" size={iconSize}/>;
    }
    return <IconCheckmark isCircled color="green300" size={iconSize}/>;
};
var CrashFree = function (_a) {
    var percent = _a.percent, _b = _a.iconSize, iconSize = _b === void 0 ? 'sm' : _b, displayOption = _a.displayOption;
    return (<Wrapper>
      {getIcon(percent, iconSize)}
      <CrashFreePercent>
        {displayCrashFreePercent(percent)}{' '}
        {defined(displayOption) && releaseDisplayLabel(displayOption, 2)}
      </CrashFreePercent>
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n  vertical-align: middle;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  align-items: center;\n  vertical-align: middle;\n"])), space(1));
var CrashFreePercent = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
export default CrashFree;
var templateObject_1, templateObject_2;
//# sourceMappingURL=crashFree.jsx.map
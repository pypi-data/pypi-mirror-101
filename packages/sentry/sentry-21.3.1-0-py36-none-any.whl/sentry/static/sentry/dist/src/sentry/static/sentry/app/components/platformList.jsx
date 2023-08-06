import { __makeTemplateObject } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { PlatformIcon } from 'platformicons';
import Tooltip from 'app/components/tooltip';
import { tn } from 'app/locale';
import getPlatformName from 'app/utils/getPlatformName';
function PlatformList(_a) {
    var _b = _a.platforms, platforms = _b === void 0 ? [] : _b, _c = _a.direction, direction = _c === void 0 ? 'right' : _c, _d = _a.max, max = _d === void 0 ? 3 : _d, _e = _a.size, size = _e === void 0 ? 16 : _e, _f = _a.consistentWidth, consistentWidth = _f === void 0 ? false : _f, _g = _a.showCounter, showCounter = _g === void 0 ? false : _g, className = _a.className;
    var visiblePlatforms = platforms.slice(0, max);
    var numNotVisiblePlatforms = platforms.length - visiblePlatforms.length;
    var displayCounter = showCounter && !!numNotVisiblePlatforms;
    function renderContent() {
        if (!platforms.length) {
            return <StyledPlatformIcon size={size} platform="default"/>;
        }
        var platformIcons = visiblePlatforms.slice().reverse();
        if (displayCounter) {
            return (<InnerWrapper>
          <PlatformIcons>
            {platformIcons.map(function (visiblePlatform, index) { return (<Tooltip key={visiblePlatform + index} title={getPlatformName(visiblePlatform)} containerDisplayMode="inline-flex">
                <StyledPlatformIcon platform={visiblePlatform} size={size}/>
              </Tooltip>); })}
          </PlatformIcons>
          <Tooltip title={tn('%s other platform', '%s other platforms', numNotVisiblePlatforms)} containerDisplayMode="inline-flex">
            <Counter>
              {numNotVisiblePlatforms}
              <Plus>{'\u002B'}</Plus>
            </Counter>
          </Tooltip>
        </InnerWrapper>);
        }
        return (<PlatformIcons>
        {platformIcons.map(function (visiblePlatform, index) { return (<StyledPlatformIcon key={visiblePlatform + index} platform={visiblePlatform} size={size}/>); })}
      </PlatformIcons>);
    }
    return (<Wrapper consistentWidth={consistentWidth} className={className} size={size} showCounter={displayCounter} direction={direction} max={max}>
      {renderContent()}
    </Wrapper>);
}
export default PlatformList;
function getOverlapWidth(size) {
    return Math.round(size / 4);
}
var commonStyles = function (_a) {
    var theme = _a.theme;
    return "\n  cursor: default;\n  border-radius: " + theme.borderRadius + ";\n  box-shadow: 0 0 0 1px " + theme.background + ";\n  :hover {\n    z-index: 1;\n  }\n";
};
var PlatformIcons = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var InnerWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  position: relative;\n"], ["\n  display: flex;\n  position: relative;\n"])));
var Plus = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: 10px;\n"], ["\n  font-size: 10px;\n"])));
var StyledPlatformIcon = styled(PlatformIcon)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), function (p) { return commonStyles(p); });
var Counter = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  text-align: center;\n  font-weight: 600;\n  font-size: ", ";\n  background-color: ", ";\n  color: ", ";\n  padding: 0 1px;\n  position: absolute;\n  right: -1px;\n"], ["\n  ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  text-align: center;\n  font-weight: 600;\n  font-size: ", ";\n  background-color: ", ";\n  color: ", ";\n  padding: 0 1px;\n  position: absolute;\n  right: -1px;\n"])), function (p) { return commonStyles(p); }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; });
var Wrapper = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  flex-shrink: 0;\n  justify-content: ", ";\n  ", ";\n\n  ", " {\n    ", "\n  }\n\n  ", " {\n    padding-right: ", "px;\n  }\n\n  ", " {\n    height: ", "px;\n    min-width: ", "px;\n  }\n"], ["\n  display: flex;\n  flex-shrink: 0;\n  justify-content: ", ";\n  ",
    ";\n\n  ", " {\n    ",
    "\n  }\n\n  ", " {\n    padding-right: ", "px;\n  }\n\n  ", " {\n    height: ", "px;\n    min-width: ", "px;\n  }\n"])), function (p) { return (p.direction === 'right' ? 'flex-end' : 'flex-start'); }, function (p) {
    return p.consistentWidth && "width: " + (p.size + (p.max - 1) * getOverlapWidth(p.size)) + "px;";
}, PlatformIcons, function (p) {
    return p.showCounter
        ? css(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n            z-index: 1;\n            flex-direction: row-reverse;\n            > * :not(:first-child) {\n              margin-right: ", "px;\n            }\n          "], ["\n            z-index: 1;\n            flex-direction: row-reverse;\n            > * :not(:first-child) {\n              margin-right: ", "px;\n            }\n          "])), p.size * -1 + getOverlapWidth(p.size)) : css(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n            > * :not(:first-child) {\n              margin-left: ", "px;\n            }\n          "], ["\n            > * :not(:first-child) {\n              margin-left: ", "px;\n            }\n          "])), p.size * -1 + getOverlapWidth(p.size));
}, InnerWrapper, function (p) { return p.size / 2 + 1; }, Counter, function (p) { return p.size; }, function (p) { return p.size; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=platformList.jsx.map
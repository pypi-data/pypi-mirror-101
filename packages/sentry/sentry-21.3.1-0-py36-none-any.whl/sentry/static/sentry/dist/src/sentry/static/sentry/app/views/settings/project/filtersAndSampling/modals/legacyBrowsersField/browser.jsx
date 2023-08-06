import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Switch from 'app/components/switchButton';
import space from 'app/styles/space';
import { LEGACY_BROWSER_LIST } from '../utils';
function Browser(_a) {
    var browser = _a.browser, isEnabled = _a.isEnabled, onToggle = _a.onToggle;
    var _b = LEGACY_BROWSER_LIST[browser], icon = _b.icon, title = _b.title;
    return (<React.Fragment>
      <BrowserWrapper>
        <Icon className={"icon-" + icon}/>
        {title}
      </BrowserWrapper>
      <SwitchWrapper>
        <Switch size="lg" isActive={isEnabled} toggle={onToggle}/>
      </SwitchWrapper>
    </React.Fragment>);
}
export default Browser;
var BrowserWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-column-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeLarge; });
var Icon = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  width: 24px;\n  height: 24px;\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: 24px 24px;\n  flex-shrink: 0;\n"], ["\n  width: 24px;\n  height: 24px;\n  background-repeat: no-repeat;\n  background-position: center;\n  background-size: 24px 24px;\n  flex-shrink: 0;\n"])));
var SwitchWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=browser.jsx.map
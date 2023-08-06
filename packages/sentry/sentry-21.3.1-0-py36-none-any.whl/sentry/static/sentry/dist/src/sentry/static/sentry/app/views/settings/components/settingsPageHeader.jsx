import { __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { HeaderTitle } from 'app/styles/organization';
import space from 'app/styles/space';
var UnstyledSettingsPageHeader = /** @class */ (function (_super) {
    __extends(UnstyledSettingsPageHeader, _super);
    function UnstyledSettingsPageHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UnstyledSettingsPageHeader.prototype.render = function () {
        var _a = this.props, icon = _a.icon, title = _a.title, subtitle = _a.subtitle, action = _a.action, tabs = _a.tabs, noTitleStyles = _a.noTitleStyles, body = _a.body, props = __rest(_a, ["icon", "title", "subtitle", "action", "tabs", "noTitleStyles", "body"]);
        // If Header is narrow, use align-items to center <Action>.
        // Otherwise, use a fixed margin to prevent an odd alignment.
        // This is needed as Actions could be a button or a dropdown.
        var isNarrow = !subtitle;
        return (<div {...props}>
        <TitleAndActions isNarrow={isNarrow}>
          <TitleWrapper>
            {icon && <Icon>{icon}</Icon>}
            {title && (<Title tabs={tabs} styled={noTitleStyles}>
                <HeaderTitle>{title}</HeaderTitle>
                {subtitle && <Subtitle>{subtitle}</Subtitle>}
              </Title>)}
          </TitleWrapper>
          {action && <Action isNarrow={isNarrow}>{action}</Action>}
        </TitleAndActions>

        {body && <BodyWrapper>{body}</BodyWrapper>}
        {tabs && <TabsWrapper>{tabs}</TabsWrapper>}
      </div>);
    };
    UnstyledSettingsPageHeader.defaultProps = {
        noTitleStyles: false,
    };
    return UnstyledSettingsPageHeader;
}(React.Component));
var TitleAndActions = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: ", ";\n"], ["\n  display: flex;\n  align-items: ", ";\n"])), function (p) { return (p.isNarrow ? 'center' : 'flex-start'); });
var TitleWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  margin: ", " ", " ", " 0;\n"], ["\n  ", ";\n  margin: ", " ", " ", " 0;\n"])), function (p) { return !p.styled && "font-size: 20px; font-weight: 600;"; }, space(4), space(2), space(3));
var Subtitle = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: 400;\n  font-size: ", ";\n  padding: ", " 0 0;\n"], ["\n  color: ", ";\n  font-weight: 400;\n  font-size: ", ";\n  padding: ", " 0 0;\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.fontSizeLarge; }, space(1.5));
var Icon = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var Action = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), function (p) { return (p.isNarrow ? '0' : space(4)); });
var SettingsPageHeader = styled(UnstyledSettingsPageHeader)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: 14px;\n  margin-top: -", ";\n"], ["\n  font-size: 14px;\n  margin-top: -", ";\n"])), space(4));
var BodyWrapper = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex: 1;\n  margin: 0 0 ", ";\n"], ["\n  flex: 1;\n  margin: 0 0 ", ";\n"])), space(3));
var TabsWrapper = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  flex: 1;\n  margin: 0; /* sentry/components/navTabs has added margin */\n"], ["\n  flex: 1;\n  margin: 0; /* sentry/components/navTabs has added margin */\n"])));
export default SettingsPageHeader;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=settingsPageHeader.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import { t } from '../../locale';
import ExternalLink from '../links/externalLink';
var SidebarPanelItem = function (_a) {
    var hasSeen = _a.hasSeen, title = _a.title, image = _a.image, message = _a.message, link = _a.link, cta = _a.cta, children = _a.children;
    return (<SidebarPanelItemRoot>
    {title && <Title hasSeen={hasSeen}>{title}</Title>}
    {image && (<ImageBox>
        <img src={image}/>
      </ImageBox>)}
    {message && <Message>{message}</Message>}

    {children}

    {link && (<Text>
        <ExternalLink href={link}>{cta || t('Read More')}</ExternalLink>
      </Text>)}
  </SidebarPanelItemRoot>);
};
export default SidebarPanelItem;
var SidebarPanelItemRoot = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  line-height: 1.5;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n  padding: ", ";\n"], ["\n  line-height: 1.5;\n  border-bottom: 1px solid ", ";\n  background: ", ";\n  font-size: ", ";\n  padding: ", ";\n"])), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.background; }, function (p) { return p.theme.fontSizeMedium; }, space(3));
var ImageBox = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border: 1px solid #e1e4e5;\n  padding: ", ";\n  border-radius: 2px;\n"], ["\n  border: 1px solid #e1e4e5;\n  padding: ", ";\n  border-radius: 2px;\n"])), space(2));
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n  color: ", ";\n  ", ";\n\n  .culprit {\n    font-weight: normal;\n  }\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n  color: ", ";\n  ", ";\n\n  .culprit {\n    font-weight: normal;\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, space(1), function (p) { return p.theme.textColor; }, function (p) { return !p.hasSeen && 'font-weight: 600;'; });
var Text = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: 5px;\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"], ["\n  margin-bottom: 5px;\n\n  &:last-child {\n    margin-bottom: 0;\n  }\n"])));
var Message = styled(Text)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=sidebarPanelItem.jsx.map
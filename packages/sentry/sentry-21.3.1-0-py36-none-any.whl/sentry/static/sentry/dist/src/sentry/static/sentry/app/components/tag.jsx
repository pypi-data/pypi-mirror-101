import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import Tooltip from 'app/components/tooltip';
import { IconClose, IconOpen } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import theme from 'app/utils/theme';
var TAG_HEIGHT = '20px';
function Tag(_a) {
    var _b = _a.type, type = _b === void 0 ? 'default' : _b, icon = _a.icon, tooltipText = _a.tooltipText, to = _a.to, onClick = _a.onClick, href = _a.href, onDismiss = _a.onDismiss, children = _a.children, _c = _a.textMaxWidth, textMaxWidth = _c === void 0 ? 150 : _c, props = __rest(_a, ["type", "icon", "tooltipText", "to", "onClick", "href", "onDismiss", "children", "textMaxWidth"]);
    var iconsProps = {
        size: '11px',
        color: theme.tag[type].iconColor,
    };
    var tag = (<Tooltip title={tooltipText} containerDisplayMode="inline-flex">
      <Background type={type}>
        {tagIcon()}

        <Text type={type} maxWidth={textMaxWidth}>
          {children}
        </Text>

        {defined(onDismiss) && (<DismissButton onClick={handleDismiss} size="zero" priority="link" label={t('Dismiss')}>
            <IconClose isCircled {...iconsProps}/>
          </DismissButton>)}
      </Background>
    </Tooltip>);
    function handleDismiss(event) {
        event.preventDefault();
        onDismiss === null || onDismiss === void 0 ? void 0 : onDismiss();
    }
    function tagIcon() {
        if (React.isValidElement(icon)) {
            return <IconWrapper>{React.cloneElement(icon, __assign({}, iconsProps))}</IconWrapper>;
        }
        if ((defined(href) || defined(to)) && icon === undefined) {
            return (<IconWrapper>
          <IconOpen {...iconsProps}/>
        </IconWrapper>);
        }
        return null;
    }
    function tagWithParent() {
        if (defined(href)) {
            return <ExternalLink href={href}>{tag}</ExternalLink>;
        }
        if (defined(to) && defined(onClick)) {
            return (<Link to={to} onClick={onClick}>
          {tag}
        </Link>);
        }
        else if (defined(to)) {
            return <Link to={to}>{tag}</Link>;
        }
        return tag;
    }
    return <TagWrapper {...props}>{tagWithParent()}</TagWrapper>;
}
var TagWrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; });
export var Background = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-flex;\n  align-items: center;\n  height: ", ";\n  border-radius: ", ";\n  background-color: ", ";\n  padding: 0 ", ";\n"], ["\n  display: inline-flex;\n  align-items: center;\n  height: ", ";\n  border-radius: ", ";\n  background-color: ", ";\n  padding: 0 ", ";\n"])), TAG_HEIGHT, TAG_HEIGHT, function (p) { return p.theme.tag[p.type].background; }, space(1));
var IconWrapper = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n  display: inline-flex;\n"], ["\n  margin-right: ", ";\n  display: inline-flex;\n"])), space(0.5));
var Text = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  max-width: ", "px;\n  overflow: hidden;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  line-height: ", ";\n"], ["\n  color: ", ";\n  max-width: ", "px;\n  overflow: hidden;\n  white-space: nowrap;\n  text-overflow: ellipsis;\n  line-height: ", ";\n"])), function (p) { return (['black', 'focus'].includes(p.type) ? p.theme.white : p.theme.gray500); }, function (p) { return p.maxWidth; }, TAG_HEIGHT);
var DismissButton = styled(Button)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-left: ", ";\n  border: none;\n"], ["\n  margin-left: ", ";\n  border: none;\n"])), space(0.5));
export default Tag;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=tag.jsx.map
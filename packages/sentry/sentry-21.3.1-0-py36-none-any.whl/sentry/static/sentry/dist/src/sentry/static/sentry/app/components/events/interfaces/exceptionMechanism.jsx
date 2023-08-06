import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import forOwn from 'lodash/forOwn';
import isNil from 'lodash/isNil';
import isObject from 'lodash/isObject';
import Hovercard from 'app/components/hovercard';
import ExternalLink from 'app/components/links/externalLink';
import Pill from 'app/components/pill';
import Pills from 'app/components/pills';
import { IconInfo, IconOpen } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { isUrl } from 'app/utils';
var ExceptionMechanism = /** @class */ (function (_super) {
    __extends(ExceptionMechanism, _super);
    function ExceptionMechanism() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ExceptionMechanism.prototype.render = function () {
        var mechanism = this.props.data;
        var type = mechanism.type, description = mechanism.description, help_link = mechanism.help_link, handled = mechanism.handled, _a = mechanism.meta, meta = _a === void 0 ? {} : _a, _b = mechanism.data, data = _b === void 0 ? {} : _b;
        var errno = meta.errno, signal = meta.signal, mach_exception = meta.mach_exception;
        var linkElement = help_link && isUrl(help_link) && (<StyledExternalLink href={help_link}>
        <IconOpen size="xs"/>
      </StyledExternalLink>);
        var descriptionElement = description && (<Hovercard header={<span>
            <Details>{t('Details')}</Details> {linkElement}
          </span>} body={description}>
        <StyledIconInfo size="14px"/>
      </Hovercard>);
        var pills = [
            <Pill key="mechanism" name="mechanism" value={type || 'unknown'}>
        {descriptionElement || linkElement}
      </Pill>,
        ];
        if (!isNil(handled)) {
            pills.push(<Pill key="handled" name="handled" value={handled}/>);
        }
        if (errno) {
            var value = errno.name || errno.number;
            pills.push(<Pill key="errno" name="errno" value={value}/>);
        }
        if (mach_exception) {
            var value = mach_exception.name || mach_exception.exception;
            pills.push(<Pill key="mach" name="mach exception" value={value}/>);
        }
        if (signal) {
            var code = signal.code_name || t('code') + " " + signal.code;
            var name_1 = signal.name || signal.number;
            var value = isNil(signal.code) ? name_1 : name_1 + " (" + code + ")";
            pills.push(<Pill key="signal" name="signal" value={value}/>);
        }
        forOwn(data, function (value, key) {
            if (!isObject(value)) {
                pills.push(<Pill key={"data:" + key} name={key} value={value}/>);
            }
        });
        return (<Wrapper>
        <Pills>{pills}</Pills>
      </Wrapper>);
    };
    return ExceptionMechanism;
}(React.Component));
export default ExceptionMechanism;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin: ", " 0;\n"], ["\n  margin: ", " 0;\n"])), space(2));
var iconStyle = function (p) { return css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  transition: 0.1s linear color;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"], ["\n  transition: 0.1s linear color;\n  color: ", ";\n  :hover {\n    color: ", ";\n  }\n"])), p.theme.gray300, p.theme.gray500); };
var StyledExternalLink = styled(ExternalLink)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-flex !important;\n  ", ";\n"], ["\n  display: inline-flex !important;\n  ", ";\n"])), iconStyle);
var Details = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var StyledIconInfo = styled(IconInfo)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  ", ";\n"], ["\n  display: flex;\n  ", ";\n"])), iconStyle);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=exceptionMechanism.jsx.map
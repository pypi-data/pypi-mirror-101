import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { getMeta } from 'app/components/events/meta/metaProxy';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { getSortedRegisters } from './utils';
import Value from './value';
function FrameRegisters(_a) {
    var registers = _a.registers, deviceArch = _a.deviceArch;
    // make sure that clicking on the registers does not actually do
    // anything on the containing element.
    var handlePreventToggling = function (event) {
        event.stopPropagation();
    };
    var sortedRegisters = getSortedRegisters(registers, deviceArch);
    return (<Wrapper>
      <Heading>{t('registers')}</Heading>
      <Registers>
        {sortedRegisters.map(function (_a) {
            var _b = __read(_a, 2), name = _b[0], value = _b[1];
            if (!defined(value)) {
                return null;
            }
            return (<Register key={name} onClick={handlePreventToggling}>
              <Name>{name}</Name>
              <Value value={value} meta={getMeta(registers, name)}/>
            </Register>);
        })}
      </Registers>
    </Wrapper>);
}
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding-top: 10px;\n"], ["\n  border-top: 1px solid ", ";\n  padding-top: 10px;\n"])), function (p) { return p.theme.innerBorder; });
var Registers = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  margin-left: 125px;\n  padding: ", " 0px;\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  margin-left: 125px;\n  padding: ", " 0px;\n"])), space(0.25));
var Register = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: ", " 5px;\n"], ["\n  padding: ", " 5px;\n"])), space(0.5));
var Heading = styled('strong')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-weight: 600;\n  font-size: 13px;\n  width: 125px;\n  max-width: 125px;\n  word-wrap: break-word;\n  padding: 10px 15px 10px 0;\n  line-height: 1.4;\n  float: left;\n"], ["\n  font-weight: 600;\n  font-size: 13px;\n  width: 125px;\n  max-width: 125px;\n  word-wrap: break-word;\n  padding: 10px 15px 10px 0;\n  line-height: 1.4;\n  float: left;\n"])));
var Name = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: inline-block;\n  font-size: 13px;\n  font-weight: 600;\n  text-align: right;\n  width: 4em;\n"], ["\n  display: inline-block;\n  font-size: 13px;\n  font-weight: 600;\n  text-align: right;\n  width: 4em;\n"])));
export default FrameRegisters;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map
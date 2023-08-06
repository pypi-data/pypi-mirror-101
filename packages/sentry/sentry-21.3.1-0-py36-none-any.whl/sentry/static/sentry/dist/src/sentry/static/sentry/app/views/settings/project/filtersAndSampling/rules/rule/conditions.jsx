import { __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { DynamicSamplingConditionOperator, } from 'app/types/dynamicSampling';
import { getInnerNameLabel } from './utils';
function Conditions(_a) {
    var condition = _a.condition;
    function getConvertedValue(value) {
        if (Array.isArray(value)) {
            return (<React.Fragment>
          {__spreadArray([], __read(value)).map(function (v, index) { return (<React.Fragment key={v}>
              <Value>{v}</Value>
              {index !== value.length - 1 && <Separator>{'\u002C'}</Separator>}
            </React.Fragment>); })}
        </React.Fragment>);
        }
        return <Value>{String(value)}</Value>;
    }
    switch (condition.op) {
        case DynamicSamplingConditionOperator.AND: {
            var inner = condition.inner;
            if (!inner.length) {
                return <Label>{t('All')}</Label>;
            }
            return (<Wrapper>
          {inner.map(function (_a, index) {
                    var value = _a.value, name = _a.name;
                    return (<div key={index}>
              <Label>{getInnerNameLabel(name)}</Label>
              {getConvertedValue(value)}
            </div>);
                })}
        </Wrapper>);
        }
        default: {
            Sentry.captureException(new Error('Unknown dynamic sampling condition operator'));
            return null; //this shall not happen
        }
    }
}
export default Conditions;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
var Label = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var Value = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  word-break: break-all;\n  white-space: pre-wrap;\n  color: ", ";\n"], ["\n  word-break: break-all;\n  white-space: pre-wrap;\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var Separator = styled(Value)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding-right: ", ";\n"], ["\n  padding-right: ", ";\n"])), space(0.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=conditions.jsx.map
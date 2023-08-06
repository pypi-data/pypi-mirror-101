import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import { DynamicSamplingRuleType } from 'app/types/dynamicSampling';
function Type(_a) {
    var type = _a.type;
    switch (type) {
        case DynamicSamplingRuleType.ERROR:
            return <ErrorLabel>{t('Errors only')}</ErrorLabel>;
        case DynamicSamplingRuleType.TRANSACTION:
            return <TransactionLabel>{t('Individual transactions')}</TransactionLabel>;
        case DynamicSamplingRuleType.TRACE:
            return <TransactionLabel>{t('Transaction traces')}</TransactionLabel>;
        default: {
            Sentry.captureException(new Error('Unknown dynamic sampling rule type'));
            return null; //this shall never happen
        }
    }
}
export default Type;
var ErrorLabel = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  white-space: pre-wrap;\n"], ["\n  color: ", ";\n  white-space: pre-wrap;\n"])), function (p) { return p.theme.pink300; });
var TransactionLabel = styled(ErrorLabel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.linkColor; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=type.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import Tag from 'app/components/tag';
import { t } from 'app/locale';
import { ImageStatus } from 'app/types/debugImage';
function Status(_a) {
    var status = _a.status;
    switch (status) {
        case ImageStatus.OTHER:
        case ImageStatus.FETCHING_FAILED:
        case ImageStatus.MALFORMED:
        case ImageStatus.TIMEOUT: {
            return <StyledTag type="error">{t('Error')}</StyledTag>;
        }
        case ImageStatus.MISSING: {
            return <StyledTag type="error">{t('Missing')}</StyledTag>;
        }
        case ImageStatus.FOUND: {
            return <StyledTag type="success">{t('Ok')}</StyledTag>;
        }
        case ImageStatus.UNUSED: {
            return <StyledTag>{t('Unreferenced')}</StyledTag>;
        }
        default: {
            Sentry.withScope(function (scope) {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image status'));
            });
            return <StyledTag>{t('Unknown')}</StyledTag>; // This shall not happen
        }
    }
}
export default Status;
var StyledTag = styled(Tag)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  &,\n  span div {\n    max-width: 100%;\n  }\n"], ["\n  &,\n  span div {\n    max-width: 100%;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=status.jsx.map
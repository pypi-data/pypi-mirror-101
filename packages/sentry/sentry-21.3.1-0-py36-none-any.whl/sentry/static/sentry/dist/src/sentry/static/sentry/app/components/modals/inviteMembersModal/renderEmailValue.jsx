import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { components as selectComponents } from 'react-select';
import styled from '@emotion/styled';
import LoadingIndicator from 'app/components/loadingIndicator';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark, IconWarning } from 'app/icons';
import space from 'app/styles/space';
function renderEmailValue(status, valueProps) {
    var children = valueProps.children, props = __rest(valueProps, ["children"]);
    var error = status && status.error;
    var emailLabel = status === undefined ? (children) : (<Tooltip disabled={!error} title={error}>
        <EmailLabel>
          {children}
          {!status.sent && !status.error && <SendingIndicator />}
          {status.error && <IconWarning size="10px"/>}
          {status.sent && <IconCheckmark size="10px" color="success"/>}
        </EmailLabel>
      </Tooltip>);
    return (<selectComponents.MultiValue {...props}>{emailLabel}</selectComponents.MultiValue>);
}
var EmailLabel = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(0.5));
var SendingIndicator = styled(LoadingIndicator)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n  .loading-indicator {\n    border-width: 2px;\n  }\n"], ["\n  margin: 0;\n  .loading-indicator {\n    border-width: 2px;\n  }\n"])));
SendingIndicator.defaultProps = {
    hideMessage: true,
    size: 14,
};
export default renderEmailValue;
var templateObject_1, templateObject_2;
//# sourceMappingURL=renderEmailValue.jsx.map
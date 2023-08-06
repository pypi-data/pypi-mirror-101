import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import classNames from 'classnames';
import ActionButton from './button';
import ConfirmableAction from './confirmableAction';
export default function ActionLink(_a) {
    var message = _a.message, className = _a.className, title = _a.title, onAction = _a.onAction, type = _a.type, confirmLabel = _a.confirmLabel, disabled = _a.disabled, children = _a.children, shouldConfirm = _a.shouldConfirm, confirmPriority = _a.confirmPriority, props = __rest(_a, ["message", "className", "title", "onAction", "type", "confirmLabel", "disabled", "children", "shouldConfirm", "confirmPriority"]);
    var action = (<StyledAction as={type === 'button' ? ActionButton : 'a'} aria-label={title} className={classNames(className, { disabled: disabled })} onClick={disabled ? undefined : onAction} disabled={disabled} {...props}>
      {children}
    </StyledAction>);
    if (shouldConfirm && onAction) {
        return (<ConfirmableAction shouldConfirm={shouldConfirm} priority={confirmPriority} disabled={disabled} message={message} confirmText={confirmLabel} onConfirm={onAction} stopPropagation={disabled}>
        {action}
      </ConfirmableAction>);
    }
    return action;
}
var StyledAction = styled('a')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  ", "\n"], ["\n  display: flex;\n  align-items: center;\n  ",
    "\n"])), function (p) {
    return p.disabled &&
        "\n    cursor: not-allowed;\n    ";
});
var templateObject_1;
//# sourceMappingURL=actionLink.jsx.map
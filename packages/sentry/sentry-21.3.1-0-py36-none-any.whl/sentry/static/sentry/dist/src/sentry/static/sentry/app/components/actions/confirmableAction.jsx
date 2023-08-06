import { __rest } from "tslib";
import React from 'react';
import Confirm from 'app/components/confirm';
export default function ConfirmableAction(_a) {
    var shouldConfirm = _a.shouldConfirm, children = _a.children, props = __rest(_a, ["shouldConfirm", "children"]);
    if (shouldConfirm) {
        return <Confirm {...props}>{children}</Confirm>;
    }
    return <React.Fragment>{children}</React.Fragment>;
}
//# sourceMappingURL=confirmableAction.jsx.map
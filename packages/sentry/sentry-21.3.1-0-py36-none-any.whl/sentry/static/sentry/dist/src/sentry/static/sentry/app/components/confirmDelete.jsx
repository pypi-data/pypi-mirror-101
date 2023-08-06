import { __rest } from "tslib";
import React from 'react';
import Alert from 'app/components/alert';
import Confirm from 'app/components/confirm';
import { t } from 'app/locale';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
var ConfirmDelete = function (_a) {
    var message = _a.message, confirmInput = _a.confirmInput, props = __rest(_a, ["message", "confirmInput"]);
    return (<Confirm {...props} bypass={false} disableConfirmButton renderMessage={function (_a) {
            var disableConfirmButton = _a.disableConfirmButton;
            return (<React.Fragment>
        <Alert type="error">{message}</Alert>
        <Field flexibleControlStateSize inline={false} label={t('Please enter %s to confirm the deletion', <code>{confirmInput}</code>)}>
          <Input type="text" placeholder={confirmInput} onChange={function (e) { return disableConfirmButton(e.target.value !== confirmInput); }}/>
        </Field>
      </React.Fragment>);
        }}/>);
};
export default ConfirmDelete;
//# sourceMappingURL=confirmDelete.jsx.map
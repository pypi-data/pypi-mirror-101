import React from 'react';
import { Observer } from 'mobx-react';
import FormState from 'app/components/forms/state';
import ControlState from 'app/views/settings/components/forms/field/controlState';
/**
 * ControlState (i.e. loading/error icons) for connected form components
 */
var FormFieldControlState = function (_a) {
    var model = _a.model, name = _a.name;
    return (<Observer>
    {function () {
            var isSaving = model.getFieldState(name, FormState.SAVING);
            var isSaved = model.getFieldState(name, FormState.READY);
            var error = model.getError(name);
            return <ControlState isSaving={isSaving} isSaved={isSaved} error={error}/>;
        }}
  </Observer>);
};
export default FormFieldControlState;
//# sourceMappingURL=controlState.jsx.map
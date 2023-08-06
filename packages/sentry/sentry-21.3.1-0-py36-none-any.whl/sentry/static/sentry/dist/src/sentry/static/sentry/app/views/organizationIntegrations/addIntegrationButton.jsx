import { __extends, __rest } from "tslib";
import React from 'react';
import Button from 'app/components/button';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import AddIntegration from './addIntegration';
var AddIntegrationButton = /** @class */ (function (_super) {
    __extends(AddIntegrationButton, _super);
    function AddIntegrationButton() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AddIntegrationButton.prototype.render = function () {
        var _a = this.props, provider = _a.provider, buttonText = _a.buttonText, onAddIntegration = _a.onAddIntegration, organization = _a.organization, reinstall = _a.reinstall, analyticsParams = _a.analyticsParams, modalParams = _a.modalParams, buttonProps = __rest(_a, ["provider", "buttonText", "onAddIntegration", "organization", "reinstall", "analyticsParams", "modalParams"]);
        var label = buttonText || t(reinstall ? 'Enable' : 'Add %s', provider.metadata.noun);
        return (<Tooltip disabled={provider.canAdd} title={"Integration cannot be added on Sentry. Enable this integration via the " + provider.name + " instance."}>
        <AddIntegration provider={provider} onInstall={onAddIntegration} organization={organization} analyticsParams={analyticsParams} modalParams={modalParams}>
          {function (onClick) { return (<Button disabled={!provider.canAdd} {...buttonProps} onClick={function () { return onClick(); }}>
              {label}
            </Button>); }}
        </AddIntegration>
      </Tooltip>);
    };
    return AddIntegrationButton;
}(React.Component));
export default AddIntegrationButton;
//# sourceMappingURL=addIntegrationButton.jsx.map
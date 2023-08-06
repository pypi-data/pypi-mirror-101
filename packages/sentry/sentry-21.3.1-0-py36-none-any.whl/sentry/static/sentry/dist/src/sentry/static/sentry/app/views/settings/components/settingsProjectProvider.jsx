import { __assign, __extends } from "tslib";
import React from 'react';
import SentryTypes from 'app/sentryTypes';
/**
 * Simple Component that takes project from context and passes it as props to children
 *
 * Don't do anything additional (e.g. loader) because not all children require project
 *
 * This is made because some components (e.g. ProjectPluginDetail) takes project as prop
 */
var SettingsProjectProvider = /** @class */ (function (_super) {
    __extends(SettingsProjectProvider, _super);
    function SettingsProjectProvider() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SettingsProjectProvider.prototype.render = function () {
        var children = this.props.children;
        var project = this.context.project;
        if (React.isValidElement(children)) {
            return React.cloneElement(children, __assign(__assign(__assign({}, this.props), children.props), { project: project }));
        }
        return null;
    };
    SettingsProjectProvider.contextTypes = {
        project: SentryTypes.Project,
    };
    return SettingsProjectProvider;
}(React.Component));
export default SettingsProjectProvider;
//# sourceMappingURL=settingsProjectProvider.jsx.map
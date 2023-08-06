import { __extends, __rest } from "tslib";
import React from 'react';
import PlatformList from 'app/components/platformList';
import Tooltip from 'app/components/tooltip';
var ProjectAvatar = /** @class */ (function (_super) {
    __extends(ProjectAvatar, _super);
    function ProjectAvatar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getPlatforms = function (project) {
            // `platform` is a user selectable option that is performed during the onboarding process. The reason why this
            // is not the default is because there currently is no way to update it. Fallback to this if project does not
            // have recent events with a platform.
            if (project && project.platform) {
                return [project.platform];
            }
            return [];
        };
        return _this;
    }
    ProjectAvatar.prototype.render = function () {
        var _a = this.props, project = _a.project, hasTooltip = _a.hasTooltip, tooltip = _a.tooltip, props = __rest(_a, ["project", "hasTooltip", "tooltip"]);
        return (<Tooltip disabled={!hasTooltip} title={tooltip}>
        <PlatformList platforms={this.getPlatforms(project)} {...props} max={1}/>
      </Tooltip>);
    };
    return ProjectAvatar;
}(React.Component));
export default ProjectAvatar;
//# sourceMappingURL=projectAvatar.jsx.map
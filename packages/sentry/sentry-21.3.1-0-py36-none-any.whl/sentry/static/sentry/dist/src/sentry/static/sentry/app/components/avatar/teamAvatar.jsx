import { __extends, __rest } from "tslib";
import React from 'react';
import BaseAvatar from 'app/components/avatar/baseAvatar';
import { explodeSlug } from 'app/utils';
var TeamAvatar = /** @class */ (function (_super) {
    __extends(TeamAvatar, _super);
    function TeamAvatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TeamAvatar.prototype.render = function () {
        var _a = this.props, team = _a.team, tooltipProp = _a.tooltip, props = __rest(_a, ["team", "tooltip"]);
        if (!team) {
            return null;
        }
        var slug = (team && team.slug) || '';
        var title = explodeSlug(slug);
        var tooltip = tooltipProp !== null && tooltipProp !== void 0 ? tooltipProp : "#" + title;
        return (<BaseAvatar {...props} type={(team.avatar && team.avatar.avatarType) || 'letter_avatar'} uploadPath="team-avatar" uploadId={team.avatar && team.avatar.avatarUuid} letterId={slug} tooltip={tooltip} title={title}/>);
    };
    return TeamAvatar;
}(React.Component));
export default TeamAvatar;
//# sourceMappingURL=teamAvatar.jsx.map
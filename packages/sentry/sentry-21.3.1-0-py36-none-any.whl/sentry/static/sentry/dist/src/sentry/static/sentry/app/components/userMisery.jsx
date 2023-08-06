import React from 'react';
import ScoreBar from 'app/components/scoreBar';
import Tooltip from 'app/components/tooltip';
import CHART_PALETTE from 'app/constants/chartPalette';
import { tct } from 'app/locale';
import { defined } from 'app/utils';
function UserMisery(props) {
    var bars = props.bars, barHeight = props.barHeight, userMisery = props.userMisery, miseryLimit = props.miseryLimit, totalUsers = props.totalUsers, miserableUsers = props.miserableUsers;
    // User Misery will always be > 0 because of the maximum a posteriori estimate
    // and below 5% will always be an overestimation of the actual proportion
    // of miserable to total unique users. We are going to visualize it as
    // 0 User Misery while still preserving the actual value for sorting purposes.
    var adjustedMisery = userMisery > 0.05 ? userMisery : 0;
    var palette = new Array(bars).fill([CHART_PALETTE[0][0]]);
    var score = Math.round(adjustedMisery * palette.length);
    var title;
    if (defined(miserableUsers) && defined(totalUsers) && defined(miseryLimit)) {
        title = tct('[miserableUsers] out of [totalUsers] unique users waited more than [duration]ms', {
            miserableUsers: miserableUsers,
            totalUsers: totalUsers,
            duration: 4 * miseryLimit,
        });
    }
    else if (defined(miseryLimit)) {
        title = tct('User Misery score is [userMisery], representing users who waited more than more than [duration]ms.', {
            duration: 4 * miseryLimit,
            userMisery: userMisery.toFixed(3),
        });
    }
    else {
        title = tct('User Misery score is [userMisery].', {
            userMisery: userMisery.toFixed(3),
        });
    }
    return (<Tooltip title={title} containerDisplayMode="block">
      <ScoreBar size={barHeight} score={score} palette={palette} radius={0}/>
    </Tooltip>);
}
export default UserMisery;
//# sourceMappingURL=userMisery.jsx.map
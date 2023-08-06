import React from 'react';
import getConfiguration from 'app/views/settings/account/navigationConfiguration';
import SettingsNavigation from 'app/views/settings/components/settingsNavigation';
var AccountSettingsNavigation = function (_a) {
    var organization = _a.organization;
    return (<SettingsNavigation navigationObjects={getConfiguration({ organization: organization })}/>);
};
export default AccountSettingsNavigation;
//# sourceMappingURL=accountSettingsNavigation.jsx.map
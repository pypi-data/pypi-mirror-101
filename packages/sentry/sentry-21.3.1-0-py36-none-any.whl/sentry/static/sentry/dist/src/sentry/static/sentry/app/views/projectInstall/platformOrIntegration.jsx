import React from 'react';
import * as qs from 'query-string';
import { platfromToIntegrationMap } from 'app/utils/integrationUtil';
import Platform from './platform';
import PlatformIntegrationSetup from './platformIntegrationSetup';
var PlatformOrIntegration = function (props) {
    var parsed = qs.parse(window.location.search);
    var platform = props.params.platform;
    var integrationSlug = platform && platfromToIntegrationMap[platform];
    // check for manual override query param
    if (integrationSlug && parsed.manual !== '1') {
        return <PlatformIntegrationSetup integrationSlug={integrationSlug} {...props}/>;
    }
    return <Platform {...props}/>;
};
export default PlatformOrIntegration;
//# sourceMappingURL=platformOrIntegration.jsx.map
import React from 'react';
import * as qs from 'query-string';
import { platfromToIntegrationMap } from 'app/utils/integrationUtil';
import ProjectSetup from './documentationSetup';
import IntegrationSetup from './integrationSetup';
var SdkConfiguration = function (props) {
    var parsed = qs.parse(window.location.search);
    var platform = props.platform;
    var integrationSlug = platform && platfromToIntegrationMap[platform];
    // check for manual override query param
    if (integrationSlug && parsed.manual !== '1') {
        return <IntegrationSetup integrationSlug={integrationSlug} {...props}/>;
    }
    return <ProjectSetup {...props}/>;
};
export default SdkConfiguration;
//# sourceMappingURL=sdkConfiguration.jsx.map
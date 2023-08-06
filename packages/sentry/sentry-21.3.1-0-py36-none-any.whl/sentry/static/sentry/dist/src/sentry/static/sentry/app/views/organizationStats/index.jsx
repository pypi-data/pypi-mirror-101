import React from 'react';
import withOrganization from 'app/utils/withOrganization';
import Redesign from '../usageStats';
import Container from './container';
var OrganizationStats = function (props) {
    return props.organization.features.includes('usage-stats-graph') ||
        window.localStorage.getItem('ORG_STATS_REDESIGN') ? (<Redesign {...props}/>) : (<Container {...props}/>);
};
export default withOrganization(OrganizationStats);
//# sourceMappingURL=index.jsx.map
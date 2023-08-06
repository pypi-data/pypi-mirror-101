import { __rest } from "tslib";
import React from 'react';
import Access from 'app/components/acl/access';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import { PanelAlert } from 'app/components/panels';
import { t } from 'app/locale';
import withOrganization from 'app/utils/withOrganization';
import FiltersAndSampling from './filtersAndSampling';
var Index = function (_a) {
    var organization = _a.organization, props = __rest(_a, ["organization"]);
    return (<Feature features={['filters-and-sampling']} organization={organization} renderDisabled={function () { return (<FeatureDisabled alert={PanelAlert} features={organization.features} featureName={t('Filters & Sampling')}/>); }}>
    <Access organization={organization} access={['project:write']}>
      {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<FiltersAndSampling {...props} hasAccess={hasAccess} organization={organization}/>);
        }}
    </Access>
  </Feature>);
};
export default withOrganization(Index);
//# sourceMappingURL=index.jsx.map
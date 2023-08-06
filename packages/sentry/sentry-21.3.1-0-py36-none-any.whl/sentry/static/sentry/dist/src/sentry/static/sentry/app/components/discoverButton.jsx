import { __rest } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import Button from 'app/components/button';
import Hovercard from 'app/components/hovercard';
import { t } from 'app/locale';
/**
 * Provide a button that turns itself off if the current organization
 * doesn't have access to discover results.
 */
function DiscoverButton(_a) {
    var children = _a.children, buttonProps = __rest(_a, ["children"]);
    var noFeatureMessage = t('Requires discover feature.');
    var renderDisabled = function (p) { return (<Hovercard body={<FeatureDisabled features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
      {p.children(p)}
    </Hovercard>); };
    return (<Feature hookName="feature-disabled:open-discover" features={['organizations:discover-basic']} renderDisabled={renderDisabled}>
      {function (_a) {
            var hasFeature = _a.hasFeature;
            return (<Button disabled={!hasFeature} {...buttonProps}>
          {children}
        </Button>);
        }}
    </Feature>);
}
export default DiscoverButton;
//# sourceMappingURL=discoverButton.jsx.map
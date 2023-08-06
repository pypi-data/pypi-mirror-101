import { __rest } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import withOrganization from 'app/utils/withOrganization';
import WidgetNew from './widgetNew';
function WidgetNewContainer(_a) {
    var organization = _a.organization, props = __rest(_a, ["organization"]);
    return (<Feature features={['metrics']} organization={organization} renderDisabled={function () { return (<PageContent>
          <Alert type="warning">{t("You don't have access to this feature")}</Alert>
        </PageContent>); }}>
      <WidgetNew {...props}/>
    </Feature>);
}
export default withOrganization(WidgetNewContainer);
//# sourceMappingURL=index.jsx.map
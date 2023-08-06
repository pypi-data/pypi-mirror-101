import { __extends } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import withOrganization from 'app/utils/withOrganization';
var DashboardsV2Container = /** @class */ (function (_super) {
    __extends(DashboardsV2Container, _super);
    function DashboardsV2Container() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DashboardsV2Container.prototype.render = function () {
        var _a = this.props, organization = _a.organization, children = _a.children;
        return (<Feature features={['dashboards-basic']} organization={organization}>
        {children}
      </Feature>);
    };
    return DashboardsV2Container;
}(React.Component));
export default withOrganization(DashboardsV2Container);
//# sourceMappingURL=index.jsx.map
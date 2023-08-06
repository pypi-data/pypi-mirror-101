import { __extends } from "tslib";
import React from 'react';
import AsyncComponent from 'app/components/asyncComponent';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel, PanelBody } from 'app/components/panels';
var UsageStatsProjects = /** @class */ (function (_super) {
    __extends(UsageStatsProjects, _super);
    function UsageStatsProjects() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    UsageStatsProjects.prototype.getEndpoints = function () {
        var organization = this.props.organization;
        return [
            [
                'orgStats',
                "/organizations/" + organization.slug + "/stats_v2/projects/",
                {
                    query: {
                        interval: '1d',
                    },
                },
            ],
        ];
    };
    UsageStatsProjects.prototype.renderError = function (e) {
        return (<Panel>
        <PanelBody>UsageStatsProjects has an error: {e.message}</PanelBody>
      </Panel>);
    };
    UsageStatsProjects.prototype.renderLoading = function () {
        return (<Panel>
        <PanelBody>
          <LoadingIndicator />
        </PanelBody>
      </Panel>);
    };
    UsageStatsProjects.prototype.renderBody = function () {
        return (<Panel>
        <PanelBody>UsageStatsProjects is okay</PanelBody>
      </Panel>);
    };
    return UsageStatsProjects;
}(AsyncComponent));
export default UsageStatsProjects;
//# sourceMappingURL=usageStatsProjects.jsx.map
import { __extends } from "tslib";
import React from 'react';
import { ChartContainer, ChartControls, InlineContainer, SectionHeading, SectionValue, } from 'app/components/charts/styles';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import withApi from 'app/utils/withApi';
import ProjectBaseSessionsChart from 'app/views/projectDetail/charts/projectBaseSessionsChart';
import { DisplayModes } from 'app/views/projectDetail/projectCharts';
import { getSessionTermDescription, SessionTerm } from '../utils/sessionTerm';
var ReleasesStabilityChart = /** @class */ (function (_super) {
    __extends(ReleasesStabilityChart, _super);
    function ReleasesStabilityChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            totalValues: null,
        };
        _this.handleTotalValuesChange = function (value) {
            if (value !== _this.state.totalValues) {
                _this.setState({ totalValues: value });
            }
        };
        return _this;
    }
    ReleasesStabilityChart.prototype.render = function () {
        var _a = this.props, api = _a.api, router = _a.router, organization = _a.organization;
        var totalValues = this.state.totalValues;
        return (<Panel>
        <ChartContainer>
          <ProjectBaseSessionsChart title={t('Crash Free Sessions')} help={getSessionTermDescription(SessionTerm.STABILITY, null)} router={router} api={api} organization={organization} onTotalValuesChange={this.handleTotalValuesChange} displayMode={DisplayModes.STABILITY}/>
        </ChartContainer>
        <ChartControls>
          <InlineContainer>
            <SectionHeading>{t('Total Sessions')}</SectionHeading>
            <SectionValue>
              {typeof totalValues === 'number' ? totalValues.toLocaleString() : '\u2014'}
            </SectionValue>
          </InlineContainer>
        </ChartControls>
      </Panel>);
    };
    return ReleasesStabilityChart;
}(React.Component));
export default withApi(ReleasesStabilityChart);
//# sourceMappingURL=releasesStabilityChart.jsx.map
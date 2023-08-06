import { __extends } from "tslib";
import React from 'react';
import capitalize from 'lodash/capitalize';
import moment from 'moment';
import PageHeading from 'app/components/pageHeading';
import { tct } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import { DataCategory } from 'app/types';
import UsageStatsOrg from './usageStatsOrg';
import UsageStatsProjects from './usageStatsProjects';
var OrganizationStats = /** @class */ (function (_super) {
    __extends(OrganizationStats, _super);
    function OrganizationStats() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dataCategory: DataCategory.ERRORS,
            dateStart: moment().subtract(14, 'days'),
            dateEnd: moment(),
        };
        _this.setDataCategory = function (dataCategory) {
            _this.setState({ dataCategory: dataCategory });
        };
        _this.setDateRange = function (dateStart, dateEnd) {
            _this.setState({ dateStart: dateStart, dateEnd: dateEnd });
        };
        return _this;
    }
    Object.defineProperty(OrganizationStats.prototype, "dataCategoryName", {
        get: function () {
            return capitalize(this.state.dataCategory);
        },
        enumerable: false,
        configurable: true
    });
    OrganizationStats.prototype.render = function () {
        var organization = this.props.organization;
        var _a = this.state, dataCategory = _a.dataCategory, dateStart = _a.dateStart, dateEnd = _a.dateEnd;
        return (<PageContent>
        <PageHeader>
          <PageHeading>
            {tct('Organization Usage Stats for [dataCategory]', {
                dataCategory: this.dataCategoryName,
            })}
          </PageHeading>
        </PageHeader>

        <UsageStatsOrg organization={organization} dataCategory={dataCategory} dataCategoryName={this.dataCategoryName} dateStart={dateStart} dateEnd={dateEnd} onChangeDataCategory={this.setDataCategory} onChangeDateRange={this.setDateRange}/>

        <UsageStatsProjects organization={organization} dataCategory={dataCategory} dataCategoryName={this.dataCategoryName} dateStart={dateStart} dateEnd={dateEnd}/>
      </PageContent>);
    };
    return OrganizationStats;
}(React.Component));
export default OrganizationStats;
//# sourceMappingURL=index.jsx.map
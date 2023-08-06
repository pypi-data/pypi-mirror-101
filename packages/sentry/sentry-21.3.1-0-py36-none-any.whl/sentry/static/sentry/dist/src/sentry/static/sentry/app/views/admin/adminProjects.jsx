import { __extends } from "tslib";
import React from 'react';
import moment from 'moment';
import ResultGrid from 'app/components/resultGrid';
import { t } from 'app/locale';
import AsyncView from 'app/views/asyncView';
var AdminProjects = /** @class */ (function (_super) {
    __extends(AdminProjects, _super);
    function AdminProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getRow = function (row) { return [
            <td key="name">
      <strong>
        <a href={"/" + row.organization.slug + "/" + row.slug + "/"}>{row.name}</a>
      </strong>
      <br />
      <small>{row.organization.name}</small>
    </td>,
            <td key="status" style={{ textAlign: 'center' }}>
      {row.status}
    </td>,
            <td key="dateCreated" style={{ textAlign: 'right' }}>
      {moment(row.dateCreated).format('ll')}
    </td>,
        ]; };
        return _this;
    }
    AdminProjects.prototype.render = function () {
        var columns = [
            <th key="name">Project</th>,
            <th key="status" style={{ width: 150, textAlign: 'center' }}>
        Status
      </th>,
            <th key="dateCreated" style={{ width: 200, textAlign: 'right' }}>
        Created
      </th>,
        ];
        return (<div>
        <h3>{t('Projects')}</h3>
        <ResultGrid path="/manage/projects/" endpoint="/projects/?show=all" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch filters={{
                status: {
                    name: 'Status',
                    options: [
                        ['active', 'Active'],
                        ['deleted', 'Deleted'],
                    ],
                },
            }} sortOptions={[['date', 'Date Created']]} defaultSort="date" {...this.props}/>
      </div>);
    };
    return AdminProjects;
}(AsyncView));
export default AdminProjects;
//# sourceMappingURL=adminProjects.jsx.map
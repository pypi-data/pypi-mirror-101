import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PanelTable, { PanelTableHeader } from 'app/components/panels/panelTable';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { fieldAlignment } from 'app/utils/discover/fields';
import withOrganization from 'app/utils/withOrganization';
import { decodeColumnOrder } from 'app/views/eventsV2/utils';
var SimpleTableChart = /** @class */ (function (_super) {
    __extends(SimpleTableChart, _super);
    function SimpleTableChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SimpleTableChart.prototype.renderRow = function (index, row, tableMeta, columns) {
        var _a = this.props, location = _a.location, organization = _a.organization;
        return columns.map(function (column) {
            var fieldRenderer = getFieldRenderer(column.name, tableMeta);
            var rendered = fieldRenderer(row, { organization: organization, location: location });
            return <div key={index + ":" + column.name}>{rendered}</div>;
        });
    };
    SimpleTableChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, loading = _a.loading, fields = _a.fields, metadata = _a.metadata, data = _a.data, title = _a.title;
        var meta = metadata !== null && metadata !== void 0 ? metadata : {};
        var columns = decodeColumnOrder(fields.map(function (field) { return ({ field: field }); }));
        return (<React.Fragment>
        {title && <h4>{title}</h4>}
        <StyledPanelTable className={className} isLoading={loading} headers={columns.map(function (column, index) {
                var align = fieldAlignment(column.name, column.type, meta);
                return (<HeadCell key={index} align={align}>
                {column.name}
              </HeadCell>);
            })}>
          {data === null || data === void 0 ? void 0 : data.map(function (row, index) { return _this.renderRow(index, row, meta, columns); })}
        </StyledPanelTable>
      </React.Fragment>);
    };
    return SimpleTableChart;
}(React.Component));
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  border-radius: 0;\n  border-left: 0;\n  border-right: 0;\n  border-bottom: 0;\n\n  margin: 0;\n  ", " {\n    height: min-content;\n  }\n"], ["\n  border-radius: 0;\n  border-left: 0;\n  border-right: 0;\n  border-bottom: 0;\n\n  margin: 0;\n  " /* sc-selector */, " {\n    height: min-content;\n  }\n"])), /* sc-selector */ PanelTableHeader);
var HeadCell = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), function (p) { return (p.align ? "text-align: " + p.align + ";" : ''); });
export default withOrganization(SimpleTableChart);
var templateObject_1, templateObject_2;
//# sourceMappingURL=simpleTableChart.jsx.map
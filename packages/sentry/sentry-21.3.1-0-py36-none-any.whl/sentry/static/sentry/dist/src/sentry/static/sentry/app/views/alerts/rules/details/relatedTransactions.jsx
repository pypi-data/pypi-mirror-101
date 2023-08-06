import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import GridEditable, { COL_WIDTH_UNDEFINED } from 'app/components/gridEditable';
import Link from 'app/components/links/link';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import EventView from 'app/utils/discover/eventView';
import { getFieldRenderer } from 'app/utils/discover/fieldRenderers';
import { fieldAlignment } from 'app/utils/discover/fields';
import { transactionSummaryRouteWithQuery } from 'app/views/performance/transactionSummary/utils';
var COLUMN_TITLES = ['slowest transactions', 'project', 'p95', 'users', 'user misery'];
export function getProjectID(eventData, projects) {
    var projectSlug = (eventData === null || eventData === void 0 ? void 0 : eventData.project) || undefined;
    if (typeof projectSlug === undefined) {
        return undefined;
    }
    var project = projects.find(function (currentProject) { return currentProject.slug === projectSlug; });
    if (!project) {
        return undefined;
    }
    return project.id;
}
var Table = /** @class */ (function (_super) {
    __extends(Table, _super);
    function Table() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            widths: [],
        };
        _this.renderBodyCellWithData = function (tableData) {
            return function (column, dataRow) { return _this.renderBodyCell(tableData, column, dataRow); };
        };
        _this.renderHeadCellWithMeta = function (tableMeta) {
            return function (column, index) {
                return _this.renderHeadCell(tableMeta, column, COLUMN_TITLES[index]);
            };
        };
        _this.handleResizeColumn = function (columnIndex, nextColumn) {
            var widths = __spreadArray([], __read(_this.state.widths));
            widths[columnIndex] = nextColumn.width
                ? Number(nextColumn.width)
                : COL_WIDTH_UNDEFINED;
            _this.setState({ widths: widths });
        };
        return _this;
    }
    Table.prototype.renderBodyCell = function (tableData, column, dataRow) {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects, location = _a.location, summaryConditions = _a.summaryConditions;
        if (!tableData || !tableData.meta) {
            return dataRow[column.key];
        }
        var tableMeta = tableData.meta;
        var field = String(column.key);
        var fieldRenderer = getFieldRenderer(field, tableMeta);
        var rendered = fieldRenderer(dataRow, { organization: organization, location: location });
        if (field === 'transaction') {
            var projectID = getProjectID(dataRow, projects);
            var summaryView = eventView.clone();
            summaryView.query = summaryConditions;
            var target = transactionSummaryRouteWithQuery({
                orgSlug: organization.slug,
                transaction: String(dataRow.transaction) || '',
                query: summaryView.generateQueryStringObject(),
                projectID: projectID,
            });
            return <Link to={target}>{rendered}</Link>;
        }
        return rendered;
    };
    Table.prototype.renderHeadCell = function (tableMeta, column, title) {
        var align = fieldAlignment(column.name, column.type, tableMeta);
        var field = { field: column.name, width: column.width };
        return <HeaderCell align={align}>{title || field.field}</HeaderCell>;
    };
    Table.prototype.getSortedEventView = function () {
        var eventView = this.props.eventView;
        return eventView.withSorts(__spreadArray([], __read(eventView.sorts)));
    };
    Table.prototype.render = function () {
        var _this = this;
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, location = _a.location;
        var widths = this.state.widths;
        var columnOrder = eventView
            .getColumns()
            .map(function (col, i) {
            if (typeof widths[i] === 'number') {
                return __assign(__assign({}, col), { width: widths[i] });
            }
            return col;
        });
        var sortedEventView = this.getSortedEventView();
        var columnSortBy = sortedEventView.getSorts();
        return (<React.Fragment>
        <DiscoverQuery eventView={sortedEventView} orgSlug={organization.slug} location={location}>
          {function (_a) {
                var isLoading = _a.isLoading, tableData = _a.tableData;
                return (<GridEditable isLoading={isLoading} data={tableData ? tableData.data.slice(0, 5) : []} columnOrder={columnOrder} columnSortBy={columnSortBy} grid={{
                        onResizeColumn: _this.handleResizeColumn,
                        renderHeadCell: _this.renderHeadCellWithMeta(tableData === null || tableData === void 0 ? void 0 : tableData.meta),
                        renderBodyCell: _this.renderBodyCellWithData(tableData),
                    }} location={location}/>);
            }}
        </DiscoverQuery>
      </React.Fragment>);
    };
    return Table;
}(React.Component));
var RelatedTransactions = /** @class */ (function (_super) {
    __extends(RelatedTransactions, _super);
    function RelatedTransactions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RelatedTransactions.prototype.render = function () {
        var _a = this.props, rule = _a.rule, projects = _a.projects, filter = _a.filter, location = _a.location, organization = _a.organization, start = _a.start, end = _a.end;
        var eventQuery = {
            id: undefined,
            name: 'Slowest Transactions',
            fields: [
                'transaction',
                'project',
                'p95()',
                'count_unique(user)',
                "user_misery(" + organization.apdexThreshold + ")",
            ],
            orderby: "user_misery(" + organization.apdexThreshold + ")",
            query: "" + rule.query,
            version: 2,
            projects: projects.map(function (project) { return Number(project.id); }),
            start: start,
            end: end,
        };
        var eventView = EventView.fromSavedQuery(eventQuery);
        return (<Table eventView={eventView} projects={projects} organization={organization} location={location} summaryConditions={rule.query + " " + filter}/>);
    };
    return RelatedTransactions;
}(React.Component));
export default RelatedTransactions;
var HeaderCell = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  ", "\n"], ["\n  display: block;\n  width: 100%;\n  white-space: nowrap;\n  ", "\n"])), function (p) { return (p.align ? "text-align: " + p.align + ";" : ''); });
var templateObject_1;
//# sourceMappingURL=relatedTransactions.jsx.map
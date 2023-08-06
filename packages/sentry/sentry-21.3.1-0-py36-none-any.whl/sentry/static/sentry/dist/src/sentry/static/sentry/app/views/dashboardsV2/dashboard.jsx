import { __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import { closestCenter, DndContext } from '@dnd-kit/core';
import { arrayMove, rectSortingStrategy, SortableContext } from '@dnd-kit/sortable';
import styled from '@emotion/styled';
import { openAddDashboardWidgetModal } from 'app/actionCreators/modal';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import AddWidget, { ADD_WIDGET_BUTTON_DRAG_ID } from './addWidget';
import SortableWidget from './sortableWidget';
var Dashboard = /** @class */ (function (_super) {
    __extends(Dashboard, _super);
    function Dashboard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleStartAdd = function () {
            var _a = _this.props, organization = _a.organization, dashboard = _a.dashboard, selection = _a.selection;
            openAddDashboardWidgetModal({
                organization: organization,
                dashboard: dashboard,
                selection: selection,
                onAddWidget: _this.handleAddComplete,
            });
        };
        _this.handleAddComplete = function (widget) {
            _this.props.onUpdate(__spreadArray(__spreadArray([], __read(_this.props.dashboard.widgets)), [widget]));
        };
        _this.handleUpdateComplete = function (index) { return function (nextWidget) {
            var nextList = __spreadArray([], __read(_this.props.dashboard.widgets));
            nextList[index] = nextWidget;
            _this.props.onUpdate(nextList);
        }; };
        _this.handleDeleteWidget = function (index) { return function () {
            var nextList = __spreadArray([], __read(_this.props.dashboard.widgets));
            nextList.splice(index, 1);
            _this.props.onUpdate(nextList);
        }; };
        _this.handleEditWidget = function (widget, index) { return function () {
            var _a = _this.props, organization = _a.organization, dashboard = _a.dashboard, selection = _a.selection;
            openAddDashboardWidgetModal({
                organization: organization,
                dashboard: dashboard,
                widget: widget,
                selection: selection,
                onAddWidget: _this.handleAddComplete,
                onUpdateWidget: _this.handleUpdateComplete(index),
            });
        }; };
        return _this;
    }
    Dashboard.prototype.componentDidMount = function () {
        var isEditing = this.props.isEditing;
        // Load organization tags when in edit mode.
        if (isEditing) {
            this.fetchTags();
        }
    };
    Dashboard.prototype.componentDidUpdate = function (prevProps) {
        var isEditing = this.props.isEditing;
        // Load organization tags when going into edit mode.
        // We use tags on the add widget modal.
        if (prevProps.isEditing !== isEditing && isEditing) {
            this.fetchTags();
        }
    };
    Dashboard.prototype.fetchTags = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
    };
    Dashboard.prototype.getWidgetIds = function () {
        return __spreadArray(__spreadArray([], __read(this.props.dashboard.widgets.map(function (widget, index) {
            return generateWidgetId(widget, index);
        }))), [
            ADD_WIDGET_BUTTON_DRAG_ID,
        ]);
    };
    Dashboard.prototype.renderWidget = function (widget, index) {
        var isEditing = this.props.isEditing;
        var key = generateWidgetId(widget, index);
        var dragId = key;
        return (<SortableWidget key={key} widget={widget} dragId={dragId} isEditing={isEditing} onDelete={this.handleDeleteWidget(index)} onEdit={this.handleEditWidget(widget, index)}/>);
    };
    Dashboard.prototype.render = function () {
        var _this = this;
        var _a = this.props, isEditing = _a.isEditing, onUpdate = _a.onUpdate, widgets = _a.dashboard.widgets, organization = _a.organization;
        var items = this.getWidgetIds();
        return (<DndContext collisionDetection={closestCenter} onDragEnd={function (_a) {
                var over = _a.over, active = _a.active;
                var activeDragId = active.id;
                var getIndex = items.indexOf.bind(items);
                var activeIndex = activeDragId ? getIndex(activeDragId) : -1;
                if (over && over.id !== ADD_WIDGET_BUTTON_DRAG_ID) {
                    var overIndex = getIndex(over.id);
                    if (activeIndex !== overIndex) {
                        onUpdate(arrayMove(widgets, activeIndex, overIndex));
                    }
                }
            }}>
        <WidgetContainer>
          <SortableContext items={items} strategy={rectSortingStrategy}>
            {widgets.map(function (widget, index) { return _this.renderWidget(widget, index); })}
            {isEditing && (<AddWidget orgSlug={organization.slug} orgFeatures={organization.features} onClick={this.handleStartAdd}/>)}
          </SortableContext>
        </WidgetContainer>
      </DndContext>);
    };
    return Dashboard;
}(React.Component));
export default withApi(withGlobalSelection(Dashboard));
var WidgetContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  grid-auto-flow: row dense;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(6, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(8, minmax(0, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(0, 1fr));\n  grid-auto-flow: row dense;\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(4, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(6, minmax(0, 1fr));\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(8, minmax(0, 1fr));\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.breakpoints[3]; }, function (p) { return p.theme.breakpoints[4]; });
function generateWidgetId(widget, index) {
    return widget.id ? widget.id + "-index-" + index : "index-" + index;
}
var templateObject_1;
//# sourceMappingURL=dashboard.jsx.map
import { __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import ReactDOM from 'react-dom';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { SectionHeading } from 'app/components/charts/styles';
import { IconAdd, IconDelete, IconGrabbable } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
import { getPointerPosition } from 'app/utils/touch';
import { setBodyUserSelect } from 'app/utils/userselect';
import { QueryField } from './queryField';
var DRAG_CLASS = 'draggable-item';
var GHOST_PADDING = 4;
var MAX_COL_COUNT = 20;
var PlaceholderPosition;
(function (PlaceholderPosition) {
    PlaceholderPosition[PlaceholderPosition["TOP"] = 0] = "TOP";
    PlaceholderPosition[PlaceholderPosition["BOTTOM"] = 1] = "BOTTOM";
})(PlaceholderPosition || (PlaceholderPosition = {}));
var ColumnEditCollection = /** @class */ (function (_super) {
    __extends(ColumnEditCollection, _super);
    function ColumnEditCollection() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isDragging: false,
            draggingIndex: void 0,
            draggingTargetIndex: void 0,
            draggingGrabbedOffset: void 0,
            left: void 0,
            top: void 0,
        };
        _this.previousUserSelect = null;
        _this.portal = null;
        _this.dragGhostRef = React.createRef();
        // Signal to the parent that a new column has been added.
        _this.handleAddColumn = function () {
            var newColumn = { kind: 'field', field: '' };
            _this.props.onChange(__spreadArray(__spreadArray([], __read(_this.props.columns)), [newColumn]));
        };
        _this.handleUpdateColumn = function (index, column) {
            var newColumns = __spreadArray([], __read(_this.props.columns));
            newColumns.splice(index, 1, column);
            _this.props.onChange(newColumns);
        };
        _this.onDragMove = function (event) {
            var _a, _b;
            var _c = _this.state, isDragging = _c.isDragging, draggingTargetIndex = _c.draggingTargetIndex, draggingGrabbedOffset = _c.draggingGrabbedOffset;
            if (!isDragging || !['mousemove', 'touchmove'].includes(event.type)) {
                return;
            }
            event.preventDefault();
            event.stopPropagation();
            var pointerX = getPointerPosition(event, 'pageX');
            var pointerY = getPointerPosition(event, 'pageY');
            var dragOffsetX = (_a = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.x) !== null && _a !== void 0 ? _a : 0;
            var dragOffsetY = (_b = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.y) !== null && _b !== void 0 ? _b : 0;
            if (_this.dragGhostRef.current) {
                // move the ghost box
                var ghostDOM = _this.dragGhostRef.current;
                // Adjust so cursor is over the grab handle.
                ghostDOM.style.left = pointerX - dragOffsetX + "px";
                ghostDOM.style.top = pointerY - dragOffsetY + "px";
            }
            var dragItems = document.querySelectorAll("." + DRAG_CLASS);
            // Find the item that the ghost is currently over.
            var targetIndex = Array.from(dragItems).findIndex(function (dragItem) {
                var rects = dragItem.getBoundingClientRect();
                var top = pointerY;
                var thresholdStart = window.scrollY + rects.top;
                var thresholdEnd = window.scrollY + rects.top + rects.height;
                return top >= thresholdStart && top <= thresholdEnd;
            });
            if (targetIndex >= 0 && targetIndex !== draggingTargetIndex) {
                _this.setState({ draggingTargetIndex: targetIndex });
            }
        };
        _this.onDragEnd = function (event) {
            if (!_this.state.isDragging || !['mouseup', 'touchend'].includes(event.type)) {
                return;
            }
            var sourceIndex = _this.state.draggingIndex;
            var targetIndex = _this.state.draggingTargetIndex;
            if (typeof sourceIndex !== 'number' || typeof targetIndex !== 'number') {
                return;
            }
            // remove listeners that were attached in startColumnDrag
            _this.cleanUpListeners();
            // restore body user-select values
            if (_this.previousUserSelect) {
                setBodyUserSelect(_this.previousUserSelect);
                _this.previousUserSelect = null;
            }
            // Reorder columns and trigger change.
            var newColumns = __spreadArray([], __read(_this.props.columns));
            var removed = newColumns.splice(sourceIndex, 1);
            newColumns.splice(targetIndex, 0, removed[0]);
            _this.props.onChange(newColumns);
            _this.setState({
                isDragging: false,
                left: undefined,
                top: undefined,
                draggingIndex: undefined,
                draggingTargetIndex: undefined,
                draggingGrabbedOffset: undefined,
            });
        };
        return _this;
    }
    ColumnEditCollection.prototype.componentDidMount = function () {
        if (!this.portal) {
            var portal = document.createElement('div');
            portal.style.position = 'absolute';
            portal.style.top = '0';
            portal.style.left = '0';
            portal.style.zIndex = String(theme.zIndex.modal);
            this.portal = portal;
            document.body.appendChild(this.portal);
        }
    };
    ColumnEditCollection.prototype.componentWillUnmount = function () {
        if (this.portal) {
            document.body.removeChild(this.portal);
        }
        this.cleanUpListeners();
    };
    ColumnEditCollection.prototype.keyForColumn = function (column, isGhost) {
        if (column.kind === 'function') {
            return __spreadArray(__spreadArray([], __read(column.function)), [isGhost]).join(':');
        }
        return __spreadArray(__spreadArray([], __read(column.field)), [isGhost]).join(':');
    };
    ColumnEditCollection.prototype.cleanUpListeners = function () {
        if (this.state.isDragging) {
            window.removeEventListener('mousemove', this.onDragMove);
            window.removeEventListener('touchmove', this.onDragMove);
            window.removeEventListener('mouseup', this.onDragEnd);
            window.removeEventListener('touchend', this.onDragEnd);
        }
    };
    ColumnEditCollection.prototype.removeColumn = function (index) {
        var newColumns = __spreadArray([], __read(this.props.columns));
        newColumns.splice(index, 1);
        this.props.onChange(newColumns);
    };
    ColumnEditCollection.prototype.startDrag = function (event, index) {
        var isDragging = this.state.isDragging;
        if (isDragging || !['mousedown', 'touchstart'].includes(event.type)) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        var top = getPointerPosition(event, 'pageY');
        var left = getPointerPosition(event, 'pageX');
        // Compute where the user clicked on the drag handle. Avoids the element
        // jumping from the cursor on mousedown.
        var _a = Array.from(document.querySelectorAll("." + DRAG_CLASS))
            .find(function (n) { return n.contains(event.currentTarget); })
            .getBoundingClientRect(), x = _a.x, y = _a.y;
        var draggingGrabbedOffset = {
            x: left - x + GHOST_PADDING,
            y: top - y + GHOST_PADDING,
        };
        // prevent the user from selecting things when dragging a column.
        this.previousUserSelect = setBodyUserSelect({
            userSelect: 'none',
            MozUserSelect: 'none',
            msUserSelect: 'none',
            webkitUserSelect: 'none',
        });
        // attach event listeners so that the mouse cursor can drag anywhere
        window.addEventListener('mousemove', this.onDragMove);
        window.addEventListener('touchmove', this.onDragMove);
        window.addEventListener('mouseup', this.onDragEnd);
        window.addEventListener('touchend', this.onDragEnd);
        this.setState({
            isDragging: true,
            draggingIndex: index,
            draggingTargetIndex: index,
            draggingGrabbedOffset: draggingGrabbedOffset,
            top: top,
            left: left,
        });
    };
    ColumnEditCollection.prototype.renderGhost = function (gridColumns) {
        var _a, _b;
        var _c = this.state, isDragging = _c.isDragging, draggingIndex = _c.draggingIndex, draggingGrabbedOffset = _c.draggingGrabbedOffset;
        var index = draggingIndex;
        if (typeof index !== 'number' || !isDragging || !this.portal) {
            return null;
        }
        var dragOffsetX = (_a = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.x) !== null && _a !== void 0 ? _a : 0;
        var dragOffsetY = (_b = draggingGrabbedOffset === null || draggingGrabbedOffset === void 0 ? void 0 : draggingGrabbedOffset.y) !== null && _b !== void 0 ? _b : 0;
        var top = Number(this.state.top) - dragOffsetY;
        var left = Number(this.state.left) - dragOffsetX;
        var col = this.props.columns[index];
        var style = {
            top: top + "px",
            left: left + "px",
        };
        var ghost = (<Ghost ref={this.dragGhostRef} style={style}>
        {this.renderItem(col, index, { isGhost: true, gridColumns: gridColumns })}
      </Ghost>);
        return ReactDOM.createPortal(ghost, this.portal);
    };
    ColumnEditCollection.prototype.renderItem = function (col, i, _a) {
        var _this = this;
        var _b = _a.canDelete, canDelete = _b === void 0 ? true : _b, _c = _a.isGhost, isGhost = _c === void 0 ? false : _c, _d = _a.gridColumns, gridColumns = _d === void 0 ? 2 : _d;
        var fieldOptions = this.props.fieldOptions;
        var _e = this.state, isDragging = _e.isDragging, draggingTargetIndex = _e.draggingTargetIndex, draggingIndex = _e.draggingIndex;
        var placeholder = null;
        // Add a placeholder above the target row.
        if (isDragging && isGhost === false && draggingTargetIndex === i) {
            placeholder = (<DragPlaceholder key={"placeholder:" + this.keyForColumn(col, isGhost)} className={DRAG_CLASS}/>);
        }
        // If the current row is the row in the drag ghost return the placeholder
        // or a hole if the placeholder is elsewhere.
        if (isDragging && isGhost === false && draggingIndex === i) {
            return placeholder;
        }
        var position = Number(draggingTargetIndex) <= Number(draggingIndex)
            ? PlaceholderPosition.TOP
            : PlaceholderPosition.BOTTOM;
        return (<React.Fragment key={i + ":" + this.keyForColumn(col, isGhost)}>
        {position === PlaceholderPosition.TOP && placeholder}
        <RowContainer className={isGhost ? '' : DRAG_CLASS}>
          {canDelete ? (<Button aria-label={t('Drag to reorder')} onMouseDown={function (event) { return _this.startDrag(event, i); }} onTouchStart={function (event) { return _this.startDrag(event, i); }} icon={<IconGrabbable size="xs"/>} size="zero" borderless/>) : (<span />)}
          <QueryField fieldOptions={fieldOptions} gridColumns={gridColumns} fieldValue={col} onChange={function (value) { return _this.handleUpdateColumn(i, value); }} takeFocus={i === this.props.columns.length - 1}/>
          {canDelete ? (<Button aria-label={t('Remove column')} onClick={function () { return _this.removeColumn(i); }} icon={<IconDelete />} borderless/>) : (<span />)}
        </RowContainer>
        {position === PlaceholderPosition.BOTTOM && placeholder}
      </React.Fragment>);
    };
    ColumnEditCollection.prototype.render = function () {
        var _this = this;
        var _a = this.props, className = _a.className, columns = _a.columns;
        var canDelete = columns.length > 1;
        var canAdd = columns.length < MAX_COL_COUNT;
        var title = canAdd
            ? undefined
            : "Sorry, you reached the maximum number of columns. Delete columns to add more.";
        // Get the longest number of columns so we can layout the rows.
        // We always want at least 2 columns.
        var gridColumns = Math.max.apply(Math, __spreadArray([], __read(columns.map(function (col) {
            return col.kind === 'function' && col.function[2] !== undefined ? 3 : 2;
        }))));
        return (<div className={className}>
        {this.renderGhost(gridColumns)}
        <RowContainer>
          <Heading gridColumns={gridColumns}>
            <StyledSectionHeading>{t('Tag / Field / Function')}</StyledSectionHeading>
            <StyledSectionHeading>{t('Field Parameter')}</StyledSectionHeading>
          </Heading>
        </RowContainer>
        {columns.map(function (col, i) {
                return _this.renderItem(col, i, { canDelete: canDelete, gridColumns: gridColumns });
            })}
        <RowContainer>
          <Actions>
            <Button size="small" label={t('Add a Column')} onClick={this.handleAddColumn} title={title} disabled={!canAdd} icon={<IconAdd isCircled size="xs"/>}>
              {t('Add a Column')}
            </Button>
          </Actions>
        </RowContainer>
      </div>);
    };
    return ColumnEditCollection;
}(React.Component));
var RowContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: ", " 1fr ", ";\n  justify-content: center;\n  align-items: center;\n  width: 100%;\n  touch-action: none;\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: ", " 1fr ", ";\n  justify-content: center;\n  align-items: center;\n  width: 100%;\n  touch-action: none;\n  padding-bottom: ", ";\n"])), space(3), space(3), space(1));
var Ghost = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: ", ";\n  display: block;\n  position: absolute;\n  padding: ", "px;\n  border-radius: ", ";\n  box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);\n  width: 710px;\n  opacity: 0.8;\n  cursor: grabbing;\n  padding-right: ", ";\n\n  & > ", " {\n    padding-bottom: 0;\n  }\n\n  & svg {\n    cursor: grabbing;\n  }\n"], ["\n  background: ", ";\n  display: block;\n  position: absolute;\n  padding: ", "px;\n  border-radius: ", ";\n  box-shadow: 0 0 15px rgba(0, 0, 0, 0.15);\n  width: 710px;\n  opacity: 0.8;\n  cursor: grabbing;\n  padding-right: ", ";\n\n  & > ", " {\n    padding-bottom: 0;\n  }\n\n  & svg {\n    cursor: grabbing;\n  }\n"])), function (p) { return p.theme.background; }, GHOST_PADDING, function (p) { return p.theme.borderRadius; }, space(2), RowContainer);
var DragPlaceholder = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin: 0 ", " ", " ", ";\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  height: 41px;\n"], ["\n  margin: 0 ", " ", " ", ";\n  border: 2px dashed ", ";\n  border-radius: ", ";\n  height: 41px;\n"])), space(3), space(1), space(3), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; });
var Actions = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-column: 2 / 3;\n"], ["\n  grid-column: 2 / 3;\n"])));
var Heading = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-column: 2 / 3;\n\n  /* Emulate the grid used in the column editor rows */\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-column-gap: ", ";\n"], ["\n  grid-column: 2 / 3;\n\n  /* Emulate the grid used in the column editor rows */\n  display: grid;\n  grid-template-columns: repeat(", ", 1fr);\n  grid-column-gap: ", ";\n"])), function (p) { return p.gridColumns; }, space(1));
var StyledSectionHeading = styled(SectionHeading)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
export default ColumnEditCollection;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=columnEditCollection.jsx.map
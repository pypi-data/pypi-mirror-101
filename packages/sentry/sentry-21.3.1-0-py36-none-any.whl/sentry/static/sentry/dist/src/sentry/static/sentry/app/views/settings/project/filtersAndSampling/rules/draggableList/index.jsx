import { __extends } from "tslib";
import React from 'react';
import { createPortal } from 'react-dom';
import { DndContext, DragOverlay } from '@dnd-kit/core';
import { arrayMove, SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import Item from './item';
import SortableItem from './sortableItem';
var DraggableList = /** @class */ (function (_super) {
    __extends(DraggableList, _super);
    function DraggableList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        _this.handleChangeActive = function (activeId) {
            _this.setState({ activeId: activeId });
        };
        return _this;
    }
    DraggableList.prototype.render = function () {
        var _this = this;
        var activeId = this.state.activeId;
        var _a = this.props, items = _a.items, onUpdateItems = _a.onUpdateItems, renderItem = _a.renderItem, disabled = _a.disabled, wrapperStyle = _a.wrapperStyle, innerWrapperStyle = _a.innerWrapperStyle;
        var getIndex = items.indexOf.bind(items);
        var activeIndex = activeId ? getIndex(activeId) : -1;
        return (<DndContext onDragStart={function (_a) {
                var active = _a.active;
                if (!active) {
                    return;
                }
                _this.handleChangeActive(active.id);
            }} onDragEnd={function (_a) {
                var over = _a.over;
                _this.handleChangeActive(undefined);
                if (over) {
                    var overIndex = getIndex(over.id);
                    if (activeIndex !== overIndex) {
                        onUpdateItems({
                            activeIndex: activeIndex,
                            overIndex: overIndex,
                            reorderedItems: arrayMove(items, activeIndex, overIndex),
                        });
                    }
                }
            }} onDragCancel={function () { return _this.handleChangeActive(undefined); }}>
        <SortableContext items={items} strategy={verticalListSortingStrategy}>
          {items.map(function (item, index) { return (<SortableItem key={item} id={item} index={index} renderItem={renderItem} disabled={disabled} wrapperStyle={wrapperStyle} innerWrapperStyle={innerWrapperStyle}/>); })}
        </SortableContext>
        {createPortal(<DragOverlay>
            {activeId ? (<Item value={items[activeIndex]} renderItem={renderItem} wrapperStyle={wrapperStyle({
                        id: items[activeIndex],
                        index: activeIndex,
                        isDragging: true,
                        isSorting: false,
                    })} innerWrapperStyle={innerWrapperStyle({
                        id: items[activeIndex],
                        index: activeIndex,
                        isSorting: activeId !== null,
                        isDragging: true,
                        overIndex: -1,
                        isDragOverlay: true,
                    })}/>) : null}
          </DragOverlay>, document.body)}
      </DndContext>);
    };
    DraggableList.defaultProps = {
        disabled: false,
        wrapperStyle: function () { return ({}); },
        innerWrapperStyle: function () { return ({}); },
    };
    return DraggableList;
}(React.Component));
export default DraggableList;
//# sourceMappingURL=index.jsx.map
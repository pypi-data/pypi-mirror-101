import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import Item from './item';
function SortableItem(_a) {
    var id = _a.id, index = _a.index, renderItem = _a.renderItem, disabled = _a.disabled, wrapperStyle = _a.wrapperStyle, innerWrapperStyle = _a.innerWrapperStyle;
    var _b = useSortable({ id: id, disabled: disabled }), attributes = _b.attributes, isSorting = _b.isSorting, isDragging = _b.isDragging, listeners = _b.listeners, setNodeRef = _b.setNodeRef, overIndex = _b.overIndex, transform = _b.transform, transition = _b.transition;
    return (<Item forwardRef={setNodeRef} value={id} sorting={isSorting} renderItem={renderItem} index={index} transform={transform} transition={transition} listeners={listeners} attributes={attributes} wrapperStyle={wrapperStyle({ id: id, index: index, isDragging: isDragging, isSorting: isSorting })} innerWrapperStyle={innerWrapperStyle({
            id: id,
            index: index,
            isDragging: isDragging,
            isSorting: isSorting,
            overIndex: overIndex,
            isDragOverlay: false,
        })}/>);
}
export default SortableItem;
//# sourceMappingURL=sortableItem.jsx.map
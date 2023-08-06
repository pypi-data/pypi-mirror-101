import { __assign, __extends, __values } from "tslib";
import React from 'react';
import getDisplayName from 'app/utils/getDisplayName';
import { setBodyUserSelect } from 'app/utils/userselect';
import { clamp, rectOfContent, toPercent } from './utils';
var ScrollbarManagerContext = React.createContext({
    generateContentSpanBarRef: function () { return function () { return undefined; }; },
    virtualScrollbarRef: React.createRef(),
    onDragStart: function () { },
    updateScrollState: function () { },
});
var selectRefs = function (refs, transform) {
    if (!(refs instanceof Set)) {
        if (refs.current) {
            transform(refs.current);
        }
        return;
    }
    refs.forEach(function (element) {
        if (document.body.contains(element)) {
            transform(element);
        }
    });
};
// simple linear interpolation between start and end such that needle is between [0, 1]
var lerp = function (start, end, needle) {
    return start + needle * (end - start);
};
var Provider = /** @class */ (function (_super) {
    __extends(Provider, _super);
    function Provider() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            maxContentWidth: undefined,
        };
        _this.contentSpanBar = new Set();
        _this.virtualScrollbar = React.createRef();
        _this.isDragging = false;
        _this.previousUserSelect = null;
        _this.initializeScrollState = function () {
            if (_this.contentSpanBar.size === 0 || !_this.hasInteractiveLayer()) {
                return;
            }
            // reset all span bar content containers to their natural widths
            selectRefs(_this.contentSpanBar, function (spanBarDOM) {
                spanBarDOM.style.removeProperty('width');
                spanBarDOM.style.removeProperty('max-width');
                spanBarDOM.style.removeProperty('overflow');
                spanBarDOM.style.removeProperty('transform');
            });
            // Find the maximum content width. We set each content spanbar to be this maximum width,
            // such that all content spanbar widths are uniform.
            var maxContentWidth = Array.from(_this.contentSpanBar).reduce(function (currentMaxWidth, currentSpanBar) {
                var isHidden = currentSpanBar.offsetParent === null;
                if (!document.body.contains(currentSpanBar) || isHidden) {
                    return currentMaxWidth;
                }
                var maybeMaxWidth = currentSpanBar.scrollWidth;
                if (maybeMaxWidth > currentMaxWidth) {
                    return maybeMaxWidth;
                }
                return currentMaxWidth;
            }, 0);
            selectRefs(_this.contentSpanBar, function (spanBarDOM) {
                spanBarDOM.style.width = maxContentWidth + "px";
                spanBarDOM.style.maxWidth = maxContentWidth + "px";
                spanBarDOM.style.overflow = 'hidden';
            });
            var spanBarDOM = _this.getReferenceSpanBar();
            if (spanBarDOM) {
                _this.syncVirtualScrollbar(spanBarDOM);
            }
        };
        _this.syncVirtualScrollbar = function (spanBar) {
            // sync the virtual scrollbar's width scrolledSpanBar's width
            if (!_this.virtualScrollbar.current || !_this.hasInteractiveLayer()) {
                return;
            }
            var virtualScrollbarDOM = _this.virtualScrollbar.current;
            var maxContentWidth = spanBar.getBoundingClientRect().width;
            var interactiveLayerRect = rectOfContent(_this.props.interactiveLayerRef.current);
            if (maxContentWidth === undefined || maxContentWidth <= 0) {
                virtualScrollbarDOM.style.width = '0';
                return;
            }
            var visibleWidth = interactiveLayerRect.width;
            // This is the width of the content not visible.
            var maxScrollDistance = maxContentWidth - visibleWidth;
            var virtualScrollbarWidth = visibleWidth / (visibleWidth + maxScrollDistance);
            if (virtualScrollbarWidth >= 1) {
                virtualScrollbarDOM.style.width = '0';
                return;
            }
            virtualScrollbarDOM.style.width = "max(50px, " + toPercent(virtualScrollbarWidth) + ")";
            virtualScrollbarDOM.style.removeProperty('transform');
        };
        _this.generateContentSpanBarRef = function () {
            var previousInstance = null;
            var addContentSpanBarRef = function (instance) {
                if (previousInstance) {
                    _this.contentSpanBar.delete(previousInstance);
                    previousInstance = null;
                }
                if (instance) {
                    _this.contentSpanBar.add(instance);
                    previousInstance = instance;
                }
            };
            return addContentSpanBarRef;
        };
        _this.hasInteractiveLayer = function () { return !!_this.props.interactiveLayerRef.current; };
        _this.initialMouseClickX = undefined;
        _this.onDragStart = function (event) {
            if (_this.isDragging ||
                event.type !== 'mousedown' ||
                !_this.hasInteractiveLayer() ||
                !_this.virtualScrollbar.current) {
                return;
            }
            event.stopPropagation();
            var virtualScrollbarRect = rectOfContent(_this.virtualScrollbar.current);
            // get intitial x-coordinate of the mouse click on the virtual scrollbar
            _this.initialMouseClickX = Math.abs(event.clientX - virtualScrollbarRect.x);
            // prevent the user from selecting things outside the minimap when dragging
            // the mouse cursor inside the minimap
            _this.previousUserSelect = setBodyUserSelect({
                userSelect: 'none',
                MozUserSelect: 'none',
                msUserSelect: 'none',
                webkitUserSelect: 'none',
            });
            // attach event listeners so that the mouse cursor does not select text during a drag
            window.addEventListener('mousemove', _this.onDragMove);
            window.addEventListener('mouseup', _this.onDragEnd);
            // indicate drag has begun
            _this.isDragging = true;
            selectRefs(_this.virtualScrollbar, function (scrollbarDOM) {
                scrollbarDOM.classList.add('dragging');
                document.body.style.setProperty('cursor', 'grabbing', 'important');
            });
        };
        _this.onDragMove = function (event) {
            if (!_this.isDragging ||
                event.type !== 'mousemove' ||
                !_this.hasInteractiveLayer() ||
                !_this.virtualScrollbar.current ||
                _this.initialMouseClickX === undefined) {
                return;
            }
            var virtualScrollbarDOM = _this.virtualScrollbar.current;
            var interactiveLayerRect = rectOfContent(_this.props.interactiveLayerRef.current);
            var virtualScrollBarRect = rectOfContent(virtualScrollbarDOM);
            // Mouse x-coordinate relative to the interactive layer's left side
            var localDragX = event.pageX - interactiveLayerRect.x;
            // The drag movement with respect to the interactive layer's width.
            var rawMouseX = (localDragX - _this.initialMouseClickX) / interactiveLayerRect.width;
            var maxVirtualScrollableArea = 1 - virtualScrollBarRect.width / interactiveLayerRect.width;
            // clamp rawMouseX to be within [0, 1]
            var virtualScrollbarPosition = clamp(rawMouseX, 0, 1);
            var virtualLeft = clamp(virtualScrollbarPosition, 0, maxVirtualScrollableArea) *
                interactiveLayerRect.width;
            virtualScrollbarDOM.style.transform = "translate3d(" + virtualLeft + "px, 0, 0)";
            virtualScrollbarDOM.style.transformOrigin = 'left';
            var virtualScrollPercentage = clamp(rawMouseX / maxVirtualScrollableArea, 0, 1);
            // Update scroll positions of all the span bars
            selectRefs(_this.contentSpanBar, function (spanBarDOM) {
                var maxScrollDistance = spanBarDOM.getBoundingClientRect().width - interactiveLayerRect.width;
                var left = -lerp(0, maxScrollDistance, virtualScrollPercentage);
                spanBarDOM.style.transform = "translate3d(" + left + "px, 0, 0)";
                spanBarDOM.style.transformOrigin = 'left';
            });
        };
        _this.onDragEnd = function (event) {
            if (!_this.isDragging || event.type !== 'mouseup' || !_this.hasInteractiveLayer()) {
                return;
            }
            // remove listeners that were attached in onDragStart
            _this.cleanUpListeners();
            // restore body styles
            if (_this.previousUserSelect) {
                setBodyUserSelect(_this.previousUserSelect);
                _this.previousUserSelect = null;
            }
            // indicate drag has ended
            _this.isDragging = false;
            selectRefs(_this.virtualScrollbar, function (scrollbarDOM) {
                scrollbarDOM.classList.remove('dragging');
                document.body.style.removeProperty('cursor');
            });
        };
        _this.cleanUpListeners = function () {
            if (_this.isDragging) {
                // we only remove listeners during a drag
                window.removeEventListener('mousemove', _this.onDragMove);
                window.removeEventListener('mouseup', _this.onDragEnd);
            }
        };
        return _this;
    }
    Provider.prototype.componentDidMount = function () {
        // React will guarantee that refs are set before componentDidMount() is called;
        // but only for DOM elements that actually got rendered
        this.initializeScrollState();
    };
    Provider.prototype.componentDidUpdate = function (prevProps) {
        // Re-initialize the scroll state whenever:
        // - the window was selected via the minimap or,
        // - the divider was re-positioned.
        var dividerPositionChanged = this.props.dividerPosition !== prevProps.dividerPosition;
        var viewWindowChanged = prevProps.dragProps &&
            this.props.dragProps &&
            (prevProps.dragProps.viewWindowStart !== this.props.dragProps.viewWindowStart ||
                prevProps.dragProps.viewWindowEnd !== this.props.dragProps.viewWindowEnd);
        if (dividerPositionChanged || viewWindowChanged) {
            this.initializeScrollState();
        }
    };
    Provider.prototype.componentWillUnmount = function () {
        this.cleanUpListeners();
    };
    Provider.prototype.getReferenceSpanBar = function () {
        var e_1, _a;
        try {
            for (var _b = __values(this.contentSpanBar), _c = _b.next(); !_c.done; _c = _b.next()) {
                var currentSpanBar = _c.value;
                var isHidden = currentSpanBar.offsetParent === null;
                if (!document.body.contains(currentSpanBar) || isHidden) {
                    continue;
                }
                return currentSpanBar;
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return undefined;
    };
    Provider.prototype.render = function () {
        var childrenProps = {
            generateContentSpanBarRef: this.generateContentSpanBarRef,
            onDragStart: this.onDragStart,
            virtualScrollbarRef: this.virtualScrollbar,
            updateScrollState: this.initializeScrollState,
        };
        return (<ScrollbarManagerContext.Provider value={childrenProps}>
        {this.props.children}
      </ScrollbarManagerContext.Provider>);
    };
    return Provider;
}(React.Component));
export { Provider };
export var Consumer = ScrollbarManagerContext.Consumer;
export var withScrollbarManager = function (WrappedComponent) { var _a; return _a = /** @class */ (function (_super) {
        __extends(class_1, _super);
        function class_1() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        class_1.prototype.render = function () {
            var _this = this;
            return (<ScrollbarManagerContext.Consumer>
          {function (context) {
                    var props = __assign(__assign({}, _this.props), context);
                    return <WrappedComponent {...props}/>;
                }}
        </ScrollbarManagerContext.Consumer>);
        };
        return class_1;
    }(React.Component)),
    _a.displayName = "withScrollbarManager(" + getDisplayName(WrappedComponent) + ")",
    _a; };
//# sourceMappingURL=scrollbarManager.jsx.map
import { __assign, __awaiter, __extends, __generator, __read, __rest, __spreadArray } from "tslib";
/**
 * Inspired by [Downshift](https://github.com/paypal/downshift)
 *
 * Implemented with a stripped-down, compatible API for our use case.
 * May be worthwhile to switch if we find we need more features
 *
 * Basic idea is that we call `children` with props necessary to render with any sort of component structure.
 * This component handles logic like when the dropdown menu should be displayed, as well as handling keyboard input, how
 * it is rendered should be left to the child.
 */
import React from 'react';
import DropdownMenu from 'app/components/dropdownMenu';
var defaultProps = {
    itemToString: function () { return ''; },
    /**
     * If input should be considered an "actor". If there is another parent actor, then this should be `false`.
     * e.g. You have a button that opens this <AutoComplete> in a dropdown.
     */
    inputIsActor: true,
    disabled: false,
    closeOnSelect: true,
    /**
     * Can select autocomplete item with "Enter" key
     */
    shouldSelectWithEnter: true,
    /**
     * Can select autocomplete item with "Tab" key
     */
    shouldSelectWithTab: false,
};
var AutoComplete = /** @class */ (function (_super) {
    __extends(AutoComplete, _super);
    function AutoComplete() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.items = new Map();
        _this.isControlled = function () { return typeof _this.props.isOpen !== 'undefined'; };
        _this.getOpenState = function () {
            var isOpen = _this.props.isOpen;
            return _this.isControlled() ? isOpen : _this.state.isOpen;
        };
        /**
         * Resets `this.items` and `this.state.highlightedIndex`.
         * Should be called whenever `inputValue` changes.
         */
        _this.resetHighlightState = function () {
            // reset items and expect `getInputProps` in child to give us a list of new items
            _this.setState({
                highlightedIndex: _this.props.defaultHighlightedIndex || 0,
            });
        };
        _this.handleInputChange = function (_a) {
            var onChange = _a.onChange;
            return function (e) {
                var value = e.target.value;
                // We force `isOpen: true` here because:
                // 1) it's possible to have menu closed but input with focus (i.e. hitting "Esc")
                // 2) you select an item, input still has focus, and then change input
                _this.openMenu();
                _this.setState({
                    inputValue: value,
                });
                onChange === null || onChange === void 0 ? void 0 : onChange(e);
            };
        };
        _this.handleInputFocus = function (_a) {
            var onFocus = _a.onFocus;
            return function (e) {
                _this.openMenu();
                onFocus === null || onFocus === void 0 ? void 0 : onFocus(e);
            };
        };
        /**
         *
         * We need this delay because we want to close the menu when input
         * is blurred (i.e. clicking or via keyboard). However we have to handle the
         * case when we want to click on the dropdown and causes focus.
         *
         * Clicks outside should close the dropdown immediately via <DropdownMenu />,
         * however blur via keyboard will have a 200ms delay
         */
        _this.handleInputBlur = function (_a) {
            var onBlur = _a.onBlur;
            return function (e) {
                _this.blurTimer = setTimeout(function () {
                    _this.closeMenu();
                    onBlur === null || onBlur === void 0 ? void 0 : onBlur(e);
                }, 200);
            };
        };
        // Dropdown detected click outside, we should close
        _this.handleClickOutside = function () { return __awaiter(_this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        // Otherwise, it's possible that this gets fired multiple times
                        // e.g. click outside triggers closeMenu and at the same time input gets blurred, so
                        // a timer is set to close the menu
                        if (this.blurTimer) {
                            clearTimeout(this.blurTimer);
                        }
                        // Wait until the current macrotask completes, in the case that the click
                        // happened on a hovercard or some other element rendered outside of the
                        // autocomplete, but controlled by the existence of the autocomplete, we
                        // need to ensure any click handlers are run.
                        return [4 /*yield*/, new Promise(function (resolve) { return setTimeout(resolve); })];
                    case 1:
                        // Wait until the current macrotask completes, in the case that the click
                        // happened on a hovercard or some other element rendered outside of the
                        // autocomplete, but controlled by the existence of the autocomplete, we
                        // need to ensure any click handlers are run.
                        _a.sent();
                        this.closeMenu();
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleInputKeyDown = function (_a) {
            var onKeyDown = _a.onKeyDown;
            return function (e) {
                var hasHighlightedItem = _this.items.size && _this.items.has(_this.state.highlightedIndex);
                var canSelectWithEnter = _this.props.shouldSelectWithEnter && e.key === 'Enter';
                var canSelectWithTab = _this.props.shouldSelectWithTab && e.key === 'Tab';
                if (hasHighlightedItem && (canSelectWithEnter || canSelectWithTab)) {
                    _this.handleSelect(_this.items.get(_this.state.highlightedIndex), e);
                    e.preventDefault();
                }
                if (e.key === 'ArrowUp') {
                    _this.moveHighlightedIndex(-1);
                    e.preventDefault();
                }
                if (e.key === 'ArrowDown') {
                    _this.moveHighlightedIndex(1);
                    e.preventDefault();
                }
                if (e.key === 'Escape') {
                    _this.closeMenu();
                }
                onKeyDown === null || onKeyDown === void 0 ? void 0 : onKeyDown(e);
            };
        };
        _this.handleItemClick = function (_a) {
            var onClick = _a.onClick, item = _a.item, index = _a.index;
            return function (e) {
                if (_this.blurTimer) {
                    clearTimeout(_this.blurTimer);
                }
                _this.setState({ highlightedIndex: index });
                _this.handleSelect(item, e);
                onClick === null || onClick === void 0 ? void 0 : onClick(item)(e);
            };
        };
        _this.handleMenuMouseDown = function () {
            // Cancel close menu from input blur (mouseDown event can occur before input blur :()
            setTimeout(function () {
                if (_this.blurTimer) {
                    clearTimeout(_this.blurTimer);
                }
            });
        };
        /**
         * When an item is selected via clicking or using the keyboard (e.g. pressing "Enter")
         */
        _this.handleSelect = function (item, e) {
            var _a = _this.props, onSelect = _a.onSelect, itemToString = _a.itemToString, closeOnSelect = _a.closeOnSelect;
            onSelect === null || onSelect === void 0 ? void 0 : onSelect(item, _this.state, e);
            if (closeOnSelect) {
                _this.closeMenu();
                _this.setState({
                    inputValue: itemToString(item),
                    selectedItem: item,
                });
                return;
            }
            _this.setState({ selectedItem: item });
        };
        /**
         * Open dropdown menu
         *
         * This is exposed to render function
         */
        _this.openMenu = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = _this.props, onOpen = _a.onOpen, disabled = _a.disabled;
            onOpen === null || onOpen === void 0 ? void 0 : onOpen.apply(void 0, __spreadArray([], __read(args)));
            if (disabled || _this.isControlled()) {
                return;
            }
            _this.resetHighlightState();
            _this.setState({
                isOpen: true,
            });
        };
        /**
         * Close dropdown menu
         *
         * This is exposed to render function
         */
        _this.closeMenu = function () {
            var args = [];
            for (var _i = 0; _i < arguments.length; _i++) {
                args[_i] = arguments[_i];
            }
            var _a = _this.props, onClose = _a.onClose, resetInputOnClose = _a.resetInputOnClose;
            onClose === null || onClose === void 0 ? void 0 : onClose.apply(void 0, __spreadArray([], __read(args)));
            if (_this.isControlled()) {
                return;
            }
            _this.setState(function (state) { return ({
                isOpen: false,
                inputValue: resetInputOnClose ? '' : state.inputValue,
            }); });
        };
        _this.getInputProps = function (inputProps) {
            var _a = inputProps !== null && inputProps !== void 0 ? inputProps : {}, onChange = _a.onChange, onKeyDown = _a.onKeyDown, onFocus = _a.onFocus, onBlur = _a.onBlur, rest = __rest(_a, ["onChange", "onKeyDown", "onFocus", "onBlur"]);
            return __assign(__assign({}, rest), { value: _this.state.inputValue, onChange: _this.handleInputChange({ onChange: onChange }), onKeyDown: _this.handleInputKeyDown({ onKeyDown: onKeyDown }), onFocus: _this.handleInputFocus({ onFocus: onFocus }), onBlur: _this.handleInputBlur({ onBlur: onBlur }) });
        };
        _this.getItemProps = function (itemProps) {
            var _a = itemProps !== null && itemProps !== void 0 ? itemProps : {}, item = _a.item, index = _a.index, props = __rest(_a, ["item", "index"]);
            if (!item) {
                // eslint-disable-next-line no-console
                console.warn('getItemProps requires an object with an `item` key');
            }
            var newIndex = index !== null && index !== void 0 ? index : _this.items.size;
            _this.items.set(newIndex, item);
            return __assign(__assign({}, props), { onClick: _this.handleItemClick(__assign({ item: item, index: newIndex }, props)) });
        };
        _this.getMenuProps = function (props) {
            _this.itemCount = props === null || props === void 0 ? void 0 : props.itemCount;
            return __assign(__assign({}, (props !== null && props !== void 0 ? props : {})), { onMouseDown: _this.handleMenuMouseDown });
        };
        return _this;
    }
    AutoComplete.prototype.getInitialState = function () {
        var _a = this.props, defaultHighlightedIndex = _a.defaultHighlightedIndex, isOpen = _a.isOpen, defaultInputValue = _a.defaultInputValue;
        return {
            isOpen: !!isOpen,
            highlightedIndex: defaultHighlightedIndex || 0,
            inputValue: defaultInputValue || '',
            selectedItem: undefined,
        };
    };
    AutoComplete.prototype.UNSAFE_componentWillReceiveProps = function (nextProps, nextState) {
        // If we do NOT want to close on select, then we should not reset highlight state
        // when we select an item (when we select an item, `this.state.selectedItem` changes)
        if (!nextProps.closeOnSelect && this.state.selectedItem !== nextState.selectedItem) {
            return;
        }
        this.resetHighlightState();
    };
    AutoComplete.prototype.UNSAFE_componentWillUpdate = function () {
        this.items.clear();
    };
    AutoComplete.prototype.moveHighlightedIndex = function (step) {
        var newIndex = this.state.highlightedIndex + step;
        // when this component is in virtualized mode, only a subset of items will be passed
        // down, making the array length inaccurate. instead we manually pass the length as itemCount
        var listSize = this.itemCount || this.items.size;
        // Make sure new index is within bounds
        newIndex = Math.max(0, Math.min(newIndex, listSize - 1));
        this.setState({ highlightedIndex: newIndex });
    };
    AutoComplete.prototype.render = function () {
        var _this = this;
        var _a = this.props, children = _a.children, onMenuOpen = _a.onMenuOpen, inputIsActor = _a.inputIsActor;
        var _b = this.state, selectedItem = _b.selectedItem, inputValue = _b.inputValue, highlightedIndex = _b.highlightedIndex;
        var isOpen = this.getOpenState();
        return (<DropdownMenu isOpen={isOpen} onClickOutside={this.handleClickOutside} onOpen={onMenuOpen}>
        {function (dropdownMenuProps) {
                return children(__assign(__assign({}, dropdownMenuProps), { getMenuProps: function (props) {
                        return dropdownMenuProps.getMenuProps(_this.getMenuProps(props));
                    }, getInputProps: function (props) {
                        var inputProps = _this.getInputProps(props);
                        if (!inputIsActor) {
                            return inputProps;
                        }
                        return dropdownMenuProps.getActorProps(inputProps);
                    }, getItemProps: _this.getItemProps, inputValue: inputValue,
                    selectedItem: selectedItem,
                    highlightedIndex: highlightedIndex, actions: {
                        open: _this.openMenu,
                        close: _this.closeMenu,
                    } }));
            }}
      </DropdownMenu>);
    };
    AutoComplete.defaultProps = defaultProps;
    return AutoComplete;
}(React.Component));
export default AutoComplete;
//# sourceMappingURL=autoComplete.jsx.map
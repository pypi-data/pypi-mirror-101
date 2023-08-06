import { __assign, __extends, __read, __spreadArray } from "tslib";
import React from 'react';
import intersection from 'lodash/intersection';
import isEqual from 'lodash/isEqual';
import uniq from 'lodash/uniq';
import xor from 'lodash/xor';
import BulkNotice from './bulkNotice';
var BulkController = /** @class */ (function (_super) {
    __extends(BulkController, _super);
    function BulkController() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.handleRowToggle = function (id) {
            _this.setState(function (state) { return ({
                selectedIds: xor(state.selectedIds, [id]),
                isAllSelected: false,
            }); });
        };
        _this.handleAllRowsToggle = function (select) {
            var pageIds = _this.props.pageIds;
            _this.setState({
                selectedIds: select ? __spreadArray([], __read(pageIds)) : [],
                isAllSelected: select,
            });
        };
        _this.handlePageRowsToggle = function (select) {
            var pageIds = _this.props.pageIds;
            _this.setState(function (state) { return ({
                selectedIds: select
                    ? uniq(__spreadArray(__spreadArray([], __read(state.selectedIds)), __read(pageIds)))
                    : state.selectedIds.filter(function (id) { return !pageIds.includes(id); }),
                isAllSelected: false,
            }); });
        };
        return _this;
    }
    BulkController.prototype.getInitialState = function () {
        var _a = this.props, defaultSelectedIds = _a.defaultSelectedIds, pageIds = _a.pageIds;
        return {
            selectedIds: intersection(defaultSelectedIds !== null && defaultSelectedIds !== void 0 ? defaultSelectedIds : [], pageIds),
            isAllSelected: false,
        };
    };
    BulkController.getDerivedStateFromProps = function (props, state) {
        return __assign(__assign({}, state), { selectedIds: intersection(state.selectedIds, props.pageIds) });
    };
    BulkController.prototype.componentDidUpdate = function (_prevProps, prevState) {
        var _a, _b;
        if (!isEqual(prevState, this.state)) {
            (_b = (_a = this.props).onChange) === null || _b === void 0 ? void 0 : _b.call(_a, this.state);
        }
    };
    BulkController.prototype.render = function () {
        var _this = this;
        var _a = this.props, pageIds = _a.pageIds, children = _a.children, columnsCount = _a.columnsCount, allRowsCount = _a.allRowsCount, bulkLimit = _a.bulkLimit;
        var _b = this.state, selectedIds = _b.selectedIds, isAllSelected = _b.isAllSelected;
        var isPageSelected = pageIds.length > 0 && pageIds.every(function (id) { return selectedIds.includes(id); });
        var renderProps = {
            selectedIds: selectedIds,
            isAllSelected: isAllSelected,
            isPageSelected: isPageSelected,
            onRowToggle: this.handleRowToggle,
            onAllRowsToggle: this.handleAllRowsToggle,
            onPageRowsToggle: this.handlePageRowsToggle,
            renderBulkNotice: function () { return (<BulkNotice allRowsCount={allRowsCount} selectedRowsCount={selectedIds.length} onUnselectAllRows={function () { return _this.handleAllRowsToggle(false); }} onSelectAllRows={function () { return _this.handleAllRowsToggle(true); }} columnsCount={columnsCount} isPageSelected={isPageSelected} isAllSelected={isAllSelected} bulkLimit={bulkLimit}/>); },
        };
        return children(renderProps);
    };
    return BulkController;
}(React.Component));
export default BulkController;
//# sourceMappingURL=index.jsx.map
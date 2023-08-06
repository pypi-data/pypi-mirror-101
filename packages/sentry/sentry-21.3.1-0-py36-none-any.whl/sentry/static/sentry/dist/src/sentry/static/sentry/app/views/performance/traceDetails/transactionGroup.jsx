import { __extends } from "tslib";
import React from 'react';
import TransactionBar from './transactionBar';
var TransactionGroup = /** @class */ (function (_super) {
    __extends(TransactionGroup, _super);
    function TransactionGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isExpanded: true,
        };
        _this.toggleExpandedState = function () {
            _this.setState(function (_a) {
                var isExpanded = _a.isExpanded;
                return ({ isExpanded: !isExpanded });
            });
        };
        return _this;
    }
    TransactionGroup.prototype.render = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, transaction = _a.transaction, traceInfo = _a.traceInfo, continuingDepths = _a.continuingDepths, isOrphan = _a.isOrphan, isLast = _a.isLast, index = _a.index, isVisible = _a.isVisible, renderedChildren = _a.renderedChildren;
        var isExpanded = this.state.isExpanded;
        return (<React.Fragment>
        <TransactionBar location={location} organization={organization} index={index} transaction={transaction} traceInfo={traceInfo} continuingDepths={continuingDepths} isOrphan={isOrphan} isLast={isLast} isExpanded={isExpanded} toggleExpandedState={this.toggleExpandedState} isVisible={isVisible}/>
        {isExpanded && renderedChildren}
      </React.Fragment>);
    };
    return TransactionGroup;
}(React.Component));
export default TransactionGroup;
//# sourceMappingURL=transactionGroup.jsx.map
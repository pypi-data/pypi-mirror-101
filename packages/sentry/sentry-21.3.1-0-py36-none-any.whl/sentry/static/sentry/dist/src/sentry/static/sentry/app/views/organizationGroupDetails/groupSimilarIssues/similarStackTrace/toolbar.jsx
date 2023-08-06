import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { PanelHeader } from 'app/components/panels';
import ToolbarHeader from 'app/components/toolbarHeader';
import { t } from 'app/locale';
import GroupingStore from 'app/stores/groupingStore';
import space from 'app/styles/space';
import { callIfFunction } from 'app/utils/callIfFunction';
var inititalState = {
    mergeCount: 0,
};
var SimilarToolbar = /** @class */ (function (_super) {
    __extends(SimilarToolbar, _super);
    function SimilarToolbar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = inititalState;
        _this.onGroupChange = function (_a) {
            var mergeList = _a.mergeList;
            if (!(mergeList === null || mergeList === void 0 ? void 0 : mergeList.length)) {
                return;
            }
            if (mergeList.length !== _this.state.mergeCount) {
                _this.setState({ mergeCount: mergeList.length });
            }
        };
        _this.listener = GroupingStore.listen(_this.onGroupChange, undefined);
        return _this;
    }
    SimilarToolbar.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    SimilarToolbar.prototype.render = function () {
        var _a = this.props, onMerge = _a.onMerge, v2 = _a.v2;
        var mergeCount = this.state.mergeCount;
        return (<PanelHeader hasButtons>
        <Confirm data-test-id="merge" disabled={mergeCount === 0} message={t('Are you sure you want to merge these issues?')} onConfirm={onMerge}>
          <Button size="small" title={t('Merging %s issues', mergeCount)}>
            {t('Merge %s', "(" + (mergeCount || 0) + ")")}
          </Button>
        </Confirm>

        <Columns>
          <StyledToolbarHeader>{t('Events')}</StyledToolbarHeader>

          {v2 ? (<StyledToolbarHeader>{t('Score')}</StyledToolbarHeader>) : (<React.Fragment>
              <StyledToolbarHeader>{t('Exception')}</StyledToolbarHeader>
              <StyledToolbarHeader>{t('Message')}</StyledToolbarHeader>
            </React.Fragment>)}
        </Columns>
      </PanelHeader>);
    };
    return SimilarToolbar;
}(React.Component));
export default SimilarToolbar;
var Columns = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n  min-width: 300px;\n  width: 300px;\n"], ["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n  min-width: 300px;\n  width: 300px;\n"])));
var StyledToolbarHeader = styled(ToolbarHeader)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n  flex-shrink: 0;\n  display: flex;\n  justify-content: center;\n  padding: ", " 0;\n"], ["\n  flex: 1;\n  flex-shrink: 0;\n  display: flex;\n  justify-content: center;\n  padding: ", " 0;\n"])), space(0.5));
var templateObject_1, templateObject_2;
//# sourceMappingURL=toolbar.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import BulkController from 'app/components/bulkController';
import { PanelTable } from 'app/components/panels';
import Switch from 'app/components/switchButton';
import { LegacyBrowser } from 'app/types/dynamicSampling';
import Browser from './browser';
var legacyBrowsers = Object.values(LegacyBrowser);
function LegacyBrowsersField(_a) {
    var onChange = _a.onChange, _b = _a.selectedLegacyBrowsers, selectedLegacyBrowsers = _b === void 0 ? [] : _b;
    function handleChange(_a) {
        var selectedIds = _a.selectedIds;
        onChange(selectedIds);
    }
    return (<BulkController pageIds={legacyBrowsers} defaultSelectedIds={selectedLegacyBrowsers} allRowsCount={legacyBrowsers.length} onChange={handleChange} columnsCount={0}>
      {function (_a) {
            var selectedIds = _a.selectedIds, onRowToggle = _a.onRowToggle, onPageRowsToggle = _a.onPageRowsToggle, isPageSelected = _a.isPageSelected;
            return (<StyledPanelTable headers={[
                    '',
                    <Switch key="switch" size="lg" isActive={isPageSelected} toggle={function () {
                            onPageRowsToggle(!isPageSelected);
                        }}/>,
                ]}>
          {legacyBrowsers.map(function (legacyBrowser) { return (<Browser key={legacyBrowser} browser={legacyBrowser} isEnabled={selectedIds.includes(legacyBrowser)} onToggle={function () {
                        onRowToggle(legacyBrowser);
                    }}/>); })}
        </StyledPanelTable>);
        }}
    </BulkController>);
}
export default LegacyBrowsersField;
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: 1fr max-content;\n  grid-column: 1 / -2;\n"], ["\n  grid-template-columns: 1fr max-content;\n  grid-column: 1 / -2;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map
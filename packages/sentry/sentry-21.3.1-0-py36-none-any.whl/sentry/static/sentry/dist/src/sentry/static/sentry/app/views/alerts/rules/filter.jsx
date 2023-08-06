import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl from 'app/components/dropdownControl';
import { IconFilter } from 'app/icons';
import { t, tn } from 'app/locale';
import space from 'app/styles/space';
var Filter = /** @class */ (function (_super) {
    __extends(Filter, _super);
    function Filter() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.toggleFilter = function (filter) {
            var _a = _this.props, onFilterChange = _a.onFilterChange, selection = _a.selection;
            var newSelection = new Set(selection);
            if (newSelection.has(filter)) {
                newSelection.delete(filter);
            }
            else {
                newSelection.add(filter);
            }
            onFilterChange(newSelection);
        };
        _this.toggleAllFilters = function () {
            var _a = _this.props, filterList = _a.filterList, onFilterChange = _a.onFilterChange, selection = _a.selection;
            var newSelection = selection.size === filterList.length ? new Set() : new Set(filterList);
            onFilterChange(newSelection);
        };
        _this.getNumberOfActiveFilters = function () {
            var selection = _this.props.selection;
            return selection.size;
        };
        return _this;
    }
    Filter.prototype.render = function () {
        var _this = this;
        var _a = this.props, children = _a.children, header = _a.header, filterList = _a.filterList;
        var checkedQuantity = this.getNumberOfActiveFilters();
        var dropDownButtonProps = {
            children: (<React.Fragment>
          <IconFilter size="xs"/>
          <FilterLabel>{t('Filter')}</FilterLabel>
        </React.Fragment>),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        if (checkedQuantity > 0) {
            dropDownButtonProps.children = (<span>{tn('%s Active Filter', '%s Active Filters', checkedQuantity)}</span>);
            dropDownButtonProps.priority = 'primary';
            dropDownButtonProps.hasDarkBorderBottomColor = true;
        }
        return (<DropdownControl menuWidth="240px" blendWithActor button={function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
            {dropDownButtonProps.children}
          </StyledDropdownButton>);
            }}>
        <MenuContent>
          <Header>
            <span>{header}</span>
            <CheckboxFancy isChecked={checkedQuantity > 0} isIndeterminate={checkedQuantity > 0 && checkedQuantity !== filterList.length} onClick={function (event) {
                event.stopPropagation();
                _this.toggleAllFilters();
            }}/>
          </Header>
          {children({ toggleFilter: this.toggleFilter })}
        </MenuContent>
      </DropdownControl>);
    };
    return Filter;
}(React.Component));
var MenuContent = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  max-height: 250px;\n  overflow-y: auto;\n"], ["\n  max-height: 250px;\n  overflow-y: auto;\n"])));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), space(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(2), function (p) { return p.theme.border; });
var FilterLabel = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var StyledDropdownButton = styled(DropdownButton)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n\n  &:hover,\n  &:active {\n    ", "\n  }\n\n  ", "\n"], ["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n\n  &:hover,\n  &:active {\n    ",
    "\n  }\n\n  ",
    "\n"])), function (p) { return p.theme.zIndex.dropdown; }, function (p) {
    return !p.isOpen &&
        p.hasDarkBorderBottomColor &&
        "\n          border-bottom-color: " + p.theme.button.primary.border + ";\n        ";
}, function (p) {
    return !p.isOpen &&
        p.hasDarkBorderBottomColor &&
        "\n      border-bottom-color: " + p.theme.button.primary.border + ";\n    ";
});
export default Filter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=filter.jsx.map
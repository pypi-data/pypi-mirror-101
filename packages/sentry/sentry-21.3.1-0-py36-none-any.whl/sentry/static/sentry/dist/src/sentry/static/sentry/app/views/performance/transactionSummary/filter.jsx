import { __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl from 'app/components/dropdownControl';
import { pickSpanBarColour } from 'app/components/events/interfaces/spans/utils';
import Radio from 'app/components/radio';
import { IconFilter } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
export var SpanOperationBreakdownFilter;
(function (SpanOperationBreakdownFilter) {
    SpanOperationBreakdownFilter["None"] = "none";
    SpanOperationBreakdownFilter["Http"] = "http";
    SpanOperationBreakdownFilter["Db"] = "db";
    SpanOperationBreakdownFilter["Browser"] = "browser";
    SpanOperationBreakdownFilter["Resource"] = "resource";
})(SpanOperationBreakdownFilter || (SpanOperationBreakdownFilter = {}));
var OPTIONS = [
    SpanOperationBreakdownFilter.Http,
    SpanOperationBreakdownFilter.Db,
    SpanOperationBreakdownFilter.Browser,
    SpanOperationBreakdownFilter.Resource,
];
var Filter = /** @class */ (function (_super) {
    __extends(Filter, _super);
    function Filter() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Filter.prototype.render = function () {
        var _a = this.props, currentFilter = _a.currentFilter, onChangeFilter = _a.onChangeFilter, organization = _a.organization;
        if (!organization.features.includes('performance-ops-breakdown')) {
            return null;
        }
        var dropDownButtonProps = {
            children: (<React.Fragment>
          <IconFilter size="xs"/>
          <FilterLabel>
            {currentFilter === SpanOperationBreakdownFilter.None
                    ? t('Filter')
                    : tct('Filter - [operationName]', {
                        operationName: currentFilter,
                    })}
          </FilterLabel>
        </React.Fragment>),
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        return (<Wrapper>
        <DropdownControl menuWidth="240px" blendWithActor button={function (_a) {
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} showChevron={false} isOpen={isOpen} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
              {dropDownButtonProps.children}
            </StyledDropdownButton>);
            }}>
          <MenuContent onClick={function (event) {
                // propagated clicks will dismiss the menu; we stop this here
                event.stopPropagation();
            }}>
            <Header onClick={function (event) {
                event.stopPropagation();
                onChangeFilter(SpanOperationBreakdownFilter.None);
            }}>
              <HeaderTitle>{t('Operation')}</HeaderTitle>
              <Radio radioSize="small" checked={SpanOperationBreakdownFilter.None === currentFilter}/>
            </Header>
            <List>
              {Array.from(__spreadArray([], __read(OPTIONS)), function (filterOption, index) {
                var operationName = filterOption;
                return (<ListItem key={String(index)} isChecked={false} onClick={function (event) {
                        event.stopPropagation();
                        onChangeFilter(filterOption);
                    }}>
                    <OperationDot backgroundColor={pickSpanBarColour(operationName)}/>
                    <OperationName>{operationName}</OperationName>
                    <Radio radioSize="small" checked={filterOption === currentFilter}/>
                  </ListItem>);
            })}
            </List>
          </MenuContent>
        </DropdownControl>
      </Wrapper>);
    };
    return Filter;
}(React.Component));
var FilterLabel = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var Wrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n\n  margin-right: ", ";\n"], ["\n  position: relative;\n  display: flex;\n\n  margin-right: ", ";\n"])), space(1));
var StyledDropdownButton = styled(DropdownButton)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n\n  &:hover,\n  &:active {\n    ", "\n  }\n\n  ", "\n"], ["\n  white-space: nowrap;\n  max-width: 200px;\n\n  z-index: ", ";\n\n  &:hover,\n  &:active {\n    ",
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
var MenuContent = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  max-height: 250px;\n  overflow-y: auto;\n  border-top: 1px solid ", ";\n"], ["\n  max-height: 250px;\n  overflow-y: auto;\n  border-top: 1px solid ", ";\n"])), function (p) { return p.theme.gray200; });
var Header = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto min-content;\n  grid-column-gap: ", ";\n  align-items: center;\n\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), space(1), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(2), function (p) { return p.theme.border; });
var HeaderTitle = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var List = styled('ul')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"], ["\n  list-style: none;\n  margin: 0;\n  padding: 0;\n"])));
var ListItem = styled('li')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr max-content;\n  grid-column-gap: ", ";\n  align-items: center;\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n  :hover {\n    background-color: ", ";\n  }\n\n  &:hover span {\n    color: ", ";\n    text-decoration: underline;\n  }\n"])), space(1), space(1), space(2), function (p) { return p.theme.border; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.blue300; });
var OperationDot = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n\n  background-color: ", ";\n"], ["\n  content: '';\n  display: block;\n  width: 8px;\n  min-width: 8px;\n  height: 8px;\n  margin-right: ", ";\n  border-radius: 100%;\n\n  background-color: ", ";\n"])), space(1), function (p) { return p.backgroundColor; });
var OperationName = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-size: ", ";\n  ", ";\n"], ["\n  font-size: ", ";\n  ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, overflowEllipsis);
export function filterToField(option) {
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return undefined;
        default: {
            return "span_op_breakdowns.ops." + option;
        }
    }
}
export function filterToSearchConditions(option) {
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return undefined;
        default: {
            return "has:" + filterToField(option);
        }
    }
}
export function filterToColour(option) {
    switch (option) {
        case SpanOperationBreakdownFilter.None:
            return pickSpanBarColour('');
        default: {
            return pickSpanBarColour(option);
        }
    }
}
export default Filter;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=filter.jsx.map
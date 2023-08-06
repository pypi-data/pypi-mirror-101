import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import CheckboxFancy from 'app/components/checkboxFancy/checkboxFancy';
import DropdownControl, { Content } from 'app/components/dropdownControl';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import space from 'app/styles/space';
import DropDownButton from './dropDownButton';
function Filter(_a) {
    var options = _a.options, onFilter = _a.onFilter, className = _a.className;
    var checkedQuantity = Object.values(options)
        .flatMap(function (option) { return option; })
        .filter(function (option) { return option.isChecked; }).length;
    function handleClick(category, option) {
        return function () {
            var _a;
            var updatedOptions = __assign(__assign({}, options), (_a = {}, _a[category] = options[category].map(function (groupedOption) {
                if (option.id === groupedOption.id) {
                    return __assign(__assign({}, groupedOption), { isChecked: !groupedOption.isChecked });
                }
                return groupedOption;
            }), _a));
            onFilter(updatedOptions);
        };
    }
    return (<Wrapper className={className}>
      <DropdownControl button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<DropDownButton isOpen={isOpen} getActorProps={getActorProps} checkedQuantity={checkedQuantity}/>);
        }}>
        {function (_a) {
            var getMenuProps = _a.getMenuProps, isOpen = _a.isOpen;
            return (<StyledContent {...getMenuProps()} alignMenu="left" width="240px" isOpen={isOpen} className="drop-down-filter-menu" blendWithActor blendCorner>
            {Object.keys(options).map(function (category) { return (<React.Fragment key={category}>
                <Header>{category}</Header>
                <List>
                  {options[category].map(function (groupedOption) {
                        var symbol = groupedOption.symbol, isChecked = groupedOption.isChecked, id = groupedOption.id;
                        return (<StyledListItem key={id} onClick={handleClick(category, groupedOption)} isChecked={isChecked}>
                        {symbol}
                        <CheckboxFancy isChecked={isChecked}/>
                      </StyledListItem>);
                    })}
                </List>
              </React.Fragment>); })}
          </StyledContent>);
        }}
      </DropdownControl>
    </Wrapper>);
}
export default Filter;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  display: flex;\n"], ["\n  position: relative;\n  display: flex;\n"])));
var StyledContent = styled(Content)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  > * :last-child {\n    margin-bottom: -1px;\n  }\n"], ["\n  > * :last-child {\n    margin-bottom: -1px;\n  }\n"])));
var Header = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  margin: 0;\n  background-color: ", ";\n  color: ", ";\n  font-weight: normal;\n  font-size: ", ";\n  padding: ", " ", ";\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(2), function (p) { return p.theme.border; });
var StyledListItem = styled(ListItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  padding: ", " ", ";\n  align-items: center;\n  cursor: pointer;\n  border-bottom: 1px solid ", ";\n  ", " {\n    opacity: ", ";\n  }\n\n  :hover {\n    background-color: ", ";\n    ", " {\n      opacity: 1;\n    }\n    span {\n      color: ", ";\n      text-decoration: underline;\n    }\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-column-gap: ", ";\n  padding: ", " ", ";\n  align-items: center;\n  cursor: pointer;\n  border-bottom: 1px solid ", ";\n  ", " {\n    opacity: ", ";\n  }\n\n  :hover {\n    background-color: ", ";\n    ", " {\n      opacity: 1;\n    }\n    span {\n      color: ", ";\n      text-decoration: underline;\n    }\n  }\n"])), space(1), space(1), space(2), function (p) { return p.theme.border; }, CheckboxFancy, function (p) { return (p.isChecked ? 1 : 0.3); }, function (p) { return p.theme.backgroundSecondary; }, CheckboxFancy, function (p) { return p.theme.blue300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=index.jsx.map
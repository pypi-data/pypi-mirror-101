import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownButton from 'app/components/dropdownButton';
import SelectControl from 'app/components/forms/selectControl';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined, objectIsEmpty } from 'app/utils';
import InputField from 'app/views/settings/components/forms/inputField';
var defaultProps = {
    addButtonText: t('Add Item'),
    perItemMapping: false,
    allowEmpty: false,
};
var ChoiceMapper = /** @class */ (function (_super) {
    __extends(ChoiceMapper, _super);
    function ChoiceMapper() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.hasValue = function (value) { return defined(value) && !objectIsEmpty(value); };
        _this.renderField = function (props) {
            var _a, _b, _c, _d;
            var onChange = props.onChange, onBlur = props.onBlur, addButtonText = props.addButtonText, addDropdown = props.addDropdown, mappedColumnLabel = props.mappedColumnLabel, columnLabels = props.columnLabels, mappedSelectors = props.mappedSelectors, perItemMapping = props.perItemMapping, disabled = props.disabled, allowEmpty = props.allowEmpty;
            var mappedKeys = Object.keys(columnLabels);
            var emptyValue = mappedKeys.reduce(function (a, v) {
                var _a;
                return (__assign(__assign({}, a), (_a = {}, _a[v] = null, _a)));
            }, {});
            var valueIsEmpty = _this.hasValue(props.value);
            var value = valueIsEmpty ? props.value : {};
            var saveChanges = function (nextValue) {
                onChange === null || onChange === void 0 ? void 0 : onChange(nextValue, {});
                var validValues = !Object.values(nextValue)
                    .map(function (o) { return Object.values(o).find(function (v) { return v === null; }); })
                    .includes(null);
                if (allowEmpty || validValues) {
                    onBlur === null || onBlur === void 0 ? void 0 : onBlur();
                }
            };
            var addRow = function (data) {
                var _a;
                saveChanges(__assign(__assign({}, value), (_a = {}, _a[data.value] = emptyValue, _a)));
            };
            var removeRow = function (itemKey) {
                //eslint-disable-next-line no-unused-vars
                var _a = value, _b = itemKey, _ = _a[_b], updatedValue = __rest(_a, [typeof _b === "symbol" ? _b : _b + ""]);
                saveChanges(updatedValue);
            };
            var setValue = function (itemKey, fieldKey, fieldValue) {
                var _a, _b;
                saveChanges(__assign(__assign({}, value), (_a = {}, _a[itemKey] = __assign(__assign({}, value[itemKey]), (_b = {}, _b[fieldKey] = fieldValue, _b)), _a)));
            };
            // Remove already added values from the items list
            var selectableValues = (_b = (_a = addDropdown.items) === null || _a === void 0 ? void 0 : _a.filter(function (i) { return !value.hasOwnProperty(i.value); })) !== null && _b !== void 0 ? _b : [];
            var valueMap = (_d = (_c = addDropdown.items) === null || _c === void 0 ? void 0 : _c.reduce(function (map, item) {
                map[item.value] = item.label;
                return map;
            }, {})) !== null && _d !== void 0 ? _d : {};
            var dropdown = (<DropdownAutoComplete {...addDropdown} alignMenu={valueIsEmpty ? 'right' : 'left'} items={selectableValues} onSelect={addRow} disabled={disabled}>
        {function (_a) {
                    var isOpen = _a.isOpen;
                    return (<DropdownButton icon={<IconAdd size="xs" isCircled/>} isOpen={isOpen} size="xsmall" disabled={disabled}>
            {addButtonText}
          </DropdownButton>);
                }}
      </DropdownAutoComplete>);
            // The field will be set to inline when there is no value set for the
            // field, just show the dropdown.
            if (!valueIsEmpty) {
                return <div>{dropdown}</div>;
            }
            return (<React.Fragment>
        <Header>
          <LabelColumn>
            <HeadingItem>{mappedColumnLabel}</HeadingItem>
          </LabelColumn>
          {mappedKeys.map(function (fieldKey, i) { return (<Heading key={fieldKey}>
              <HeadingItem>{columnLabels[fieldKey]}</HeadingItem>
              {i === mappedKeys.length - 1 && dropdown}
            </Heading>); })}
        </Header>
        {Object.keys(value).map(function (itemKey) { return (<Row key={itemKey}>
            <LabelColumn>{valueMap[itemKey]}</LabelColumn>
            {mappedKeys.map(function (fieldKey, i) { return (<Column key={fieldKey}>
                <Control>
                  <SelectControl {...(perItemMapping
                        ? mappedSelectors[itemKey][fieldKey]
                        : mappedSelectors[fieldKey])} height={30} disabled={disabled} onChange={function (v) { return setValue(itemKey, fieldKey, v ? v.value : null); }} value={value[itemKey][fieldKey]}/>
                </Control>
                {i === mappedKeys.length - 1 && (<Actions>
                    <Button icon={<IconDelete />} size="small" disabled={disabled} onClick={function () { return removeRow(itemKey); }}/>
                  </Actions>)}
              </Column>); })}
          </Row>); })}
      </React.Fragment>);
        };
        return _this;
    }
    ChoiceMapper.prototype.render = function () {
        var _this = this;
        return (<InputField {...this.props} inline={function (_a) {
            var model = _a.model;
            return !_this.hasValue(model.getValue(_this.props.name));
        }} field={this.renderField}/>);
    };
    ChoiceMapper.defaultProps = defaultProps;
    return ChoiceMapper;
}(React.Component));
export default ChoiceMapper;
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var Heading = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  margin-left: ", ";\n  flex: 1 0 0;\n  align-items: center;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  margin-left: ", ";\n  flex: 1 0 0;\n  align-items: center;\n  justify-content: space-between;\n"])), space(1));
var Row = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  margin-top: ", ";\n  align-items: center;\n"], ["\n  display: flex;\n  margin-top: ", ";\n  align-items: center;\n"])), space(1));
var Column = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  margin-left: ", ";\n  align-items: center;\n  flex: 1 0 0;\n"], ["\n  display: flex;\n  margin-left: ", ";\n  align-items: center;\n  flex: 1 0 0;\n"])), space(1));
var Control = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var LabelColumn = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex: 0 0 200px;\n"], ["\n  flex: 0 0 200px;\n"])));
var HeadingItem = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  font-size: 0.8em;\n  text-transform: uppercase;\n  color: ", ";\n"], ["\n  font-size: 0.8em;\n  text-transform: uppercase;\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var Actions = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=choiceMapperField.jsx.map
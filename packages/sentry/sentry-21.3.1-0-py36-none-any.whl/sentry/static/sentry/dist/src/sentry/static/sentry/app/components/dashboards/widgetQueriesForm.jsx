import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import Button from 'app/components/button';
import SearchBar from 'app/components/events/searchBar';
import SelectControl from 'app/components/forms/selectControl';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { getAggregateAlias } from 'app/utils/discover/fields';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
import WidgetQueryFields from './widgetQueryFields';
var generateOrderOptions = function (fields) {
    var options = [];
    fields.forEach(function (field) {
        var alias = getAggregateAlias(field);
        options.push({ label: t('%s asc', field), value: alias });
        options.push({ label: t('%s desc', field), value: "-" + alias });
    });
    return options;
};
/**
 * Contain widget queries interactions and signal changes via the onChange
 * callback. This component's state should live in the parent.
 */
var WidgetQueriesForm = /** @class */ (function (_super) {
    __extends(WidgetQueriesForm, _super);
    function WidgetQueriesForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Handle scalar field values changing.
        _this.handleFieldChange = function (queryIndex, field) {
            var _a = _this.props, queries = _a.queries, onChange = _a.onChange;
            var widgetQuery = queries[queryIndex];
            return function handleChange(value) {
                var _a;
                var newQuery = __assign(__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
                onChange(queryIndex, newQuery);
            };
        };
        return _this;
    }
    WidgetQueriesForm.prototype.getFirstQueryError = function (key) {
        var errors = this.props.errors;
        if (!errors) {
            return undefined;
        }
        return errors.find(function (queryError) { return queryError && queryError[key]; });
    };
    WidgetQueriesForm.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, organization = _b.organization, selection = _b.selection, errors = _b.errors, queries = _b.queries, canAddSearchConditions = _b.canAddSearchConditions, handleAddSearchConditions = _b.handleAddSearchConditions, handleDeleteQuery = _b.handleDeleteQuery, displayType = _b.displayType, fieldOptions = _b.fieldOptions, onChange = _b.onChange;
        var hideLegendAlias = ['table', 'world_map', 'big_number'].includes(displayType);
        return (<QueryWrapper>
        {queries.map(function (widgetQuery, queryIndex) {
                return (<Field key={queryIndex} label={queryIndex === 0 ? t('Query') : null} inline={false} style={{ paddingBottom: "8px" }} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors[queryIndex].conditions}>
              <SearchConditionsWrapper>
                <StyledSearchBar organization={organization} projectIds={selection.projects} query={widgetQuery.conditions} fields={[]} onSearch={_this.handleFieldChange(queryIndex, 'conditions')} onBlur={_this.handleFieldChange(queryIndex, 'conditions')} useFormWrapper={false}/>
                {!hideLegendAlias && (<LegendAliasInput type="text" name="name" required value={widgetQuery.name} placeholder={t('Legend Alias')} onChange={function (event) {
                            return _this.handleFieldChange(queryIndex, 'name')(event.target.value);
                        }}/>)}
                {queries.length > 1 && (<Button size="zero" borderless onClick={function (event) {
                            event.preventDefault();
                            handleDeleteQuery(queryIndex);
                        }} icon={<IconDelete />} title={t('Remove query')} label={t('Remove query')}/>)}
              </SearchConditionsWrapper>
            </Field>);
            })}
        {canAddSearchConditions && (<Button size="small" icon={<IconAdd isCircled/>} onClick={function (event) {
                    event.preventDefault();
                    handleAddSearchConditions();
                }}>
            {t('Add Query')}
          </Button>)}
        <WidgetQueryFields displayType={displayType} fieldOptions={fieldOptions} errors={this.getFirstQueryError('fields')} fields={queries[0].fields} onChange={function (fields) {
                queries.forEach(function (widgetQuery, queryIndex) {
                    var newQuery = cloneDeep(widgetQuery);
                    newQuery.fields = fields;
                    onChange(queryIndex, newQuery);
                });
            }}/>
        {displayType === 'table' && (<Field label={t('Sort by')} inline={false} flexibleControlStateSize stacked error={(_a = this.getFirstQueryError('orderby')) === null || _a === void 0 ? void 0 : _a.orderby} style={{ marginBottom: space(1) }}>
            <SelectControl value={queries[0].orderby} name="orderby" options={generateOrderOptions(queries[0].fields)} onChange={function (option) {
                    return _this.handleFieldChange(0, 'orderby')(option.value);
                }} onSelectResetsInput={false} onCloseResetsInput={false} onBlurResetsInput={false}/>
          </Field>)}
      </QueryWrapper>);
    };
    return WidgetQueriesForm;
}(React.Component));
var QueryWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
export var SearchConditionsWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), space(1));
var StyledSearchBar = styled(SearchBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var LegendAliasInput = styled(Input)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  width: 33%;\n"], ["\n  width: 33%;\n"])));
export default WidgetQueriesForm;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=widgetQueriesForm.jsx.map
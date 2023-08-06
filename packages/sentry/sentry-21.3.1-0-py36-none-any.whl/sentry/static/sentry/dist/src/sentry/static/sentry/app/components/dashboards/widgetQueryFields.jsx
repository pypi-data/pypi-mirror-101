import { __assign, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { aggregateFunctionOutputType, explodeField, generateFieldAsString, isLegalYAxisType, } from 'app/utils/discover/fields';
import ColumnEditCollection from 'app/views/eventsV2/table/columnEditCollection';
import { QueryField } from 'app/views/eventsV2/table/queryField';
import { FieldValueKind } from 'app/views/eventsV2/table/types';
import Field from 'app/views/settings/components/forms/field';
function WidgetQueryFields(_a) {
    var displayType = _a.displayType, errors = _a.errors, fields = _a.fields, fieldOptions = _a.fieldOptions, onChange = _a.onChange, style = _a.style;
    // Handle new fields being added.
    function handleAdd(event) {
        event.preventDefault();
        var newFields = __spreadArray(__spreadArray([], __read(fields)), ['']);
        onChange(newFields);
    }
    function handleRemove(event, fieldIndex) {
        event.preventDefault();
        var newFields = __spreadArray([], __read(fields));
        newFields.splice(fieldIndex, 1);
        onChange(newFields);
    }
    function handleChangeField(value, fieldIndex) {
        var newFields = __spreadArray([], __read(fields));
        newFields[fieldIndex] = generateFieldAsString(value);
        onChange(newFields);
    }
    function handleColumnChange(columns) {
        var newFields = columns.map(generateFieldAsString);
        onChange(newFields);
    }
    if (displayType === 'table') {
        return (<Field data-test-id="columns" label={t('Columns')} inline={false} style={__assign({ padding: space(1) + " 0" }, (style !== null && style !== void 0 ? style : {}))} error={errors === null || errors === void 0 ? void 0 : errors.fields} flexibleControlStateSize stacked required>
        <StyledColumnEditCollection columns={fields.map(function (field) { return explodeField({ field: field }); })} onChange={handleColumnChange} fieldOptions={fieldOptions}/>
      </Field>);
    }
    var hideAddYAxisButton = (['world_map', 'big_number'].includes(displayType) && fields.length === 1) ||
        (['line', 'area', 'stacked_area', 'bar'].includes(displayType) &&
            fields.length === 3);
    // Any function/field choice for Big Number widgets is legal since the
    // data source is from an endpoint that is not timeseries-based.
    // The function/field choice for World Map widget will need to be numeric-like.
    // Column builder for Table widget is already handled above.
    var doNotValidateYAxis = displayType === 'big_number';
    return (<Field data-test-id="y-axis" label={t('Y-Axis')} inline={false} style={__assign({ padding: space(2) + " 0 24px 0" }, (style !== null && style !== void 0 ? style : {}))} flexibleControlStateSize error={errors === null || errors === void 0 ? void 0 : errors.fields} required stacked>
      {fields.map(function (field, i) {
            var fieldValue = explodeField({ field: field });
            return (<QueryFieldWrapper key={field + ":" + i}>
            <QueryField fieldValue={fieldValue} fieldOptions={fieldOptions} onChange={function (value) { return handleChangeField(value, i); }} filterPrimaryOptions={function (option) {
                    // Only validate function names for timeseries widgets and
                    // world map widgets.
                    if (!doNotValidateYAxis &&
                        option.value.kind === FieldValueKind.FUNCTION) {
                        var primaryOutput = aggregateFunctionOutputType(option.value.meta.name, undefined);
                        if (primaryOutput) {
                            // If a function returns a specific type, then validate it.
                            return isLegalYAxisType(primaryOutput);
                        }
                    }
                    return option.value.kind === FieldValueKind.FUNCTION;
                }} filterAggregateParameters={function (option) {
                    // Only validate function parameters for timeseries widgets and
                    // world map widgets.
                    if (doNotValidateYAxis) {
                        return true;
                    }
                    if (fieldValue.kind !== 'function') {
                        return true;
                    }
                    var functionName = fieldValue.function[0];
                    var primaryOutput = aggregateFunctionOutputType(functionName, option.value.meta.name);
                    if (primaryOutput) {
                        return isLegalYAxisType(primaryOutput);
                    }
                    if (option.value.kind === FieldValueKind.FUNCTION) {
                        // Functions are not legal options as an aggregate/function parameter.
                        return false;
                    }
                    return isLegalYAxisType(option.value.meta.dataType);
                }}/>
            {fields.length > 1 && (<Button size="zero" borderless onClick={function (event) { return handleRemove(event, i); }} icon={<IconDelete />} title={t('Remove this Y-Axis')} label={t('Remove this Y-Axis')}/>)}
          </QueryFieldWrapper>);
        })}
      {!hideAddYAxisButton && (<div>
          <Button size="small" icon={<IconAdd isCircled/>} onClick={handleAdd}>
            {t('Add Overlay')}
          </Button>
        </div>)}
    </Field>);
}
var StyledColumnEditCollection = styled(ColumnEditCollection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(1));
export var QueryFieldWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n\n  > * + * {\n    margin-left: ", ";\n  }\n"])), space(1), space(1));
export default WidgetQueryFields;
var templateObject_1, templateObject_2;
//# sourceMappingURL=widgetQueryFields.jsx.map
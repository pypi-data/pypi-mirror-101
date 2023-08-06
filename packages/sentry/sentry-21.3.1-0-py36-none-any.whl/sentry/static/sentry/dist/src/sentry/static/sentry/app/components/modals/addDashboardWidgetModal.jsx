import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spreadArray, __values } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import set from 'lodash/set';
import { validateWidget } from 'app/actionCreators/dashboards';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import WidgetQueriesForm from 'app/components/dashboards/widgetQueriesForm';
import SelectControl from 'app/components/forms/selectControl';
import { PanelAlert } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { aggregateOutputType, isAggregateField, isLegalYAxisType, } from 'app/utils/discover/fields';
import Measurements from 'app/utils/measurements/measurements';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withTags from 'app/utils/withTags';
import { DISPLAY_TYPE_CHOICES } from 'app/views/dashboardsV2/data';
import { DisplayType, } from 'app/views/dashboardsV2/types';
import WidgetCard from 'app/views/dashboardsV2/widgetCard';
import { generateFieldOptions } from 'app/views/eventsV2/utils';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
var newQuery = {
    name: '',
    fields: ['count()'],
    conditions: '',
    orderby: '',
};
function mapErrors(data, update) {
    Object.keys(data).forEach(function (key) {
        var value = data[key];
        // Recurse into nested objects.
        if (Array.isArray(value) && typeof value[0] === 'string') {
            update[key] = value[0];
        }
        else if (Array.isArray(value) && typeof value[0] === 'object') {
            update[key] = value.map(function (item) { return mapErrors(item, {}); });
        }
        else {
            update[key] = mapErrors(value, {});
        }
    });
    return update;
}
function normalizeQueries(displayType, queries) {
    var e_1, _a, e_2, _b;
    var isTimeseriesChart = ['line', 'area', 'stacked_area', 'bar'].includes(displayType);
    if (['table', 'world_map', 'big_number'].includes(displayType)) {
        // Some display types may only support at most 1 query.
        queries = queries.slice(0, 1);
    }
    else if (isTimeseriesChart) {
        // Timeseries charts supports at most 3 queries.
        queries = queries.slice(0, 3);
    }
    if (displayType === 'table') {
        return queries;
    }
    // Filter out non-aggregate fields
    queries = queries.map(function (query) {
        var fields = query.fields.filter(isAggregateField);
        if (isTimeseriesChart || displayType === 'world_map') {
            // Filter out fields that will not generate numeric output types
            fields = fields.filter(function (field) { return isLegalYAxisType(aggregateOutputType(field)); });
        }
        if (isTimeseriesChart && fields.length && fields.length > 3) {
            // Timeseries charts supports at most 3 fields.
            fields = fields.slice(0, 3);
        }
        return __assign(__assign({}, query), { fields: fields.length ? fields : ['count()'] });
    });
    if (isTimeseriesChart) {
        // For timeseries widget, all queries must share identical set of fields.
        var referenceFields_1 = __spreadArray([], __read(queries[0].fields));
        try {
            queryLoop: for (var queries_1 = __values(queries), queries_1_1 = queries_1.next(); !queries_1_1.done; queries_1_1 = queries_1.next()) {
                var query = queries_1_1.value;
                if (referenceFields_1.length >= 3) {
                    break;
                }
                if (isEqual(referenceFields_1, query.fields)) {
                    continue;
                }
                try {
                    for (var _c = (e_2 = void 0, __values(query.fields)), _d = _c.next(); !_d.done; _d = _c.next()) {
                        var field = _d.value;
                        if (referenceFields_1.length >= 3) {
                            break queryLoop;
                        }
                        if (!referenceFields_1.includes(field)) {
                            referenceFields_1.push(field);
                        }
                    }
                }
                catch (e_2_1) { e_2 = { error: e_2_1 }; }
                finally {
                    try {
                        if (_d && !_d.done && (_b = _c.return)) _b.call(_c);
                    }
                    finally { if (e_2) throw e_2.error; }
                }
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (queries_1_1 && !queries_1_1.done && (_a = queries_1.return)) _a.call(queries_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        queries = queries.map(function (query) {
            return __assign(__assign({}, query), { fields: referenceFields_1 });
        });
    }
    if (['world_map', 'big_number'].includes(displayType)) {
        // For world map chart, cap fields of the queries to only one field.
        queries = queries.map(function (query) {
            return __assign(__assign({}, query), { fields: query.fields.slice(0, 1) });
        });
    }
    return queries;
}
var AddDashboardWidgetModal = /** @class */ (function (_super) {
    __extends(AddDashboardWidgetModal, _super);
    function AddDashboardWidgetModal(props) {
        var _this = _super.call(this, props) || this;
        _this.handleSubmit = function (event) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, closeModal, organization, onAddWidget, onUpdateWidget, previousWidget, widgetData, err_1, errors;
            var _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        event.preventDefault();
                        _a = this.props, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, onAddWidget = _a.onAddWidget, onUpdateWidget = _a.onUpdateWidget, previousWidget = _a.widget;
                        this.setState({ loading: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, 4, 5]);
                        widgetData = pick(this.state, [
                            'title',
                            'displayType',
                            'interval',
                            'queries',
                        ]);
                        return [4 /*yield*/, validateWidget(api, organization.slug, widgetData)];
                    case 2:
                        _c.sent();
                        if (typeof onUpdateWidget === 'function' && !!previousWidget) {
                            onUpdateWidget(__assign({ id: previousWidget === null || previousWidget === void 0 ? void 0 : previousWidget.id }, widgetData));
                            addSuccessMessage(t('Updated widget.'));
                        }
                        else {
                            onAddWidget(widgetData);
                            addSuccessMessage(t('Added widget.'));
                        }
                        closeModal();
                        return [3 /*break*/, 5];
                    case 3:
                        err_1 = _c.sent();
                        errors = mapErrors((_b = err_1 === null || err_1 === void 0 ? void 0 : err_1.responseJSON) !== null && _b !== void 0 ? _b : {}, {});
                        this.setState({ errors: errors });
                        return [3 /*break*/, 5];
                    case 4:
                        this.setState({ loading: false });
                        return [7 /*endfinally*/];
                    case 5: return [2 /*return*/];
                }
            });
        }); };
        _this.handleFieldChange = function (field) { return function (value) {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                set(newState, field, value);
                if (field === 'displayType') {
                    var displayType = value;
                    set(newState, 'queries', normalizeQueries(displayType, prevState.queries));
                }
                return __assign(__assign({}, newState), { errors: undefined });
            });
        }; };
        _this.handleQueryChange = function (widgetQuery, index) {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                set(newState, "queries." + index, widgetQuery);
                return __assign(__assign({}, newState), { errors: undefined });
            });
        };
        _this.handleQueryRemove = function (index) {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                newState.queries.splice(index, index + 1);
                return __assign(__assign({}, newState), { errors: undefined });
            });
        };
        _this.handleAddSearchConditions = function () {
            _this.setState(function (prevState) {
                var newState = cloneDeep(prevState);
                newState.queries.push(cloneDeep(newQuery));
                return newState;
            });
        };
        var widget = props.widget;
        if (!widget) {
            _this.state = {
                title: '',
                displayType: DisplayType.LINE,
                interval: '5m',
                queries: [__assign({}, newQuery)],
                errors: undefined,
                loading: false,
            };
            return _this;
        }
        _this.state = {
            title: widget.title,
            displayType: widget.displayType,
            interval: widget.interval,
            queries: normalizeQueries(widget.displayType, widget.queries),
            errors: undefined,
            loading: false,
        };
        return _this;
    }
    AddDashboardWidgetModal.prototype.canAddSearchConditions = function () {
        var rightDisplayType = ['line', 'area', 'stacked_area', 'bar'].includes(this.state.displayType);
        var underQueryLimit = this.state.queries.length < 3;
        return rightDisplayType && underQueryLimit;
    };
    AddDashboardWidgetModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Footer = _a.Footer, Body = _a.Body, Header = _a.Header, api = _a.api, closeModal = _a.closeModal, organization = _a.organization, selection = _a.selection, tags = _a.tags, onUpdateWidget = _a.onUpdateWidget, previousWidget = _a.widget;
        var state = this.state;
        var errors = state.errors;
        var fieldOptions = function (measurementKeys) {
            return generateFieldOptions({
                organization: organization,
                tagKeys: Object.values(tags).map(function (_a) {
                    var key = _a.key;
                    return key;
                }),
                measurementKeys: measurementKeys,
            });
        };
        var isUpdatingWidget = typeof onUpdateWidget === 'function' && !!previousWidget;
        return (<React.Fragment>
        <Header closeButton onHide={closeModal}>
          <h4>{isUpdatingWidget ? t('Edit Widget') : t('Add Widget')}</h4>
        </Header>
        <Body>
          <DoubleFieldWrapper>
            <Field data-test-id="widget-name" label={t('Widget Name')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.title} required>
              <Input type="text" name="title" maxLength={255} required value={state.title} onChange={function (event) {
                _this.handleFieldChange('title')(event.target.value);
            }}/>
            </Field>
            <Field data-test-id="chart-type" label={t('Visualization Display')} inline={false} flexibleControlStateSize stacked error={errors === null || errors === void 0 ? void 0 : errors.displayType} required>
              <SelectControl required options={DISPLAY_TYPE_CHOICES.slice()} name="displayType" label={t('Visualization Display')} value={state.displayType} onChange={function (option) {
                _this.handleFieldChange('displayType')(option.value);
            }}/>
            </Field>
          </DoubleFieldWrapper>
          <Measurements>
            {function (_a) {
                var measurements = _a.measurements;
                var measurementKeys = Object.values(measurements).map(function (_a) {
                    var key = _a.key;
                    return key;
                });
                var amendedFieldOptions = fieldOptions(measurementKeys);
                return (<WidgetQueriesForm organization={organization} selection={selection} fieldOptions={amendedFieldOptions} displayType={state.displayType} queries={state.queries} errors={errors === null || errors === void 0 ? void 0 : errors.queries} onChange={function (queryIndex, widgetQuery) {
                        return _this.handleQueryChange(widgetQuery, queryIndex);
                    }} canAddSearchConditions={_this.canAddSearchConditions()} handleAddSearchConditions={_this.handleAddSearchConditions} handleDeleteQuery={_this.handleQueryRemove}/>);
            }}
          </Measurements>
          <WidgetCard api={api} organization={organization} selection={selection} widget={this.state} isEditing={false} onDelete={function () { return undefined; }} onEdit={function () { return undefined; }} renderErrorMessage={function (errorMessage) {
                return typeof errorMessage === 'string' && (<PanelAlert type="error">{errorMessage}</PanelAlert>);
            }} isSorting={false} currentWidgetDragging={false}/>
        </Body>
        <Footer>
          <ButtonBar gap={1}>
            <Button external href="https://docs.sentry.io/product/dashboards/custom-dashboards/#widget-builder">
              {t('Read the docs')}
            </Button>
            <Button data-test-id="add-widget" priority="primary" type="button" onClick={this.handleSubmit} disabled={state.loading} busy={state.loading}>
              {isUpdatingWidget ? t('Update Widget') : t('Add Widget')}
            </Button>
          </ButtonBar>
        </Footer>
      </React.Fragment>);
    };
    return AddDashboardWidgetModal;
}(React.Component));
var DoubleFieldWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-column-gap: ", ";\n  width: 100%;\n"], ["\n  display: inline-grid;\n  grid-template-columns: repeat(2, 1fr);\n  grid-column-gap: ", ";\n  width: 100%;\n"])), space(1));
export var modalCss = css(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  .modal-dialog {\n    position: unset;\n    width: 100%;\n    max-width: 700px;\n    margin: 70px auto;\n  }\n"], ["\n  .modal-dialog {\n    position: unset;\n    width: 100%;\n    max-width: 700px;\n    margin: 70px auto;\n  }\n"])));
export default withApi(withGlobalSelection(withTags(AddDashboardWidgetModal)));
var templateObject_1, templateObject_2;
//# sourceMappingURL=addDashboardWidgetModal.jsx.map
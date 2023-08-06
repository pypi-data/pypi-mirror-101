import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import cloneDeep from 'lodash/cloneDeep';
import set from 'lodash/set';
import Breadcrumbs from 'app/components/breadcrumbs';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import SelectControl from 'app/components/forms/selectControl';
import * as Layout from 'app/components/layouts/thirds';
import List from 'app/components/list';
import { PanelAlert } from 'app/components/panels';
import { t, tct } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import routeTitleGen from 'app/utils/routeTitle';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import { DisplayType } from 'app/views/dashboardsV2/types';
import WidgetCard from 'app/views/dashboardsV2/widgetCard';
import RadioField from 'app/views/settings/components/forms/radioField';
import BuildStep from './buildStep';
import EventSteps from './eventSteps';
import MetricSteps from './metricSteps';
import { displayTypes } from './utils';
var DataSet;
(function (DataSet) {
    DataSet["EVENTS"] = "events";
    DataSet["METRICS"] = "metrics";
})(DataSet || (DataSet = {}));
var newEventQuery = {
    name: '',
    fields: ['count()'],
    conditions: '',
    orderby: '',
};
var newMetricQuery = {
    tags: '',
    groupBy: '',
    aggregation: '',
};
var dataSetChoices = [
    ['events', t('Events')],
    ['metrics', t('Metrics')],
];
var WidgetNew = /** @class */ (function (_super) {
    __extends(WidgetNew, _super);
    function WidgetNew() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFieldChange = function (field, value) {
            if (field === 'displayType') {
                _this.setState(function (state) {
                    var _a;
                    return (__assign(__assign({}, state), (_a = {}, _a[field] = value, _a.title = tct('Custom [displayType] Widget', { displayType: displayTypes[value] }), _a)));
                });
                return;
            }
            _this.setState(function (state) {
                var _a;
                return (__assign(__assign({}, state), (_a = {}, _a[field] = value, _a)));
            });
        };
        _this.handleEventQueryChange = function (index, widgetQuery) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                set(newState, "eventQueries." + index, widgetQuery);
                return newState;
            });
        };
        _this.handleMetricQueryChange = function (index, metricQuery) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                set(newState, "metricQueries." + index, metricQuery);
                return newState;
            });
        };
        _this.handleRemoveQuery = function (index) {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                if (state.dataSet === DataSet.EVENTS) {
                    newState.eventQueries.splice(index, index + 1);
                    return newState;
                }
                newState.metricQueries.splice(index, index + 1);
                return newState;
            });
        };
        _this.handleAddQuery = function () {
            _this.setState(function (state) {
                var newState = cloneDeep(state);
                if (state.dataSet === DataSet.EVENTS) {
                    newState.eventQueries.push(cloneDeep(newEventQuery));
                    return newState;
                }
                newState.metricQueries.push(cloneDeep(newMetricQuery));
                return newState;
            });
        };
        return _this;
    }
    WidgetNew.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { title: tct('Custom [displayType] Widget', { displayType: DisplayType.AREA }), displayType: DisplayType.AREA, interval: '5m', eventQueries: [__assign({}, newEventQuery)], metricQueries: [__assign({}, newMetricQuery)], dataSet: DataSet.EVENTS });
    };
    WidgetNew.prototype.getTitle = function () {
        var params = this.props.params;
        return routeTitleGen(t('Dashboards - Widget Builder'), params.orgId, false);
    };
    WidgetNew.prototype.render = function () {
        var _this = this;
        var _a = this.props, params = _a.params, organization = _a.organization, selection = _a.selection;
        var _b = this.state, displayType = _b.displayType, dataSet = _b.dataSet, title = _b.title, interval = _b.interval, eventQueries = _b.eventQueries, metricQueries = _b.metricQueries;
        return (<StyledPageContent>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumbs crumbs={[
                {
                    to: "/organizations/" + params.orgId + "/dashboards/",
                    label: t('Dashboards'),
                },
                { label: t('Widget Builder') },
            ]}/>
            <Layout.Title>{title}</Layout.Title>
          </Layout.HeaderContent>

          <Layout.HeaderActions>
            <ButtonBar gap={1}>
              <Button title={t("You’re seeing the metrics project because you have the feature flag 'organizations:metrics' enabled. Send us feedback via email.")} href="mailto:metrics-feedback@sentry.io?subject=Metrics Feedback">
                {t('Give Feedback')}
              </Button>
              <Button priority="primary">{t('Save Widget')}</Button>
            </ButtonBar>
          </Layout.HeaderActions>
        </Layout.Header>

        <Layout.Body>
          <BuildSteps symbol="colored-numeric">
            <BuildStep title={t('Choose your visualization')} description={t('This is a preview of how your widget will appear in the dashboard.')}>
              <VisualizationWrapper>
                <SelectControl name="displayType" options={Object.keys(displayTypes).map(function (value) { return ({
                label: displayTypes[value],
                value: value,
            }); })} value={displayType} onChange={function (option) {
                _this.handleFieldChange('displayType', option.value);
            }}/>
                <WidgetCard api={this.api} organization={organization} selection={selection} widget={{
                title: title,
                displayType: displayType,
                queries: eventQueries,
                interval: interval,
            }} isEditing={false} onDelete={function () { return undefined; }} onEdit={function () { return undefined; }} renderErrorMessage={function (errorMessage) {
                return typeof errorMessage === 'string' && (<PanelAlert type="error">{errorMessage}</PanelAlert>);
            }} isSorting={false} currentWidgetDragging={false}/>
              </VisualizationWrapper>
            </BuildStep>
            <BuildStep title={t('Choose your data set')} description={t('Monitor specific events such as errors and transactions or get metric readings on TBD.')}>
              <RadioField name="dataSet" onChange={function (value) { return _this.handleFieldChange('dataSet', value); }} value={dataSet} choices={dataSetChoices} inline={false} orientInline hideControlState stacked/>
            </BuildStep>
            {dataSet === DataSet.METRICS ? (<MetricSteps metricQueries={metricQueries} onAddQuery={this.handleAddQuery} onRemoveQuery={this.handleRemoveQuery} onChangeQuery={this.handleMetricQueryChange} onChangeField={this.handleFieldChange}/>) : (<EventSteps selectedProjectIds={selection.projects} organization={organization} eventQueries={eventQueries} displayType={displayType} onAddQuery={this.handleAddQuery} onRemoveQuery={this.handleRemoveQuery} onChangeQuery={this.handleEventQueryChange}/>)}
          </BuildSteps>
        </Layout.Body>
      </StyledPageContent>);
    };
    return WidgetNew;
}(AsyncView));
export default withOrganization(withGlobalSelection(WidgetNew));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var BuildSteps = styled(List)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  max-width: 100%;\n\n  @media (min-width: ", ") {\n    max-width: 50%;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  max-width: 100%;\n\n  @media (min-width: ", ") {\n    max-width: 50%;\n  }\n"])), space(4), function (p) { return p.theme.breakpoints[4]; });
var VisualizationWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(1.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=widgetNew.jsx.map
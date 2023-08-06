import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { components } from 'react-select';
import styled from '@emotion/styled';
import Highlight from 'app/components/highlight';
import { t } from 'app/locale';
import SelectField from 'app/views/settings/components/forms/selectField';
import BuildStep from '../buildStep';
import { metrics } from '../utils';
import Queries from './queries';
function MetricSteps(_a) {
    var metricQueries = _a.metricQueries, onAddQuery = _a.onAddQuery, onRemoveQuery = _a.onRemoveQuery, onChangeQuery = _a.onChangeQuery, onChangeField = _a.onChangeField;
    return (<React.Fragment>
      <BuildStep title={t('Choose your y-axis metric')} description={t('Determine what type of metric you want to graph by.')}>
        <StyledSelectField name="metric" choices={metrics.map(function (metric) { return [metric, metric]; })} placeholder={t('Select metric')} onChange={function (value) { return onChangeField('metric', String(value)); }} components={{
            Option: function (_a) {
                var label = _a.label, optionProps = __rest(_a, ["label"]);
                var selectProps = optionProps.selectProps;
                var inputValue = selectProps.inputValue;
                return (<components.Option label={label} {...optionProps}>
                  <Highlight text={inputValue !== null && inputValue !== void 0 ? inputValue : ''}>{label}</Highlight>
                </components.Option>);
            },
        }} inline={false} flexibleControlStateSize stacked allowClear/>
      </BuildStep>
      <BuildStep title={t('Begin your search')} description={t('Add another query to compare projects, tags, etc.')}>
        <Queries queries={metricQueries} onAddQuery={onAddQuery} onRemoveQuery={onRemoveQuery} onChangeQuery={onChangeQuery}/>
      </BuildStep>
    </React.Fragment>);
}
export default MetricSteps;
var StyledSelectField = styled(SelectField)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map
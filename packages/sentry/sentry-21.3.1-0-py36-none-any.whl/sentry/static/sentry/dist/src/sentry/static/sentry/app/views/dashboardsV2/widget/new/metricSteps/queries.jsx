import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import SmartSearchBar from 'app/components/smartSearchBar';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Field from 'app/views/settings/components/forms/field';
import SelectField from 'app/views/settings/components/forms/selectField';
import { Aggregation, metricGroupByOptions, metricTags } from '../utils';
function Queries(_a) {
    var queries = _a.queries, onRemoveQuery = _a.onRemoveQuery, onAddQuery = _a.onAddQuery, onChangeQuery = _a.onChangeQuery;
    function handleFieldChange(queryIndex, field) {
        var widgetQuery = queries[queryIndex];
        return function handleChange(value) {
            var _a;
            var newQuery = __assign(__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
            onChangeQuery(queryIndex, newQuery);
        };
    }
    function getTagValue(_a, _query, _params) {
        var key = _a.key;
        return Promise.resolve([metricTags[key].value]);
    }
    return (<div>
      {queries.map(function (metricQuery, queryIndex) {
            return (<StyledField key={queryIndex} inline={false} flexibleControlStateSize stacked>
            <Fields displayDeleteButton={queries.length > 1}>
              <SmartSearchBar hasRecentSearches maxSearchItems={5} placeholder={t('Search for tag')} supportedTags={metricTags} onChange={function (value) { return handleFieldChange(queryIndex, 'tags')(value); }} onBlur={function (value) { return handleFieldChange(queryIndex, 'tags')(value); }} onGetTagValues={getTagValue} excludeEnvironment/>
              <StyledSelectField name="groupBy" placeholder={t('Select Group By')} choices={metricGroupByOptions} value={metricQuery.groupBy} onChange={function (value) {
                    return handleFieldChange(queryIndex, 'groupBy')(value);
                }} inline={false} allowClear={false} flexibleControlStateSize stacked/>
              <StyledSelectField name="aggregation" placeholder={t('Select Aggregation')} choices={Object.values(Aggregation).map(function (aggregation) { return [
                    aggregation,
                    aggregation,
                ]; })} value={metricQuery.aggregation} onChange={function (value) { return handleFieldChange(queryIndex, 'aggregation')(value); }} inline={false} allowClear={false} flexibleControlStateSize stacked/>
              {queries.length > 1 && (<Button size="zero" borderless onClick={function (event) {
                        event.preventDefault();
                        onRemoveQuery(queryIndex);
                    }} icon={<IconDelete />} title={t('Remove query')} label={t('Remove query')}/>)}
            </Fields>
          </StyledField>);
        })}
      <Button size="small" icon={<IconAdd isCircled/>} onClick={function (event) {
            event.preventDefault();
            onAddQuery();
        }}>
        {t('Add Query')}
      </Button>
    </div>);
}
export default Queries;
var Fields = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: ", ";\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: ",
    ";\n  grid-gap: ", ";\n  align-items: center;\n"])), function (p) {
    return p.displayDeleteButton ? '1fr 0.5fr 0.5fr max-content' : '1fr 0.5fr 0.5fr';
}, space(1));
var StyledField = styled(Field)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var StyledSelectField = styled(SelectField)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-right: 0;\n  padding-bottom: 0;\n"], ["\n  padding-right: 0;\n  padding-bottom: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=queries.jsx.map
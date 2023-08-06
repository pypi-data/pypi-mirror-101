import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import SearchBar from 'app/components/events/searchBar';
import { IconAdd, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
import { DisplayType } from '../../../types';
function Queries(_a) {
    var queries = _a.queries, selectedProjectIds = _a.selectedProjectIds, organization = _a.organization, displayType = _a.displayType, onRemoveQuery = _a.onRemoveQuery, onAddQuery = _a.onAddQuery, onChangeQuery = _a.onChangeQuery;
    function handleFieldChange(queryIndex, field) {
        var widgetQuery = queries[queryIndex];
        return function handleChange(value) {
            var _a;
            var newQuery = __assign(__assign({}, widgetQuery), (_a = {}, _a[field] = value, _a));
            onChangeQuery(queryIndex, newQuery);
        };
    }
    function canAddNewQuery() {
        var rightDisplayType = [
            DisplayType.LINE,
            DisplayType.AREA,
            DisplayType.STACKED_AREA,
            DisplayType.BAR,
        ].includes(displayType);
        var underQueryLimit = queries.length < 3;
        return rightDisplayType && underQueryLimit;
    }
    var hideLegendAlias = [
        DisplayType.TABLE,
        DisplayType.WORLD_MAP,
        DisplayType.BIG_NUMBER,
    ].includes(displayType);
    return (<div>
      {queries.map(function (eventQuery, queryIndex) {
            var displayDeleteButton = queries.length > 1;
            var displayLegendAlias = !hideLegendAlias;
            return (<StyledField key={queryIndex} inline={false} flexibleControlStateSize stacked>
            <Fields displayDeleteButton={displayDeleteButton} displayLegendAlias={displayLegendAlias}>
              <SearchBar organization={organization} projectIds={selectedProjectIds} query={eventQuery.conditions} fields={[]} onSearch={handleFieldChange(queryIndex, 'conditions')} onBlur={handleFieldChange(queryIndex, 'conditions')} useFormWrapper={false}/>
              {displayLegendAlias && (<Input type="text" name="name" required value={eventQuery.name} placeholder={t('Legend Alias')} onChange={function (event) {
                        return handleFieldChange(queryIndex, 'name')(event.target.value);
                    }}/>)}
              {displayDeleteButton && (<Button size="zero" borderless onClick={function (event) {
                        event.preventDefault();
                        onRemoveQuery(queryIndex);
                    }} icon={<IconDelete />} title={t('Remove query')} label={t('Remove query')}/>)}
            </Fields>
          </StyledField>);
        })}
      {canAddNewQuery() && (<Button size="small" icon={<IconAdd isCircled/>} onClick={function (event) {
                event.preventDefault();
                onAddQuery();
            }}>
          {t('Add Query')}
        </Button>)}
    </div>);
}
export default Queries;
var fieldsColumns = function (p) {
    if (!p.displayDeleteButton && !p.displayLegendAlias) {
        return '1fr';
    }
    if (!p.displayDeleteButton) {
        return '1fr 33%';
    }
    if (!p.displayLegendAlias) {
        return '1fr max-content';
    }
    return '1fr 33% max-content';
};
var Fields = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: ", ";\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: ", ";\n  grid-gap: ", ";\n  align-items: center;\n"])), fieldsColumns, space(1));
var StyledField = styled(Field)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=queries.jsx.map
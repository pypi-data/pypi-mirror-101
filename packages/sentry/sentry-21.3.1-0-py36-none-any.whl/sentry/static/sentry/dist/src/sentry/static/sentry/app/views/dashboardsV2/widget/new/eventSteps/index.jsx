import React from 'react';
import cloneDeep from 'lodash/cloneDeep';
import WidgetQueryFields from 'app/components/dashboards/widgetQueryFields';
import { t } from 'app/locale';
import Measurements from 'app/utils/measurements/measurements';
import withTags from 'app/utils/withTags';
import { generateFieldOptions } from 'app/views/eventsV2/utils';
import { DisplayType } from '../../../types';
import BuildStep from '../buildStep';
import Queries from './queries';
function EventSteps(_a) {
    var eventQueries = _a.eventQueries, selectedProjectIds = _a.selectedProjectIds, organization = _a.organization, tags = _a.tags, displayType = _a.displayType, onRemoveQuery = _a.onRemoveQuery, onAddQuery = _a.onAddQuery, onChangeQuery = _a.onChangeQuery;
    function fieldOptions(measurementKeys) {
        return generateFieldOptions({
            organization: organization,
            tagKeys: Object.values(tags).map(function (_a) {
                var key = _a.key;
                return key;
            }),
            measurementKeys: measurementKeys,
        });
    }
    return (<React.Fragment>
      <BuildStep title={t('Begin your search')} description={t('Add another query to compare projects, tags, etc.')}>
        <Queries queries={eventQueries} selectedProjectIds={selectedProjectIds} organization={organization} displayType={displayType} onRemoveQuery={onRemoveQuery} onAddQuery={onAddQuery} onChangeQuery={onChangeQuery}/>
      </BuildStep>
      <Measurements>
        {function (_a) {
            var measurements = _a.measurements;
            var measurementKeys = Object.values(measurements).map(function (_a) {
                var key = _a.key;
                return key;
            });
            var amendedFieldOptions = fieldOptions(measurementKeys);
            var buildStepContent = (<WidgetQueryFields style={{ padding: 0 }} displayType={displayType} fieldOptions={amendedFieldOptions} fields={eventQueries[0].fields} onChange={function (fields) {
                    eventQueries.forEach(function (eventQuery, queryIndex) {
                        var newQuery = cloneDeep(eventQuery);
                        newQuery.fields = fields;
                        onChangeQuery(queryIndex, newQuery);
                    });
                }}/>);
            return (<BuildStep title={displayType === DisplayType.TABLE
                    ? t('Choose your columns')
                    : t('Choose your y-axis')} description={t('We’ll use this to determine what gets graphed in the y-axis and any additional overlays.')}>
              {buildStepContent}
            </BuildStep>);
        }}
      </Measurements>
    </React.Fragment>);
}
export default withTags(EventSteps);
//# sourceMappingURL=index.jsx.map
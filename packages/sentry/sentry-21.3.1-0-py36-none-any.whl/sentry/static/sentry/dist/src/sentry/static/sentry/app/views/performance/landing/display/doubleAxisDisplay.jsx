import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { Panel } from 'app/components/panels';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import withApi from 'app/utils/withApi';
import _Footer from '../../charts/footer';
import { getTransactionSearchQuery } from '../../utils';
import { SingleAxisChart } from './singleAxisChart';
function DoubleAxisDisplay(props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, axisOptions = props.axisOptions, leftAxis = props.leftAxis, rightAxis = props.rightAxis;
    var onFilterChange = function (field) { return function (minValue, maxValue) {
        var filterString = getTransactionSearchQuery(location);
        var conditions = tokenizeSearch(filterString);
        conditions.setTagValues(field, [
            ">=" + Math.round(minValue),
            "<" + Math.round(maxValue),
        ]);
        var query = stringifyQueryObject(conditions);
        trackAnalyticsEvent({
            eventKey: 'performance_views.landingv2.display.filter_change',
            eventName: 'Performance Views: Landing v2 Display Filter Change',
            organization_id: parseInt(organization.id, 10),
            field: field,
            min_value: parseInt(minValue, 10),
            max_value: parseInt(maxValue, 10),
        });
        browserHistory.push({
            pathname: location.pathname,
            query: __assign(__assign({}, location.query), { query: String(query).trim() }),
        });
    }; };
    return (<Panel>
      <DoubleChartContainer>
        <SingleAxisChart axis={leftAxis} onFilterChange={onFilterChange(leftAxis.field)} {...props}/>
        <SingleAxisChart axis={rightAxis} onFilterChange={onFilterChange(rightAxis.field)} {...props}/>
      </DoubleChartContainer>

      <Footer options={axisOptions} leftAxis={leftAxis.value} rightAxis={rightAxis.value} organization={organization} eventView={eventView} location={location}/>
    </Panel>);
}
var DoubleChartContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n  min-height: 282px;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 1fr;\n  grid-gap: ", ";\n  min-height: 282px;\n"])), space(3));
var Footer = withApi(_Footer);
export default DoubleAxisDisplay;
var templateObject_1;
//# sourceMappingURL=doubleAxisDisplay.jsx.map
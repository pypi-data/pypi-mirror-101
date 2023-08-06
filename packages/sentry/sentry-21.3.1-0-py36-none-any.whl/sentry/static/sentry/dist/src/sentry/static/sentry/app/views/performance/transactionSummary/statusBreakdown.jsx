import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import BreakdownBars from 'app/components/charts/breakdownBars';
import ErrorPanel from 'app/components/charts/errorPanel';
import { SectionHeading } from 'app/components/charts/styles';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import Placeholder from 'app/components/placeholder';
import QuestionTooltip from 'app/components/questionTooltip';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import { getTermHelp, PERFORMANCE_TERM } from 'app/views/performance/data';
function StatusBreakdown(_a) {
    var eventView = _a.eventView, location = _a.location, organization = _a.organization;
    var breakdownView = eventView
        .withColumns([
        { kind: 'function', function: ['count', '', ''] },
        { kind: 'field', field: 'transaction.status' },
    ])
        .withSorts([{ kind: 'desc', field: 'count' }]);
    return (<React.Fragment>
      <SectionHeading>
        {t('Status Breakdown')}
        <QuestionTooltip position="top" title={getTermHelp(organization, PERFORMANCE_TERM.STATUS_BREAKDOWN)} size="sm"/>
      </SectionHeading>
      <DiscoverQuery eventView={breakdownView} location={location} orgSlug={organization.slug} referrer="api.performance.status-breakdown">
        {function (_a) {
            var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
            if (isLoading) {
                return <Placeholder height="124px"/>;
            }
            if (error) {
                return (<ErrorPanel height="124px">
                <IconWarning color="gray300" size="lg"/>
              </ErrorPanel>);
            }
            if (!tableData || tableData.data.length === 0) {
                return (<EmptyStatusBreakdown small>{t('No statuses found')}</EmptyStatusBreakdown>);
            }
            var points = tableData.data.map(function (row) { return ({
                label: String(row['transaction.status']),
                value: parseInt(String(row.count), 10),
            }); });
            return <BreakdownBars data={points}/>;
        }}
      </DiscoverQuery>
    </React.Fragment>);
}
var EmptyStatusBreakdown = styled(EmptyStateWarning)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 124px;\n  padding: 50px 15%;\n"], ["\n  height: 124px;\n  padding: 50px 15%;\n"])));
export default StatusBreakdown;
var templateObject_1;
//# sourceMappingURL=statusBreakdown.jsx.map
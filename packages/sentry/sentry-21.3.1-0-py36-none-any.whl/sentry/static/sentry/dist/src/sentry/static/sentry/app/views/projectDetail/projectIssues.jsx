import { __assign, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import Button from 'app/components/button';
import { SectionHeading } from 'app/components/charts/styles';
import GroupList from 'app/components/issues/groupList';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { Panel, PanelBody } from 'app/components/panels';
import { DEFAULT_RELATIVE_PERIODS, DEFAULT_STATS_PERIOD } from 'app/constants';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { decodeScalar } from 'app/utils/queryString';
import NoGroupsHandler from '../issueList/noGroupsHandler';
function ProjectIssues(_a) {
    var organization = _a.organization, location = _a.location, projectId = _a.projectId, api = _a.api;
    function handleOpenClick() {
        trackAnalyticsEvent({
            eventKey: 'project_detail.open_issues',
            eventName: 'Project Detail: Open issues from project detail',
            organization_id: parseInt(organization.id, 10),
        });
    }
    var endpointPath = "/organizations/" + organization.slug + "/issues/";
    var issueQuery = 'is:unresolved error.unhandled:true';
    var queryParams = __assign(__assign({ limit: 5 }, getParams(pick(location.query, __spreadArray(__spreadArray([], __read(Object.values(URL_PARAM))), ['cursor'])))), { query: issueQuery, sort: 'freq' });
    var issueSearch = {
        pathname: endpointPath,
        query: queryParams,
    };
    function renderEmptyMessage() {
        var selectedTimePeriod = location.query.start
            ? null
            : DEFAULT_RELATIVE_PERIODS[decodeScalar(location.query.statsPeriod, DEFAULT_STATS_PERIOD)];
        var displayedPeriod = selectedTimePeriod
            ? selectedTimePeriod.toLowerCase()
            : t('given timeframe');
        return (<Panel>
        <PanelBody>
          <NoGroupsHandler api={api} organization={organization} query={issueQuery} selectedProjectIds={[projectId]} groupIds={[]} emptyMessage={tct('No unhandled issues for the [timePeriod].', {
                timePeriod: displayedPeriod,
            })}/>
        </PanelBody>
      </Panel>);
    }
    return (<React.Fragment>
      <ControlsWrapper>
        <SectionHeading>{t('Frequent Unhandled Issues')}</SectionHeading>
        <Button data-test-id="issues-open" size="small" to={issueSearch} onClick={handleOpenClick}>
          {t('Open in Issues')}
        </Button>
      </ControlsWrapper>

      <TableWrapper>
        <GroupList orgId={organization.slug} endpointPath={endpointPath} queryParams={queryParams} query="" canSelectGroups={false} renderEmptyMessage={renderEmptyMessage} withChart={false} withPagination/>
      </TableWrapper>
    </React.Fragment>);
}
var ControlsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(1));
var TableWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space(4), Panel, space(1));
export default ProjectIssues;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectIssues.jsx.map
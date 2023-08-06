import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import { SectionHeading } from 'app/components/charts/styles';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import GroupList from 'app/components/issues/groupList';
import { Panel, PanelBody } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { IconInfo } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var RelatedIssues = /** @class */ (function (_super) {
    __extends(RelatedIssues, _super);
    function RelatedIssues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderEmptyMessage = function () {
            return (<Panel>
        <PanelBody>
          <EmptyStateWarning small withIcon={false}>
            {t('No issues for this alert rule')}
          </EmptyStateWarning>
        </PanelBody>
      </Panel>);
        };
        return _this;
    }
    RelatedIssues.prototype.render = function () {
        var _a = this.props, rule = _a.rule, projects = _a.projects, organization = _a.organization, timePeriod = _a.timePeriod;
        var start = timePeriod.start, end = timePeriod.end;
        var path = "/organizations/" + organization.slug + "/issues/";
        var queryParams = {
            start: start,
            end: end,
            groupStatsPeriod: 'auto',
            limit: 5,
            sort: rule.aggregate === 'count_unique(user)' ? 'user' : 'freq',
            query: rule.query,
            project: projects.map(function (project) { return project.id; }),
        };
        var issueSearch = {
            pathname: "/organizations/" + organization.slug + "/issues/",
            query: queryParams,
        };
        return (<React.Fragment>
        <ControlsWrapper>
          <SectionHeading>
            {t('Related Issues')}
            <Tooltip title={t('Top issues containing events matching the metric.')}>
              <IconInfo size="xs"/>
            </Tooltip>
          </SectionHeading>
          <Button data-test-id="issues-open" size="small" to={issueSearch}>
            {t('Open in Issues')}
          </Button>
        </ControlsWrapper>

        <TableWrapper>
          <GroupList orgId={organization.slug} endpointPath={path} queryParams={queryParams} query={"start=" + start + "&end=" + end + "&groupStatsPeriod=auto"} canSelectGroups={false} renderEmptyMessage={this.renderEmptyMessage} withChart withPagination={false} useFilteredStats customStatsPeriod={timePeriod}/>
        </TableWrapper>
      </React.Fragment>);
    };
    return RelatedIssues;
}(React.Component));
var ControlsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(1));
var TableWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space(4), Panel, space(1));
export default RelatedIssues;
var templateObject_1, templateObject_2;
//# sourceMappingURL=relatedIssues.jsx.map
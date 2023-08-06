import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withProfiler } from '@sentry/react';
import omit from 'lodash/omit';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import EventUserFeedback from 'app/components/events/userFeedback';
import CompactIssue from 'app/components/issues/compactIssue';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import PageHeading from 'app/components/pageHeading';
import Pagination from 'app/components/pagination';
import { Panel } from 'app/components/panels';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import UserFeedbackEmpty from './userFeedbackEmpty';
import { getQuery } from './utils';
var OrganizationUserFeedback = /** @class */ (function (_super) {
    __extends(OrganizationUserFeedback, _super);
    function OrganizationUserFeedback() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    OrganizationUserFeedback.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, search = _a.location.search;
        return [
            [
                'reportList',
                "/organizations/" + organization.slug + "/user-feedback/",
                {
                    query: getQuery(search),
                },
            ],
        ];
    };
    OrganizationUserFeedback.prototype.getTitle = function () {
        return t('User Feedback') + " - " + this.props.organization.slug;
    };
    Object.defineProperty(OrganizationUserFeedback.prototype, "projectIds", {
        get: function () {
            var project = this.props.location.query.project;
            return Array.isArray(project)
                ? project
                : typeof project === 'string'
                    ? [project]
                    : [];
        },
        enumerable: false,
        configurable: true
    });
    OrganizationUserFeedback.prototype.renderResults = function () {
        var orgId = this.props.params.orgId;
        return (<Panel className="issue-list" data-test-id="user-feedback-list">
        {this.state.reportList.map(function (item) {
                var issue = item.issue;
                return (<CompactIssue key={item.id} id={issue.id} data={issue} eventId={item.eventID}>
              <StyledEventUserFeedback report={item} orgId={orgId} issueId={issue.id}/>
            </CompactIssue>);
            })}
      </Panel>);
    };
    OrganizationUserFeedback.prototype.renderEmpty = function () {
        return <UserFeedbackEmpty projectIds={this.projectIds}/>;
    };
    OrganizationUserFeedback.prototype.renderLoading = function () {
        return this.renderBody();
    };
    OrganizationUserFeedback.prototype.renderStreamBody = function () {
        var _a = this.state, loading = _a.loading, reportList = _a.reportList;
        if (loading) {
            return (<Panel>
          <LoadingIndicator />
        </Panel>);
        }
        if (!reportList.length) {
            return this.renderEmpty();
        }
        return this.renderResults();
    };
    OrganizationUserFeedback.prototype.renderBody = function () {
        var organization = this.props.organization;
        var location = this.props.location;
        var pathname = location.pathname, search = location.search, query = location.query;
        var status = getQuery(search).status;
        var reportListPageLinks = this.state.reportListPageLinks;
        var unresolvedQuery = omit(query, 'status');
        var allIssuesQuery = __assign(__assign({}, query), { status: '' });
        return (<GlobalSelectionHeader>
        <PageContent>
          <LightWeightNoProjectMessage organization={organization}>
            <div data-test-id="user-feedback">
              <Header>
                <PageHeading>{t('User Feedback')}</PageHeading>
                <ButtonBar active={!Array.isArray(status) ? status || '' : ''} merged>
                  <Button size="small" barId="unresolved" to={{ pathname: pathname, query: unresolvedQuery }}>
                    {t('Unresolved')}
                  </Button>
                  <Button size="small" barId="" to={{ pathname: pathname, query: allIssuesQuery }}>
                    {t('All Issues')}
                  </Button>
                </ButtonBar>
              </Header>
              {this.renderStreamBody()}
              <Pagination pageLinks={reportListPageLinks}/>
            </div>
          </LightWeightNoProjectMessage>
        </PageContent>
      </GlobalSelectionHeader>);
    };
    return OrganizationUserFeedback;
}(AsyncView));
export default withOrganization(withProfiler(OrganizationUserFeedback));
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n"])), space(2));
var StyledEventUserFeedback = styled(EventUserFeedback)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: ", " 0 0;\n"], ["\n  margin: ", " 0 0;\n"])), space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map
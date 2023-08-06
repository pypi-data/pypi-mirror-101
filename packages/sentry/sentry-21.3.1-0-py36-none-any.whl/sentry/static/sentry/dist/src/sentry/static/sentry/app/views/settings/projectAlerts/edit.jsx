import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PageHeading from 'app/components/pageHeading';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import BuilderBreadCrumbs from 'app/views/alerts/builder/builderBreadCrumbs';
import IncidentRulesDetails from 'app/views/settings/incidentRules/details';
import IssueEditor from 'app/views/settings/projectAlerts/issueRuleEditor';
var ProjectAlertsEditor = /** @class */ (function (_super) {
    __extends(ProjectAlertsEditor, _super);
    function ProjectAlertsEditor() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            alertType: '',
            ruleName: '',
        };
        _this.handleChangeTitle = function (ruleName) {
            _this.setState({ ruleName: ruleName });
        };
        return _this;
    }
    ProjectAlertsEditor.prototype.getTitle = function () {
        var ruleName = this.state.ruleName;
        var defaultTitle = t('Edit Alert Rule');
        if (!ruleName) {
            return defaultTitle;
        }
        return defaultTitle + ": " + ruleName;
    };
    ProjectAlertsEditor.prototype.render = function () {
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, location = _a.location, organization = _a.organization, project = _a.project;
        var alertType = location.pathname.includes('/alerts/metric-rules/')
            ? 'metric'
            : 'issue';
        return (<SentryDocumentTitle title={this.getTitle()} orgSlug={organization.slug} projectSlug={project.slug}>
        <PageContent>
          <BuilderBreadCrumbs hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} title={this.getTitle()} projectSlug={project.slug}/>
          <StyledPageHeader>
            <PageHeading>{this.getTitle()}</PageHeading>
          </StyledPageHeader>
          {(!hasMetricAlerts || alertType === 'issue') && (<IssueEditor {...this.props} project={project} onChangeTitle={this.handleChangeTitle}/>)}
          {hasMetricAlerts && alertType === 'metric' && (<IncidentRulesDetails {...this.props} project={project} onChangeTitle={this.handleChangeTitle}/>)}
        </PageContent>
      </SentryDocumentTitle>);
    };
    return ProjectAlertsEditor;
}(React.Component));
var StyledPageHeader = styled(PageHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
export default ProjectAlertsEditor;
var templateObject_1;
//# sourceMappingURL=edit.jsx.map
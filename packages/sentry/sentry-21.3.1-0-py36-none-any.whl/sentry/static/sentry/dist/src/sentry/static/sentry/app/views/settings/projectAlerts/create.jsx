import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import PageHeading from 'app/components/pageHeading';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import EventView from 'app/utils/discover/eventView';
import { uniqueId } from 'app/utils/guid';
import BuilderBreadCrumbs from 'app/views/alerts/builder/builderBreadCrumbs';
import { AlertWizardAlertNames, } from 'app/views/alerts/wizard/options';
import { getAlertTypeFromAggregateDataset } from 'app/views/alerts/wizard/utils';
import IncidentRulesCreate from 'app/views/settings/incidentRules/create';
import IssueRuleEditor from 'app/views/settings/projectAlerts/issueRuleEditor';
import AlertTypeChooser from './alertTypeChooser';
var Create = /** @class */ (function (_super) {
    __extends(Create, _super);
    function Create() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: undefined,
            alertType: _this.props.location.pathname.includes('/alerts/rules/')
                ? 'issue'
                : _this.props.location.pathname.includes('/alerts/metric-rules/')
                    ? 'metric'
                    : null,
        };
        /** Used to track analytics within one visit to the creation page */
        _this.sessionId = uniqueId();
        _this.handleChangeAlertType = function (alertType) {
            // alertType should be `issue` or `metric`
            _this.setState({ alertType: alertType });
        };
        return _this;
    }
    Create.prototype.componentDidMount = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, project = _a.project;
        trackAnalyticsEvent({
            eventKey: 'new_alert_rule.viewed',
            eventName: 'New Alert Rule: Viewed',
            organization_id: organization.id,
            project_id: project.id,
            session_id: this.sessionId,
        });
        if (location === null || location === void 0 ? void 0 : location.query) {
            var query = location.query;
            var createFromDiscover = query.createFromDiscover, createFromWizard = query.createFromWizard;
            if (createFromDiscover) {
                var eventView = EventView.fromLocation(location);
                // eslint-disable-next-line react/no-did-mount-set-state
                this.setState({ alertType: 'metric', eventView: eventView });
            }
            else if (createFromWizard) {
                var aggregate = query.aggregate, dataset = query.dataset, eventTypes = query.eventTypes;
                if (aggregate && dataset && eventTypes) {
                    // eslint-disable-next-line react/no-did-mount-set-state
                    this.setState({
                        alertType: 'metric',
                        wizardTemplate: { aggregate: aggregate, dataset: dataset, eventTypes: eventTypes },
                    });
                }
                else {
                    // eslint-disable-next-line react/no-did-mount-set-state
                    this.setState({
                        alertType: 'issue',
                    });
                }
            }
        }
    };
    Create.prototype.render = function () {
        var _a;
        var _b = this.props, hasMetricAlerts = _b.hasMetricAlerts, organization = _b.organization, project = _b.project, projectId = _b.params.projectId, location = _b.location;
        var _c = this.state, alertType = _c.alertType, eventView = _c.eventView, wizardTemplate = _c.wizardTemplate;
        var hasWizard = organization.features.includes('alert-wizard');
        var shouldShowAlertTypeChooser = hasMetricAlerts && !hasWizard;
        var wizardAlertType;
        if ((_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.createFromWizard) {
            wizardAlertType = wizardTemplate
                ? getAlertTypeFromAggregateDataset(wizardTemplate)
                : 'issues';
        }
        var title = t('New Alert Rule');
        return (<React.Fragment>
        <SentryDocumentTitle title={title} projectSlug={projectId}/>
        <PageContent>
          <BuilderBreadCrumbs hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} alertName={wizardAlertType && AlertWizardAlertNames[wizardAlertType]} title={wizardAlertType ? t('Create Alert Rule') : title} projectSlug={projectId}/>
          <StyledPageHeader>
            <PageHeading>
              {wizardAlertType ? t('Set Alert Conditions') : title}
            </PageHeading>
          </StyledPageHeader>
          {shouldShowAlertTypeChooser && (<AlertTypeChooser organization={organization} selected={alertType} onChange={this.handleChangeAlertType}/>)}

          {(!hasMetricAlerts || alertType === 'issue') && (<IssueRuleEditor {...this.props} project={project}/>)}

          {hasMetricAlerts && alertType === 'metric' && (<IncidentRulesCreate {...this.props} eventView={eventView} wizardTemplate={wizardTemplate} sessionId={this.sessionId} project={project}/>)}
        </PageContent>
      </React.Fragment>);
    };
    return Create;
}(React.Component));
var StyledPageHeader = styled(PageHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
export default Create;
var templateObject_1;
//# sourceMappingURL=create.jsx.map
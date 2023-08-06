import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import Badge from 'app/components/badge';
import CreateAlertButton from 'app/components/createAlertButton';
import ExternalLink from 'app/components/links/externalLink';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import PageHeading from 'app/components/pageHeading';
import { Panel, PanelBody } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent, PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import BuilderBreadCrumbs from 'app/views/alerts/builder/builderBreadCrumbs';
import { Dataset } from 'app/views/settings/incidentRules/types';
import { AlertWizardAlertNames, AlertWizardOptions, AlertWizardPanelContent, AlertWizardRuleTemplates, WebVitalAlertTypes, } from './options';
import RadioPanelGroup from './radioPanelGroup';
var AlertWizard = /** @class */ (function (_super) {
    __extends(AlertWizard, _super);
    function AlertWizard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            alertOption: null,
        };
        _this.handleChangeAlertOption = function (alertOption) {
            _this.setState({ alertOption: alertOption });
        };
        return _this;
    }
    AlertWizard.prototype.renderCreateAlertButton = function () {
        var _a;
        var _b = this.props, organization = _b.organization, project = _b.project, location = _b.location;
        var alertOption = this.state.alertOption;
        var metricRuleTemplate = alertOption && AlertWizardRuleTemplates[alertOption];
        var disabled = !organization.features.includes('performance-view') &&
            (metricRuleTemplate === null || metricRuleTemplate === void 0 ? void 0 : metricRuleTemplate.dataset) === Dataset.TRANSACTIONS;
        var to = {
            pathname: "/organizations/" + organization.slug + "/alerts/" + project.slug + "/new/",
            query: __assign(__assign({}, (metricRuleTemplate && metricRuleTemplate)), { createFromWizard: true, referrer: (_a = location === null || location === void 0 ? void 0 : location.query) === null || _a === void 0 ? void 0 : _a.referrer }),
        };
        return (<CreateAlertButton organization={organization} projectSlug={project.slug} priority="primary" to={to} disabled={disabled}/>);
    };
    AlertWizard.prototype.render = function () {
        var _this = this;
        var _a = this.props, hasMetricAlerts = _a.hasMetricAlerts, organization = _a.organization, projectId = _a.params.projectId;
        var alertOption = this.state.alertOption;
        var title = t('Alert Creation Wizard');
        var panelContent = alertOption && AlertWizardPanelContent[alertOption];
        return (<React.Fragment>
        <SentryDocumentTitle title={title} projectSlug={projectId}/>
        <PageContent>
          <Feature features={['organizations:alert-wizard']}>
            <BuilderBreadCrumbs hasMetricAlerts={hasMetricAlerts} orgSlug={organization.slug} projectSlug={projectId} title={t('Create Alert Rule')}/>
            <StyledPageHeader>
              <PageHeading>{t('What do you want to alert on?')}</PageHeading>
            </StyledPageHeader>
            <Heading>{t('Errors')}</Heading>
            <WizardBody>
              <WizardOptions>
                {AlertWizardOptions.map(function (_a, i) {
                var categoryHeading = _a.categoryHeading, options = _a.options;
                return (<OptionsWrapper key={categoryHeading}>
                    {i > 0 && <Heading>{categoryHeading}</Heading>}
                    <RadioPanelGroup choices={options.map(function (alertType) {
                        return __spreadArray([
                            alertType,
                            AlertWizardAlertNames[alertType]
                        ], __read((WebVitalAlertTypes.has(alertType)
                            ? [<StyledBadge key={alertType} text={t('Web Vital')}/>]
                            : [])));
                    })} onChange={_this.handleChangeAlertOption} value={alertOption} label="alert-option"/>
                  </OptionsWrapper>);
            })}
              </WizardOptions>
              <WizardPanel visible={!!panelContent && !!alertOption}>
                {panelContent && alertOption && (<WizardPanelBody>
                    <PageHeading>{AlertWizardAlertNames[alertOption]}</PageHeading>
                    <PanelDescription>
                      {panelContent.description}{' '}
                      {panelContent.docsLink && (<ExternalLink href={panelContent.docsLink}>
                          {t('Learn more')}
                        </ExternalLink>)}
                    </PanelDescription>
                    <Placeholder height="250px"/>
                    <ExampleHeader>{t('Examples')}</ExampleHeader>
                    <List symbol="bullet">
                      {panelContent.examples.map(function (example, i) { return (<ExampleItem key={i}>{example}</ExampleItem>); })}
                    </List>
                  </WizardPanelBody>)}
                {this.renderCreateAlertButton()}
              </WizardPanel>
            </WizardBody>
          </Feature>
        </PageContent>
      </React.Fragment>);
    };
    return AlertWizard;
}(React.Component));
var StyledPageHeader = styled(PageHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
var Heading = styled('h1')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: normal;\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: normal;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(1));
var WizardBody = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var WizardOptions = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 3;\n  margin-right: ", ";\n"], ["\n  flex: 3;\n  margin-right: ", ";\n"])), space(4));
var StyledBadge = styled(Badge)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n"], ["\n  color: ", ";\n  font-weight: normal;\n"])), function (p) { return p.theme.textColor; });
var WizardPanel = styled(Panel)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  padding: ", ";\n  flex: 5;\n  display: flex;\n  ", ";\n  flex-direction: column;\n  align-items: start;\n  align-self: flex-start;\n"], ["\n  padding: ", ";\n  flex: 5;\n  display: flex;\n  ", ";\n  flex-direction: column;\n  align-items: start;\n  align-self: flex-start;\n"])), space(3), function (p) { return !p.visible && 'visibility: hidden'; });
var WizardPanelBody = styled(PanelBody)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  flex: 1;\n"], ["\n  margin-bottom: ", ";\n  flex: 1;\n"])), space(2));
var PanelDescription = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  color: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.subText; }, space(2));
var ExampleHeader = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  margin: ", " 0;\n  font-size: ", ";\n"], ["\n  margin: ", " 0;\n  font-size: ", ";\n"])), space(2), function (p) { return p.theme.fontSizeLarge; });
var ExampleItem = styled(ListItem)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var OptionsWrapper = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(4));
export default AlertWizard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=index.jsx.map
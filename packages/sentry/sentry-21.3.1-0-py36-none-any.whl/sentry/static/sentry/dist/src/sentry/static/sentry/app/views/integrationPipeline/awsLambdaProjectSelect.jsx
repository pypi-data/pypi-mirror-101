import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Observer } from 'mobx-react';
import * as qs from 'query-string';
import { addLoadingMessage } from 'app/actionCreators/indicator';
import Alert from 'app/components/alert';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { t } from 'app/locale';
import space from 'app/styles/space';
import Form from 'app/views/settings/components/forms/form';
import FormModel from 'app/views/settings/components/forms/model';
import SentryProjectSelectorField from 'app/views/settings/components/forms/sentryProjectSelectorField';
import FooterWithButtons from './components/footerWithButtons';
import HeaderWithHelp from './components/headerWithHelp';
var AwsLambdaProjectSelect = /** @class */ (function (_super) {
    __extends(AwsLambdaProjectSelect, _super);
    function AwsLambdaProjectSelect() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.model = new FormModel();
        _this.handleSubmit = function (e) {
            e.preventDefault();
            var data = _this.model.getData();
            addLoadingMessage(t('Submitting\u2026'));
            _this.model.setFormSaving();
            var origin = window.location.origin;
            // redirect to the extensions endpoint with the form fields as query params
            // this is needed so we don't restart the pipeline loading from the original
            // OrganizationIntegrationSetupView route
            var newUrl = origin + "/extensions/aws_lambda/setup/?" + qs.stringify(data);
            window.location.assign(newUrl);
        };
        return _this;
    }
    AwsLambdaProjectSelect.prototype.render = function () {
        var _this = this;
        var projects = this.props.projects;
        // TODO: Add logic if no projects
        return (<React.Fragment>
        <HeaderWithHelp docsUrl="https://docs.sentry.io/product/integrations/aws-lambda/"/>
        <StyledList symbol="colored-numeric">
          <React.Fragment />
          <ListItem>
            <h3>{t('Select a project for your AWS Lambdas')}</h3>
            <Form model={this.model} hideFooter>
              <StyledSentryProjectSelectorField placeholder={t('Select a project')} name="projectId" projects={projects} inline={false} hasControlState flexibleControlStateSize stacked/>
              <Alert type="info">
                {t('Currently only supports Node and Python Lambda functions')}
              </Alert>
            </Form>
          </ListItem>
        </StyledList>
        <Observer>
          {function () { return (<FooterWithButtons buttonText={t('Next')} onClick={_this.handleSubmit} disabled={_this.model.isSaving || !_this.model.getValue('projectId')}/>); }}
        </Observer>
      </React.Fragment>);
    };
    return AwsLambdaProjectSelect;
}(React.Component));
export default AwsLambdaProjectSelect;
var StyledList = styled(List)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 100px 50px 50px 50px;\n"], ["\n  padding: 100px 50px 50px 50px;\n"])));
var StyledSentryProjectSelectorField = styled(SentryProjectSelectorField)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: 0 0 ", " 0;\n"], ["\n  padding: 0 0 ", " 0;\n"])), space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=awsLambdaProjectSelect.jsx.map
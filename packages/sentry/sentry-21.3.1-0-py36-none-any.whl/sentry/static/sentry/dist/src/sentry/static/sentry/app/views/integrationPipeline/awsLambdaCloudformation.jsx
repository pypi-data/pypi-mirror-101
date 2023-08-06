import { __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';
import * as qs from 'query-string';
import { addErrorMessage, addLoadingMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/actions/button';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import { t } from 'app/locale';
import { uniqueId } from 'app/utils/guid';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import SelectField from 'app/views/settings/components/forms/selectField';
import TextField from 'app/views/settings/components/forms/textField';
import FooterWithButtons from './components/footerWithButtons';
import HeaderWithHelp from './components/headerWithHelp';
// let the browser generate and store the external ID
// this way the same user always has the same external ID if they restart the pipeline
var ID_NAME = 'AWS_EXTERNAL_ID';
var getAwsExternalId = function () {
    var awsExternalId = window.localStorage.getItem(ID_NAME);
    if (!awsExternalId) {
        awsExternalId = uniqueId();
        window.localStorage.setItem(ID_NAME, awsExternalId);
    }
    return awsExternalId;
};
var accountNumberRegex = /^\d{12}$/;
var testAccountNumber = function (arn) { return accountNumberRegex.test(arn); };
var AwsLambdaCloudformation = /** @class */ (function (_super) {
    __extends(AwsLambdaCloudformation, _super);
    function AwsLambdaCloudformation() {
        var _a;
        var _this = _super.apply(this, __spreadArray([], __read(arguments))) || this;
        _this.state = {
            accountNumber: _this.props.accountNumber,
            region: _this.props.region,
            awsExternalId: (_a = _this.props.awsExternalId) !== null && _a !== void 0 ? _a : getAwsExternalId(),
            showInputs: !!_this.props.awsExternalId,
        };
        _this.handleSubmit = function (e) {
            _this.setState({ submitting: true });
            e.preventDefault();
            //use the external ID from the form on on the submission
            var _a = _this.state, accountNumber = _a.accountNumber, region = _a.region, awsExternalId = _a.awsExternalId;
            var data = {
                accountNumber: accountNumber,
                region: region,
                awsExternalId: awsExternalId,
            };
            addLoadingMessage(t('Submitting\u2026'));
            var origin = window.location.origin;
            // redirect to the extensions endpoint with the form fields as query params
            // this is needed so we don't restart the pipeline loading from the original
            // OrganizationIntegrationSetupView route
            var newUrl = origin + "/extensions/aws_lambda/setup/?" + qs.stringify(data);
            window.location.assign(newUrl);
        };
        _this.validateAccountNumber = function (value) {
            // validate the account number
            var accountNumberError = '';
            if (!value) {
                accountNumberError = t('Account number required');
            }
            else if (!testAccountNumber(value)) {
                accountNumberError = t('Invalid account number');
            }
            _this.setState({ accountNumberError: accountNumberError });
        };
        _this.handleChangeArn = function (accountNumber) {
            _this.debouncedTrackValueChanged('accountNumber');
            // reset the error if we ever get a valid account number
            if (testAccountNumber(accountNumber)) {
                _this.setState({ accountNumberError: '' });
            }
            _this.setState({ accountNumber: accountNumber });
        };
        _this.hanldeChangeRegion = function (region) {
            _this.debouncedTrackValueChanged('region');
            _this.setState({ region: region });
        };
        _this.handleChangeExternalId = function (awsExternalId) {
            _this.debouncedTrackValueChanged('awsExternalId');
            awsExternalId = awsExternalId.trim();
            _this.setState({ awsExternalId: awsExternalId });
        };
        _this.handleChangeShowInputs = function () {
            _this.setState({ showInputs: true });
            trackIntegrationEvent('integrations.installation_input_value_changed', {
                integration: 'aws_lambda',
                integration_type: 'first_party',
                field_name: 'showInputs',
            }, _this.props.organization);
        };
        //debounce so we don't send a request on every input change
        _this.debouncedTrackValueChanged = debounce(function (fieldName) {
            trackIntegrationEvent('integrations.installation_input_value_changed', {
                integration: 'aws_lambda',
                integration_type: 'first_party',
                field_name: fieldName,
            }, _this.props.organization);
        }, 200);
        _this.trackOpenCloudFormation = function () {
            trackIntegrationEvent('integrations.cloudformation_link_clicked', {
                integration: 'aws_lambda',
                integration_type: 'first_party',
            }, _this.props.organization);
        };
        _this.render = function () {
            var initialStepNumber = _this.props.initialStepNumber;
            var _a = _this.state, accountNumber = _a.accountNumber, region = _a.region, accountNumberError = _a.accountNumberError, submitting = _a.submitting, awsExternalId = _a.awsExternalId, showInputs = _a.showInputs;
            return (<React.Fragment>
        <HeaderWithHelp docsUrl="https://docs.sentry.io/product/integrations/aws-lambda/"/>
        <StyledList symbol="colored-numeric" initialCounterValue={initialStepNumber}>
          <ListItem>
            <h3>{t("Add Sentry's CloudFormation")}</h3>
            <StyledButton priority="primary" onClick={_this.trackOpenCloudFormation} external href={_this.cloudformationUrl}>
              {t('Go to AWS')}
            </StyledButton>
            {!showInputs && (<React.Fragment>
                <p>
                  {t("Once you've created Sentry's CloudFormation stack (or if you already have one) press the button below to continue.")}
                </p>
                <Button name="showInputs" onClick={_this.handleChangeShowInputs}>
                  {t("I've created the stack")}
                </Button>
              </React.Fragment>)}
          </ListItem>
          {showInputs ? (<ListItem>
              <h3>{t('Add AWS Account Information')}</h3>
              <TextField name="accountNumber" value={accountNumber} onChange={_this.handleChangeArn} onBlur={_this.validateAccountNumber} error={accountNumberError} inline={false} stacked label={t('AWS Account Number')} showHelpInTooltip help={t('Your account number can be found on the right side of the header in AWS')}/>
              <SelectField name="region" value={region} onChange={_this.hanldeChangeRegion} options={_this.regionOptions} allowClear={false} inline={false} stacked label={t('AWS Region')} showHelpInTooltip help={t('Your current region can be found on the right side of the header in AWS')}/>
              <TextField name="awsExternalId" value={awsExternalId} onChange={_this.handleChangeExternalId} inline={false} stacked error={awsExternalId ? '' : t('External ID Required')} label={t('External ID')} showHelpInTooltip help={t('Do not edit unless you are copying from a previously created CloudFormation stack')}/>
            </ListItem>) : (<React.Fragment />)}
        </StyledList>
        <FooterWithButtons buttonText={t('Next')} onClick={_this.handleSubmit} disabled={submitting || !_this.formValid}/>
      </React.Fragment>);
        };
        return _this;
    }
    AwsLambdaCloudformation.prototype.componentDidMount = function () {
        // show the error if we have it
        var error = this.props.error;
        if (error) {
            addErrorMessage(error, { duration: 10000 });
        }
    };
    Object.defineProperty(AwsLambdaCloudformation.prototype, "initialData", {
        get: function () {
            var _a = this.props, region = _a.region, accountNumber = _a.accountNumber;
            var awsExternalId = this.state.awsExternalId;
            return {
                awsExternalId: awsExternalId,
                region: region,
                accountNumber: accountNumber,
            };
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaCloudformation.prototype, "cloudformationUrl", {
        get: function () {
            // generarate the cloudformation URL using the params we get from the server
            // and the external id we generate
            var _a = this.props, baseCloudformationUrl = _a.baseCloudformationUrl, templateUrl = _a.templateUrl, stackName = _a.stackName;
            //always us the generated AWS External ID in local storage
            var awsExternalId = getAwsExternalId();
            var query = qs.stringify({
                templateURL: templateUrl,
                stackName: stackName,
                param_ExternalId: awsExternalId,
            });
            return baseCloudformationUrl + "?" + query;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaCloudformation.prototype, "regionOptions", {
        get: function () {
            return this.props.regionList.map(function (region) { return ({ value: region, label: region }); });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaCloudformation.prototype, "formValid", {
        get: function () {
            var _a = this.state, accountNumber = _a.accountNumber, region = _a.region, awsExternalId = _a.awsExternalId;
            return !!region && testAccountNumber(accountNumber || '') && !!awsExternalId;
        },
        enumerable: false,
        configurable: true
    });
    return AwsLambdaCloudformation;
}(React.Component));
export default AwsLambdaCloudformation;
var StyledList = styled(List)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 100px 50px 50px 50px;\n"], ["\n  padding: 100px 50px 50px 50px;\n"])));
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: 20px;\n"], ["\n  margin-bottom: 20px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=awsLambdaCloudformation.jsx.map
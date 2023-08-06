import { __decorate, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import reduce from 'lodash/reduce';
import { computed } from 'mobx';
import { Observer } from 'mobx-react';
import List from 'app/components/list';
import ListItem from 'app/components/list/listItem';
import LoadingIndicator from 'app/components/loadingIndicator';
import { PanelHeader } from 'app/components/panels';
import Switch from 'app/components/switchButton';
import Tooltip from 'app/components/tooltip';
import { t, tn } from 'app/locale';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import FormModel from 'app/views/settings/components/forms/model';
import FooterWithButtons from './components/footerWithButtons';
import HeaderWithHelp from './components/headerWithHelp';
var LAMBDA_COUNT_THRESHOLD = 10;
var getLabel = function (func) { return func.FunctionName; };
var AwsLambdaFunctionSelect = /** @class */ (function (_super) {
    __extends(AwsLambdaFunctionSelect, _super);
    function AwsLambdaFunctionSelect() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            submitting: false,
        };
        _this.model = new FormModel({ apiOptions: { baseUrl: window.location.origin } });
        _this.handleSubmit = function () {
            _this.model.saveForm();
            _this.setState({ submitting: true });
        };
        _this.handleToggle = function () {
            var newState = !_this.toggleAllState;
            _this.lambdaFunctions.forEach(function (lambda) {
                _this.model.setValue(lambda.FunctionName, newState, { quiet: true });
            });
        };
        _this.renderWhatWeFound = function () {
            var count = _this.lambdaFunctions.length;
            return (<h4>
        {tn('We found %s function with a Node or Python runtime', 'We found %s functions with Node or Python runtimes', count)}
      </h4>);
        };
        _this.renderLoadingScreeen = function () {
            var count = _this.enabledCount;
            var text = count > LAMBDA_COUNT_THRESHOLD
                ? t('This might take a while\u2026', count)
                : t('This might take a sec\u2026');
            return (<LoadingWrapper>
        <StyledLoadingIndicator />
        <h4>{t('Adding Sentry to %s functions', count)}</h4>
        {text}
      </LoadingWrapper>);
        };
        _this.renderCore = function () {
            var initialStepNumber = _this.props.initialStepNumber;
            var model = _this.model;
            var FormHeader = (<StyledPanelHeader>
        {t('Lambda Functions')}
        <SwitchHolder>
          <Observer>
            {function () { return (<Tooltip title={_this.toggleAllState ? t('Disable All') : t('Enable All')} position="left">
                <StyledSwitch size="lg" name="toggleAll" toggle={_this.handleToggle} isActive={_this.toggleAllState}/>
              </Tooltip>); }}
          </Observer>
        </SwitchHolder>
      </StyledPanelHeader>);
            var formFields = {
                fields: _this.lambdaFunctions.map(function (func) {
                    return {
                        name: func.FunctionName,
                        type: 'boolean',
                        required: false,
                        label: getLabel(func),
                        alignRight: true,
                    };
                }),
            };
            return (<List symbol="colored-numeric" initialCounterValue={initialStepNumber}>
        <ListItem>
          <Header>{_this.renderWhatWeFound()}</Header>
          {t('Decide which functions you would like to enable for Sentry monitoring')}
          <StyledForm initialData={_this.initialData} skipPreventDefault model={model} apiEndpoint="/extensions/aws_lambda/setup/" hideFooter>
            <JsonForm renderHeader={function () { return FormHeader; }} forms={[formFields]}/>
          </StyledForm>
        </ListItem>
        <React.Fragment />
      </List>);
        };
        _this.render = function () {
            return (<React.Fragment>
        <HeaderWithHelp docsUrl="https://docs.sentry.io/product/integrations/aws-lambda/"/>
        <Wrapper>
          {_this.state.submitting ? _this.renderLoadingScreeen() : _this.renderCore()}
        </Wrapper>
        <Observer>
          {function () { return (<FooterWithButtons buttonText={t('Finish Setup')} onClick={_this.handleSubmit} disabled={_this.model.isError || _this.model.isSaving}/>); }}
        </Observer>
      </React.Fragment>);
        };
        return _this;
    }
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "initialData", {
        get: function () {
            var lambdaFunctions = this.props.lambdaFunctions;
            var initialData = lambdaFunctions.reduce(function (accum, func) {
                accum[func.FunctionName] = true;
                return accum;
            }, {});
            return initialData;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "lambdaFunctions", {
        get: function () {
            return this.props.lambdaFunctions.sort(function (a, b) {
                return getLabel(a).toLowerCase() < getLabel(b).toLowerCase() ? -1 : 1;
            });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "enabledCount", {
        get: function () {
            var data = this.model.getTransformedData();
            return reduce(data, function (acc, val) { return (val ? acc + 1 : acc); }, 0);
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AwsLambdaFunctionSelect.prototype, "toggleAllState", {
        get: function () {
            //check if any of the lambda functions have a falsy value
            //no falsy values means everything is enabled
            return Object.values(this.model.getData()).every(function (val) { return val; });
        },
        enumerable: false,
        configurable: true
    });
    __decorate([
        computed
    ], AwsLambdaFunctionSelect.prototype, "toggleAllState", null);
    return AwsLambdaFunctionSelect;
}(React.Component));
export default AwsLambdaFunctionSelect;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 100px 50px 50px 50px;\n"], ["\n  padding: 100px 50px 50px 50px;\n"])));
// TODO(ts): Understand why styled is not correctly inheriting props here
var StyledForm = styled(Form)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: 10px;\n"], ["\n  margin-top: 10px;\n"])));
var Header = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  text-align: left;\n  margin-bottom: 10px;\n"], ["\n  text-align: left;\n  margin-bottom: 10px;\n"])));
var LoadingWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding: 50px;\n  text-align: center;\n"], ["\n  padding: 50px;\n  text-align: center;\n"])));
var StyledLoadingIndicator = styled(LoadingIndicator)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var SwitchHolder = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var StyledSwitch = styled(Switch)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin: auto;\n"], ["\n  margin: auto;\n"])));
//padding is based on fom control width
var StyledPanelHeader = styled(PanelHeader)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  padding-right: 36px;\n"], ["\n  padding-right: 36px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=awsLambdaFunctionSelect.jsx.map
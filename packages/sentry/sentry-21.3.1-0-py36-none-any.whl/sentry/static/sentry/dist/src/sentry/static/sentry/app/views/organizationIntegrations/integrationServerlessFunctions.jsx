import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
// eslint-disable-next-line simple-import-sort/imports
import React from 'react';
import styled from '@emotion/styled';
import AsyncComponent from 'app/components/asyncComponent';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import space from 'app/styles/space';
import Alert from 'app/components/alert';
import withOrganization from 'app/utils/withOrganization';
import { t } from 'app/locale';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import IntegrationServerlessRow from './integrationServerlessRow';
var IntegrationServerlessFunctions = /** @class */ (function (_super) {
    __extends(IntegrationServerlessFunctions, _super);
    function IntegrationServerlessFunctions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFunctionUpdate = function (serverlessFunctionUpdate, index) {
            var serverlessFunctions = __spreadArray([], __read(_this.serverlessFunctions));
            var serverlessFunction = __assign(__assign({}, serverlessFunctions[index]), serverlessFunctionUpdate);
            serverlessFunctions[index] = serverlessFunction;
            _this.setState({ serverlessFunctions: serverlessFunctions });
        };
        return _this;
    }
    IntegrationServerlessFunctions.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { serverlessFunctions: [] });
    };
    IntegrationServerlessFunctions.prototype.getEndpoints = function () {
        var orgSlug = this.props.organization.slug;
        return [
            [
                'serverlessFunctions',
                "/organizations/" + orgSlug + "/integrations/" + this.props.integration.id + "/serverless-functions/",
            ],
        ];
    };
    Object.defineProperty(IntegrationServerlessFunctions.prototype, "serverlessFunctions", {
        get: function () {
            return this.state.serverlessFunctions;
        },
        enumerable: false,
        configurable: true
    });
    IntegrationServerlessFunctions.prototype.onLoadAllEndpointsSuccess = function () {
        trackIntegrationEvent('integrations.serverless_functions_viewed', {
            integration: this.props.integration.provider.key,
            integration_type: 'first_party',
            num_functions: this.serverlessFunctions.length,
        }, this.props.organization);
    };
    IntegrationServerlessFunctions.prototype.renderBody = function () {
        var _this = this;
        return (<React.Fragment>
        <Alert type="info">
          {t('Manage your AWS Lambda functions below. Only Node and Python runtimes are currently supported.')}
        </Alert>
        <Panel>
          <StyledPanelHeader disablePadding hasButtons>
            <NameHeader>{t('Name')}</NameHeader>
            <LayerStatusWrapper>{t('Layer Status')}</LayerStatusWrapper>
            <EnableHeader>{t('Enabled')}</EnableHeader>
          </StyledPanelHeader>
          <StyledPanelBody>
            {this.serverlessFunctions.map(function (serverlessFunction, i) { return (<IntegrationServerlessRow key={serverlessFunction.name} serverlessFunction={serverlessFunction} onUpdateFunction={function (update) {
                    return _this.handleFunctionUpdate(update, i);
                }} {..._this.props}/>); })}
          </StyledPanelBody>
        </Panel>
      </React.Fragment>);
    };
    return IntegrationServerlessFunctions;
}(AsyncComponent));
export default withOrganization(IntegrationServerlessFunctions);
var StyledPanelHeader = styled(PanelHeader)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr;\n  grid-template-areas: 'function-name layer-status enable-switch';\n"], ["\n  padding: ", ";\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr;\n  grid-template-areas: 'function-name layer-status enable-switch';\n"])), space(2), space(1));
var HeaderText = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var StyledPanelBody = styled(PanelBody)(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
var NameHeader = styled(HeaderText)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-area: function-name;\n"], ["\n  grid-area: function-name;\n"])));
var LayerStatusWrapper = styled(HeaderText)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-area: layer-status;\n"], ["\n  grid-area: layer-status;\n"])));
var EnableHeader = styled(HeaderText)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  grid-area: enable-switch;\n"], ["\n  grid-area: enable-switch;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=integrationServerlessFunctions.jsx.map
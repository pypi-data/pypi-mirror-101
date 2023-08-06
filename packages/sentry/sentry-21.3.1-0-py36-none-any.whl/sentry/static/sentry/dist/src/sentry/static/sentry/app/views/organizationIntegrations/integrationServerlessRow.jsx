import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import Switch from 'app/components/switchButton';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackIntegrationEvent } from 'app/utils/integrationUtil';
import withApi from 'app/utils/withApi';
var IntegrationServerlessRow = /** @class */ (function (_super) {
    __extends(IntegrationServerlessRow, _super);
    function IntegrationServerlessRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            submitting: false,
        };
        _this.recordAction = function (action) {
            trackIntegrationEvent('integrations.serverless_function_action', {
                integration: _this.props.integration.provider.key,
                integration_type: 'first_party',
                action: action,
            }, _this.props.organization);
        };
        _this.toggleEnable = function () { return __awaiter(_this, void 0, void 0, function () {
            var serverlessFunction, action, data, resp, err_1;
            var _a, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        serverlessFunction = this.props.serverlessFunction;
                        action = this.enabled ? 'disable' : 'enable';
                        data = {
                            action: action,
                            target: serverlessFunction.name,
                        };
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        addLoadingMessage();
                        this.setState({ submitting: true });
                        //optimistically update enable state
                        this.props.onUpdateFunction({ enabled: !this.enabled });
                        this.recordAction(action);
                        return [4 /*yield*/, this.props.api.requestPromise(this.endpoint, {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        resp = _c.sent();
                        //update remaining after response
                        this.props.onUpdateFunction(resp);
                        addSuccessMessage(t('Success'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _c.sent();
                        //restore original on failure
                        this.props.onUpdateFunction(serverlessFunction);
                        addErrorMessage((_b = (_a = err_1.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : t('Error occurred'));
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ submitting: false });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.updateVersion = function () { return __awaiter(_this, void 0, void 0, function () {
            var serverlessFunction, data, resp, err_2;
            var _a, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        serverlessFunction = this.props.serverlessFunction;
                        data = {
                            action: 'updateVersion',
                            target: serverlessFunction.name,
                        };
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        this.setState({ submitting: true });
                        // don't know the latest version but at least optimistically remove the update button
                        this.props.onUpdateFunction({ outOfDate: false });
                        addLoadingMessage();
                        this.recordAction('updateVersion');
                        return [4 /*yield*/, this.props.api.requestPromise(this.endpoint, {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        resp = _c.sent();
                        //update remaining after response
                        this.props.onUpdateFunction(resp);
                        addSuccessMessage(t('Success'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        //restore original on failure
                        this.props.onUpdateFunction(serverlessFunction);
                        addErrorMessage((_b = (_a = err_2.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : t('Error occurred'));
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ submitting: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    Object.defineProperty(IntegrationServerlessRow.prototype, "enabled", {
        get: function () {
            return this.props.serverlessFunction.enabled;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationServerlessRow.prototype, "endpoint", {
        get: function () {
            var orgSlug = this.props.organization.slug;
            return "/organizations/" + orgSlug + "/integrations/" + this.props.integration.id + "/serverless-functions/";
        },
        enumerable: false,
        configurable: true
    });
    IntegrationServerlessRow.prototype.renderLayerStatus = function () {
        var serverlessFunction = this.props.serverlessFunction;
        if (!serverlessFunction.outOfDate) {
            return this.enabled ? t('Latest') : t('Disabled');
        }
        return (<UpdateButton size="small" priority="primary" onClick={this.updateVersion}>
        {t('Update')}
      </UpdateButton>);
    };
    IntegrationServerlessRow.prototype.render = function () {
        var serverlessFunction = this.props.serverlessFunction;
        var version = serverlessFunction.version;
        //during optimistic update, we might be enabled without a version
        var versionText = this.enabled && version > 0 ? (<React.Fragment>&nbsp;|&nbsp;v{version}</React.Fragment>) : null;
        return (<Item>
        <NameWrapper>
          <NameRuntimeVersionWrapper>
            <Name>{serverlessFunction.name}</Name>
            <RuntimeAndVersion>
              <DetailWrapper>{serverlessFunction.runtime}</DetailWrapper>
              <DetailWrapper>{versionText}</DetailWrapper>
            </RuntimeAndVersion>
          </NameRuntimeVersionWrapper>
        </NameWrapper>
        <LayerStatusWrapper>{this.renderLayerStatus()}</LayerStatusWrapper>
        <StyledSwitch isActive={this.enabled} isDisabled={this.state.submitting} size="sm" toggle={this.toggleEnable}/>
      </Item>);
    };
    return IntegrationServerlessRow;
}(React.Component));
export default withApi(IntegrationServerlessRow);
var Item = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr;\n  grid-template-areas: 'function-name layer-status enable-switch';\n"], ["\n  padding: ", ";\n\n  &:not(:last-child) {\n    border-bottom: 1px solid ", ";\n  }\n\n  display: grid;\n  grid-column-gap: ", ";\n  align-items: center;\n  grid-template-columns: 2fr 1fr 0.5fr;\n  grid-template-areas: 'function-name layer-status enable-switch';\n"])), space(2), function (p) { return p.theme.innerBorder; }, space(1));
var ItemWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 32px;\n  vertical-align: middle;\n  display: flex;\n  align-items: center;\n"], ["\n  height: 32px;\n  vertical-align: middle;\n  display: flex;\n  align-items: center;\n"])));
var NameWrapper = styled(ItemWrapper)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-area: function-name;\n"], ["\n  grid-area: function-name;\n"])));
var LayerStatusWrapper = styled(ItemWrapper)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  grid-area: layer-status;\n"], ["\n  grid-area: layer-status;\n"])));
var StyledSwitch = styled(Switch)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-area: enable-switch;\n"], ["\n  grid-area: enable-switch;\n"])));
var UpdateButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject([""], [""])));
var NameRuntimeVersionWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var Name = styled("span")(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space(1));
var RuntimeAndVersion = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  color: ", ";\n"], ["\n  display: flex;\n  flex-direction: row;\n  color: ", ";\n"])), function (p) { return p.theme.gray300; });
var DetailWrapper = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  line-height: 1.2;\n"], ["\n  line-height: 1.2;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=integrationServerlessRow.jsx.map
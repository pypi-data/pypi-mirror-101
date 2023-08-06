import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import styled from '@emotion/styled';
import QRCode from 'qrcode.react';
import { addErrorMessage, addLoadingMessage, addSuccessMessage, } from 'app/actionCreators/indicator';
import { openRecoveryOptions } from 'app/actionCreators/modal';
import { fetchOrganizationByMember } from 'app/actionCreators/organizations';
import Button from 'app/components/button';
import CircleIndicator from 'app/components/circleIndicator';
import { PanelItem } from 'app/components/panels';
import U2fsign from 'app/components/u2f/u2fsign';
import { t } from 'app/locale';
import space from 'app/styles/space';
import getPendingInvite from 'app/utils/getPendingInvite';
import AsyncView from 'app/views/asyncView';
import RemoveConfirm from 'app/views/settings/account/accountSecurity/components/removeConfirm';
import Field from 'app/views/settings/components/forms/field';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import FormModel from 'app/views/settings/components/forms/model';
import TextCopyInput from 'app/views/settings/components/forms/textCopyInput';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
/**
 * Retrieve additional form fields (or modify ones) based on 2fa method
 */
var getFields = function (_a) {
    var authenticator = _a.authenticator, hasSentCode = _a.hasSentCode, sendingCode = _a.sendingCode, onSmsReset = _a.onSmsReset, onU2fTap = _a.onU2fTap;
    var form = authenticator.form;
    if (!form) {
        return null;
    }
    if (authenticator.id === 'totp') {
        return __spreadArray(__spreadArray([
            function () { return (<PanelItem key="qrcode" justifyContent="center" p={2}>
          <StyledQRCode value={authenticator.qrcode} size={228}/>
        </PanelItem>); },
            function () {
                var _a;
                return (<Field key="secret" label={t('Authenticator secret')}>
          <TextCopyInput>{(_a = authenticator.secret) !== null && _a !== void 0 ? _a : ''}</TextCopyInput>
        </Field>);
            }
        ], __read(form)), [
            function () { return (<PanelItem key="confirm" justifyContent="flex-end" p={2}>
          <Button priority="primary" type="submit">
            {t('Confirm')}
          </Button>
        </PanelItem>); },
        ]);
    }
    // Sms Form needs a start over button + confirm button
    // Also inputs being disabled vary based on hasSentCode
    if (authenticator.id === 'sms') {
        // Ideally we would have greater flexibility when rendering footer
        return __spreadArray(__spreadArray([
            __assign(__assign({}, form[0]), { disabled: sendingCode || hasSentCode })
        ], __read((hasSentCode ? [__assign(__assign({}, form[1]), { required: true })] : []))), [
            function () { return (<PanelItem key="sms-footer" justifyContent="flex-end" p={2} pr="36px">
          {hasSentCode && (<Button css={{ marginRight: 6 }} onClick={onSmsReset}>
              {t('Start Over')}
            </Button>)}
          <Button priority="primary" type="submit">
            {hasSentCode ? t('Confirm') : t('Send Code')}
          </Button>
        </PanelItem>); },
        ]);
    }
    // Need to render device name field + U2f component
    if (authenticator.id === 'u2f') {
        var deviceNameField = form.find(function (_a) {
            var name = _a.name;
            return name === 'deviceName';
        });
        return [
            deviceNameField,
            function () { return (<U2fsign key="u2f-enroll" style={{ marginBottom: 0 }} challengeData={authenticator.challenge} displayMode="enroll" onTap={onU2fTap}/>); },
        ];
    }
    return null;
};
/**
 * Renders necessary forms in order to enroll user in 2fa
 */
var AccountSecurityEnroll = /** @class */ (function (_super) {
    __extends(AccountSecurityEnroll, _super);
    function AccountSecurityEnroll() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.formModel = new FormModel();
        _this.pendingInvitation = null;
        // This resets state so that user can re-enter their phone number again
        _this.handleSmsReset = function () { return _this.setState({ hasSentCode: false }, _this.remountComponent); };
        // Handles SMS authenticators
        _this.handleSmsSubmit = function (dataModel) { return __awaiter(_this, void 0, void 0, function () {
            var _a, authenticator, hasSentCode, phone, otp, data, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.state, authenticator = _a.authenticator, hasSentCode = _a.hasSentCode;
                        phone = dataModel.phone, otp = dataModel.otp;
                        // Don't submit if empty
                        if (!phone || !authenticator) {
                            return [2 /*return*/];
                        }
                        data = {
                            phone: phone,
                            // Make sure `otp` is undefined if we are submitting OTP verification
                            // Otherwise API will think that we are on verification step (e.g. after submitting phone)
                            otp: hasSentCode ? otp : undefined,
                            secret: authenticator.secret,
                        };
                        // Only show loading when submitting OTP
                        this.setState({ sendingCode: !hasSentCode });
                        if (!hasSentCode) {
                            addLoadingMessage(t('Sending code to %s...', data.phone));
                        }
                        else {
                            addLoadingMessage(t('Verifying OTP...'));
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.enrollEndpoint, { data: data })];
                    case 2:
                        _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.formModel.resetForm();
                        addErrorMessage(this.state.hasSentCode ? t('Incorrect OTP') : t('Error sending SMS'));
                        this.setState({
                            hasSentCode: false,
                            sendingCode: false,
                        });
                        // Re-mount because we want to fetch a fresh secret
                        this.remountComponent();
                        return [2 /*return*/];
                    case 4:
                        if (!hasSentCode) {
                            // Just successfully finished sending OTP to user
                            this.setState({ hasSentCode: true, sendingCode: false });
                            addSuccessMessage(t('Sent code to %s', data.phone));
                        }
                        else {
                            // OTP was accepted and SMS was added as a 2fa method
                            this.handleEnrollSuccess();
                        }
                        return [2 /*return*/];
                }
            });
        }); };
        // Handle u2f device tap
        _this.handleU2fTap = function (tapData) { return __awaiter(_this, void 0, void 0, function () {
            var data, err_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        data = __assign(__assign({}, tapData), this.formModel.fields.toJS());
                        this.setState({ loading: true });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.enrollEndpoint, { data: data })];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        this.handleEnrollError();
                        return [2 /*return*/];
                    case 4:
                        this.handleEnrollSuccess();
                        return [2 /*return*/];
                }
            });
        }); };
        // Currently only TOTP uses this
        _this.handleTotpSubmit = function (dataModel) { return __awaiter(_this, void 0, void 0, function () {
            var data, err_2;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!this.state.authenticator) {
                            return [2 /*return*/];
                        }
                        data = __assign(__assign({}, (dataModel !== null && dataModel !== void 0 ? dataModel : {})), { secret: this.state.authenticator.secret });
                        this.setState({ loading: true });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.enrollEndpoint, { method: 'POST', data: data })];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _a.sent();
                        this.handleEnrollError();
                        return [2 /*return*/];
                    case 4:
                        this.handleEnrollSuccess();
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubmit = function (data) {
            var _a;
            var id = (_a = _this.state.authenticator) === null || _a === void 0 ? void 0 : _a.id;
            if (id === 'totp') {
                _this.handleTotpSubmit(data);
                return;
            }
            if (id === 'sms') {
                _this.handleSmsSubmit(data);
                return;
            }
        };
        // Removes an authenticator
        _this.handleRemove = function () { return __awaiter(_this, void 0, void 0, function () {
            var authenticator, err_3;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        authenticator = this.state.authenticator;
                        if (!authenticator || !authenticator.authId) {
                            return [2 /*return*/];
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.authenticatorEndpoint, { method: 'DELETE' })];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_3 = _a.sent();
                        addErrorMessage(t('Error removing authenticator'));
                        return [2 /*return*/];
                    case 4:
                        this.props.router.push('/settings/account/security/');
                        addSuccessMessage(t('Authenticator has been removed'));
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AccountSecurityEnroll.prototype.getTitle = function () {
        return t('Security');
    };
    AccountSecurityEnroll.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { hasSentCode: false });
    };
    Object.defineProperty(AccountSecurityEnroll.prototype, "authenticatorEndpoint", {
        get: function () {
            return "/users/me/authenticators/" + this.props.params.authId + "/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AccountSecurityEnroll.prototype, "enrollEndpoint", {
        get: function () {
            return this.authenticatorEndpoint + "enroll/";
        },
        enumerable: false,
        configurable: true
    });
    AccountSecurityEnroll.prototype.getEndpoints = function () {
        var _this = this;
        var errorHandler = function (err) {
            var alreadyEnrolled = err &&
                err.status === 400 &&
                err.responseJSON &&
                err.responseJSON.details === 'Already enrolled';
            if (alreadyEnrolled) {
                _this.props.router.push('/settings/account/security/');
                addErrorMessage(t('Already enrolled'));
            }
            // Allow the endpoint to fail if the user is already enrolled
            return alreadyEnrolled;
        };
        return [['authenticator', this.enrollEndpoint, {}, { allowError: errorHandler }]];
    };
    AccountSecurityEnroll.prototype.componentDidMount = function () {
        this.pendingInvitation = getPendingInvite();
    };
    Object.defineProperty(AccountSecurityEnroll.prototype, "authenticatorName", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.state.authenticator) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Authenticator';
        },
        enumerable: false,
        configurable: true
    });
    // Handler when we successfully add a 2fa device
    AccountSecurityEnroll.prototype.handleEnrollSuccess = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!this.pendingInvitation) return [3 /*break*/, 2];
                        return [4 /*yield*/, fetchOrganizationByMember(this.pendingInvitation.memberId.toString(), {
                                addOrg: true,
                                fetchOrgDetails: true,
                            })];
                    case 1:
                        _a.sent();
                        _a.label = 2;
                    case 2:
                        this.props.router.push('/settings/account/security/');
                        openRecoveryOptions({ authenticatorName: this.authenticatorName });
                        return [2 /*return*/];
                }
            });
        });
    };
    // Handler when we failed to add a 2fa device
    AccountSecurityEnroll.prototype.handleEnrollError = function () {
        this.setState({ loading: false });
        addErrorMessage(t('Error adding %s authenticator', this.authenticatorName));
    };
    AccountSecurityEnroll.prototype.renderBody = function () {
        var _a;
        var _b = this.state, authenticator = _b.authenticator, hasSentCode = _b.hasSentCode, sendingCode = _b.sendingCode;
        if (!authenticator) {
            return null;
        }
        var fields = getFields({
            authenticator: authenticator,
            hasSentCode: hasSentCode,
            sendingCode: sendingCode,
            onSmsReset: this.handleSmsReset,
            onU2fTap: this.handleU2fTap,
        });
        // Attempt to extract `defaultValue` from server generated form fields
        var defaultValues = fields
            ? fields
                .filter(function (field) {
                return typeof field !== 'function' && typeof field.defaultValue !== 'undefined';
            })
                .map(function (field) { return [
                field.name,
                typeof field !== 'function' ? field.defaultValue : '',
            ]; })
                .reduce(function (acc, _a) {
                var _b = __read(_a, 2), name = _b[0], value = _b[1];
                acc[name] = value;
                return acc;
            }, {})
            : {};
        return (<React.Fragment>
        <SettingsPageHeader title={<React.Fragment>
              <span>{authenticator.name}</span>
              <CircleIndicator css={{ marginLeft: 6 }} enabled={authenticator.isEnrolled}/>
            </React.Fragment>} action={authenticator.isEnrolled &&
                authenticator.removeButton && (<RemoveConfirm onConfirm={this.handleRemove}>
                <Button priority="danger">{authenticator.removeButton}</Button>
              </RemoveConfirm>)}/>

        <TextBlock>{authenticator.description}</TextBlock>

        {!!((_a = authenticator.form) === null || _a === void 0 ? void 0 : _a.length) && (<Form model={this.formModel} apiMethod="POST" apiEndpoint={this.authenticatorEndpoint} onSubmit={this.handleSubmit} initialData={__assign(__assign({}, defaultValues), authenticator)} hideFooter>
            <JsonForm forms={[{ title: 'Configuration', fields: fields !== null && fields !== void 0 ? fields : [] }]}/>
          </Form>)}
      </React.Fragment>);
    };
    return AccountSecurityEnroll;
}(AsyncView));
var StyledQRCode = styled(QRCode)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: white;\n  padding: ", ";\n"], ["\n  background: white;\n  padding: ", ";\n"])), space(2));
export default withRouter(AccountSecurityEnroll);
var templateObject_1;
//# sourceMappingURL=accountSecurityEnroll.jsx.map
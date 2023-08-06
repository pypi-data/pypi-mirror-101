import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import u2f from 'u2f-api';
import { t, tct } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
var U2fInterface = /** @class */ (function (_super) {
    __extends(U2fInterface, _super);
    function U2fInterface() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isSupported: null,
            formElement: null,
            challengeElement: null,
            hasBeenTapped: false,
            deviceFailure: null,
            responseElement: null,
        };
        _this.onTryAgain = function () {
            _this.setState({ hasBeenTapped: false, deviceFailure: null }, function () { return void _this.invokeU2fFlow(); });
        };
        _this.bindChallengeElement = function (ref) {
            _this.setState({
                challengeElement: ref,
                formElement: ref && ref.form,
            });
            if (ref) {
                ref.value = JSON.stringify(_this.props.challengeData);
            }
        };
        _this.bindResponseElement = function (ref) {
            return _this.setState({ responseElement: ref });
        };
        _this.renderFailure = function () {
            var deviceFailure = _this.state.deviceFailure;
            var supportMail = ConfigStore.get('supportEmail');
            var support = supportMail ? (<a href={'mailto:' + supportMail}>{supportMail}</a>) : (<span>{t('Support')}</span>);
            return (<div className="failure-message">
        <div>
          <strong>{t('Error: ')}</strong>{' '}
          {{
                    UNKNOWN_ERROR: t('There was an unknown problem, please try again'),
                    DEVICE_ERROR: t('Your U2F device reported an error.'),
                    DUPLICATE_DEVICE: t('This device is already in use.'),
                    UNKNOWN_DEVICE: t('The device you used for sign-in is unknown.'),
                    BAD_APPID: tct('[p1:The Sentry server administrator modified the ' +
                        'device registrations.]' +
                        '[p2:You need to remove and re-add the device to continue ' +
                        'using your U2F device. Use a different sign-in method or ' +
                        'contact [support] for assistance.]', {
                        p1: <p />,
                        p2: <p />,
                        support: support,
                    }),
                }[deviceFailure || '']}
        </div>
        {_this.canTryAgain && (<div style={{ marginTop: 18 }}>
            <a onClick={_this.onTryAgain} className="btn btn-primary">
              {t('Try Again')}
            </a>
          </div>)}
      </div>);
        };
        return _this;
    }
    U2fInterface.prototype.componentDidMount = function () {
        return __awaiter(this, void 0, void 0, function () {
            var supported;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, u2f.isSupported()];
                    case 1:
                        supported = _a.sent();
                        // eslint-disable-next-line react/no-did-mount-set-state
                        this.setState({ isSupported: supported });
                        if (supported) {
                            this.invokeU2fFlow();
                        }
                        return [2 /*return*/];
                }
            });
        });
    };
    U2fInterface.prototype.invokeU2fFlow = function () {
        var _this = this;
        var promise;
        if (this.props.flowMode === 'sign') {
            promise = u2f.sign(this.props.challengeData.authenticateRequests);
        }
        else if (this.props.flowMode === 'enroll') {
            var _a = this.props.challengeData, registerRequests = _a.registerRequests, authenticateRequests = _a.authenticateRequests;
            promise = u2f.register(registerRequests, authenticateRequests);
        }
        else {
            throw new Error("Unsupported flow mode '" + this.props.flowMode + "'");
        }
        promise
            .then(function (data) {
            _this.setState({
                hasBeenTapped: true,
            }, function () {
                var _a;
                var u2fResponse = JSON.stringify(data);
                var challenge = JSON.stringify(_this.props.challengeData);
                if (_this.state.responseElement) {
                    // eslint-disable-next-line react/no-direct-mutation-state
                    _this.state.responseElement.value = u2fResponse;
                }
                if (!_this.props.onTap) {
                    (_a = _this.state.formElement) === null || _a === void 0 ? void 0 : _a.submit();
                    return;
                }
                _this.props
                    .onTap({
                    response: u2fResponse,
                    challenge: challenge,
                })
                    .catch(function () {
                    // This is kind of gross but I want to limit the amount of changes to this component
                    _this.setState({
                        deviceFailure: 'UNKNOWN_ERROR',
                        hasBeenTapped: false,
                    });
                });
            });
        })
            .catch(function (err) {
            var failure = 'DEVICE_ERROR';
            // in some rare cases there is no metadata on the error which
            // causes this to blow up badly.
            if (err.metaData) {
                if (err.metaData.type === 'DEVICE_INELIGIBLE') {
                    if (_this.props.flowMode === 'enroll') {
                        failure = 'DUPLICATE_DEVICE';
                    }
                    else {
                        failure = 'UNKNOWN_DEVICE';
                    }
                }
                else if (err.metaData.type === 'BAD_REQUEST') {
                    failure = 'BAD_APPID';
                }
            }
            // we want to know what is happening here.  There are some indicators
            // that users are getting errors that should not happen through the
            // regular u2f flow.
            Sentry.captureException(err);
            _this.setState({
                deviceFailure: failure,
                hasBeenTapped: false,
            });
        });
    };
    U2fInterface.prototype.renderUnsupported = function () {
        return this.props.silentIfUnsupported ? null : (<div className="u2f-box">
        <div className="inner">
          <p className="error">
            {t("\n             Unfortunately your browser does not support U2F. You need to use\n             a different two-factor method or switch to a browser that supports\n             it (Google Chrome or Microsoft Edge).")}
          </p>
        </div>
      </div>);
    };
    Object.defineProperty(U2fInterface.prototype, "canTryAgain", {
        get: function () {
            return this.state.deviceFailure !== 'BAD_APPID';
        },
        enumerable: false,
        configurable: true
    });
    U2fInterface.prototype.renderBody = function () {
        return this.state.deviceFailure ? this.renderFailure() : this.props.children;
    };
    U2fInterface.prototype.renderPrompt = function () {
        var style = this.props.style;
        return (<div style={style} className={'u2f-box' +
                (this.state.hasBeenTapped ? ' tapped' : '') +
                (this.state.deviceFailure ? ' device-failure' : '')}>
        <div className="device-animation-frame">
          <div className="device-failed"/>
          <div className="device-animation"/>
          <div className="loading-dots">
            <span className="dot"/>
            <span className="dot"/>
            <span className="dot"/>
          </div>
        </div>
        <input type="hidden" name="challenge" ref={this.bindChallengeElement}/>
        <input type="hidden" name="response" ref={this.bindResponseElement}/>
        <div className="inner">{this.renderBody()}</div>
      </div>);
    };
    U2fInterface.prototype.render = function () {
        var isSupported = this.state.isSupported;
        // if we are still waiting for the browser to tell us if we can do u2f this
        // will be null.
        if (isSupported === null) {
            return null;
        }
        if (!isSupported) {
            return this.renderUnsupported();
        }
        return this.renderPrompt();
    };
    return U2fInterface;
}(React.Component));
export default U2fInterface;
//# sourceMappingURL=u2finterface.jsx.map
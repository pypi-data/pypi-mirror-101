import { __extends } from "tslib";
import React from 'react';
import ReactDOM from 'react-dom';
import copy from 'copy-text-to-clipboard';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { t } from 'app/locale';
/**
 * copy-text-to-clipboard relies on `document.execCommand('copy')`
 */
function isSupported() {
    var support = !!document.queryCommandSupported;
    return support && !!document.queryCommandSupported('copy');
}
var Clipboard = /** @class */ (function (_super) {
    __extends(Clipboard, _super);
    function Clipboard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleClick = function () {
            var _a = _this.props, value = _a.value, hideMessages = _a.hideMessages, successMessage = _a.successMessage, errorMessage = _a.errorMessage, onSuccess = _a.onSuccess, onError = _a.onError;
            // Copy returns whether it succeeded to copy the text
            var success = copy(value);
            if (!success) {
                if (!hideMessages) {
                    addErrorMessage(errorMessage);
                }
                onError === null || onError === void 0 ? void 0 : onError();
                return;
            }
            if (!hideMessages) {
                addSuccessMessage(successMessage);
            }
            onSuccess === null || onSuccess === void 0 ? void 0 : onSuccess();
        };
        _this.handleMount = function (ref) {
            var _a;
            if (!ref) {
                return;
            }
            // eslint-disable-next-line react/no-find-dom-node
            _this.element = ReactDOM.findDOMNode(ref);
            (_a = _this.element) === null || _a === void 0 ? void 0 : _a.addEventListener('click', _this.handleClick);
        };
        return _this;
    }
    Clipboard.prototype.componentWillUnmount = function () {
        var _a;
        (_a = this.element) === null || _a === void 0 ? void 0 : _a.removeEventListener('click', this.handleClick);
    };
    Clipboard.prototype.render = function () {
        var _a = this.props, children = _a.children, hideUnsupported = _a.hideUnsupported;
        // Browser doesn't support `execCommand`
        if (hideUnsupported && !isSupported()) {
            return null;
        }
        if (!React.isValidElement(children)) {
            return null;
        }
        return React.cloneElement(children, {
            ref: this.handleMount,
        });
    };
    Clipboard.defaultProps = {
        hideMessages: false,
        successMessage: t('Copied to clipboard'),
        errorMessage: t('Error copying to clipboard'),
    };
    return Clipboard;
}(React.Component));
export default Clipboard;
//# sourceMappingURL=clipboard.jsx.map
import { __extends, __rest } from "tslib";
import React from 'react';
import debounce from 'lodash/debounce';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { Client } from 'app/api';
import { t } from 'app/locale';
import handleXhrErrorResponse from 'app/utils/handleXhrErrorResponse';
import SelectControl from './selectControl';
/**
 * Performs an API request to `url` when menu is initially opened
 */
var SelectAsyncControl = /** @class */ (function (_super) {
    __extends(SelectAsyncControl, _super);
    function SelectAsyncControl(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {};
        _this.doQuery = debounce(function (cb) {
            var _a = _this.props, url = _a.url, onQuery = _a.onQuery;
            var query = _this.state.query;
            if (!_this.api) {
                return null;
            }
            return _this.api
                .requestPromise(url, {
                query: typeof onQuery === 'function' ? onQuery(query) : { query: query },
            })
                .then(function (data) { return cb(null, data); }, function (err) { return cb(err); });
        }, 250);
        _this.handleLoadOptions = function () {
            return new Promise(function (resolve, reject) {
                _this.doQuery(function (err, result) {
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(result);
                    }
                });
            }).then(function (resp) {
                var _a = _this.props, onResults = _a.onResults, deprecatedSelectControl = _a.deprecatedSelectControl;
                // react-select v3 expects a bare list, while v2 requires an object with `options`.
                if (!deprecatedSelectControl) {
                    return typeof onResults === 'function' ? onResults(resp) : resp;
                }
                // Note `SelectControl` expects this data type:
                // {
                //   options: [{ label, value}],
                // }
                return {
                    options: typeof onResults === 'function' ? onResults(resp) : resp,
                };
            }, function (err) {
                addErrorMessage(t('There was a problem with the request.'));
                handleXhrErrorResponse('SelectAsync failed')(err);
                // eslint-disable-next-line no-console
                console.error(err);
            });
        };
        _this.handleInputChange = function (query) {
            _this.setState({ query: query });
        };
        _this.api = new Client();
        _this.state = {
            query: '',
        };
        _this.cache = {};
        return _this;
    }
    SelectAsyncControl.prototype.componentWillUnmount = function () {
        if (!this.api) {
            return;
        }
        this.api.clear();
        this.api = null;
    };
    SelectAsyncControl.prototype.render = function () {
        var _a = this.props, value = _a.value, forwardedRef = _a.forwardedRef, props = __rest(_a, ["value", "forwardedRef"]);
        return (<SelectControl ref={forwardedRef} value={value} defaultOptions loadOptions={this.handleLoadOptions} onInputChange={this.handleInputChange} async cache={this.cache} {...props}/>);
    };
    SelectAsyncControl.defaultProps = {
        placeholder: '--',
    };
    return SelectAsyncControl;
}(React.Component));
var forwardRef = function (p, ref) { return <SelectAsyncControl {...p} forwardedRef={ref}/>; };
forwardRef.displayName = 'SelectAsyncControl';
export default React.forwardRef(forwardRef);
//# sourceMappingURL=selectAsyncControl.jsx.map
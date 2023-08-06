import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isEmpty from 'lodash/isEmpty';
import mapKeys from 'lodash/mapKeys';
import startCase from 'lodash/startCase';
import moment from 'moment';
import Button from 'app/components/button';
import KeyValueList from 'app/components/events/interfaces/keyValueList/keyValueList';
import ListItem from 'app/components/list/listItem';
import { t } from 'app/locale';
import space from 'app/styles/space';
var keyMapping = {
    image_uuid: 'Debug ID',
    image_name: 'File Name',
    image_path: 'File Path',
};
var ErrorItem = /** @class */ (function (_super) {
    __extends(ErrorItem, _super);
    function ErrorItem() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isOpen: false,
        };
        _this.handleToggle = function () {
            _this.setState({ isOpen: !_this.state.isOpen });
        };
        return _this;
    }
    ErrorItem.prototype.shouldComponentUpdate = function (_nextProps, nextState) {
        return this.state.isOpen !== nextState.isOpen;
    };
    ErrorItem.prototype.cleanedData = function (errorData) {
        var data = __assign({}, errorData);
        // The name is rendered as path in front of the message
        if (typeof data.name === 'string') {
            delete data.name;
        }
        if (data.message === 'None') {
            // Python ensures a message string, but "None" doesn't make sense here
            delete data.message;
        }
        if (typeof data.image_path === 'string') {
            // Separate the image name for readability
            var separator = /^([a-z]:\\|\\\\)/i.test(data.image_path) ? '\\' : '/';
            var path = data.image_path.split(separator);
            data.image_name = path.splice(-1, 1)[0];
            data.image_path = path.length ? path.join(separator) + separator : '';
        }
        if (typeof data.server_time === 'string' && typeof data.sdk_time === 'string') {
            data.message = t('Adjusted timestamps by %s', moment
                .duration(moment.utc(data.server_time).diff(moment.utc(data.sdk_time)))
                .humanize());
        }
        return mapKeys(data, function (_value, key) { return t(keyMapping[key] || startCase(key)); });
    };
    ErrorItem.prototype.renderPath = function (data) {
        var name = data.name;
        if (!name || typeof name !== 'string') {
            return null;
        }
        return (<React.Fragment>
        <strong>{name}</strong>
        {': '}
      </React.Fragment>);
    };
    ErrorItem.prototype.render = function () {
        var _a;
        var error = this.props.error;
        var isOpen = this.state.isOpen;
        var data = (_a = error === null || error === void 0 ? void 0 : error.data) !== null && _a !== void 0 ? _a : {};
        var cleanedData = this.cleanedData(data);
        return (<StyledListItem>
        <OverallInfo>
          <div>
            {this.renderPath(data)}
            {error.message}
          </div>
          {!isEmpty(cleanedData) && (<ToggleButton onClick={this.handleToggle} priority="link">
              {isOpen ? t('Collapse') : t('Expand')}
            </ToggleButton>)}
        </OverallInfo>
        {isOpen && <KeyValueList data={cleanedData} isContextData/>}
      </StyledListItem>);
    };
    return ErrorItem;
}(React.Component));
export default ErrorItem;
var ToggleButton = styled(Button)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: ", ";\n  font-weight: 700;\n  color: ", ";\n  :hover,\n  :focus {\n    color: ", ";\n  }\n"], ["\n  margin-left: ", ";\n  font-weight: 700;\n  color: ", ";\n  :hover,\n  :focus {\n    color: ", ";\n  }\n"])), space(1.5), function (p) { return p.theme.subText; }, function (p) { return p.theme.textColor; });
var StyledListItem = styled(ListItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(0.75));
var OverallInfo = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(auto, max-content));\n  word-break: break-all;\n"], ["\n  display: grid;\n  grid-template-columns: repeat(2, minmax(auto, max-content));\n  word-break: break-all;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=errorItem.jsx.map
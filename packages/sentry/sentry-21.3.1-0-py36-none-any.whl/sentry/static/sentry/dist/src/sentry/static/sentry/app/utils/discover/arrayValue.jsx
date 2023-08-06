import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
var ArrayValue = /** @class */ (function (_super) {
    __extends(ArrayValue, _super);
    function ArrayValue() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            expanded: false,
        };
        _this.handleToggle = function () {
            _this.setState(function (prevState) { return ({
                expanded: !prevState.expanded,
            }); });
        };
        return _this;
    }
    ArrayValue.prototype.render = function () {
        var expanded = this.state.expanded;
        var value = this.props.value;
        return (<ArrayContainer expanded={expanded}>
        {expanded &&
                value
                    .slice(0, value.length - 1)
                    .map(function (item, i) { return <ArrayItem key={i + ":" + item}>{item}</ArrayItem>; })}
        <ArrayItem>{value.slice(-1)[0]}</ArrayItem>
        {value.length > 1 ? (<ButtonContainer>
            <button onClick={this.handleToggle}>
              {expanded ? t('[collapse]') : t('[+%s more]', value.length - 1)}
            </button>
          </ButtonContainer>) : null}
      </ArrayContainer>);
    };
    return ArrayValue;
}(React.Component));
var ArrayContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: ", ";\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n    cursor: pointer;\n    color: ", ";\n    margin-left: ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: ", ";\n\n  & button {\n    background: none;\n    border: 0;\n    outline: none;\n    padding: 0;\n    cursor: pointer;\n    color: ", ";\n    margin-left: ", ";\n  }\n"])), function (p) { return (p.expanded ? 'column' : 'row'); }, function (p) { return p.theme.blue300; }, space(0.5));
var ArrayItem = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-shrink: 1;\n  display: block;\n\n  ", ";\n  width: unset;\n"], ["\n  flex-shrink: 1;\n  display: block;\n\n  ", ";\n  width: unset;\n"])), overflowEllipsis);
var ButtonContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
export default ArrayValue;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=arrayValue.jsx.map
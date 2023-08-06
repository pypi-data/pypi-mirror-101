import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
var Truncate = /** @class */ (function (_super) {
    __extends(Truncate, _super);
    function Truncate() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isExpanded: false,
        };
        _this.onFocus = function () {
            var _a = _this.props, value = _a.value, maxLength = _a.maxLength;
            if (value.length <= maxLength) {
                return;
            }
            _this.setState({ isExpanded: true });
        };
        _this.onBlur = function () {
            if (_this.state.isExpanded) {
                _this.setState({ isExpanded: false });
            }
        };
        return _this;
    }
    Truncate.prototype.render = function () {
        var _a = this.props, className = _a.className, leftTrim = _a.leftTrim, trimRegex = _a.trimRegex, minLength = _a.minLength, maxLength = _a.maxLength, value = _a.value, expandable = _a.expandable, expandDirection = _a.expandDirection;
        var isTruncated = value.length > maxLength;
        var shortValue = '';
        if (isTruncated) {
            var slicedValue = leftTrim
                ? value.slice(value.length - (maxLength - 4), value.length)
                : value.slice(0, maxLength - 4);
            // Try to trim to values from the regex
            if (trimRegex && leftTrim) {
                var valueIndex = slicedValue.search(trimRegex);
                shortValue = (<span>
            …{' '}
            {valueIndex > 0 && valueIndex <= maxLength - minLength
                        ? slicedValue.slice(slicedValue.search(trimRegex), slicedValue.length)
                        : slicedValue}
          </span>);
            }
            else if (trimRegex && !leftTrim) {
                var matches = slicedValue.match(trimRegex);
                var lastIndex = matches
                    ? slicedValue.lastIndexOf(matches[matches.length - 1]) + 1
                    : slicedValue.length;
                if (lastIndex <= minLength) {
                    lastIndex = slicedValue.length;
                }
                shortValue = <span>{slicedValue.slice(0, lastIndex)} …</span>;
            }
            else if (leftTrim) {
                shortValue = <span>… {slicedValue}</span>;
            }
            else {
                shortValue = <span>{slicedValue} …</span>;
            }
        }
        else {
            shortValue = value;
        }
        return (<Wrapper className={className} onMouseOver={expandable ? this.onFocus : undefined} onMouseOut={expandable ? this.onBlur : undefined} onFocus={expandable ? this.onFocus : undefined} onBlur={expandable ? this.onBlur : undefined}>
        <span>{shortValue}</span>
        {isTruncated && (<FullValue expanded={this.state.isExpanded} expandDirection={expandDirection}>
            {value}
          </FullValue>)}
      </Wrapper>);
    };
    Truncate.defaultProps = {
        className: '',
        minLength: 15,
        maxLength: 50,
        leftTrim: false,
        expandable: true,
        expandDirection: 'right',
    };
    return Truncate;
}(React.Component));
var Wrapper = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
export var FullValue = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: none;\n  position: absolute;\n  background: ", ";\n  padding: ", ";\n  border: 1px solid ", ";\n  white-space: nowrap;\n  border-radius: ", ";\n  top: -5px;\n  ", "\n  ", "\n\n  ", "\n"], ["\n  display: none;\n  position: absolute;\n  background: ", ";\n  padding: ", ";\n  border: 1px solid ", ";\n  white-space: nowrap;\n  border-radius: ", ";\n  top: -5px;\n  ", "\n  ", "\n\n  ",
    "\n"])), function (p) { return p.theme.background; }, space(0.5), function (p) { return p.theme.innerBorder; }, space(0.5), function (p) { return p.expandDirection === 'left' && 'right: -5px;'; }, function (p) { return p.expandDirection === 'right' && 'left: -5px;'; }, function (p) {
    return p.expanded &&
        "\n    z-index: " + p.theme.zIndex.truncationFullValue + ";\n    display: block;\n    ";
});
export default Truncate;
var templateObject_1, templateObject_2;
//# sourceMappingURL=truncate.jsx.map
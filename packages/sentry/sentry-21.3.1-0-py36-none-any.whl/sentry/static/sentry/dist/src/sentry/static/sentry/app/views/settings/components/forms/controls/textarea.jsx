import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import TextareaAutosize from 'react-autosize-textarea';
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import { inputStyles } from 'app/styles/input';
import space from 'app/styles/space';
var TextAreaControl = React.forwardRef(function TextAreaControl(_a, ref) {
    var autosize = _a.autosize, rows = _a.rows, maxRows = _a.maxRows, p = __rest(_a, ["autosize", "rows", "maxRows"]);
    return autosize ? (<TextareaAutosize {...p} async ref={ref} rows={rows ? rows : 2} maxRows={maxRows}/>) : (<textarea ref={ref} {...p}/>);
});
TextAreaControl.displayName = 'TextAreaControl';
var propFilter = function (p) {
    return ['autosize', 'rows', 'maxRows'].includes(p) || isPropValid(p);
};
var TextArea = styled(TextAreaControl, { shouldForwardProp: propFilter })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  min-height: 40px;\n  padding: calc(", " - 1px) ", ";\n  line-height: 1.5em;\n  ", "\n"], ["\n  ", ";\n  min-height: 40px;\n  padding: calc(", " - 1px) ", ";\n  line-height: 1.5em;\n  ",
    "\n"])), inputStyles, space(1), space(1), function (p) {
    return p.autosize &&
        "\n      padding: calc(" + space(1) + " - 2px) " + space(1) + ";\n      line-height: 1.6em;\n    ";
});
export default TextArea;
var templateObject_1;
//# sourceMappingURL=textarea.jsx.map
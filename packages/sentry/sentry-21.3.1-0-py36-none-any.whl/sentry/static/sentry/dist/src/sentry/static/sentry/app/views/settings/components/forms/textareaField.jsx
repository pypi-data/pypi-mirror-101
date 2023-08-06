import { __rest } from "tslib";
import React from 'react';
import omit from 'lodash/omit';
import Textarea from 'app/views/settings/components/forms/controls/textarea';
import InputField from 'app/views/settings/components/forms/inputField';
export default function TextareaField(_a) {
    var monospace = _a.monospace, rows = _a.rows, autosize = _a.autosize, props = __rest(_a, ["monospace", "rows", "autosize"]);
    return (<InputField {...props} field={function (fieldProps) { return (<Textarea {...{ monospace: monospace, rows: rows, autosize: autosize }} {...omit(fieldProps, ['onKeyDown', 'children'])}/>); }}/>);
}
//# sourceMappingURL=textareaField.jsx.map
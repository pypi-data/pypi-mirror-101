import { __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import sortBy from 'lodash/sortBy';
import ContextData from 'app/components/contextData';
import theme from 'app/utils/theme';
/**
 * Generic KeyValue data renderer. The V2 version
 * of this component can also render annotations
 * for datascrubbing.
 */
function KeyValueList(_a) {
    // TODO(dcramer): use non-string keys as reserved words ("unauthorized")
    // break rendering
    var data = _a.data, onClick = _a.onClick, _b = _a.isContextData, isContextData = _b === void 0 ? false : _b, _c = _a.isSorted, isSorted = _c === void 0 ? true : _c, _d = _a.raw, raw = _d === void 0 ? false : _d, _e = _a.longKeys, longKeys = _e === void 0 ? false : _e;
    if (data === undefined || data === null) {
        data = [];
    }
    else if (!(data instanceof Array)) {
        data = Object.entries(data);
    }
    else {
        data = data.filter(function (kv) { return kv !== null; });
    }
    data = isSorted ? sortBy(data, [function (_a) {
            var _b = __read(_a, 1), key = _b[0];
            return key;
        }]) : data;
    return (<table className="table key-value" onClick={onClick}>
      <tbody>
        {data.map(function (_a) {
            var _b = __read(_a, 2), key = _b[0], value = _b[1];
            if (isContextData) {
                return [
                    <tr key={key}>
                <TableData className="key" wide={longKeys}>
                  {key}
                </TableData>
                <td className="val">
                  <ContextData data={!raw ? value : JSON.stringify(value)}/>
                </td>
              </tr>,
                ];
            }
            else {
                return [
                    <tr key={key}>
                <TableData className="key" wide={longKeys}>
                  {key}
                </TableData>
                <td className="val">
                  <pre className="val-string">{'' + value || ' '}</pre>
                </td>
              </tr>,
                ];
            }
        })}
      </tbody>
    </table>);
}
var TableData = styled('td')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    max-width: ", ";\n  }\n"], ["\n  @media (min-width: ", ") {\n    max-width: ", ";\n  }\n"])), theme.breakpoints[2], function (p) { return (p.wide ? '620px !important' : null); });
export default KeyValueList;
var templateObject_1;
//# sourceMappingURL=keyValueList.jsx.map
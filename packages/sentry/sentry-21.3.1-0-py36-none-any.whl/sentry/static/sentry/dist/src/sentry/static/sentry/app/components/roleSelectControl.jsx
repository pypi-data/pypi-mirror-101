import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { components } from 'react-select';
import styled from '@emotion/styled';
import SelectControl from 'app/components/forms/selectControl';
import space from 'app/styles/space';
import theme from 'app/utils/theme';
function RoleSelectControl(_a) {
    var roles = _a.roles, disableUnallowed = _a.disableUnallowed, props = __rest(_a, ["roles", "disableUnallowed"]);
    return (<SelectControl options={roles === null || roles === void 0 ? void 0 : roles.map(function (r) {
            return ({
                value: r.id,
                label: r.name,
                disabled: disableUnallowed && !r.allowed,
                description: r.desc,
            });
        })} components={{
            Option: function (_a) {
                var label = _a.label, data = _a.data, optionProps = __rest(_a, ["label", "data"]);
                return (<components.Option label={label} {...optionProps}>
            <RoleItem>
              <h1>{label}</h1>
              <div>{data.description}</div>
            </RoleItem>
          </components.Option>);
            },
        }} styles={{
            control: function (provided) { return (__assign(__assign({}, provided), { borderBottomLeftRadius: theme.borderRadius, borderBottomRightRadius: theme.borderRadius })); },
            menu: function (provided) { return (__assign(__assign({}, provided), { borderRadius: theme.borderRadius, marginTop: space(0.5), width: '350px', overflow: 'hidden' })); },
        }} {...props}/>);
}
var RoleItem = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 80px 1fr;\n  grid-gap: ", ";\n\n  h1,\n  div {\n    font-size: ", ";\n    line-height: 1.4;\n    margin: ", " 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 80px 1fr;\n  grid-gap: ", ";\n\n  h1,\n  div {\n    font-size: ", ";\n    line-height: 1.4;\n    margin: ", " 0;\n  }\n"])), space(1), function (p) { return p.theme.fontSizeSmall; }, space(0.25));
export default RoleSelectControl;
var templateObject_1;
//# sourceMappingURL=roleSelectControl.jsx.map
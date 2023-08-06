import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ListItem from 'app/components/list/listItem';
import space from 'app/styles/space';
function BuildStep(_a) {
    var title = _a.title, description = _a.description, children = _a.children;
    return (<StyledListItem>
      <Header>
        <Description>{title}</Description>
        <SubDescription>{description}</SubDescription>
      </Header>
      <Content>{children}</Content>
    </StyledListItem>);
}
export default BuildStep;
var StyledListItem = styled(ListItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(2));
var Description = styled('h4')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-weight: 400;\n  margin-bottom: 0;\n"], ["\n  font-weight: 400;\n  margin-bottom: 0;\n"])));
var SubDescription = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return p.theme.gray300; }, function (p) { return p.theme.fontSizeMedium; });
var Header = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space(0.5));
var Content = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=buildStep.jsx.map
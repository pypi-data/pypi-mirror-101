import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import CircleIndicator from 'app/components/circleIndicator';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { COLORS } from './constants';
var StatusWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var IntegrationStatus = styled(withTheme(function (props) {
    var theme = props.theme, status = props.status, p = __rest(props, ["theme", "status"]);
    return (<StatusWrapper>
        <CircleIndicator size={6} color={theme[COLORS[status]]}/>
        <div {...p}>{"" + t(status)}</div>
      </StatusWrapper>);
}))(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n  font-weight: light;\n  margin-right: ", ";\n"], ["\n  color: ", ";\n  margin-left: ", ";\n  font-weight: light;\n  margin-right: ", ";\n"])), function (p) { return p.theme[COLORS[p.status]]; }, space(0.5), space(0.75));
export default IntegrationStatus;
var templateObject_1, templateObject_2;
//# sourceMappingURL=integrationStatus.jsx.map
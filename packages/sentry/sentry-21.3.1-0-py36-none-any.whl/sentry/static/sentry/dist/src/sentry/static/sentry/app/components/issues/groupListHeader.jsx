import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Box, Flex } from 'reflexbox'; // eslint-disable-line no-restricted-imports
import { PanelHeader } from 'app/components/panels';
import { t } from 'app/locale';
import space from 'app/styles/space';
var GroupListHeader = function (_a) {
    var _b = _a.withChart, withChart = _b === void 0 ? true : _b;
    return (<PanelHeader disablePadding>
    <Box width={[8 / 12, 8 / 12, 6 / 12]} mx={2} flex="1">
      {t('Issue')}
    </Box>
    {withChart && (<Flex width={160} mx={2} justifyContent="space-between" className="hidden-xs hidden-sm">
        {t('Graph')}
      </Flex>)}
    <EventUserWrapper>{t('events')}</EventUserWrapper>
    <EventUserWrapper>{t('users')}</EventUserWrapper>
    <Flex width={80} mx={2} justifyContent="flex-end" className="hidden-xs hidden-sm toolbar-header">
      {t('Assignee')}
    </Flex>
  </PanelHeader>);
};
export default GroupListHeader;
var EventUserWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-self: center;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-self: center;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; });
var templateObject_1;
//# sourceMappingURL=groupListHeader.jsx.map
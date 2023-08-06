import { __makeTemplateObject } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import ProgressRing from 'app/components/progressRing';
import { t } from 'app/locale';
import space from 'app/styles/space';
var ProgressHeader = function (_a) {
    var theme = _a.theme, allTasks = _a.allTasks, completedTasks = _a.completedTasks;
    return (<Container>
    <StyledProgressRing size={80} barWidth={8} text={allTasks.length - completedTasks.length} animateText value={(completedTasks.length / allTasks.length) * 100} progressEndcaps="round" backgroundColor={theme.gray100} textCss={function () { return css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n        font-size: 26px;\n        color: ", ";\n      "], ["\n        font-size: 26px;\n        color: ", ";\n      "])), theme.textColor); }}/>
    <HeaderTitle>{t('Quick Start')}</HeaderTitle>
    <Description>
      {t("Take full advantage of Sentry's powerful monitoring features.")}
    </Description>
  </Container>);
};
export default withTheme(ProgressHeader);
var Container = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: min-content 1fr;\n  grid-template-rows: min-content 1fr;\n  grid-column-gap: ", ";\n  margin: 90px ", " 0 ", ";\n"], ["\n  display: grid;\n  grid-template-columns: min-content 1fr;\n  grid-template-rows: min-content 1fr;\n  grid-column-gap: ", ";\n  margin: 90px ", " 0 ", ";\n"])), space(2), space(4), space(4));
var StyledProgressRing = styled(ProgressRing)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-column: 1/2;\n  grid-row: 1/3;\n"], ["\n  grid-column: 1/2;\n  grid-row: 1/3;\n"])));
var HeaderTitle = styled('h3')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0;\n  grid-column: 2/3;\n  grid-row: 1/2;\n"], ["\n  margin: 0;\n  grid-column: 2/3;\n  grid-row: 1/2;\n"])));
var Description = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  grid-column: 2/3;\n  grid-row: 2/3;\n"], ["\n  color: ", ";\n  grid-column: 2/3;\n  grid-row: 2/3;\n"])), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=progressHeader.jsx.map
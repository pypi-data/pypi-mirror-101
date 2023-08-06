import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { Panel } from 'app/components/panels';
import QuestionTooltip from 'app/components/questionTooltip';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined } from 'app/utils';
function ScoreCard(_a) {
    var title = _a.title, score = _a.score, help = _a.help, trend = _a.trend, trendStatus = _a.trendStatus, className = _a.className;
    return (<StyledPanel className={className}>
      <HeaderTitle>
        <Title>{title}</Title>
        {help && <QuestionTooltip title={help} size="sm" position="top"/>}
      </HeaderTitle>

      <ScoreWrapper>
        <Score>{score !== null && score !== void 0 ? score : '\u2014'}</Score>
        {defined(trend) && <Trend trendStatus={trendStatus}>{trend}</Trend>}
      </ScoreWrapper>
    </StyledPanel>);
}
function getTrendColor(p) {
    switch (p.trendStatus) {
        case 'good':
            return p.theme.green300;
        case 'bad':
            return p.theme.red300;
        default:
            return p.theme.gray300;
    }
}
var StyledPanel = styled(Panel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n  padding: ", " ", ";\n  min-height: 96px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  justify-content: space-between;\n  padding: ", " ", ";\n  min-height: 96px;\n"])), space(2), space(3));
var HeaderTitle = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  width: fit-content;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n  width: fit-content;\n"])), space(1));
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n"], ["\n  ", ";\n"])), overflowEllipsis);
var ScoreWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  align-items: baseline;\n"], ["\n  display: flex;\n  align-items: baseline;\n"])));
var Score = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: 32px;\n  line-height: 1;\n"], ["\n  font-size: 32px;\n  line-height: 1;\n"])));
var Trend = styled('span')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  margin-left: ", ";\n  line-height: 1;\n  ", ";\n"], ["\n  color: ", ";\n  margin-left: ", ";\n  line-height: 1;\n  ", ";\n"])), getTrendColor, space(1), overflowEllipsis);
export default ScoreCard;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=scoreCard.jsx.map
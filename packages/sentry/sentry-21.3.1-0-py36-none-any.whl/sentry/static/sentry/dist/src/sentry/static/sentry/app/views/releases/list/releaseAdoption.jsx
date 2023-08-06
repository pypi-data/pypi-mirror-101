import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import Count from 'app/components/count';
import ProgressBar from 'app/components/progressBar';
import TextOverflow from 'app/components/textOverflow';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { releaseDisplayLabel } from '../utils';
function ReleaseAdoption(_a) {
    var adoption = _a.adoption, releaseCount = _a.releaseCount, projectCount = _a.projectCount, displayOption = _a.displayOption, theme = _a.theme, withLabels = _a.withLabels;
    return (<div>
      {withLabels && (<Labels>
          <TextOverflow>
            <Count value={releaseCount}/>/<Count value={projectCount}/>{' '}
            {releaseDisplayLabel(displayOption, projectCount)}
          </TextOverflow>

          <span>{!adoption ? 0 : adoption < 1 ? '<1' : Math.round(adoption)}%</span>
        </Labels>)}

      <Tooltip containerDisplayMode="block" popperStyle={{
            background: theme.gray500,
            maxWidth: '300px',
        }} title={<TooltipWrapper>
            <TooltipRow>
              <Title>
                <Dot color={theme.progressBar}/>
                {t('This Release')}
              </Title>
              <Value>
                <Count value={releaseCount}/>{' '}
                {releaseDisplayLabel(displayOption, releaseCount)}
              </Value>
            </TooltipRow>
            <TooltipRow>
              <Title>
                <Dot color={theme.progressBackground}/>
                {t('Total Project')}
              </Title>
              <Value>
                <Count value={projectCount}/>{' '}
                {releaseDisplayLabel(displayOption, projectCount)}
              </Value>
            </TooltipRow>
            <Divider />

            <Time>{t('Last 24 hours')}</Time>
          </TooltipWrapper>}>
        <ProgressBarWrapper>
          <ProgressBar value={Math.ceil(adoption)}/>
        </ProgressBarWrapper>
      </Tooltip>
    </div>);
}
var Labels = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr max-content;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: 1fr max-content;\n"])), space(1));
var TooltipWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", ";\n  font-size: ", ";\n  line-height: 21px;\n  font-weight: normal;\n"], ["\n  padding: ", ";\n  font-size: ", ";\n  line-height: 21px;\n  font-weight: normal;\n"])), space(0.75), function (p) { return p.theme.fontSizeMedium; });
var TooltipRow = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  justify-content: space-between;\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: auto auto;\n  grid-gap: ", ";\n  justify-content: space-between;\n  padding-bottom: ", ";\n"])), space(3), space(0.25));
var Title = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var Dot = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: inline-block;\n  margin-right: ", ";\n  border-radius: 10px;\n  width: 10px;\n  height: 10px;\n  background-color: ", ";\n"], ["\n  display: inline-block;\n  margin-right: ", ";\n  border-radius: 10px;\n  width: 10px;\n  height: 10px;\n  background-color: ", ";\n"])), space(0.75), function (p) { return p.color; });
var Value = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  text-align: right;\n"], ["\n  color: ", ";\n  text-align: right;\n"])), function (p) { return p.theme.gray300; });
var Divider = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  margin: ", " -", " ", ";\n"], ["\n  border-top: 1px solid ", ";\n  margin: ", " -", " ", ";\n"])), function (p) { return p.theme.gray400; }, space(0.75), space(2), space(1));
var Time = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  color: ", ";\n  text-align: center;\n"], ["\n  color: ", ";\n  text-align: center;\n"])), function (p) { return p.theme.gray300; });
var ProgressBarWrapper = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  /* A bit of padding makes hovering for tooltip easier */\n  padding: ", " 0;\n"], ["\n  /* A bit of padding makes hovering for tooltip easier */\n  padding: ", " 0;\n"])), space(0.5));
export default withTheme(ReleaseAdoption);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=releaseAdoption.jsx.map
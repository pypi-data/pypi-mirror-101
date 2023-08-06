import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import FeatureBadge from 'app/components/featureBadge';
import QuestionTooltip from 'app/components/questionTooltip';
import space from 'app/styles/space';
export function MetaData(_a) {
    var headingText = _a.headingText, tooltipText = _a.tooltipText, bodyText = _a.bodyText, subtext = _a.subtext, beta = _a.beta;
    return (<HeaderInfo>
      <StyledSectionHeading>
        {headingText}
        <QuestionTooltip position="top" size="sm" containerDisplayMode="block" title={tooltipText}/>
        {beta && <StyledFeatureBadge type="beta"/>}
      </StyledSectionHeading>
      <SectionBody>{bodyText}</SectionBody>
      <SectionSubtext>{subtext}</SectionSubtext>
    </HeaderInfo>);
}
var HeaderInfo = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 78px;\n"], ["\n  height: 78px;\n"])));
var StyledSectionHeading = styled(SectionHeading)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var SectionBody = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  padding: ", " 0;\n  max-height: 32px;\n"], ["\n  font-size: ", ";\n  padding: ", " 0;\n  max-height: 32px;\n"])), function (p) { return p.theme.fontSizeExtraLarge; }, space(0.5));
var StyledFeatureBadge = styled(FeatureBadge)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
export var SectionSubtext = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n"], ["\n  color: ", ";\n  font-size: ", ";\n"])), function (p) { return (p.type === 'error' ? p.theme.error : p.theme.subText); }, function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=styles.jsx.map
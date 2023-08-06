import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ExternalLink from 'app/components/links/externalLink';
import { Panel, PanelItem } from 'app/components/panels';
import { IconCheckmark, IconWarning } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import FooterWithButtons from './components/footerWithButtons';
import HeaderWithHelp from './components/headerWithHelp';
export default function AwsLambdaFailureDetails(_a) {
    var lambdaFunctionFailures = _a.lambdaFunctionFailures, successCount = _a.successCount;
    var baseDocsUrl = 'https://docs.sentry.io/product/integrations/aws-lambda/';
    return (<React.Fragment>
      <HeaderWithHelp docsUrl={baseDocsUrl}/>
      <Wrapper>
        <div>
          <StyledCheckmark isCircled color="green300"/>
          <h3>
            {tn('Succesfully updated %s function', 'Succesfully updated %s functions', successCount)}
          </h3>
        </div>
        <div>
          <StyledWarning color="red300"/>
          <h3>
            {tn('Failed to update %s function', 'Failed to update %s functions', lambdaFunctionFailures.length)}
          </h3>
          <Troubleshooting>
            {tct('See [link:Troubleshooting Docs]', {
            link: <ExternalLink href={baseDocsUrl + '#troubleshooting'}/>,
        })}
          </Troubleshooting>
        </div>
        <StyledPanel>{lambdaFunctionFailures.map(SingleFailure)}</StyledPanel>
      </Wrapper>
      <FooterWithButtons buttonText={t('Finish Setup')} href="?finish_pipeline=1"/>
    </React.Fragment>);
}
function SingleFailure(errorDetail) {
    return (<StyledRow key={errorDetail.name}>
      <span>{errorDetail.name}</span>
      <Error>{errorDetail.error}</Error>
    </StyledRow>);
}
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 100px 50px 50px 50px;\n"], ["\n  padding: 100px 50px 50px 50px;\n"])));
var StyledRow = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var Error = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var StyledPanel = styled(Panel)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  overflow: hidden;\n  margin-left: 34px;\n"], ["\n  overflow: hidden;\n  margin-left: 34px;\n"])));
var Troubleshooting = styled('p')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-left: 34px;\n"], ["\n  margin-left: 34px;\n"])));
var StyledCheckmark = styled(IconCheckmark)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  float: left;\n  margin-right: 10px;\n  height: 24px;\n  width: 24px;\n"], ["\n  float: left;\n  margin-right: 10px;\n  height: 24px;\n  width: 24px;\n"])));
var StyledWarning = styled(IconWarning)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  float: left;\n  margin-right: 10px;\n  height: 24px;\n  width: 24px;\n"], ["\n  float: left;\n  margin-right: 10px;\n  height: 24px;\n  width: 24px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=awsLambdaFailureDetails.jsx.map
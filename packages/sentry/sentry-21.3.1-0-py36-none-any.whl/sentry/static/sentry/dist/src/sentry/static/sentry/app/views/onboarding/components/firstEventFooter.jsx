import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import CreateSampleEventButton from 'app/views/onboarding/createSampleEventButton';
import FirstEventIndicator from './firstEventIndicator';
export default function FirstEventFooter(_a) {
    var organization = _a.organization, project = _a.project, docsLink = _a.docsLink, docsOnClick = _a.docsOnClick;
    return (<React.Fragment>
      <FirstEventIndicator organization={organization} project={project} eventType="error">
        {function (_a) {
            var indicator = _a.indicator, firstEventButton = _a.firstEventButton;
            return (<CTAFooter>
            <Actions gap={2}>
              {firstEventButton}
              <Button external href={docsLink} onClick={docsOnClick}>
                {t('View full documentation')}
              </Button>
            </Actions>
            {indicator}
          </CTAFooter>);
        }}
      </FirstEventIndicator>
      <CTASecondary>
        {tct('Just want to poke around before getting too cozy with the SDK? [sample:View a sample event for this SDK] and finish setup later.', {
            sample: (<CreateSampleEventButton project={project} source="onboarding" priority="link"/>),
        })}
      </CTASecondary>
    </React.Fragment>);
}
var CTAFooter = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  margin: ", " 0;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  justify-content: space-between;\n  margin: ", " 0;\n  margin-top: ", ";\n"])), space(2), space(4));
var CTASecondary = styled('p')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  margin: 0;\n  max-width: 500px;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  margin: 0;\n  max-width: 500px;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; });
var Actions = styled(ButtonBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: inline-grid;\n  justify-self: start;\n"], ["\n  display: inline-grid;\n  justify-self: start;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=firstEventFooter.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tooltip from 'app/components/tooltip';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { formatPercentage } from 'app/utils/formatters';
import { VitalState, vitalStateIcons, webVitalMeh, webVitalPoor } from './utils';
function getVitalStateText(vital, vitalState) {
    switch (vitalState) {
        case VitalState.POOR:
            return Array.isArray(vital)
                ? t('Poor')
                : tct('Poor: >[threshold]ms', { threshold: webVitalPoor[vital] });
        case VitalState.MEH:
            return Array.isArray(vital)
                ? t('Needs improvement')
                : tct('Needs improvement: >[threshold]ms', { threshold: webVitalMeh[vital] });
        case VitalState.GOOD:
            return Array.isArray(vital)
                ? t('Good')
                : tct('Good: <[threshold]ms', { threshold: webVitalMeh[vital] });
        default:
            return null;
    }
}
export default function VitalPercents(props) {
    return (<VitalSet>
      {props.percents.map(function (pct) {
            return (<Tooltip key={pct.vitalState} title={getVitalStateText(props.vital, pct.vitalState)}>
            <VitalStatus>
              {vitalStateIcons[pct.vitalState]}
              <span>
                {props.showVitalPercentNames && t("" + pct.vitalState)}{' '}
                {formatPercentage(pct.percent, 0)}
              </span>
            </VitalStatus>
          </Tooltip>);
        })}
    </VitalSet>);
}
var VitalSet = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  gap: ", ";\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  gap: ", ";\n"])), space(2));
var VitalStatus = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  gap: ", ";\n  font-size: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  gap: ", ";\n  font-size: ", ";\n"])), space(0.5), function (p) { return p.theme.fontSizeMedium; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=vitalPercents.jsx.map
import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Link from 'app/components/links/link';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { HealthStatsPeriodOption } from 'app/types';
import withGlobalSelection from 'app/utils/withGlobalSelection';
var HealthStatsPeriod = function (_a) {
    var _b;
    var location = _a.location, selection = _a.selection;
    var activePeriod = location.query.healthStatsPeriod || HealthStatsPeriodOption.TWENTY_FOUR_HOURS;
    var pathname = location.pathname, query = location.query;
    return (<Wrapper>
      {selection.datetime.period !== HealthStatsPeriodOption.TWENTY_FOUR_HOURS && (<Period to={{
                pathname: pathname,
                query: __assign(__assign({}, query), { healthStatsPeriod: HealthStatsPeriodOption.TWENTY_FOUR_HOURS }),
            }} selected={activePeriod === HealthStatsPeriodOption.TWENTY_FOUR_HOURS}>
          {t('24h')}
        </Period>)}

      <Period to={{
            pathname: pathname,
            query: __assign(__assign({}, query), { healthStatsPeriod: HealthStatsPeriodOption.AUTO }),
        }} selected={activePeriod === HealthStatsPeriodOption.AUTO}>
        {selection.datetime.start ? t('Custom') : (_b = selection.datetime.period) !== null && _b !== void 0 ? _b : t('14d')}
      </Period>
    </Wrapper>);
};
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  flex: 1;\n  justify-content: flex-end;\n  text-align: right;\n  margin-left: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-column-gap: ", ";\n  flex: 1;\n  justify-content: flex-end;\n  text-align: right;\n  margin-left: ", ";\n"])), space(0.75), space(0.5));
var Period = styled(Link)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n\n  &:hover,\n  &:focus {\n    color: ", ";\n  }\n"])), function (p) { return (p.selected ? p.theme.gray400 : p.theme.gray300); }, function (p) { return (p.selected ? p.theme.gray400 : p.theme.gray300); });
export default withGlobalSelection(HealthStatsPeriod);
var templateObject_1, templateObject_2;
//# sourceMappingURL=healthStatsPeriod.jsx.map
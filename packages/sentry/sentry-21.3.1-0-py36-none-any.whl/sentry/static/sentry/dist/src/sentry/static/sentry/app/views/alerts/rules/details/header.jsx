import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import isPropValid from '@emotion/is-prop-valid';
import styled from '@emotion/styled';
import Breadcrumbs from 'app/components/breadcrumbs';
import Button from 'app/components/button';
import PageHeading from 'app/components/pageHeading';
import { IconEdit } from 'app/icons';
import { t } from 'app/locale';
import { PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { isIssueAlert } from '../../utils';
var DetailsHeader = /** @class */ (function (_super) {
    __extends(DetailsHeader, _super);
    function DetailsHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailsHeader.prototype.render = function () {
        var _a = this.props, hasIncidentRuleDetailsError = _a.hasIncidentRuleDetailsError, rule = _a.rule, params = _a.params;
        var isRuleReady = !!rule && !hasIncidentRuleDetailsError;
        var project = rule && rule.projects && rule.projects[0];
        var settingsLink = rule &&
            "/organizations/" + params.orgId + "/alerts/" + (isIssueAlert(rule) ? 'rules' : 'metric-rules') + "/" + project + "/" + rule.id + "/";
        return (<Header>
        <BreadCrumbBar>
          <AlertBreadcrumbs crumbs={[
                { label: t('Alerts'), to: "/organizations/" + params.orgId + "/alerts/" },
                { label: t('Alert Rule') },
            ]}/>
          <Controls>
            <Button icon={<IconEdit />} label={t('Settings')} to={settingsLink}>
              Edit Rule
            </Button>
          </Controls>
        </BreadCrumbBar>
        <Details>
          <RuleTitle data-test-id="incident-rule-title" loading={!isRuleReady}>
            {rule && !hasIncidentRuleDetailsError ? rule.name : 'Loading'}
          </RuleTitle>
        </Details>
      </Header>);
    };
    return DetailsHeader;
}(React.Component));
export default DetailsHeader;
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n"], ["\n  background-color: ", ";\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.border; });
var BreadCrumbBar = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n"], ["\n  display: flex;\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n"])), space(2), space(4), space(1));
var AlertBreadcrumbs = styled(Breadcrumbs)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n  font-size: ", ";\n  padding: 0;\n"], ["\n  flex-grow: 1;\n  font-size: ", ";\n  padding: 0;\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var Controls = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n"])), space(1));
var Details = styled(PageHeader)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n\n  grid-template-columns: max-content auto;\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n    grid-auto-flow: row;\n  }\n"], ["\n  margin-bottom: 0;\n  padding: ", " ", " ", ";\n\n  grid-template-columns: max-content auto;\n  display: grid;\n  grid-gap: ", ";\n  grid-auto-flow: column;\n\n  @media (max-width: ", ") {\n    grid-template-columns: auto;\n    grid-auto-flow: row;\n  }\n"])), space(1.5), space(4), space(2), space(3), function (p) { return p.theme.breakpoints[1]; });
var RuleTitle = styled(PageHeading, {
    shouldForwardProp: function (p) { return isPropValid(p) && p !== 'loading'; },
})(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", ";\n  line-height: 1.5;\n"], ["\n  ", ";\n  line-height: 1.5;\n"])), function (p) { return p.loading && 'opacity: 0'; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=header.jsx.map
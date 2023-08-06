import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Breadcrumbs from 'app/components/breadcrumbs';
import { t } from 'app/locale';
import space from 'app/styles/space';
function BuilderBreadCrumbs(props) {
    var hasMetricAlerts = props.hasMetricAlerts, orgSlug = props.orgSlug, title = props.title, alertName = props.alertName, projectSlug = props.projectSlug;
    var crumbs = [
        {
            to: hasMetricAlerts
                ? "/organizations/" + orgSlug + "/alerts/"
                : "/organizations/" + orgSlug + "/alerts/rules/",
            label: t('Alerts'),
            preserveGlobalSelection: true,
        },
        __assign({ label: title }, (alertName
            ? {
                to: "/organizations/" + orgSlug + "/alerts/" + projectSlug + "/wizard",
                preserveGlobalSelection: true,
            }
            : {})),
    ];
    if (alertName) {
        crumbs.push({ label: alertName });
    }
    return <StyledBreadcrumbs crumbs={crumbs}/>;
}
var StyledBreadcrumbs = styled(Breadcrumbs)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: 18px;\n  margin-bottom: ", ";\n"], ["\n  font-size: 18px;\n  margin-bottom: ", ";\n"])), space(3));
export default BuilderBreadCrumbs;
var templateObject_1;
//# sourceMappingURL=builderBreadCrumbs.jsx.map
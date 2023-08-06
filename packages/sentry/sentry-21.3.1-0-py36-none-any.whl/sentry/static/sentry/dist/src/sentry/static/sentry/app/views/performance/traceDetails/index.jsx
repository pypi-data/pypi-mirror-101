import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import { TraceFullDetailedQuery } from 'app/utils/performance/quickTrace/traceFullQuery';
import { decodeScalar } from 'app/utils/queryString';
import withOrganization from 'app/utils/withOrganization';
import TraceDetailsContent from './content';
var TraceSummary = /** @class */ (function (_super) {
    __extends(TraceSummary, _super);
    function TraceSummary() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TraceSummary.prototype.getTraceSlug = function () {
        var traceSlug = this.props.params.traceSlug;
        return typeof traceSlug === 'string' ? traceSlug.trim() : '';
    };
    TraceSummary.prototype.getDocumentTitle = function () {
        return [t('Trace Details'), t('Performance')].join(' - ');
    };
    TraceSummary.prototype.renderContent = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, params = _a.params;
        var traceSlug = this.getTraceSlug();
        var queryParams = getParams(location.query);
        var start = decodeScalar(queryParams.start);
        var end = decodeScalar(queryParams.end);
        var statsPeriod = decodeScalar(queryParams.statsPeriod);
        var content = function (_a) {
            var isLoading = _a.isLoading, error = _a.error, traces = _a.traces;
            return (<TraceDetailsContent location={location} organization={organization} params={params} traceSlug={traceSlug} start={start} end={end} statsPeriod={statsPeriod} isLoading={isLoading} error={error} traces={traces}/>);
        };
        if (!statsPeriod && (!start || !end)) {
            return content({
                isLoading: false,
                error: 'date selection not specified',
                traces: null,
            });
        }
        return (<TraceFullDetailedQuery location={location} orgSlug={organization.slug} traceId={traceSlug} start={start} end={end} statsPeriod={statsPeriod}>
        {content}
      </TraceFullDetailedQuery>);
    };
    TraceSummary.prototype.render = function () {
        var organization = this.props.organization;
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug}>
        <StyledPageContent>
          <LightWeightNoProjectMessage organization={organization}>
            {this.renderContent()}
          </LightWeightNoProjectMessage>
        </StyledPageContent>
      </SentryDocumentTitle>);
    };
    return TraceSummary;
}(React.Component));
export default withOrganization(TraceSummary);
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var templateObject_1;
//# sourceMappingURL=index.jsx.map
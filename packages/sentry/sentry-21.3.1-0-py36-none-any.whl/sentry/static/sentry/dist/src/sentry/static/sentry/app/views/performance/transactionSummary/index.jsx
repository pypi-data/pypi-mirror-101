import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { loadOrganizationTags } from 'app/actionCreators/tags';
import LightWeightNoProjectMessage from 'app/components/lightWeightNoProjectMessage';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import SentryDocumentTitle from 'app/components/sentryDocumentTitle';
import { t } from 'app/locale';
import { PageContent } from 'app/styles/organization';
import DiscoverQuery from 'app/utils/discover/discoverQuery';
import EventView from 'app/utils/discover/eventView';
import { isAggregateField } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
import { PERCENTILE as VITAL_PERCENTILE, VITAL_GROUPS, } from '../transactionVitals/constants';
import { addRoutePerformanceContext, getTransactionName } from '../utils';
import SummaryContent from './content';
var TransactionSummary = /** @class */ (function (_super) {
    __extends(TransactionSummary, _super);
    function TransactionSummary() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            eventView: generateSummaryEventView(_this.props.location, getTransactionName(_this.props.location), _this.props.organization),
        };
        return _this;
    }
    TransactionSummary.getDerivedStateFromProps = function (nextProps, prevState) {
        return __assign(__assign({}, prevState), { eventView: generateSummaryEventView(nextProps.location, getTransactionName(nextProps.location), nextProps.organization) });
    };
    TransactionSummary.prototype.componentDidMount = function () {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        loadOrganizationTags(api, organization.slug, selection);
        addRoutePerformanceContext(selection);
    };
    TransactionSummary.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, api = _a.api, organization = _a.organization, selection = _a.selection;
        if (!isEqual(prevProps.selection.projects, selection.projects) ||
            !isEqual(prevProps.selection.datetime, selection.datetime)) {
            loadOrganizationTags(api, organization.slug, selection);
            addRoutePerformanceContext(selection);
        }
    };
    TransactionSummary.prototype.getDocumentTitle = function () {
        var name = getTransactionName(this.props.location);
        var hasTransactionName = typeof name === 'string' && String(name).trim().length > 0;
        if (hasTransactionName) {
            return [String(name).trim(), t('Performance')].join(' - ');
        }
        return [t('Summary'), t('Performance')].join(' - ');
    };
    TransactionSummary.prototype.getTotalsEventView = function (organization, eventView) {
        var threshold = organization.apdexThreshold.toString();
        var vitals = VITAL_GROUPS.map(function (_a) {
            var vs = _a.vitals;
            return vs;
        }).reduce(function (keys, vs) {
            vs.forEach(function (vital) { return keys.push(vital); });
            return keys;
        }, []);
        return eventView.withColumns(__spreadArray([
            {
                kind: 'function',
                function: ['apdex', threshold, undefined],
            },
            {
                kind: 'function',
                function: ['count_miserable', 'user', threshold],
            },
            {
                kind: 'function',
                function: ['p95', '', undefined],
            },
            {
                kind: 'function',
                function: ['count', '', undefined],
            },
            {
                kind: 'function',
                function: ['count_unique', 'user', undefined],
            },
            {
                kind: 'function',
                function: ['failure_rate', '', undefined],
            },
            {
                kind: 'function',
                function: ['tpm', '', undefined],
            },
            {
                kind: 'function',
                function: ['user_misery', threshold, undefined],
            }
        ], __read(vitals.map(function (vital) {
            return ({
                kind: 'function',
                function: ['percentile', vital, VITAL_PERCENTILE.toString()],
            });
        }))));
    };
    TransactionSummary.prototype.render = function () {
        var _a = this.props, organization = _a.organization, projects = _a.projects, location = _a.location;
        var eventView = this.state.eventView;
        var transactionName = getTransactionName(location);
        if (!eventView || transactionName === undefined) {
            // If there is no transaction name, redirect to the Performance landing page
            browserHistory.replace({
                pathname: "/organizations/" + organization.slug + "/performance/",
                query: __assign({}, location.query),
            });
            return null;
        }
        var totalsView = this.getTotalsEventView(organization, eventView);
        var shouldForceProject = eventView.project.length === 1;
        var forceProject = shouldForceProject
            ? projects.find(function (p) { return parseInt(p.id, 10) === eventView.project[0]; })
            : undefined;
        var projectSlugs = eventView.project
            .map(function (projectId) { return projects.find(function (p) { return parseInt(p.id, 10) === projectId; }); })
            .filter(function (p) { return p !== undefined; })
            .map(function (p) { return p.slug; });
        return (<SentryDocumentTitle title={this.getDocumentTitle()} orgSlug={organization.slug} projectSlug={forceProject === null || forceProject === void 0 ? void 0 : forceProject.slug}>
        <GlobalSelectionHeader lockedMessageSubject={t('transaction')} shouldForceProject={shouldForceProject} forceProject={forceProject} specificProjectSlugs={projectSlugs} disableMultipleProjectSelection showProjectSettingsLink>
          <StyledPageContent>
            <LightWeightNoProjectMessage organization={organization}>
              <DiscoverQuery eventView={totalsView} orgSlug={organization.slug} location={location} referrer="api.performance.transaction-summary">
                {function (_a) {
                var _b, _c;
                var isLoading = _a.isLoading, error = _a.error, tableData = _a.tableData;
                var totals = (_c = (_b = tableData === null || tableData === void 0 ? void 0 : tableData.data) === null || _b === void 0 ? void 0 : _b[0]) !== null && _c !== void 0 ? _c : null;
                return (<SummaryContent location={location} organization={organization} eventView={eventView} transactionName={transactionName} isLoading={isLoading} error={error} totalValues={totals}/>);
            }}
              </DiscoverQuery>
            </LightWeightNoProjectMessage>
          </StyledPageContent>
        </GlobalSelectionHeader>
      </SentryDocumentTitle>);
    };
    return TransactionSummary;
}(React.Component));
var StyledPageContent = styled(PageContent)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
function generateSummaryEventView(location, transactionName, organization) {
    if (transactionName === undefined) {
        return undefined;
    }
    // Use the user supplied query but overwrite any transaction or event type
    // conditions they applied.
    var query = decodeScalar(location.query.query, '');
    var conditions = tokenizeSearch(query);
    conditions
        .setTagValues('event.type', ['transaction'])
        .setTagValues('transaction', [transactionName]);
    Object.keys(conditions.tagValues).forEach(function (field) {
        if (isAggregateField(field))
            conditions.removeTag(field);
    });
    // Handle duration filters from the latency chart
    if (location.query.startDuration || location.query.endDuration) {
        conditions.setTagValues('transaction.duration', [
            decodeScalar(location.query.startDuration),
            decodeScalar(location.query.endDuration),
        ]
            .filter(function (item) { return item; })
            .map(function (item, index) { return (index === 0 ? ">" + item : "<" + item); }));
    }
    return EventView.fromNewQueryWithLocation({
        id: undefined,
        version: 2,
        name: transactionName,
        fields: organization.features.includes('trace-view-summary')
            ? ['id', 'user.display', 'transaction.duration', 'trace', 'timestamp']
            : ['id', 'user.display', 'transaction.duration', 'timestamp'],
        query: stringifyQueryObject(conditions),
        projects: [],
    }, location);
}
export default withApi(withGlobalSelection(withProjects(withOrganization(TransactionSummary))));
var templateObject_1;
//# sourceMappingURL=index.jsx.map
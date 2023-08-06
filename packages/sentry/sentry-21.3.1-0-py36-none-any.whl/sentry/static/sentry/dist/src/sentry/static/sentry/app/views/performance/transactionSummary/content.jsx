import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import Feature from 'app/components/acl/feature';
import TransactionsList from 'app/components/discover/transactionsList';
import SearchBar from 'app/components/events/searchBar';
import GlobalSdkUpdateAlert from 'app/components/globalSdkUpdateAlert';
import * as Layout from 'app/components/layouts/thirds';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { MAX_QUERY_LENGTH } from 'app/constants';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { generateQueryWithTag } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { getAggregateAlias } from 'app/utils/discover/fields';
import { generateEventSlug } from 'app/utils/discover/urls';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import withProjects from 'app/utils/withProjects';
import { updateQuery } from 'app/views/eventsV2/table/cellAction';
import Tags from 'app/views/eventsV2/tags';
import { getTraceDetailsUrl } from 'app/views/performance/traceDetails/utils';
import { PERCENTILE as VITAL_PERCENTILE, VITAL_GROUPS, } from 'app/views/performance/transactionVitals/constants';
import { getTransactionDetailsUrl } from '../utils';
import TransactionSummaryCharts from './charts';
import Filter, { filterToSearchConditions, SpanOperationBreakdownFilter } from './filter';
import TransactionHeader, { Tab } from './header';
import RelatedIssues from './relatedIssues';
import SidebarCharts from './sidebarCharts';
import StatusBreakdown from './statusBreakdown';
import { TagExplorer } from './tagExplorer';
import UserStats from './userStats';
import { SidebarSpacer, TransactionFilterOptions } from './utils';
var SummaryContent = /** @class */ (function (_super) {
    __extends(SummaryContent, _super);
    function SummaryContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
            spanOperationBreakdownFilter: SpanOperationBreakdownFilter.None,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit(queryParams, 'cursor');
            browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.generateTagUrl = function (key, value) {
            var location = _this.props.location;
            var query = generateQueryWithTag(location.query, { key: key, value: value });
            return __assign(__assign({}, location), { query: query });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.handleCellAction = function (column) {
            return function (action, value) {
                var _a = _this.props, eventView = _a.eventView, location = _a.location;
                var searchConditions = tokenizeSearch(eventView.query);
                // remove any event.type queries since it is implied to apply to only transactions
                searchConditions.removeTag('event.type');
                // no need to include transaction as its already in the query params
                searchConditions.removeTag('transaction');
                updateQuery(searchConditions, action, column.name, value);
                browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { cursor: undefined, query: stringifyQueryObject(searchConditions) }),
                });
            };
        };
        _this.handleTransactionsListSortChange = function (value) {
            var location = _this.props.location;
            var target = {
                pathname: location.pathname,
                query: __assign(__assign({}, location.query), { showTransactions: value, transactionCursor: undefined }),
            };
            browserHistory.push(target);
        };
        _this.handleDiscoverViewClick = function () {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_in_discover',
                eventName: 'Performance Views: View in Discover from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.handleViewDetailsClick = function (_e) {
            var organization = _this.props.organization;
            trackAnalyticsEvent({
                eventKey: 'performance_views.summary.view_details',
                eventName: 'Performance Views: View Details from Transaction Summary',
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.onChangeFilter = function (newFilter) {
            _this.setState({
                spanOperationBreakdownFilter: newFilter,
            });
        };
        return _this;
    }
    SummaryContent.prototype.render = function () {
        var _a;
        var eventView = this.props.eventView;
        var _b = this.props, transactionName = _b.transactionName, location = _b.location, organization = _b.organization, projects = _b.projects, isLoading = _b.isLoading, error = _b.error, totalValues = _b.totalValues;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = decodeScalar(location.query.query, '');
        var totalCount = totalValues === null ? null : totalValues.count;
        var spanOperationBreakdownConditions = filterToSearchConditions(this.state.spanOperationBreakdownFilter);
        if (spanOperationBreakdownConditions) {
            eventView = eventView.clone();
            eventView.query = (eventView.query + " " + spanOperationBreakdownConditions).trim();
        }
        // NOTE: This is not a robust check for whether or not a transaction is a front end
        // transaction, however it will suffice for now.
        var hasWebVitals = totalValues !== null &&
            VITAL_GROUPS.some(function (group) {
                return group.vitals.some(function (vital) {
                    var alias = getAggregateAlias("percentile(" + vital + ", " + VITAL_PERCENTILE + ")");
                    return Number.isFinite(totalValues[alias]);
                });
            });
        return (<React.Fragment>
        <TransactionHeader eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={Tab.TransactionSummary} hasWebVitals={hasWebVitals} handleIncompatibleQuery={this.handleIncompatibleQuery}/>
        <Layout.Body>
          <StyledSdkUpdatesAlert />
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main>
            <Search>
              <Filter organization={organization} currentFilter={this.state.spanOperationBreakdownFilter} onChangeFilter={this.onChangeFilter}/>
              <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch} maxQueryLength={MAX_QUERY_LENGTH}/>
            </Search>
            <TransactionSummaryCharts organization={organization} location={location} eventView={eventView} totalValues={totalCount} currentFilter={this.state.spanOperationBreakdownFilter}/>
            <TransactionsList location={location} organization={organization} eventView={eventView} titles={organization.features.includes('trace-view-summary')
                ? [
                    t('event id'),
                    t('user'),
                    t('duration'),
                    t('trace id'),
                    t('timestamp'),
                ]
                : [t('event id'), t('user'), t('duration'), t('timestamp')]} handleDropdownChange={this.handleTransactionsListSortChange} generateLink={{
                id: generateTransactionLink(transactionName),
                trace: generateTraceLink(eventView.normalizeDateSelection(location)),
            }} baseline={transactionName} handleBaselineClick={this.handleViewDetailsClick} handleCellAction={this.handleCellAction} handleOpenInDiscoverClick={this.handleDiscoverViewClick} {...getTransactionsListSort(location, {
            p95: (_a = totalValues === null || totalValues === void 0 ? void 0 : totalValues.p95) !== null && _a !== void 0 ? _a : 0,
        })} forceLoading={isLoading}/>
            <Feature features={['performance-tag-explorer']}>
              <TagExplorer eventView={eventView} organization={organization} location={location} projects={projects} transactionName={transactionName}/>
            </Feature>
            <RelatedIssues organization={organization} location={location} transaction={transactionName} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
          </Layout.Main>
          <Layout.Side>
            <UserStats organization={organization} location={location} isLoading={isLoading} hasWebVitals={hasWebVitals} error={error} totals={totalValues} transactionName={transactionName} eventView={eventView}/>
            <StatusBreakdown eventView={eventView} organization={organization} location={location}/>
            <SidebarSpacer />
            <SidebarCharts organization={organization} isLoading={isLoading} error={error} totals={totalValues} eventView={eventView}/>
            <SidebarSpacer />
            <Tags generateUrl={this.generateTagUrl} totalValues={totalCount} eventView={eventView} organization={organization} location={location}/>
          </Layout.Side>
        </Layout.Body>
      </React.Fragment>);
    };
    return SummaryContent;
}(React.Component));
function generateTraceLink(dateSelection) {
    return function (organization, tableRow, _query) {
        var traceId = "" + tableRow.trace;
        if (!traceId) {
            return {};
        }
        return getTraceDetailsUrl(organization, traceId, dateSelection, {});
    };
}
function generateTransactionLink(transactionName) {
    return function (organization, tableRow, query) {
        var eventSlug = generateEventSlug(tableRow);
        return getTransactionDetailsUrl(organization, eventSlug, transactionName, query);
    };
}
function getFilterOptions(_a) {
    var p95 = _a.p95;
    return [
        {
            sort: { kind: 'asc', field: 'transaction.duration' },
            value: TransactionFilterOptions.FASTEST,
            label: t('Fastest Transactions'),
        },
        {
            query: [['transaction.duration', "<=" + p95.toFixed(0)]],
            sort: { kind: 'desc', field: 'transaction.duration' },
            value: TransactionFilterOptions.SLOW,
            label: t('Slow Transactions (p95)'),
        },
        {
            sort: { kind: 'desc', field: 'transaction.duration' },
            value: TransactionFilterOptions.OUTLIER,
            label: t('Outlier Transactions (p100)'),
        },
        {
            sort: { kind: 'desc', field: 'timestamp' },
            value: TransactionFilterOptions.RECENT,
            label: t('Recent Transactions'),
        },
    ];
}
function getTransactionsListSort(location, options) {
    var sortOptions = getFilterOptions(options);
    var urlParam = decodeScalar(location.query.showTransactions, TransactionFilterOptions.SLOW);
    var selectedSort = sortOptions.find(function (opt) { return opt.value === urlParam; }) || sortOptions[0];
    return { selected: selectedSort, options: sortOptions };
}
var Search = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  width: 100%;\n  margin-bottom: ", ";\n"])), space(3));
var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledSdkUpdatesAlert = styled(GlobalSdkUpdateAlert)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"], ["\n  @media (min-width: ", ") {\n    margin-bottom: 0;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: function (p) { return <Layout.Main fullWidth {...p}/>; },
};
export default withProjects(SummaryContent);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=content.jsx.map
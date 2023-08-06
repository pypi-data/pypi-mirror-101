import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import { withProfiler } from '@sentry/react';
import Cookies from 'js-cookie';
import isEqual from 'lodash/isEqual';
import mapValues from 'lodash/mapValues';
import omit from 'lodash/omit';
import pickBy from 'lodash/pickBy';
import * as qs from 'query-string';
import { fetchOrgMembers, indexMembersByProject } from 'app/actionCreators/members';
import { deleteSavedSearch, fetchSavedSearches, resetSavedSearches, } from 'app/actionCreators/savedSearches';
import { fetchTagValues, loadOrganizationTags } from 'app/actionCreators/tags';
import GroupActions from 'app/actions/groupActions';
import Feature from 'app/components/acl/feature';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import { extractSelectionParameters } from 'app/components/organizations/globalSelectionHeader/utils';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody } from 'app/components/panels';
import QueryCount from 'app/components/queryCount';
import StreamGroup from 'app/components/stream/group';
import ProcessingIssueList from 'app/components/stream/processingIssueList';
import { DEFAULT_QUERY, DEFAULT_STATS_PERIOD } from 'app/constants';
import { tct } from 'app/locale';
import GroupStore from 'app/stores/groupStore';
import { PageContent } from 'app/styles/organization';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { analytics, logExperiment, metric, trackAnalyticsEvent } from 'app/utils/analytics';
import { callIfFunction } from 'app/utils/callIfFunction';
import CursorPoller from 'app/utils/cursorPoller';
import { getUtcDateString } from 'app/utils/dates';
import getCurrentSentryReactTransaction from 'app/utils/getCurrentSentryReactTransaction';
import parseApiError from 'app/utils/parseApiError';
import parseLinkHeader from 'app/utils/parseLinkHeader';
import StreamManager from 'app/utils/streamManager';
import withApi from 'app/utils/withApi';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withIssueTags from 'app/utils/withIssueTags';
import withOrganization from 'app/utils/withOrganization';
import withSavedSearches from 'app/utils/withSavedSearches';
import IssueListActions from './actions';
import IssueListFilters from './filters';
import IssueListHeader from './header';
import NoGroupsHandler from './noGroupsHandler';
import IssueListSidebar from './sidebar';
import { getTabs, getTabsWithCounts, isForReviewQuery, IssueSortOptions, Query, TAB_MAX_COUNT, } from './utils';
var MAX_ITEMS = 25;
var DEFAULT_SORT = IssueSortOptions.DATE;
// the default period for the graph in each issue row
var DEFAULT_GRAPH_STATS_PERIOD = '24h';
// the allowed period choices for graph in each issue row
var DYNAMIC_COUNTS_STATS_PERIODS = new Set(['14d', '24h', 'auto']);
var IssueListOverview = /** @class */ (function (_super) {
    __extends(IssueListOverview, _super);
    function IssueListOverview() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this._streamManager = new StreamManager(GroupStore);
        _this.getEndpointParams = function () {
            var selection = _this.props.selection;
            var params = __assign({ project: selection.projects, environment: selection.environments, query: _this.getQuery() }, selection.datetime);
            if (selection.datetime.period) {
                delete params.period;
                params.statsPeriod = selection.datetime.period;
            }
            if (params.end) {
                params.end = getUtcDateString(params.end);
            }
            if (params.start) {
                params.start = getUtcDateString(params.start);
            }
            var sort = _this.getSort();
            if (sort !== DEFAULT_SORT) {
                params.sort = sort;
            }
            var groupStatsPeriod = _this.getGroupStatsPeriod();
            if (groupStatsPeriod !== DEFAULT_GRAPH_STATS_PERIOD) {
                params.groupStatsPeriod = groupStatsPeriod;
            }
            // only include defined values.
            return pickBy(params, function (v) { return defined(v); });
        };
        _this.getGlobalSearchProjectIds = function () {
            return _this.props.selection.projects;
        };
        _this.fetchStats = function (groups) {
            // If we have no groups to fetch, just skip stats
            if (!groups.length) {
                return;
            }
            var requestParams = __assign(__assign({}, _this.getEndpointParams()), { groups: groups });
            // If no stats period values are set, use default
            if (!requestParams.statsPeriod && !requestParams.start) {
                requestParams.statsPeriod = DEFAULT_STATS_PERIOD;
            }
            _this._lastStatsRequest = _this.props.api.request(_this.getGroupStatsEndpoint(), {
                method: 'GET',
                data: qs.stringify(requestParams),
                success: function (data) {
                    if (!data) {
                        return;
                    }
                    GroupActions.populateStats(groups, data);
                },
                error: function (err) {
                    _this.setState({
                        error: parseApiError(err),
                    });
                },
                complete: function () {
                    _this._lastStatsRequest = null;
                },
            });
        };
        _this.fetchCounts = function (currentQueryCount, fetchAllCounts) { return __awaiter(_this, void 0, void 0, function () {
            var organization, _queryCounts, queryCounts, endpointParams, tabQueriesWithCounts, currentTabQuery, requestParams, response, e_1, tab;
            var _a;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        organization = this.props.organization;
                        _queryCounts = this.state.queryCounts;
                        queryCounts = __assign({}, _queryCounts);
                        endpointParams = this.getEndpointParams();
                        tabQueriesWithCounts = getTabsWithCounts(organization);
                        currentTabQuery = tabQueriesWithCounts.includes(endpointParams.query)
                            ? endpointParams.query
                            : null;
                        if (!(fetchAllCounts ||
                            !tabQueriesWithCounts.every(function (tabQuery) { return queryCounts[tabQuery] !== undefined; }))) return [3 /*break*/, 4];
                        requestParams = __assign(__assign({}, omit(endpointParams, 'query')), { 
                            // fetch the counts for the tabs whose counts haven't been fetched yet
                            query: tabQueriesWithCounts.filter(function (_query) { return _query !== currentTabQuery; }) });
                        // If no stats period values are set, use default
                        if (!requestParams.statsPeriod && !requestParams.start) {
                            requestParams.statsPeriod = DEFAULT_STATS_PERIOD;
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise(this.getGroupCountsEndpoint(), {
                                method: 'GET',
                                data: qs.stringify(requestParams),
                            })];
                    case 2:
                        response = _b.sent();
                        // Counts coming from the counts endpoint is limited to 100, for >= 100 we display 99+
                        queryCounts = __assign(__assign({}, queryCounts), mapValues(response, function (count) { return ({
                            count: count,
                            hasMore: count > TAB_MAX_COUNT,
                        }); }));
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _b.sent();
                        this.setState({
                            error: parseApiError(e_1),
                        });
                        return [2 /*return*/];
                    case 4:
                        // Update the count based on the exact number of issues, these shown as is
                        if (currentTabQuery) {
                            queryCounts[currentTabQuery] = {
                                count: currentQueryCount,
                                hasMore: false,
                            };
                            tab = (_a = getTabs(organization).find(function (_a) {
                                var _b = __read(_a, 1), tabQuery = _b[0];
                                return currentTabQuery === tabQuery;
                            })) === null || _a === void 0 ? void 0 : _a[1];
                            if (tab && !endpointParams.cursor) {
                                trackAnalyticsEvent({
                                    eventKey: 'issues_tab.viewed',
                                    eventName: 'Viewed Issues Tab',
                                    organization_id: organization.id,
                                    tab: tab.analyticsName,
                                    num_issues: queryCounts[currentTabQuery].count,
                                });
                            }
                        }
                        this.setState({ queryCounts: queryCounts });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.fetchData = function (fetchAllCounts) {
            if (fetchAllCounts === void 0) { fetchAllCounts = false; }
            GroupStore.loadInitialData([]);
            _this._streamManager.reset();
            var transaction = getCurrentSentryReactTransaction();
            transaction === null || transaction === void 0 ? void 0 : transaction.setTag('query.sort', _this.getSort());
            _this.setState({
                issuesLoading: true,
                queryCount: 0,
                itemsRemoved: 0,
                error: null,
            });
            var requestParams = __assign(__assign({}, _this.getEndpointParams()), { limit: MAX_ITEMS, shortIdLookup: 1 });
            var currentQuery = _this.props.location.query || {};
            if ('cursor' in currentQuery) {
                requestParams.cursor = currentQuery.cursor;
            }
            // If no stats period values are set, use default
            if (!requestParams.statsPeriod && !requestParams.start) {
                requestParams.statsPeriod = DEFAULT_STATS_PERIOD;
            }
            var orgFeatures = new Set(_this.props.organization.features);
            var expandParams = ['owners'];
            if (orgFeatures.has('inbox')) {
                expandParams.push('inbox');
            }
            if (expandParams.length) {
                requestParams.expand = expandParams;
            }
            requestParams.collapse = 'stats';
            if (_this._lastRequest) {
                _this._lastRequest.cancel();
            }
            if (_this._lastStatsRequest) {
                _this._lastStatsRequest.cancel();
            }
            _this._poller.disable();
            _this._lastRequest = _this.props.api.request(_this.getGroupListEndpoint(), {
                method: 'GET',
                data: qs.stringify(requestParams),
                success: function (data, _, jqXHR) {
                    if (!jqXHR) {
                        return;
                    }
                    var orgId = _this.props.params.orgId;
                    // If this is a direct hit, we redirect to the intended result directly.
                    if (jqXHR.getResponseHeader('X-Sentry-Direct-Hit') === '1') {
                        var redirect = void 0;
                        if (data[0] && data[0].matchingEventId) {
                            var _a = data[0], id = _a.id, matchingEventId = _a.matchingEventId;
                            redirect = "/organizations/" + orgId + "/issues/" + id + "/events/" + matchingEventId + "/";
                        }
                        else {
                            var id = data[0].id;
                            redirect = "/organizations/" + orgId + "/issues/" + id + "/";
                        }
                        browserHistory.replace({
                            pathname: redirect,
                            query: extractSelectionParameters(_this.props.location.query),
                        });
                        return;
                    }
                    _this._streamManager.push(data);
                    _this.fetchStats(data.map(function (group) { return group.id; }));
                    var hits = jqXHR.getResponseHeader('X-Hits');
                    var queryCount = typeof hits !== 'undefined' && hits ? parseInt(hits, 10) || 0 : 0;
                    var maxHits = jqXHR.getResponseHeader('X-Max-Hits');
                    var queryMaxCount = typeof maxHits !== 'undefined' && maxHits ? parseInt(maxHits, 10) || 0 : 0;
                    var pageLinks = jqXHR.getResponseHeader('Link');
                    if (_this.props.organization.features.includes('inbox')) {
                        _this.fetchCounts(queryCount, fetchAllCounts);
                    }
                    _this.setState({
                        error: null,
                        issuesLoading: false,
                        queryCount: queryCount,
                        queryMaxCount: queryMaxCount,
                        pageLinks: pageLinks !== null ? pageLinks : '',
                    });
                },
                error: function (err) {
                    _this.setState({
                        error: parseApiError(err),
                        issuesLoading: false,
                    });
                },
                complete: function () {
                    _this._lastRequest = null;
                    _this.resumePolling();
                },
            });
        };
        _this.resumePolling = function () {
            if (!_this.state.pageLinks) {
                return;
            }
            // Only resume polling if we're on the first page of results
            var links = parseLinkHeader(_this.state.pageLinks);
            if (links && !links.previous.results && _this.state.realtimeActive) {
                // Remove collapse stats from endpoint before supplying to poller
                var issueEndpoint = new URL(links.previous.href);
                issueEndpoint.searchParams.delete('collapse');
                _this._poller.setEndpoint(decodeURIComponent(issueEndpoint.href));
                _this._poller.enable();
            }
        };
        _this.onRealtimeChange = function (realtime) {
            Cookies.set('realtimeActive', realtime.toString());
            _this.setState({ realtimeActive: realtime });
        };
        _this.onSelectStatsPeriod = function (period) {
            if (period !== _this.getGroupStatsPeriod()) {
                _this.transitionTo({ groupStatsPeriod: period });
            }
        };
        _this.onRealtimePoll = function (data, _links) {
            // Note: We do not update state with cursors from polling,
            // `CursorPoller` updates itself with new cursors
            _this._streamManager.unshift(data);
        };
        _this.listener = GroupStore.listen(function () { return _this.onGroupChange(); }, undefined);
        _this.onIssueListSidebarSearch = function (query) {
            analytics('search.searched', {
                org_id: _this.props.organization.id,
                query: query,
                search_type: 'issues',
                search_source: 'search_builder',
            });
            _this.onSearch(query);
        };
        _this.onSearch = function (query) {
            if (query === _this.state.query) {
                // if query is the same, just re-fetch data
                _this.fetchData();
            }
            else {
                // Clear the saved search as the user wants something else.
                _this.transitionTo({ query: query }, null);
            }
        };
        _this.onSortChange = function (sort) {
            _this.transitionTo({ sort: sort });
        };
        _this.onCursorChange = function (cursor, _path, query, pageDiff) {
            var queryPageInt = parseInt(query.page, 10);
            var nextPage = isNaN(queryPageInt)
                ? pageDiff
                : queryPageInt + pageDiff;
            // unset cursor and page when we navigate back to the first page
            // also reset cursor if somehow the previous button is enabled on
            // first page and user attempts to go backwards
            if (nextPage <= 0) {
                cursor = undefined;
                nextPage = undefined;
            }
            _this.transitionTo({ cursor: cursor, page: nextPage });
        };
        _this.onSidebarToggle = function () {
            var organization = _this.props.organization;
            _this.setState({
                isSidebarVisible: !_this.state.isSidebarVisible,
                renderSidebar: true,
            });
            analytics('issue.search_sidebar_clicked', {
                org_id: parseInt(organization.id, 10),
            });
        };
        _this.transitionTo = function (newParams, savedSearch) {
            if (newParams === void 0) { newParams = {}; }
            if (savedSearch === void 0) { savedSearch = _this.props.savedSearch; }
            var query = __assign(__assign({}, _this.getEndpointParams()), newParams);
            var organization = _this.props.organization;
            var path;
            if (savedSearch && savedSearch.id) {
                path = "/organizations/" + organization.slug + "/issues/searches/" + savedSearch.id + "/";
                // Remove the query as saved searches bring their own query string.
                delete query.query;
                // If we aren't going to another page in the same search
                // drop the query and replace the current project, with the saved search search project
                // if available.
                if (!query.cursor && savedSearch.projectId) {
                    query.project = [savedSearch.projectId];
                }
                if (!query.cursor && !newParams.sort && savedSearch.sort) {
                    query.sort = savedSearch.sort;
                }
            }
            else {
                path = "/organizations/" + organization.slug + "/issues/";
            }
            // Remove inbox tab specific sort
            if (query.sort === IssueSortOptions.INBOX && query.query !== Query.FOR_REVIEW) {
                delete query.sort;
            }
            if (path !== _this.props.location.pathname ||
                !isEqual(query, _this.props.location.query)) {
                browserHistory.push({
                    pathname: path,
                    query: query,
                });
                _this.setState({ issuesLoading: true });
            }
        };
        _this.renderGroupNodes = function (ids, groupStatsPeriod) {
            var topIssue = ids[0];
            var memberList = _this.state.memberList;
            var query = _this.getQuery();
            var showInboxTime = _this.getSort() === 'inbox';
            return ids.map(function (id, index) {
                var hasGuideAnchor = id === topIssue;
                var group = GroupStore.get(id);
                var members;
                if (group === null || group === void 0 ? void 0 : group.project) {
                    members = memberList[group.project.slug];
                }
                var showReprocessingTab = _this.displayReprocessingTab();
                var displayReprocessingLayout = _this.displayReprocessingLayout(showReprocessingTab, query);
                return (<StreamGroup index={index} key={id} id={id} statsPeriod={groupStatsPeriod} query={query} hasGuideAnchor={hasGuideAnchor} memberList={members} displayReprocessingLayout={displayReprocessingLayout} useFilteredStats showInboxTime={showInboxTime}/>);
            });
        };
        _this.fetchSavedSearches = function () {
            var organization = _this.props.organization;
            fetchSavedSearches(_this.props.api, organization.slug);
        };
        _this.onSavedSearchSelect = function (savedSearch) {
            _this.setState({ issuesLoading: true }, function () { return _this.transitionTo(undefined, savedSearch); });
        };
        _this.onSavedSearchDelete = function (search) {
            var orgId = _this.props.params.orgId;
            deleteSavedSearch(_this.props.api, orgId, search).then(function () {
                _this.setState({
                    issuesLoading: true,
                }, function () { return _this.transitionTo({}, null); });
            });
        };
        _this.onDelete = function () {
            _this.fetchData(true);
        };
        _this.onMarkReviewed = function (itemIds) {
            var _a;
            var query = _this.getQuery();
            if (!isForReviewQuery(query)) {
                return;
            }
            var _b = _this.state, queryCounts = _b.queryCounts, itemsRemoved = _b.itemsRemoved;
            var currentQueryCount = queryCounts[query];
            if (itemIds.length && currentQueryCount) {
                var inInboxCount = itemIds.filter(function (id) { var _a; return (_a = GroupStore.get(id)) === null || _a === void 0 ? void 0 : _a.inbox; }).length;
                currentQueryCount.count -= inInboxCount;
                _this.setState({
                    queryCounts: __assign(__assign({}, queryCounts), (_a = {}, _a[query] = currentQueryCount, _a)),
                    itemsRemoved: itemsRemoved + inInboxCount,
                });
            }
        };
        _this.tagValueLoader = function (key, search) {
            var orgId = _this.props.params.orgId;
            var projectIds = _this.getGlobalSearchProjectIds().map(function (id) { return id.toString(); });
            var endpointParams = _this.getEndpointParams();
            return fetchTagValues(_this.props.api, orgId, key, search, projectIds, endpointParams);
        };
        return _this;
    }
    IssueListOverview.prototype.getInitialState = function () {
        var realtimeActiveCookie = Cookies.get('realtimeActive');
        var realtimeActive = typeof realtimeActiveCookie === 'undefined'
            ? false
            : realtimeActiveCookie === 'true';
        return {
            groupIds: [],
            selectAllActive: false,
            realtimeActive: realtimeActive,
            pageLinks: '',
            itemsRemoved: 0,
            queryCount: 0,
            queryCounts: {},
            queryMaxCount: 0,
            error: null,
            isSidebarVisible: false,
            renderSidebar: false,
            issuesLoading: true,
            tagsLoading: true,
            memberList: {},
        };
    };
    IssueListOverview.prototype.componentDidMount = function () {
        var _a;
        var links = parseLinkHeader(this.state.pageLinks);
        this._poller = new CursorPoller({
            endpoint: ((_a = links.previous) === null || _a === void 0 ? void 0 : _a.href) || '',
            success: this.onRealtimePoll,
        });
        // Start by getting searches first so if the user is on a saved search
        // or they have a pinned search we load the correct data the first time.
        this.fetchSavedSearches();
        this.fetchTags();
        this.fetchMemberList();
        this.logInboxExperiment();
    };
    IssueListOverview.prototype.componentDidUpdate = function (prevProps, prevState) {
        // Fire off profiling/metrics first
        if (prevState.issuesLoading && !this.state.issuesLoading) {
            // First Meaningful Paint for /organizations/:orgId/issues/
            if (prevState.queryCount === null) {
                metric.measure({
                    name: 'app.page.perf.issue-list',
                    start: 'page-issue-list-start',
                    data: {
                        // start_type is set on 'page-issue-list-start'
                        org_id: parseInt(this.props.organization.id, 10),
                        group: this.props.organization.features.includes('enterprise-perf')
                            ? 'enterprise-perf'
                            : 'control',
                        milestone: 'first-meaningful-paint',
                        is_enterprise: this.props.organization.features
                            .includes('enterprise-orgs')
                            .toString(),
                        is_outlier: this.props.organization.features
                            .includes('enterprise-orgs-outliers')
                            .toString(),
                    },
                });
                metric.endTransaction({ name: '/organizations/:orgId/issues/' });
            }
        }
        if (prevState.realtimeActive !== this.state.realtimeActive) {
            // User toggled realtime button
            if (this.state.realtimeActive) {
                this.resumePolling();
            }
            else {
                this._poller.disable();
            }
        }
        // If the project selection has changed reload the member list and tag keys
        // allowing autocomplete and tag sidebar to be more accurate.
        if (!isEqual(prevProps.selection.projects, this.props.selection.projects)) {
            this.fetchMemberList();
            this.fetchTags();
        }
        // Wait for saved searches to load before we attempt to fetch stream data
        if (this.props.savedSearchLoading) {
            return;
        }
        else if (prevProps.savedSearchLoading) {
            this.fetchData();
            return;
        }
        var prevQuery = prevProps.location.query;
        var newQuery = this.props.location.query;
        var selectionChanged = !isEqual(prevProps.selection, this.props.selection);
        // If any important url parameter changed or saved search changed
        // reload data.
        if (selectionChanged ||
            prevQuery.cursor !== newQuery.cursor ||
            prevQuery.sort !== newQuery.sort ||
            prevQuery.query !== newQuery.query ||
            prevQuery.statsPeriod !== newQuery.statsPeriod ||
            prevQuery.groupStatsPeriod !== newQuery.groupStatsPeriod ||
            prevProps.savedSearch !== this.props.savedSearch) {
            this.fetchData(selectionChanged);
        }
        else if (!this._lastRequest &&
            prevState.issuesLoading === false &&
            this.state.issuesLoading) {
            // Reload if we issues are loading or their loading state changed.
            // This can happen when transitionTo is called
            this.fetchData();
        }
    };
    IssueListOverview.prototype.componentWillUnmount = function () {
        this._poller.disable();
        GroupStore.reset();
        this.props.api.clear();
        callIfFunction(this.listener);
        // Reset store when unmounting because we always fetch on mount
        // This means if you navigate away from stream and then back to stream,
        // this component will go from:
        // "ready" ->
        // "loading" (because fetching saved searches) ->
        // "ready"
        //
        // We don't render anything until saved searches is ready, so this can
        // cause weird side effects (e.g. ProcessingIssueList mounting and making
        // a request, but immediately unmounting when fetching saved searches)
        resetSavedSearches();
    };
    IssueListOverview.prototype.getQuery = function () {
        var _a = this.props, savedSearch = _a.savedSearch, organization = _a.organization, location = _a.location;
        if (savedSearch) {
            return savedSearch.query;
        }
        var query = location.query.query;
        if (query !== undefined) {
            return query;
        }
        if (organization.features.includes('inbox') &&
            organization.features.includes('inbox-tab-default')) {
            return Query.FOR_REVIEW;
        }
        return DEFAULT_QUERY;
    };
    IssueListOverview.prototype.getSort = function () {
        var _a = this.props, location = _a.location, savedSearch = _a.savedSearch;
        if (!location.query.sort && (savedSearch === null || savedSearch === void 0 ? void 0 : savedSearch.id)) {
            return savedSearch.sort;
        }
        if (location.query.sort) {
            return location.query.sort;
        }
        var organization = this.props.organization;
        if (organization.features.includes('inbox') &&
            organization.features.includes('inbox-tab-default') &&
            this.getQuery() === Query.FOR_REVIEW) {
            return IssueSortOptions.INBOX;
        }
        return DEFAULT_SORT;
    };
    IssueListOverview.prototype.getGroupStatsPeriod = function () {
        var _a;
        var currentPeriod;
        if (typeof ((_a = this.props.location.query) === null || _a === void 0 ? void 0 : _a.groupStatsPeriod) === 'string') {
            currentPeriod = this.props.location.query.groupStatsPeriod;
        }
        else if (this.getSort() === IssueSortOptions.TREND) {
            // Default to the larger graph when sorting by relative change
            currentPeriod = 'auto';
        }
        else {
            currentPeriod = DEFAULT_GRAPH_STATS_PERIOD;
        }
        return DYNAMIC_COUNTS_STATS_PERIODS.has(currentPeriod)
            ? currentPeriod
            : DEFAULT_GRAPH_STATS_PERIOD;
    };
    IssueListOverview.prototype.fetchMemberList = function () {
        var _this = this;
        var _a;
        var projectIds = (_a = this.getGlobalSearchProjectIds()) === null || _a === void 0 ? void 0 : _a.map(function (projectId) {
            return String(projectId);
        });
        fetchOrgMembers(this.props.api, this.props.organization.slug, projectIds).then(function (members) {
            _this.setState({ memberList: indexMembersByProject(members) });
        });
    };
    IssueListOverview.prototype.fetchTags = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selection = _a.selection;
        this.setState({ tagsLoading: true });
        loadOrganizationTags(this.props.api, organization.slug, selection).then(function () {
            return _this.setState({ tagsLoading: false });
        });
    };
    IssueListOverview.prototype.getGroupListEndpoint = function () {
        var orgId = this.props.params.orgId;
        return "/organizations/" + orgId + "/issues/";
    };
    IssueListOverview.prototype.getGroupCountsEndpoint = function () {
        var orgId = this.props.params.orgId;
        return "/organizations/" + orgId + "/issues-count/";
    };
    IssueListOverview.prototype.getGroupStatsEndpoint = function () {
        var orgId = this.props.params.orgId;
        return "/organizations/" + orgId + "/issues-stats/";
    };
    IssueListOverview.prototype.logInboxExperiment = function () {
        var _a;
        var organization = this.props.organization;
        // Only log users in experiment
        if ([0, 1].includes((_a = organization.experiments) === null || _a === void 0 ? void 0 : _a.InboxExperiment)) {
            logExperiment({ organization: organization, key: 'InboxExperiment' });
        }
    };
    IssueListOverview.prototype.onGroupChange = function () {
        var _a;
        var groupIds = (_a = this._streamManager.getAllItems().map(function (item) { return item.id; })) !== null && _a !== void 0 ? _a : [];
        if (!isEqual(groupIds, this.state.groupIds)) {
            this.setState({ groupIds: groupIds });
        }
    };
    /**
     * Returns true if all results in the current query are visible/on this page
     */
    IssueListOverview.prototype.allResultsVisible = function () {
        if (!this.state.pageLinks) {
            return false;
        }
        var links = parseLinkHeader(this.state.pageLinks);
        return links && !links.previous.results && !links.next.results;
    };
    IssueListOverview.prototype.displayReprocessingTab = function () {
        var _a;
        var organization = this.props.organization;
        var queryCounts = this.state.queryCounts;
        return (organization.features.includes('reprocessing-v2') &&
            !!((_a = queryCounts === null || queryCounts === void 0 ? void 0 : queryCounts[Query.REPROCESSING]) === null || _a === void 0 ? void 0 : _a.count));
    };
    IssueListOverview.prototype.displayReprocessingLayout = function (showReprocessingTab, query) {
        return showReprocessingTab && query === Query.REPROCESSING;
    };
    IssueListOverview.prototype.renderLoading = function () {
        return (<StyledPageContent>
        <LoadingIndicator />
      </StyledPageContent>);
    };
    IssueListOverview.prototype.renderStreamBody = function () {
        var _a = this.state, issuesLoading = _a.issuesLoading, error = _a.error, groupIds = _a.groupIds;
        if (issuesLoading) {
            return this.renderLoading();
        }
        if (error) {
            return <LoadingError message={error} onRetry={this.fetchData}/>;
        }
        if (groupIds.length > 0) {
            return (<PanelBody>
          {this.renderGroupNodes(groupIds, this.getGroupStatsPeriod())}
        </PanelBody>);
        }
        var _b = this.props, api = _b.api, organization = _b.organization, selection = _b.selection;
        return (<NoGroupsHandler api={api} organization={organization} query={this.getQuery()} selectedProjectIds={selection.projects} groupIds={groupIds}/>);
    };
    IssueListOverview.prototype.render = function () {
        var _this = this;
        var _a, _b, _c, _d, _e, _f, _g;
        if (this.props.savedSearchLoading) {
            return this.renderLoading();
        }
        var _h = this.state, renderSidebar = _h.renderSidebar, isSidebarVisible = _h.isSidebarVisible, tagsLoading = _h.tagsLoading, pageLinks = _h.pageLinks, queryCount = _h.queryCount, queryCounts = _h.queryCounts, realtimeActive = _h.realtimeActive, groupIds = _h.groupIds, queryMaxCount = _h.queryMaxCount, itemsRemoved = _h.itemsRemoved;
        var _j = this.props, organization = _j.organization, savedSearch = _j.savedSearch, savedSearches = _j.savedSearches, tags = _j.tags, selection = _j.selection, location = _j.location, router = _j.router;
        var links = parseLinkHeader(pageLinks);
        var query = this.getQuery();
        var queryPageInt = parseInt(location.query.page, 10);
        // Cursor must be present for the page number to be used
        var page = isNaN(queryPageInt) || !location.query.cursor ? 0 : queryPageInt;
        var pageBasedCount = page * MAX_ITEMS + groupIds.length;
        var pageCount = pageBasedCount > queryCount ? queryCount : pageBasedCount;
        if (!((_a = links === null || links === void 0 ? void 0 : links.next) === null || _a === void 0 ? void 0 : _a.results) || this.allResultsVisible()) {
            // On last available page
            pageCount = queryCount;
        }
        else if (!((_b = links === null || links === void 0 ? void 0 : links.previous) === null || _b === void 0 ? void 0 : _b.results)) {
            // On first available page
            pageCount = groupIds.length;
        }
        // Subtract # items that have been marked reviewed
        pageCount = Math.max(pageCount - itemsRemoved, 0);
        var modifiedQueryCount = Math.max(queryCount - itemsRemoved, 0);
        var displayCount = tct('[count] of [total]', {
            count: pageCount,
            total: (<StyledQueryCount hideParens hideIfEmpty={false} count={modifiedQueryCount} max={queryMaxCount || 100}/>),
        });
        // TODO(workflow): When organization:inbox flag is removed add 'inbox' to tagStore
        if (organization.features.includes('inbox') &&
            !((_d = (_c = tags === null || tags === void 0 ? void 0 : tags.is) === null || _c === void 0 ? void 0 : _c.values) === null || _d === void 0 ? void 0 : _d.includes('for_review'))) {
            (_f = (_e = tags === null || tags === void 0 ? void 0 : tags.is) === null || _e === void 0 ? void 0 : _e.values) === null || _f === void 0 ? void 0 : _f.push('for_review');
        }
        var projectIds = (_g = selection === null || selection === void 0 ? void 0 : selection.projects) === null || _g === void 0 ? void 0 : _g.map(function (p) { return p.toString(); });
        var orgSlug = organization.slug;
        var showReprocessingTab = this.displayReprocessingTab();
        var displayReprocessingActions = this.displayReprocessingLayout(showReprocessingTab, query);
        return (<Feature organization={organization} features={['organizations:inbox']}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                return (<React.Fragment>
            {hasFeature && (<IssueListHeader organization={organization} query={query} sort={_this.getSort()} queryCount={queryCount} queryCounts={queryCounts} realtimeActive={realtimeActive} onRealtimeChange={_this.onRealtimeChange} projectIds={projectIds} orgSlug={orgSlug} router={router} savedSearchList={savedSearches} onSavedSearchSelect={_this.onSavedSearchSelect} onSavedSearchDelete={_this.onSavedSearchDelete} displayReprocessingTab={showReprocessingTab}/>)}
            <StyledPageContent isInbox={hasFeature}>
              <StreamContent showSidebar={isSidebarVisible}>
                <IssueListFilters organization={organization} query={query} savedSearch={savedSearch} sort={_this.getSort()} queryCount={queryCount} queryMaxCount={queryMaxCount} onSortChange={_this.onSortChange} onSearch={_this.onSearch} onSavedSearchSelect={_this.onSavedSearchSelect} onSavedSearchDelete={_this.onSavedSearchDelete} onSidebarToggle={_this.onSidebarToggle} isSearchDisabled={isSidebarVisible} savedSearchList={savedSearches} tagValueLoader={_this.tagValueLoader} tags={tags} isInbox={hasFeature}/>

                <Panel>
                  <IssueListActions organization={organization} selection={selection} query={query} queryCount={modifiedQueryCount} displayCount={displayCount} onSelectStatsPeriod={_this.onSelectStatsPeriod} onRealtimeChange={_this.onRealtimeChange} onMarkReviewed={_this.onMarkReviewed} onDelete={_this.onDelete} realtimeActive={realtimeActive} statsPeriod={_this.getGroupStatsPeriod()} groupIds={groupIds} allResultsVisible={_this.allResultsVisible()} hasInbox={hasFeature} displayReprocessingActions={displayReprocessingActions}/>
                  <PanelBody>
                    <ProcessingIssueList organization={organization} projectIds={projectIds} showProject/>
                    {_this.renderStreamBody()}
                  </PanelBody>
                </Panel>
                <PaginationWrapper>
                  {hasFeature && (groupIds === null || groupIds === void 0 ? void 0 : groupIds.length) > 0 && (<div>
                      {/* total includes its own space */}
                      {tct('Showing [displayCount] issues', {
                            displayCount: displayCount,
                        })}
                    </div>)}
                  <StyledPagination pageLinks={pageLinks} onCursor={_this.onCursorChange}/>
                </PaginationWrapper>
              </StreamContent>

              <SidebarContainer showSidebar={isSidebarVisible}>
                {/* Avoid rendering sidebar until first accessed */}
                {renderSidebar && (<IssueListSidebar loading={tagsLoading} tags={tags} query={query} onQueryChange={_this.onIssueListSidebarSearch} tagValueLoader={_this.tagValueLoader}/>)}
              </SidebarContainer>
            </StyledPageContent>

            {hasFeature && query === Query.FOR_REVIEW && (<GuideAnchor target="is_inbox_tab"/>)}
          </React.Fragment>);
            }}
      </Feature>);
    };
    return IssueListOverview;
}(React.Component));
export default withApi(withGlobalSelection(withSavedSearches(withOrganization(withIssueTags(withProfiler(IssueListOverview))))));
export { IssueListOverview };
// TODO(workflow): Replace PageContent with thirds body
var StyledPageContent = styled(PageContent)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  ", "\n\n  @media (max-width: ", ") {\n    /* Matches thirds layout */\n    padding: ", " ", " 0 ", ";\n  }\n"], ["\n  display: flex;\n  flex-direction: row;\n  ",
    "\n\n  @media (max-width: ", ") {\n    /* Matches thirds layout */\n    padding: ", " ", " 0 ", ";\n  }\n"])), function (p) {
    return p.isInbox && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      background-color: ", ";\n    "], ["\n      background-color: ", ";\n    "])), p.theme.background);
}, function (p) { return p.theme.breakpoints[0]; }, space(2), space(2), space(2));
var StreamContent = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n\n  @media (max-width: ", ") {\n    width: 100%;\n  }\n"], ["\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n\n  @media (max-width: ", ") {\n    width: 100%;\n  }\n"])), function (p) { return (p.showSidebar ? '75%' : '100%'); }, function (p) { return p.theme.breakpoints[0]; });
var SidebarContainer = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: ", ";\n  overflow: ", ";\n  height: ", ";\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n  margin-left: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  display: ", ";\n  overflow: ", ";\n  height: ", ";\n  width: ", ";\n  transition: width 0.2s ease-in-out;\n  margin-left: 20px;\n\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return (p.showSidebar ? 'block' : 'none'); }, function (p) { return (p.showSidebar ? 'visible' : 'hidden'); }, function (p) { return (p.showSidebar ? 'auto' : 0); }, function (p) { return (p.showSidebar ? '25%' : 0); }, function (p) { return p.theme.breakpoints[0]; });
var PaginationWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: center;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledPagination = styled(Pagination)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-top: 0;\n  margin-left: ", ";\n"], ["\n  margin-top: 0;\n  margin-left: ", ";\n"])), space(2));
var StyledQueryCount = styled(QueryCount)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-left: 0;\n"], ["\n  margin-left: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=overview.jsx.map
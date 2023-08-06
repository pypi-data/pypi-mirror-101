import { __assign, __extends, __makeTemplateObject, __read, __rest } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import classNames from 'classnames';
// eslint-disable-next-line no-restricted-imports
import { Box } from 'reflexbox';
import AssigneeSelector from 'app/components/assigneeSelector';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Count from 'app/components/count';
import DropdownMenu from 'app/components/dropdownMenu';
import EventOrGroupExtraDetails from 'app/components/eventOrGroupExtraDetails';
import EventOrGroupHeader from 'app/components/eventOrGroupHeader';
import Link from 'app/components/links/link';
import MenuItem from 'app/components/menuItem';
import { getRelativeSummary } from 'app/components/organizations/timeRangeSelector/utils';
import { PanelItem } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import ProgressBar from 'app/components/progressBar';
import GroupChart from 'app/components/stream/groupChart';
import GroupCheckBox from 'app/components/stream/groupCheckBox';
import TimeSince from 'app/components/timeSince';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { t } from 'app/locale';
import GroupStore from 'app/stores/groupStore';
import SelectedGroupStore from 'app/stores/selectedGroupStore';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined, percent, valueIsEqual } from 'app/utils';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { callIfFunction } from 'app/utils/callIfFunction';
import EventView from 'app/utils/discover/eventView';
import { queryToObj } from 'app/utils/stream';
import withGlobalSelection from 'app/utils/withGlobalSelection';
import withOrganization from 'app/utils/withOrganization';
import { getTabs, isForReviewQuery, Query } from 'app/views/issueList/utils';
var DiscoveryExclusionFields = [
    'query',
    'status',
    'bookmarked_by',
    'assigned',
    'assigned_to',
    'unassigned',
    'subscribed_by',
    'active_at',
    'first_release',
    'first_seen',
    'is',
    '__text',
];
export var DEFAULT_STREAM_GROUP_STATS_PERIOD = '24h';
var defaultProps = {
    statsPeriod: DEFAULT_STREAM_GROUP_STATS_PERIOD,
    canSelect: true,
    withChart: true,
    useFilteredStats: false,
};
var StreamGroup = /** @class */ (function (_super) {
    __extends(StreamGroup, _super);
    function StreamGroup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.listener = GroupStore.listen(function (itemIds) { return _this.onGroupChange(itemIds); }, undefined);
        _this.trackClick = function () {
            var _a = _this.props, query = _a.query, organization = _a.organization;
            var data = _this.state.data;
            if (query === Query.FOR_REVIEW) {
                trackAnalyticsEvent({
                    eventKey: 'inbox_tab.issue_clicked',
                    eventName: 'Clicked Issue from Inbox Tab',
                    organization_id: organization.id,
                    group_id: data.id,
                });
            }
            if (query !== undefined) {
                trackAnalyticsEvent(__assign({ eventKey: 'issues_stream.issue_clicked', eventName: 'Clicked Issue from Issues Stream' }, _this.sharedAnalytics()));
            }
        };
        _this.trackAssign = function (type, _assignee, suggestedAssignee) {
            var query = _this.props.query;
            if (query !== undefined) {
                trackAnalyticsEvent(__assign(__assign({ eventKey: 'issues_stream.issue_assigned', eventName: 'Assigned Issue from Issues Stream' }, _this.sharedAnalytics()), { did_assign_suggestion: !!suggestedAssignee, assigned_suggestion_reason: suggestedAssignee === null || suggestedAssignee === void 0 ? void 0 : suggestedAssignee.suggestedReason, assigned_type: type }));
            }
        };
        _this.toggleSelect = function (evt) {
            var _a, _b, _c;
            var targetElement = evt.target;
            if (((_a = targetElement === null || targetElement === void 0 ? void 0 : targetElement.tagName) === null || _a === void 0 ? void 0 : _a.toLowerCase()) === 'a') {
                return;
            }
            if (((_b = targetElement === null || targetElement === void 0 ? void 0 : targetElement.tagName) === null || _b === void 0 ? void 0 : _b.toLowerCase()) === 'input') {
                return;
            }
            var e = targetElement;
            while (e.parentElement) {
                if (((_c = e === null || e === void 0 ? void 0 : e.tagName) === null || _c === void 0 ? void 0 : _c.toLowerCase()) === 'a') {
                    return;
                }
                e = e.parentElement;
            }
            SelectedGroupStore.toggleSelect(_this.state.data.id);
        };
        return _this;
    }
    StreamGroup.prototype.getInitialState = function () {
        var _a = this.props, id = _a.id, useFilteredStats = _a.useFilteredStats;
        var data = GroupStore.get(id);
        return {
            data: __assign(__assign({}, data), { filtered: useFilteredStats ? data.filtered : null }),
            reviewed: false,
        };
    };
    StreamGroup.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.id !== this.props.id ||
            nextProps.useFilteredStats !== this.props.useFilteredStats) {
            var data = GroupStore.get(this.props.id);
            this.setState({
                data: __assign(__assign({}, data), { filtered: nextProps.useFilteredStats ? data.filtered : null }),
            });
        }
    };
    StreamGroup.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        if (nextProps.statsPeriod !== this.props.statsPeriod) {
            return true;
        }
        if (!valueIsEqual(this.state.data, nextState.data)) {
            return true;
        }
        return false;
    };
    StreamGroup.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    StreamGroup.prototype.onGroupChange = function (itemIds) {
        var _a = this.props, id = _a.id, query = _a.query;
        if (!itemIds.has(id)) {
            return;
        }
        var data = GroupStore.get(id);
        this.setState(function (state) {
            var _a;
            // When searching is:for_review and the inbox reason is removed
            var reviewed = state.reviewed ||
                (isForReviewQuery(query) &&
                    ((_a = state.data.inbox) === null || _a === void 0 ? void 0 : _a.reason) !== undefined &&
                    data.inbox === false);
            return { data: data, reviewed: reviewed };
        });
    };
    /** Shared between two events */
    StreamGroup.prototype.sharedAnalytics = function () {
        var _a;
        var _b = this.props, query = _b.query, organization = _b.organization;
        var data = this.state.data;
        var tab = (_a = getTabs(organization).find(function (_a) {
            var _b = __read(_a, 1), tabQuery = _b[0];
            return tabQuery === query;
        })) === null || _a === void 0 ? void 0 : _a[1];
        var owners = (data === null || data === void 0 ? void 0 : data.owners) || [];
        return {
            organization_id: organization.id,
            group_id: data.id,
            tab: (tab === null || tab === void 0 ? void 0 : tab.analyticsName) || 'other',
            was_shown_suggestion: owners.length > 0,
        };
    };
    StreamGroup.prototype.getDiscoverUrl = function (isFiltered) {
        var _a = this.props, organization = _a.organization, query = _a.query, selection = _a.selection, customStatsPeriod = _a.customStatsPeriod;
        var data = this.state.data;
        // when there is no discover feature open events page
        var hasDiscoverQuery = organization.features.includes('discover-basic');
        var queryTerms = [];
        if (isFiltered && typeof query === 'string') {
            var queryObj = queryToObj(query);
            for (var queryTag in queryObj)
                if (!DiscoveryExclusionFields.includes(queryTag)) {
                    var queryVal = queryObj[queryTag].includes(' ')
                        ? "\"" + queryObj[queryTag] + "\""
                        : queryObj[queryTag];
                    queryTerms.push(queryTag + ":" + queryVal);
                }
            if (queryObj.__text) {
                queryTerms.push(queryObj.__text);
            }
        }
        var commonQuery = { projects: [Number(data.project.id)] };
        var searchQuery = (queryTerms.length ? ' ' : '') + queryTerms.join(' ');
        if (hasDiscoverQuery) {
            var _b = customStatsPeriod !== null && customStatsPeriod !== void 0 ? customStatsPeriod : (selection.datetime || {}), period = _b.period, start = _b.start, end = _b.end;
            var discoverQuery = __assign(__assign({}, commonQuery), { id: undefined, name: data.title || data.type, fields: ['title', 'release', 'environment', 'user', 'timestamp'], orderby: '-timestamp', query: "issue.id:" + data.id + searchQuery, version: 2 });
            if (!!start && !!end) {
                discoverQuery.start = String(start);
                discoverQuery.end = String(end);
            }
            else {
                discoverQuery.range = period || DEFAULT_STATS_PERIOD;
            }
            var discoverView = EventView.fromSavedQuery(discoverQuery);
            return discoverView.getResultsViewUrlTarget(organization.slug);
        }
        return {
            pathname: "/organizations/" + organization.slug + "/issues/" + data.id + "/events/",
            query: __assign(__assign({}, commonQuery), { query: searchQuery }),
        };
    };
    StreamGroup.prototype.renderReprocessingColumns = function () {
        var data = this.state.data;
        var _a = data, statusDetails = _a.statusDetails, count = _a.count;
        var info = statusDetails.info, pendingEvents = statusDetails.pendingEvents;
        var totalEvents = info.totalEvents, dateCreated = info.dateCreated;
        var remainingEventsToReprocess = totalEvents - pendingEvents;
        var remainingEventsToReprocessPercent = percent(remainingEventsToReprocess, totalEvents);
        var value = remainingEventsToReprocessPercent || 100;
        return (<React.Fragment>
        <StartedColumn>
          <TimeSince date={dateCreated}/>
        </StartedColumn>
        <EventsReprocessedColumn>
          {!defined(count) ? (<Placeholder height="17px"/>) : (<React.Fragment>
              <Count value={totalEvents}/>
              {'/'}
              <Count value={Number(count)}/>
            </React.Fragment>)}
        </EventsReprocessedColumn>
        <ProgressColumn>
          <ProgressBar value={value}/>
        </ProgressColumn>
      </React.Fragment>);
    };
    StreamGroup.prototype.render = function () {
        var _this = this;
        var _a, _b;
        var _c = this.state, data = _c.data, reviewed = _c.reviewed;
        var _d = this.props, index = _d.index, query = _d.query, hasGuideAnchor = _d.hasGuideAnchor, canSelect = _d.canSelect, memberList = _d.memberList, withChart = _d.withChart, statsPeriod = _d.statsPeriod, selection = _d.selection, organization = _d.organization, displayReprocessingLayout = _d.displayReprocessingLayout, showInboxTime = _d.showInboxTime, useFilteredStats = _d.useFilteredStats, customStatsPeriod = _d.customStatsPeriod;
        var _e = selection.datetime || {}, period = _e.period, start = _e.start, end = _e.end;
        var summary = (_a = customStatsPeriod === null || customStatsPeriod === void 0 ? void 0 : customStatsPeriod.label.toLowerCase()) !== null && _a !== void 0 ? _a : (!!start && !!end
            ? 'time range'
            : getRelativeSummary(period || DEFAULT_STATS_PERIOD).toLowerCase());
        // Use data.filtered to decide on which value to use
        // In case of the query has filters but we avoid showing both sets of filtered/unfiltered stats
        // we use useFilteredStats param passed to Group for deciding
        var primaryCount = data.filtered ? data.filtered.count : data.count;
        var secondaryCount = data.filtered ? data.count : undefined;
        var primaryUserCount = data.filtered ? data.filtered.userCount : data.userCount;
        var secondaryUserCount = data.filtered ? data.userCount : undefined;
        var showSecondaryPoints = Boolean(withChart && data && data.filtered && statsPeriod && useFilteredStats);
        var hasInbox = organization.features.includes('inbox');
        return (<Wrapper data-test-id="group" onClick={displayReprocessingLayout ? undefined : this.toggleSelect} reviewed={reviewed} hasInbox={hasInbox}>
        {canSelect && (<GroupCheckBoxWrapper ml={2}>
            <GroupCheckBox id={data.id} disabled={!!displayReprocessingLayout}/>
          </GroupCheckBoxWrapper>)}
        <GroupSummary width={[8 / 12, 8 / 12, 6 / 12]} ml={canSelect ? 1 : 2} mr={1} flex="1">
          <EventOrGroupHeader index={index} organization={organization} includeLink data={data} query={query} size="normal" onClick={this.trackClick}/>
          <EventOrGroupExtraDetails hasGuideAnchor={hasGuideAnchor} organization={organization} data={data} showInboxTime={showInboxTime}/>
        </GroupSummary>
        {hasGuideAnchor && <GuideAnchor target="issue_stream"/>}
        {withChart && !displayReprocessingLayout && (<ChartWrapper className="hidden-xs hidden-sm">
            {!((_b = data.filtered) === null || _b === void 0 ? void 0 : _b.stats) && !data.stats ? (<Placeholder height="24px"/>) : (<GroupChart statsPeriod={statsPeriod} data={data} showSecondaryPoints={showSecondaryPoints}/>)}
          </ChartWrapper>)}
        {displayReprocessingLayout ? (this.renderReprocessingColumns()) : (<React.Fragment>
            <EventUserWrapper>
              {!defined(primaryCount) ? (<Placeholder height="18px"/>) : (<DropdownMenu isNestedDropdown>
                  {function (_a) {
                        var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
                        var topLevelCx = classNames('dropdown', {
                            'anchor-middle': true,
                            open: isOpen,
                        });
                        return (<GuideAnchor target="dynamic_counts" disabled={!hasGuideAnchor}>
                        <span {...getRootProps({
                            className: topLevelCx,
                        })}>
                          <span {...getActorProps({})}>
                            <div className="dropdown-actor-title">
                              <PrimaryCount value={primaryCount}/>
                              {secondaryCount !== undefined && useFilteredStats && (<SecondaryCount value={secondaryCount}/>)}
                            </div>
                          </span>
                          {useFilteredStats && (<StyledDropdownList {...getMenuProps({ className: 'dropdown-menu inverted' })}>
                              {data.filtered && (<React.Fragment>
                                  <StyledMenuItem to={_this.getDiscoverUrl(true)}>
                                    <MenuItemText>
                                      {t('Matching search filters')}
                                    </MenuItemText>
                                    <MenuItemCount value={data.filtered.count}/>
                                  </StyledMenuItem>
                                  <MenuItem divider/>
                                </React.Fragment>)}

                              <StyledMenuItem to={_this.getDiscoverUrl()}>
                                <MenuItemText>{t("Total in " + summary)}</MenuItemText>
                                <MenuItemCount value={data.count}/>
                              </StyledMenuItem>

                              {data.lifetime && (<React.Fragment>
                                  <MenuItem divider/>
                                  <StyledMenuItem>
                                    <MenuItemText>{t('Since issue began')}</MenuItemText>
                                    <MenuItemCount value={data.lifetime.count}/>
                                  </StyledMenuItem>
                                </React.Fragment>)}
                            </StyledDropdownList>)}
                        </span>
                      </GuideAnchor>);
                    }}
                </DropdownMenu>)}
            </EventUserWrapper>
            <EventUserWrapper>
              {!defined(primaryUserCount) ? (<Placeholder height="18px"/>) : (<DropdownMenu isNestedDropdown>
                  {function (_a) {
                        var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
                        var topLevelCx = classNames('dropdown', {
                            'anchor-middle': true,
                            open: isOpen,
                        });
                        return (<span {...getRootProps({
                            className: topLevelCx,
                        })}>
                        <span {...getActorProps({})}>
                          <div className="dropdown-actor-title">
                            <PrimaryCount value={primaryUserCount}/>
                            {secondaryUserCount !== undefined && useFilteredStats && (<SecondaryCount dark value={secondaryUserCount}/>)}
                          </div>
                        </span>
                        {useFilteredStats && (<StyledDropdownList {...getMenuProps({ className: 'dropdown-menu inverted' })}>
                            {data.filtered && (<React.Fragment>
                                <StyledMenuItem to={_this.getDiscoverUrl(true)}>
                                  <MenuItemText>
                                    {t('Matching search filters')}
                                  </MenuItemText>
                                  <MenuItemCount value={data.filtered.userCount}/>
                                </StyledMenuItem>
                                <MenuItem divider/>
                              </React.Fragment>)}

                            <StyledMenuItem to={_this.getDiscoverUrl()}>
                              <MenuItemText>{t("Total in " + summary)}</MenuItemText>
                              <MenuItemCount value={data.userCount}/>
                            </StyledMenuItem>

                            {data.lifetime && (<React.Fragment>
                                <MenuItem divider/>
                                <StyledMenuItem>
                                  <MenuItemText>{t('Since issue began')}</MenuItemText>
                                  <MenuItemCount value={data.lifetime.userCount}/>
                                </StyledMenuItem>
                              </React.Fragment>)}
                          </StyledDropdownList>)}
                      </span>);
                    }}
                </DropdownMenu>)}
            </EventUserWrapper>
            <AssigneeWrapper className="hidden-xs hidden-sm">
              <AssigneeSelector id={data.id} memberList={memberList} onAssign={this.trackAssign}/>
            </AssigneeWrapper>
          </React.Fragment>)}
      </Wrapper>);
    };
    StreamGroup.defaultProps = defaultProps;
    return StreamGroup;
}(React.Component));
export default withGlobalSelection(withOrganization(StreamGroup));
// Position for wrapper is relative for overlay actions
var Wrapper = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n  padding: ", ";\n  line-height: 1.1;\n\n  ", ";\n\n  ", ";\n"], ["\n  position: relative;\n  padding: ", ";\n  line-height: 1.1;\n\n  ", ";\n\n  ",
    ";\n"])), function (p) { return (p.hasInbox ? space(1.5) + " 0" : space(1) + " 0"); }, function (p) { return (p.hasInbox ? p.theme.textColor : p.theme.subText); }, function (p) {
    return p.reviewed && css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n      animation: tintRow 0.2s linear forwards;\n      position: relative;\n\n      /*\n       * A mask that fills the entire row and makes the text opaque. Doing this because\n       * opacity adds a stacking context in CSS so we need to apply it to another element.\n       */\n      &:after {\n        content: '';\n        pointer-events: none;\n        position: absolute;\n        left: 0;\n        right: 0;\n        top: 0;\n        bottom: 0;\n        width: 100%;\n        height: 100%;\n        background-color: ", ";\n        opacity: 0.4;\n        z-index: 1;\n      }\n\n      @keyframes tintRow {\n        0% {\n          background-color: ", ";\n        }\n        100% {\n          background-color: ", ";\n        }\n      }\n    "], ["\n      animation: tintRow 0.2s linear forwards;\n      position: relative;\n\n      /*\n       * A mask that fills the entire row and makes the text opaque. Doing this because\n       * opacity adds a stacking context in CSS so we need to apply it to another element.\n       */\n      &:after {\n        content: '';\n        pointer-events: none;\n        position: absolute;\n        left: 0;\n        right: 0;\n        top: 0;\n        bottom: 0;\n        width: 100%;\n        height: 100%;\n        background-color: ", ";\n        opacity: 0.4;\n        z-index: 1;\n      }\n\n      @keyframes tintRow {\n        0% {\n          background-color: ", ";\n        }\n        100% {\n          background-color: ", ";\n        }\n      }\n    "])), p.theme.bodyBackground, p.theme.bodyBackground, p.theme.backgroundSecondary);
});
var GroupSummary = styled(Box)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
var GroupCheckBoxWrapper = styled(Box)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  align-self: flex-start;\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"], ["\n  align-self: flex-start;\n  & input[type='checkbox'] {\n    margin: 0;\n    display: block;\n  }\n"])));
var PrimaryCount = styled(Count)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var SecondaryCount = styled(function (_a) {
    var value = _a.value, p = __rest(_a, ["value"]);
    return <Count {...p} value={value}/>;
})(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n\n  :before {\n    content: '/';\n    padding-left: ", ";\n    padding-right: 2px;\n    color: ", ";\n  }\n"], ["\n  font-size: ", ";\n\n  :before {\n    content: '/';\n    padding-left: ", ";\n    padding-right: 2px;\n    color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeLarge; }, space(0.25), function (p) { return p.theme.gray300; });
var StyledDropdownList = styled('ul')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  z-index: ", ";\n"], ["\n  z-index: ", ";\n"])), function (p) { return p.theme.zIndex.hovercard; });
var StyledMenuItem = styled(function (_a) {
    var to = _a.to, children = _a.children, p = __rest(_a, ["to", "children"]);
    return (<MenuItem noAnchor>
    {to ? (
        // @ts-expect-error allow target _blank for this link to open in new window
        <Link to={to} target="_blank">
        <div {...p}>{children}</div>
      </Link>) : (<div className="dropdown-toggle">
        <div {...p}>{children}</div>
      </div>)}
  </MenuItem>);
})(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  margin: 0;\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n"], ["\n  margin: 0;\n  display: flex;\n  flex-direction: row;\n  justify-content: space-between;\n"])));
var MenuItemCount = styled(function (_a) {
    var value = _a.value, p = __rest(_a, ["value"]);
    return (<div {...p}>
    <Count value={value}/>
  </div>);
})(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  text-align: right;\n  font-weight: bold;\n  padding-left: ", ";\n"], ["\n  text-align: right;\n  font-weight: bold;\n  padding-left: ", ";\n"])), space(1));
var MenuItemText = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  white-space: nowrap;\n  font-weight: normal;\n  text-align: left;\n  padding-right: ", ";\n"], ["\n  white-space: nowrap;\n  font-weight: normal;\n  text-align: left;\n  padding-right: ", ";\n"])), space(1));
var ChartWrapper = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  width: 160px;\n  margin: 0 ", ";\n  align-self: center;\n"], ["\n  width: 160px;\n  margin: 0 ", ";\n  align-self: center;\n"])), space(2));
var EventUserWrapper = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-self: center;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-self: center;\n  width: 60px;\n  margin: 0 ", ";\n\n  @media (min-width: ", ") {\n    width: 80px;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[3]; });
var AssigneeWrapper = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  width: 80px;\n  margin: 0 ", ";\n  align-self: center;\n"], ["\n  width: 80px;\n  margin: 0 ", ";\n  align-self: center;\n"])), space(2));
// Reprocessing
var StartedColumn = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  align-self: center;\n  margin: 0 ", ";\n  color: ", ";\n  ", ";\n  width: 85px;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 140px;\n  }\n"], ["\n  align-self: center;\n  margin: 0 ", ";\n  color: ", ";\n  ", ";\n  width: 85px;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 140px;\n  }\n"])), space(2), function (p) { return p.theme.gray500; }, overflowEllipsis, function (p) { return p.theme.breakpoints[0]; });
var EventsReprocessedColumn = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  align-self: center;\n  margin: 0 ", ";\n  color: ", ";\n  ", ";\n  width: 75px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"], ["\n  align-self: center;\n  margin: 0 ", ";\n  color: ", ";\n  ", ";\n  width: 75px;\n\n  @media (min-width: ", ") {\n    width: 140px;\n  }\n"])), space(2), function (p) { return p.theme.gray500; }, overflowEllipsis, function (p) { return p.theme.breakpoints[0]; });
var ProgressColumn = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  margin: 0 ", ";\n  align-self: center;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 160px;\n  }\n"], ["\n  margin: 0 ", ";\n  align-self: center;\n  display: none;\n\n  @media (min-width: ", ") {\n    display: block;\n    width: 160px;\n  }\n"])), space(2), function (p) { return p.theme.breakpoints[0]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16;
//# sourceMappingURL=group.jsx.map
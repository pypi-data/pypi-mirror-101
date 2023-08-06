import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { ClassNames } from '@emotion/core';
import styled from '@emotion/styled';
import PropTypes from 'prop-types';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import PageHeading from 'app/components/pageHeading';
import QueryCount from 'app/components/queryCount';
import { t } from 'app/locale';
import { PageHeader } from 'app/styles/organization';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import SavedSearchSelector from './savedSearchSelector';
import IssueListSearchBar from './searchBar';
import IssueListSortOptions from './sortOptions';
var IssueListFilters = /** @class */ (function (_super) {
    __extends(IssueListFilters, _super);
    function IssueListFilters() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSavedSearchSelect = function (savedSearch) {
            trackAnalyticsEvent({
                eventKey: 'organization_saved_search.selected',
                eventName: 'Organization Saved Search: Selected saved search',
                organization_id: _this.props.organization.id,
                query: savedSearch.query,
                search_type: 'issues',
                id: savedSearch.id ? parseInt(savedSearch.id, 10) : -1,
            });
            if (_this.props.onSavedSearchSelect) {
                _this.props.onSavedSearchSelect(savedSearch);
            }
        };
        return _this;
    }
    IssueListFilters.prototype.render = function () {
        var _a = this.props, organization = _a.organization, savedSearch = _a.savedSearch, queryCount = _a.queryCount, queryMaxCount = _a.queryMaxCount, query = _a.query, savedSearchList = _a.savedSearchList, isSearchDisabled = _a.isSearchDisabled, sort = _a.sort, onSidebarToggle = _a.onSidebarToggle, onSearch = _a.onSearch, onSavedSearchDelete = _a.onSavedSearchDelete, onSortChange = _a.onSortChange, tagValueLoader = _a.tagValueLoader, tags = _a.tags, isInbox = _a.isInbox;
        var isAssignedQuery = /\bassigned:/.test(query);
        return (<PageHeader>
        {!isInbox && (<PageHeading>
            {t('Issues')} <QueryCount count={queryCount} max={queryMaxCount}/>
          </PageHeading>)}

        <SearchContainer isInbox={isInbox}>
          <IssueListSortOptions sort={sort} query={query} onSelect={onSortChange}/>

          <SearchSelectorContainer isInbox={isInbox}>
            {!isInbox && (<SavedSearchSelector key={query} organization={organization} savedSearchList={savedSearchList} onSavedSearchSelect={this.handleSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} query={query} sort={sort}/>)}

            <ClassNames>
              {function (_a) {
                var css = _a.css;
                return (<GuideAnchor target="assigned_or_suggested_query" disabled={!isAssignedQuery} containerClassName={css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n                    width: 100%;\n                  "], ["\n                    width: 100%;\n                  "])))}>
                  <IssueListSearchBar organization={organization} query={query || ''} sort={sort} onSearch={onSearch} disabled={isSearchDisabled} excludeEnvironment supportedTags={tags} tagValueLoader={tagValueLoader} savedSearch={savedSearch} onSidebarToggle={onSidebarToggle} isInbox={isInbox}/>
                </GuideAnchor>);
            }}
            </ClassNames>
          </SearchSelectorContainer>
        </SearchContainer>
      </PageHeader>);
    };
    IssueListFilters.contextTypes = {
        location: PropTypes.object,
    };
    return IssueListFilters;
}(React.Component));
var SearchContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  width: ", ";\n  flex-direction: ", ";\n"], ["\n  display: flex;\n  width: ", ";\n  flex-direction: ", ";\n"])), function (p) { return (p.isInbox ? '100%' : '70%'); }, function (p) { return (p.isInbox ? 'row-reverse' : 'row'); });
var SearchSelectorContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  flex-grow: 1;\n\n  margin-right: ", ";\n  margin-left: ", ";\n"], ["\n  display: flex;\n  flex-grow: 1;\n\n  margin-right: ", ";\n  margin-left: ", ";\n"])), function (p) { return (p.isInbox ? space(1) : 0); }, function (p) { return (p.isInbox ? 0 : space(1)); });
export default IssueListFilters;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=filters.jsx.map
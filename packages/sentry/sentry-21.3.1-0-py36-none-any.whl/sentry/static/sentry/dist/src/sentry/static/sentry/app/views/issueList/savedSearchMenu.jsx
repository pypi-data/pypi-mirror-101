import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import MenuItem from 'app/components/menuItem';
import Tooltip from 'app/components/tooltip';
import { IconDelete } from 'app/icons';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { getSortLabel } from './utils';
function SavedSearchMenuItem(_a) {
    var organization = _a.organization, onSavedSearchSelect = _a.onSavedSearchSelect, onSavedSearchDelete = _a.onSavedSearchDelete, search = _a.search, query = _a.query, sort = _a.sort, isLast = _a.isLast;
    return (<Tooltip title={<React.Fragment>
          {search.name + " \u2022 "}
          <TooltipSearchQuery>{search.query}</TooltipSearchQuery>
          {" \u2022 "}
          {t('Sort: ')}
          {getSortLabel(search.sort)}
        </React.Fragment>} containerDisplayMode="block" delay={1000}>
      <StyledMenuItem isActive={search.query === query && search.sort === sort} isLast={isLast}>
        <MenuItemLink tabIndex={-1} onClick={function () { return onSavedSearchSelect(search); }}>
          <SearchTitle>{search.name}</SearchTitle>
          <SearchQueryContainer>
            <SearchQuery>{search.query}</SearchQuery>
            <SearchSort>
              {t('Sort: ')}
              {getSortLabel(search.sort)}
            </SearchSort>
          </SearchQueryContainer>
        </MenuItemLink>
        {search.isGlobal === false && search.isPinned === false && (<Access organization={organization} access={['org:write']} renderNoAccessMessage={false}>
            <Confirm onConfirm={function () { return onSavedSearchDelete(search); }} message={t('Are you sure you want to delete this saved search?')} stopPropagation>
              <DeleteButton borderless title={t('Delete this saved search')} icon={<IconDelete />} label={t('delete')} size="zero"/>
            </Confirm>
          </Access>)}
      </StyledMenuItem>
    </Tooltip>);
}
function SavedSearchMenu(_a) {
    var _b;
    var savedSearchList = _a.savedSearchList, props = __rest(_a, ["savedSearchList"]);
    var savedSearches = savedSearchList.filter(function (search) { return !search.isGlobal; });
    var globalSearches = savedSearchList.filter(function (search) { return search.isGlobal; });
    if ((_b = props.organization.features) === null || _b === void 0 ? void 0 : _b.includes('inbox')) {
        // Hide "Unresolved Issues" since they have a unresolved tab
        globalSearches = globalSearches.filter(function (search) { return !search.isPinned && search.query !== 'is:unresolved'; });
    }
    return (<React.Fragment>
      <MenuHeader>{t('Saved Searches')}</MenuHeader>
      {savedSearches.length === 0 ? (<EmptyItem>{t('No saved searches yet.')}</EmptyItem>) : (savedSearches.map(function (search, index) { return (<SavedSearchMenuItem key={search.id} search={search} isLast={index === savedSearches.length - 1} {...props}/>); }))}
      <SecondaryMenuHeader>{t('Recommended searches')}</SecondaryMenuHeader>
      {/* Could only happen on self-hosted */}
      {globalSearches.length === 0 ? (<EmptyItem>{t('No recommended searches yet.')}</EmptyItem>) : (globalSearches.map(function (search, index) { return (<SavedSearchMenuItem key={search.id} search={search} isLast={index === globalSearches.length - 1} {...props}/>); }))}
    </React.Fragment>);
}
export default SavedSearchMenu;
var SearchTitle = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  ", "\n"], ["\n  color: ", ";\n  ", "\n"])), function (p) { return p.theme.textColor; }, overflowEllipsis);
var SearchQueryContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1;\n  ", "\n"], ["\n  font-size: ", ";\n  line-height: 1;\n  ", "\n"])), function (p) { return p.theme.fontSizeExtraSmall; }, overflowEllipsis);
var SearchQuery = styled('code')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  padding: 0;\n  background: inherit;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  padding: 0;\n  background: inherit;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeExtraSmall; });
var SearchSort = styled('span')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  &:before {\n    font-size: ", ";\n    color: ", ";\n    content: ' \u2022 ';\n  }\n"], ["\n  color: ", ";\n  font-size: ", ";\n  &:before {\n    font-size: ", ";\n    color: ", ";\n    content: ' \\u2022 ';\n  }\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.fontSizeExtraSmall; }, function (p) { return p.theme.textColor; });
var TooltipSearchQuery = styled('span')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  color: ", ";\n  font-weight: normal;\n  font-family: ", ";\n"], ["\n  color: ", ";\n  font-weight: normal;\n  font-family: ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.text.familyMono; });
var DeleteButton = styled(Button)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  color: ", ";\n  background: transparent;\n  flex-shrink: 0;\n  padding: ", " 0;\n\n  &:hover {\n    background: transparent;\n    color: ", ";\n  }\n"], ["\n  color: ", ";\n  background: transparent;\n  flex-shrink: 0;\n  padding: ", " 0;\n\n  &:hover {\n    background: transparent;\n    color: ", ";\n  }\n"])), function (p) { return p.theme.gray200; }, space(1), function (p) { return p.theme.blue300; });
var MenuHeader = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  align-items: center;\n  color: ", ";\n  font-weight: 400;\n  background: ", ";\n  line-height: 0.75;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n"], ["\n  align-items: center;\n  color: ", ";\n  font-weight: 400;\n  background: ", ";\n  line-height: 0.75;\n  padding: ", ";\n  border-bottom: 1px solid ", ";\n  border-radius: ", " ", " 0 0;\n"])), function (p) { return p.theme.gray400; }, function (p) { return p.theme.backgroundSecondary; }, space(1.5), function (p) { return p.theme.border; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; });
var SecondaryMenuHeader = styled(MenuHeader)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  border-top: 1px solid ", ";\n  border-radius: 0;\n"], ["\n  border-top: 1px solid ", ";\n  border-radius: 0;\n"])), function (p) { return p.theme.border; });
var StyledMenuItem = styled(MenuItem)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  border-bottom: ", ";\n  font-size: ", ";\n  padding: 0;\n\n  & > span > a {\n    padding: ", " 0 ", " 0;\n  }\n\n  ", "\n"], ["\n  border-bottom: ", ";\n  font-size: ", ";\n  padding: 0;\n\n  & > span > a {\n    padding: ", " 0 ", " 0;\n  }\n\n  ",
    "\n"])), function (p) { return (!p.isLast ? "1px solid " + p.theme.innerBorder : null); }, function (p) { return p.theme.fontSizeMedium; }, space(0.75), space(1), function (p) {
    return p.isActive &&
        "\n  " + SearchTitle + ", " + SearchQuery + ", " + SearchSort + " {\n    color: " + p.theme.white + ";\n  }\n  " + SearchSort + ":before {\n    color: " + p.theme.white + ";\n  }\n  &:hover {\n    " + SearchTitle + ", " + SearchQuery + ", " + SearchSort + " {\n      color: " + p.theme.black + ";\n    }\n    " + SearchSort + ":before {\n      color: " + p.theme.black + ";\n    }\n  }\n  ";
});
var MenuItemLink = styled('a')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: block;\n  flex-grow: 1;\n  padding: ", " 0;\n  /* Nav tabs style override */\n  border: 0;\n\n  ", "\n"], ["\n  display: block;\n  flex-grow: 1;\n  padding: ", " 0;\n  /* Nav tabs style override */\n  border: 0;\n\n  ", "\n"])), space(0.5), overflowEllipsis);
var EmptyItem = styled('li')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  padding: ", " ", ";\n  color: ", ";\n"], ["\n  padding: ", " ", ";\n  color: ", ";\n"])), space(1), space(1.5), function (p) { return p.theme.subText; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11;
//# sourceMappingURL=savedSearchMenu.jsx.map
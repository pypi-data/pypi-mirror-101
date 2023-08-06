import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Badge from 'app/components/badge';
import DropdownLink from 'app/components/dropdownLink';
import QueryCount from 'app/components/queryCount';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import SavedSearchMenu from './savedSearchMenu';
function SavedSearchTab(_a) {
    var isActive = _a.isActive, organization = _a.organization, savedSearchList = _a.savedSearchList, onSavedSearchSelect = _a.onSavedSearchSelect, onSavedSearchDelete = _a.onSavedSearchDelete, query = _a.query, queryCount = _a.queryCount, sort = _a.sort;
    var savedSearch = savedSearchList.find(function (search) { return search.query === query && search.sort === sort; });
    var title = (<TitleWrapper>
      {isActive ? (<React.Fragment>
          <TitleTextOverflow>
            {savedSearch ? savedSearch.name : t('Custom Search')}{' '}
          </TitleTextOverflow>
          {queryCount !== undefined && queryCount > 0 && (<div>
              <Badge>
                <QueryCount hideParens count={queryCount} max={1000}/>
              </Badge>
            </div>)}
        </React.Fragment>) : (t('Saved Searches'))}
    </TitleWrapper>);
    return (<TabWrapper isActive={isActive} className="saved-search-tab">
      <StyledDropdownLink alwaysRenderMenu={false} anchorMiddle caret title={title} isActive={isActive}>
        <SavedSearchMenu organization={organization} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} query={query} sort={sort}/>
      </StyledDropdownLink>
    </TabWrapper>);
}
export default SavedSearchTab;
var TabWrapper = styled('li')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  /* Color matches nav-tabs - overwritten using dark mode class saved-search-tab */\n  border-bottom: ", ";\n  /* Reposition menu under caret */\n  & > span {\n    display: block;\n  }\n  & > span > .dropdown-menu {\n    padding: 0;\n    margin-top: ", ";\n    min-width: 20vw;\n    max-width: 25vw;\n    z-index: ", ";\n\n    :after {\n      border-bottom-color: ", ";\n    }\n  }\n\n  @media (max-width: ", ") {\n    & > span > .dropdown-menu {\n      max-width: 30vw;\n    }\n  }\n\n  @media (max-width: ", ") {\n    & > span > .dropdown-menu {\n      max-width: 50vw;\n    }\n  }\n"], ["\n  /* Color matches nav-tabs - overwritten using dark mode class saved-search-tab */\n  border-bottom: ", ";\n  /* Reposition menu under caret */\n  & > span {\n    display: block;\n  }\n  & > span > .dropdown-menu {\n    padding: 0;\n    margin-top: ", ";\n    min-width: 20vw;\n    max-width: 25vw;\n    z-index: ", ";\n\n    :after {\n      border-bottom-color: ", ";\n    }\n  }\n\n  @media (max-width: ", ") {\n    & > span > .dropdown-menu {\n      max-width: 30vw;\n    }\n  }\n\n  @media (max-width: ", ") {\n    & > span > .dropdown-menu {\n      max-width: 50vw;\n    }\n  }\n"])), function (p) { return (p.isActive ? "4px solid #6c5fc7" : 0); }, space(1), function (p) { return p.theme.zIndex.globalSelectionHeader; }, function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.breakpoints[4]; }, function (p) { return p.theme.breakpoints[1]; });
var TitleWrapper = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n  user-select: none;\n  display: flex;\n  align-items: center;\n"], ["\n  margin-right: ", ";\n  user-select: none;\n  display: flex;\n  align-items: center;\n"])), space(0.5));
var TitleTextOverflow = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-right: ", ";\n  max-width: 150px;\n  ", ";\n"], ["\n  margin-right: ", ";\n  max-width: 150px;\n  ", ";\n"])), space(0.5), overflowEllipsis);
var StyledDropdownLink = styled(DropdownLink)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  position: relative;\n  display: block;\n  padding: ", " 0;\n  /* Important to override a media query from .nav-tabs */\n  font-size: ", " !important;\n  text-align: center;\n  text-transform: capitalize;\n  /* TODO(scttcper): Replace hex color when nav-tabs is replaced */\n  color: ", ";\n\n  :hover {\n    color: #2f2936;\n  }\n"], ["\n  position: relative;\n  display: block;\n  padding: ", " 0;\n  /* Important to override a media query from .nav-tabs */\n  font-size: ", " !important;\n  text-align: center;\n  text-transform: capitalize;\n  /* TODO(scttcper): Replace hex color when nav-tabs is replaced */\n  color: ", ";\n\n  :hover {\n    color: #2f2936;\n  }\n"])), space(1), function (p) { return p.theme.fontSizeLarge; }, function (p) { return (p.isActive ? p.theme.textColor : '#7c6a8e'); });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=savedSearchTab.jsx.map
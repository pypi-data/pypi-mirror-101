import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl from 'app/components/dropdownControl';
import { t } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import SavedSearchMenu from './savedSearchMenu';
function SavedSearchSelector(_a) {
    var savedSearchList = _a.savedSearchList, onSavedSearchDelete = _a.onSavedSearchDelete, onSavedSearchSelect = _a.onSavedSearchSelect, organization = _a.organization, query = _a.query, sort = _a.sort;
    function getTitle() {
        var savedSearch = savedSearchList.find(function (search) { return search.query === query && search.sort === sort; });
        return savedSearch ? savedSearch.name : t('Custom Search');
    }
    return (<DropdownControl menuWidth="35vw" blendWithActor button={function (_a) {
            var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
            return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen}>
          <ButtonTitle>{getTitle()}</ButtonTitle>
        </StyledDropdownButton>);
        }}>
      <SavedSearchMenu organization={organization} savedSearchList={savedSearchList} onSavedSearchSelect={onSavedSearchSelect} onSavedSearchDelete={onSavedSearchDelete} query={query} sort={sort}/>
    </DropdownControl>);
}
export default SavedSearchSelector;
var StyledDropdownButton = styled(DropdownButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  color: ", ";\n  background-color: ", ";\n  border-right: 0;\n  border-color: ", ";\n  z-index: ", ";\n  border-radius: ", ";\n  white-space: nowrap;\n  max-width: 200px;\n  margin-right: 0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border-color: ", ";\n    border-right: 0;\n  }\n"], ["\n  color: ", ";\n  background-color: ", ";\n  border-right: 0;\n  border-color: ", ";\n  z-index: ", ";\n  border-radius: ",
    ";\n  white-space: nowrap;\n  max-width: 200px;\n  margin-right: 0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border-color: ", ";\n    border-right: 0;\n  }\n"])), function (p) { return p.theme.textColor; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.dropdownAutocomplete.actor; }, function (p) {
    return p.isOpen
        ? p.theme.borderRadius + " 0 0 0"
        : p.theme.borderRadius + " 0 0 " + p.theme.borderRadius;
}, function (p) { return p.theme.border; });
var ButtonTitle = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var templateObject_1, templateObject_2;
//# sourceMappingURL=savedSearchSelector.jsx.map
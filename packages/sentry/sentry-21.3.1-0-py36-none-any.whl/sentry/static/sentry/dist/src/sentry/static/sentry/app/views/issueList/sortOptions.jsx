import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Tooltip from 'app/components/tooltip';
import { t } from 'app/locale';
import { getSortLabel, IssueSortOptions, Query } from 'app/views/issueList/utils';
export function getSortTooltip(key) {
    switch (key) {
        case IssueSortOptions.INBOX:
            return t('When the issue was flagged for review.');
        case IssueSortOptions.NEW:
            return t('When the issue was first seen in the selected time period.');
        case IssueSortOptions.PRIORITY:
            return t('Issues trending upward recently.');
        case IssueSortOptions.FREQ:
            return t('Number of events in the time selected.');
        case IssueSortOptions.USER:
            return t('Number of users affected in the time selected.');
        case IssueSortOptions.TREND:
            return t('% change in event count over the time selected.');
        case IssueSortOptions.DATE:
        default:
            return t('When the issue was last seen in the selected time period.');
    }
}
var IssueListSortOptions = function (_a) {
    var onSelect = _a.onSelect, sort = _a.sort, query = _a.query;
    var sortKey = sort || IssueSortOptions.DATE;
    var getMenuItem = function (key) { return (<DropdownItem onSelect={onSelect} eventKey={key} isActive={sortKey === key}>
      <StyledTooltip containerDisplayMode="block" position="top" delay={500} title={getSortTooltip(key)}>
        {getSortLabel(key)}
      </StyledTooltip>
    </DropdownItem>); };
    return (<DropdownControl buttonProps={{ prefix: t('Sort by') }} label={getSortLabel(sortKey)}>
      <React.Fragment>
        <Feature features={['inbox']}>
          {query === Query.FOR_REVIEW && getMenuItem(IssueSortOptions.INBOX)}
        </Feature>
        {getMenuItem(IssueSortOptions.DATE)}
        {getMenuItem(IssueSortOptions.NEW)}
        {getMenuItem(IssueSortOptions.PRIORITY)}
        {getMenuItem(IssueSortOptions.FREQ)}
        {getMenuItem(IssueSortOptions.USER)}
        <Feature features={['issue-list-trend-sort']}>
          {getMenuItem(IssueSortOptions.TREND)}
        </Feature>
      </React.Fragment>
    </DropdownControl>);
};
export default IssueListSortOptions;
var StyledTooltip = styled(Tooltip)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
var templateObject_1;
//# sourceMappingURL=sortOptions.jsx.map
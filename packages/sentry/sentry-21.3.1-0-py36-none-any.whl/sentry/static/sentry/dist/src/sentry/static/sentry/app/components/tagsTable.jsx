import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { SectionHeading } from 'app/components/charts/styles';
import { KeyValueTable, KeyValueTableRow } from 'app/components/keyValueTable';
import Link from 'app/components/links/link';
import Tooltip from 'app/components/tooltip';
import Version from 'app/components/version';
import { t } from 'app/locale';
import space from 'app/styles/space';
var TagsTable = function (_a) {
    var event = _a.event, query = _a.query, generateUrl = _a.generateUrl, _b = _a.title, title = _b === void 0 ? t('Tag Details') : _b;
    var tags = event.tags;
    return (<StyledTagsTable>
      <SectionHeading>{title}</SectionHeading>
      <KeyValueTable>
        {tags.map(function (tag) {
            var tagInQuery = query.includes(tag.key + ":");
            var target = tagInQuery ? undefined : generateUrl(tag);
            var renderTagValue = function () {
                switch (tag.key) {
                    case 'release':
                        return <Version version={tag.value} anchor={false} withPackage/>;
                    default:
                        return tag.value;
                }
            };
            return (<KeyValueTableRow key={tag.key} keyName={tag.key} value={tagInQuery ? (<Tooltip title={t('This tag is in the current filter conditions')}>
                    <span>{renderTagValue()}</span>
                  </Tooltip>) : (<Link to={target || ''}>{renderTagValue()}</Link>)}/>);
        })}
      </KeyValueTable>
    </StyledTagsTable>);
};
var StyledTagsTable = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
export default TagsTable;
var templateObject_1;
//# sourceMappingURL=tagsTable.jsx.map
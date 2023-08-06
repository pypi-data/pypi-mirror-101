import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Role from 'app/components/acl/role';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import FileSize from 'app/components/fileSize';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import { IconClock, IconDelete, IconDownload } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
var ProjectProguardRow = function (_a) {
    var mapping = _a.mapping, onDelete = _a.onDelete, downloadUrl = _a.downloadUrl, downloadRole = _a.downloadRole;
    var id = mapping.id, debugId = mapping.debugId, uuid = mapping.uuid, size = mapping.size, dateCreated = mapping.dateCreated;
    var handleDeleteClick = function () {
        onDelete(id);
    };
    return (<React.Fragment>
      <NameColumn>
        <Name>{debugId || uuid || "(" + t('empty') + ")"}</Name>
        <TimeWrapper>
          <IconClock size="sm"/>
          <TimeSince date={dateCreated}/>
        </TimeWrapper>
      </NameColumn>
      <SizeColumn>
        <FileSize bytes={size}/>
      </SizeColumn>
      <ActionsColumn>
        <ButtonBar gap={0.5}>
          <Role role={downloadRole}>
            {function (_a) {
            var hasRole = _a.hasRole;
            return (<Tooltip title={t('You do not have permission to download mappings.')} disabled={hasRole}>
                <Button size="small" icon={<IconDownload size="sm"/>} disabled={!hasRole} href={downloadUrl} title={hasRole ? t('Download Mapping') : undefined}/>
              </Tooltip>);
        }}
          </Role>

          <Access access={['project:releases']}>
            {function (_a) {
            var hasAccess = _a.hasAccess;
            return (<Tooltip disabled={hasAccess} title={t('You do not have permission to delete mappings.')}>
                <Confirm message={t('Are you sure you want to remove this mapping?')} onConfirm={handleDeleteClick} disabled={!hasAccess}>
                  <Button size="small" icon={<IconDelete size="sm"/>} title={hasAccess ? t('Remove Mapping') : undefined} label={t('Remove Mapping')} disabled={!hasAccess}/>
                </Confirm>
              </Tooltip>);
        }}
          </Access>
        </ButtonBar>
      </ActionsColumn>
    </React.Fragment>);
};
var NameColumn = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  justify-content: center;\n"])));
var SizeColumn = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  text-align: right;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  text-align: right;\n  align-items: center;\n"])));
var ActionsColumn = styled(SizeColumn)(templateObject_3 || (templateObject_3 = __makeTemplateObject([""], [""])));
var Name = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  padding-right: ", ";\n  overflow-wrap: break-word;\n  word-break: break-all;\n"], ["\n  padding-right: ", ";\n  overflow-wrap: break-word;\n  word-break: break-all;\n"])), space(4));
var TimeWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  font-size: ", ";\n  align-items: center;\n  color: ", ";\n  margin-top: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: min-content 1fr;\n  font-size: ", ";\n  align-items: center;\n  color: ", ";\n  margin-top: ", ";\n"])), space(0.5), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.subText; }, space(1));
export default ProjectProguardRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=projectProguardRow.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Access from 'app/components/acl/access';
import Role from 'app/components/acl/role';
import ActionButton from 'app/components/actions/button';
import MenuItemActionLink from 'app/components/actions/menuItemActionLink';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import DropdownLink from 'app/components/dropdownLink';
import Tooltip from 'app/components/tooltip';
import { IconDelete, IconDownload, IconEllipsis } from 'app/icons';
import { t } from 'app/locale';
import { CandidateDownloadStatus } from 'app/types/debugImage';
var noPermissionToDownloadDebugFilesInfo = t('You do not have permission to download debug files');
var noPermissionToDeleteDebugFilesInfo = t('You do not have permission to delete debug files');
var debugFileDeleteConfirmationInfo = t('Are you sure you wish to delete this file?');
function Actions(_a) {
    var candidate = _a.candidate, organization = _a.organization, isInternalSource = _a.isInternalSource, baseUrl = _a.baseUrl, projectId = _a.projectId, onDelete = _a.onDelete;
    var download = candidate.download, debugFileId = candidate.location;
    var status = download.status;
    if (!debugFileId || !isInternalSource) {
        return null;
    }
    var deleted = status === CandidateDownloadStatus.DELETED;
    var downloadUrl = baseUrl + "/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?id=" + debugFileId;
    var actions = (<Role role={organization.debugFilesRole} organization={organization}>
      {function (_a) {
            var hasRole = _a.hasRole;
            return (<Access access={['project:write']} organization={organization}>
          {function (_a) {
                    var hasAccess = _a.hasAccess;
                    return (<React.Fragment>
              <StyledDropdownLink caret={false} customTitle={<ActionButton label={t('Actions')} disabled={deleted} icon={<IconEllipsis size="sm"/>}/>} anchorRight>
                <Tooltip disabled={hasRole} title={noPermissionToDownloadDebugFilesInfo}>
                  <MenuItemActionLink shouldConfirm={false} icon={<IconDownload size="xs"/>} title={t('Download')} href={downloadUrl} onClick={function (event) {
                            if (deleted) {
                                event.preventDefault();
                            }
                        }} disabled={!hasRole || deleted}>
                    {t('Download')}
                  </MenuItemActionLink>
                </Tooltip>
                <Tooltip disabled={hasAccess} title={noPermissionToDeleteDebugFilesInfo}>
                  <MenuItemActionLink onAction={function () { return onDelete(debugFileId); }} message={debugFileDeleteConfirmationInfo} title={t('Delete')} disabled={!hasAccess || deleted} shouldConfirm>
                    {t('Delete')}
                  </MenuItemActionLink>
                </Tooltip>
              </StyledDropdownLink>
              <StyledButtonBar gap={1}>
                <Tooltip disabled={hasRole} title={noPermissionToDownloadDebugFilesInfo}>
                  <Button size="xsmall" icon={<IconDownload size="xs"/>} href={downloadUrl} disabled={!hasRole}>
                    {t('Download')}
                  </Button>
                </Tooltip>
                <Tooltip disabled={hasAccess} title={noPermissionToDeleteDebugFilesInfo}>
                  <Confirm confirmText={t('Delete')} message={debugFileDeleteConfirmationInfo} onConfirm={function () { return onDelete(debugFileId); }} disabled={!hasAccess}>
                    <Button priority="danger" icon={<IconDelete size="xs"/>} size="xsmall" disabled={!hasAccess}/>
                  </Confirm>
                </Tooltip>
              </StyledButtonBar>
            </React.Fragment>);
                }}
        </Access>);
        }}
    </Role>);
    if (!deleted) {
        return actions;
    }
    return (<Tooltip title={t('Actions not available because this debug file was deleted')}>
      {actions}
    </Tooltip>);
}
export default Actions;
var StyledDropdownLink = styled(DropdownLink)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n    transition: none;\n  }\n"], ["\n  display: none;\n\n  @media (min-width: ", ") {\n    display: flex;\n    align-items: center;\n    transition: none;\n  }\n"])), function (props) { return props.theme.breakpoints[2]; });
var StyledButtonBar = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (min-width: ", ") {\n    display: none;\n  }\n"])), function (props) { return props.theme.breakpoints[2]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=actions.jsx.map
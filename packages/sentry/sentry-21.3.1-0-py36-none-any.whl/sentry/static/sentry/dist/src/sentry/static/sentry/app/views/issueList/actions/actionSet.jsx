import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ActionLink from 'app/components/actions/actionLink';
import ActionButton from 'app/components/actions/button';
import IgnoreActions from 'app/components/actions/ignore';
import MenuItemActionLink from 'app/components/actions/menuItemActionLink';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import DropdownLink from 'app/components/dropdownLink';
import Tooltip from 'app/components/tooltip';
import { IconEllipsis, IconPause, IconPlay } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { ResolutionStatus } from 'app/types';
import Projects from 'app/utils/projects';
import ResolveActions from './resolveActions';
import ReviewAction from './reviewAction';
import { ConfirmAction, getConfirm, getLabel } from './utils';
function ActionSet(_a) {
    var orgSlug = _a.orgSlug, queryCount = _a.queryCount, query = _a.query, realtimeActive = _a.realtimeActive, allInQuerySelected = _a.allInQuerySelected, anySelected = _a.anySelected, multiSelected = _a.multiSelected, issues = _a.issues, onUpdate = _a.onUpdate, onShouldConfirm = _a.onShouldConfirm, onDelete = _a.onDelete, onRealtimeChange = _a.onRealtimeChange, onMerge = _a.onMerge, selectedProjectSlug = _a.selectedProjectSlug, hasInbox = _a.hasInbox;
    var numIssues = issues.size;
    var confirm = getConfirm(numIssues, allInQuerySelected, query, queryCount);
    var label = getLabel(numIssues, allInQuerySelected);
    // merges require a single project to be active in an org context
    // selectedProjectSlug is null when 0 or >1 projects are selected.
    var mergeDisabled = !(multiSelected && selectedProjectSlug);
    return (<Wrapper hasInbox={hasInbox}>
      {selectedProjectSlug ? (<Projects orgId={orgSlug} slugs={[selectedProjectSlug]}>
          {function (_a) {
                var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
                var selectedProject = projects[0];
                return (<ResolveActions onShouldConfirm={onShouldConfirm} onUpdate={onUpdate} anySelected={anySelected} orgSlug={orgSlug} params={{
                        hasReleases: selectedProject.hasOwnProperty('features')
                            ? selectedProject.features.includes('releases')
                            : false,
                        latestRelease: selectedProject.hasOwnProperty('latestRelease')
                            ? selectedProject.latestRelease
                            : undefined,
                        projectId: selectedProject.slug,
                        confirm: confirm,
                        label: label,
                        loadingProjects: !initiallyLoaded,
                        projectFetchError: !!fetchError,
                    }}/>);
            }}
        </Projects>) : (<ResolveActions onShouldConfirm={onShouldConfirm} onUpdate={onUpdate} anySelected={anySelected} orgSlug={orgSlug} params={{
                hasReleases: false,
                latestRelease: null,
                projectId: null,
                confirm: confirm,
                label: label,
            }}/>)}

      <IgnoreActions onUpdate={onUpdate} shouldConfirm={onShouldConfirm(ConfirmAction.IGNORE)} confirmMessage={confirm(ConfirmAction.IGNORE, true)} confirmLabel={label('ignore')} disabled={!anySelected}/>

      {hasInbox && (<GuideAnchor target="inbox_guide_review" position="bottom">
          <div className="hidden-sm hidden-xs">
            <ReviewAction disabled={!anySelected} onUpdate={onUpdate}/>
          </div>
        </GuideAnchor>)}

      <div className="hidden-md hidden-sm hidden-xs">
        <ActionLink type="button" disabled={mergeDisabled} onAction={onMerge} shouldConfirm={onShouldConfirm(ConfirmAction.MERGE)} message={confirm(ConfirmAction.MERGE, false)} confirmLabel={label('merge')} title={t('Merge Selected Issues')}>
          {t('Merge')}
        </ActionLink>
      </div>

      <DropdownLink key="actions" customTitle={<ActionButton label={t('Open more issue actions')} icon={<IconEllipsis size="xs"/>}/>}>
        <MenuItemActionLink className="hidden-lg hidden-xl" disabled={mergeDisabled} onAction={onMerge} shouldConfirm={onShouldConfirm(ConfirmAction.MERGE)} message={confirm(ConfirmAction.MERGE, false)} confirmLabel={label('merge')} title={t('Merge Selected Issues')}>
          {t('Merge')}
        </MenuItemActionLink>
        {hasInbox && (<MenuItemActionLink className="hidden-md hidden-lg hidden-xl" disabled={!anySelected} onAction={function () { return onUpdate({ inbox: false }); }} title={t('Mark Reviewed')}>
            {t('Mark Reviewed')}
          </MenuItemActionLink>)}
        <MenuItemActionLink disabled={!anySelected} onAction={function () { return onUpdate({ isBookmarked: true }); }} shouldConfirm={onShouldConfirm(ConfirmAction.BOOKMARK)} message={confirm(ConfirmAction.BOOKMARK, false)} confirmLabel={label('bookmark')} title={t('Add to Bookmarks')}>
          {t('Add to Bookmarks')}
        </MenuItemActionLink>
        <MenuItemActionLink disabled={!anySelected} onAction={function () { return onUpdate({ isBookmarked: false }); }} shouldConfirm={onShouldConfirm(ConfirmAction.UNBOOKMARK)} message={confirm('remove', false, ' from your bookmarks')} confirmLabel={label('remove', ' from your bookmarks')} title={t('Remove from Bookmarks')}>
          {t('Remove from Bookmarks')}
        </MenuItemActionLink>

        <MenuItemActionLink disabled={!anySelected} onAction={function () { return onUpdate({ status: ResolutionStatus.UNRESOLVED }); }} shouldConfirm={onShouldConfirm(ConfirmAction.UNRESOLVE)} message={confirm(ConfirmAction.UNRESOLVE, true)} confirmLabel={label('unresolve')} title={t('Set status to: Unresolved')}>
          {t('Set status to: Unresolved')}
        </MenuItemActionLink>
        <MenuItemActionLink disabled={!anySelected} onAction={onDelete} shouldConfirm={onShouldConfirm(ConfirmAction.DELETE)} message={confirm(ConfirmAction.DELETE, false)} confirmLabel={label('delete')} title={t('Delete Issues')}>
          {t('Delete Issues')}
        </MenuItemActionLink>
      </DropdownLink>
      {!hasInbox && (<Tooltip title={t('%s real-time updates', realtimeActive ? t('Pause') : t('Enable'))}>
          <ActionButton onClick={onRealtimeChange} label={realtimeActive
                ? t('Pause real-time updates')
                : t('Enable real-time updates')} icon={realtimeActive ? <IconPause size="xs"/> : <IconPlay size="xs"/>}/>
        </Tooltip>)}
    </Wrapper>);
}
export default ActionSet;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  @media (min-width: ", ") {\n    width: 66.66%;\n  }\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  flex: 1;\n  margin: 0 ", ";\n  display: grid;\n  gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-start;\n  white-space: nowrap;\n"], ["\n  @media (min-width: ", ") {\n    width: 66.66%;\n  }\n  @media (min-width: ", ") {\n    width: 50%;\n  }\n  flex: 1;\n  margin: 0 ", ";\n  display: grid;\n  gap: ", ";\n  grid-auto-flow: column;\n  justify-content: flex-start;\n  white-space: nowrap;\n"])), function (p) { return p.theme.breakpoints[0]; }, function (p) { return p.theme.breakpoints[2]; }, space(1), space(0.5));
var templateObject_1;
//# sourceMappingURL=actionSet.jsx.map
import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { bulkDelete, bulkUpdate } from 'app/actionCreators/group';
import { addErrorMessage, addLoadingMessage, clearIndicators, } from 'app/actionCreators/indicator';
import { openReprocessEventModal } from 'app/actionCreators/modal';
import GroupActions from 'app/actions/groupActions';
import ActionButton from 'app/components/actions/button';
import IgnoreActions from 'app/components/actions/ignore';
import ResolveActions from 'app/components/actions/resolve';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Tooltip from 'app/components/tooltip';
import { IconStar } from 'app/icons';
import { IconRefresh } from 'app/icons/iconRefresh';
import { t } from 'app/locale';
import space from 'app/styles/space';
import EventView from 'app/utils/discover/eventView';
import { displayReprocessEventAction } from 'app/utils/displayReprocessEventAction';
import { uniqueId } from 'app/utils/guid';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import ReviewAction from 'app/views/issueList/actions/reviewAction';
import ShareIssue from 'app/views/organizationGroupDetails/actions/shareIssue';
import DeleteAction from './deleteAction';
import SubscribeAction from './subscribeAction';
var Actions = /** @class */ (function (_super) {
    __extends(Actions, _super);
    function Actions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            shareBusy: false,
        };
        _this.onDelete = function () {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            addLoadingMessage(t('Delete event\u2026'));
            bulkDelete(api, {
                orgId: organization.slug,
                projectId: project.slug,
                itemIds: [group.id],
            }, {
                complete: function () {
                    clearIndicators();
                    browserHistory.push("/" + organization.slug + "/" + project.slug + "/");
                },
            });
        };
        _this.onUpdate = function (data) {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            addLoadingMessage(t('Saving changes\u2026'));
            bulkUpdate(api, {
                orgId: organization.slug,
                projectId: project.slug,
                itemIds: [group.id],
                data: data,
            }, {
                complete: clearIndicators,
            });
        };
        _this.onReprocessEvent = function () {
            var _a = _this.props, group = _a.group, organization = _a.organization;
            openReprocessEventModal({ organization: organization, groupId: group.id });
        };
        _this.onToggleShare = function () {
            _this.onShare(!_this.props.group.isPublic);
        };
        _this.onToggleBookmark = function () {
            _this.onUpdate({ isBookmarked: !_this.props.group.isBookmarked });
        };
        _this.onToggleSubscribe = function () {
            _this.onUpdate({ isSubscribed: !_this.props.group.isSubscribed });
        };
        _this.onDiscard = function () {
            var _a = _this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
            var id = uniqueId();
            addLoadingMessage(t('Discarding event\u2026'));
            GroupActions.discard(id, group.id);
            api.request("/issues/" + group.id + "/", {
                method: 'PUT',
                data: { discard: true },
                success: function (response) {
                    GroupActions.discardSuccess(id, group.id, response);
                    browserHistory.push("/" + organization.slug + "/" + project.slug + "/");
                },
                error: function (error) {
                    GroupActions.discardError(id, group.id, error);
                },
                complete: clearIndicators,
            });
        };
        return _this;
    }
    Actions.prototype.componentWillReceiveProps = function (nextProps) {
        if (this.state.shareBusy && nextProps.group.shareId !== this.props.group.shareId) {
            this.setState({ shareBusy: false });
        }
    };
    Actions.prototype.getShareUrl = function (shareId) {
        if (!shareId) {
            return '';
        }
        var path = "/share/issue/" + shareId + "/";
        var _a = window.location, host = _a.host, protocol = _a.protocol;
        return protocol + "//" + host + path;
    };
    Actions.prototype.getDiscoverUrl = function () {
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization;
        var title = group.title, id = group.id, type = group.type;
        var discoverQuery = {
            id: undefined,
            name: title || type,
            fields: ['title', 'release', 'environment', 'user.display', 'timestamp'],
            orderby: '-timestamp',
            query: "issue.id:" + id,
            projects: [Number(project.id)],
            version: 2,
            range: '90d',
        };
        var discoverView = EventView.fromSavedQuery(discoverQuery);
        return discoverView.getResultsViewUrlTarget(organization.slug);
    };
    Actions.prototype.onShare = function (shared) {
        var _a = this.props, group = _a.group, project = _a.project, organization = _a.organization, api = _a.api;
        this.setState({ shareBusy: true });
        // not sure why this is a bulkUpdate
        bulkUpdate(api, {
            orgId: organization.slug,
            projectId: project.slug,
            itemIds: [group.id],
            data: {
                isPublic: shared,
            },
        }, {
            error: function () {
                addErrorMessage(t('Error sharing'));
            },
            complete: function () {
                // shareBusy marked false in componentWillReceiveProps to sync
                // busy state update with shareId update
            },
        });
    };
    Actions.prototype.handleClick = function (disabled, onClick) {
        return function (event) {
            if (disabled) {
                event.preventDefault();
                event.stopPropagation();
                return;
            }
            onClick(event);
        };
    };
    Actions.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, group = _b.group, project = _b.project, organization = _b.organization, disabled = _b.disabled, event = _b.event;
        var status = group.status, isBookmarked = group.isBookmarked;
        var orgFeatures = new Set(organization.features);
        var bookmarkTitle = isBookmarked ? t('Remove bookmark') : t('Bookmark');
        var hasRelease = !!((_a = project.features) === null || _a === void 0 ? void 0 : _a.includes('releases'));
        var isResolved = status === 'resolved';
        var isIgnored = status === 'ignored';
        return (<Wrapper>
        <GuideAnchor target="resolve" position="bottom" offset={space(3)}>
          <ResolveActions disabled={disabled} disableDropdown={disabled} hasRelease={hasRelease} latestRelease={project.latestRelease} onUpdate={this.onUpdate} orgSlug={organization.slug} projectSlug={project.slug} isResolved={isResolved} isAutoResolved={group.status === 'resolved' ? group.statusDetails.autoResolved : undefined}/>
        </GuideAnchor>
        <GuideAnchor target="ignore_delete_discard" position="bottom" offset={space(3)}>
          <IgnoreActions isIgnored={isIgnored} onUpdate={this.onUpdate} disabled={disabled}/>
        </GuideAnchor>
        {orgFeatures.has('inbox') && (<Tooltip disabled={!!group.inbox || disabled} title={t('Issue has been reviewed')}>
            <ReviewAction onUpdate={this.onUpdate} disabled={!group.inbox || disabled}/>
          </Tooltip>)}
        <DeleteAction disabled={disabled} organization={organization} project={project} onDelete={this.onDelete} onDiscard={this.onDiscard}/>
        {orgFeatures.has('shared-issues') && (<ShareIssue disabled={disabled} loading={this.state.shareBusy} isShared={group.isPublic} shareUrl={this.getShareUrl(group.shareId)} onToggle={this.onToggleShare} onReshare={function () { return _this.onShare(true); }}/>)}

        {orgFeatures.has('discover-basic') && (<ActionButton disabled={disabled} to={disabled ? '' : this.getDiscoverUrl()}>
            <GuideAnchor target="open_in_discover">{t('Open in Discover')}</GuideAnchor>
          </ActionButton>)}

        <BookmarkButton disabled={disabled} isActive={group.isBookmarked} title={bookmarkTitle} label={bookmarkTitle} onClick={this.handleClick(disabled, this.onToggleBookmark)} icon={<IconStar isSolid size="xs"/>}/>

        <SubscribeAction disabled={disabled} group={group} onClick={this.handleClick(disabled, this.onToggleSubscribe)}/>

        {displayReprocessEventAction(organization.features, event) && (<ReprocessAction disabled={disabled} icon={<IconRefresh size="xs"/>} title={t('Reprocess this issue')} label={t('Reprocess this issue')} onClick={this.handleClick(disabled, this.onReprocessEvent)}/>)}
      </Wrapper>);
    };
    return Actions;
}(React.Component));
var ReprocessAction = styled(ActionButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var BookmarkButton = styled(ActionButton)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  ", "\n"], ["\n  ",
    "\n"])), function (p) {
    return p.isActive &&
        "\n    background: " + p.theme.yellow100 + ";\n    color: " + p.theme.yellow300 + ";\n    border-color: " + p.theme.yellow300 + ";\n    text-shadow: 0 1px 0 rgba(0, 0, 0, 0.15);\n  ";
});
var Wrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  justify-content: flex-start;\n  align-items: center;\n  grid-auto-flow: column;\n  gap: ", ";\n  margin-top: ", ";\n  white-space: nowrap;\n"], ["\n  display: grid;\n  justify-content: flex-start;\n  align-items: center;\n  grid-auto-flow: column;\n  gap: ", ";\n  margin-top: ", ";\n  white-space: nowrap;\n"])), space(0.5), space(2));
export { Actions };
export default withApi(withOrganization(Actions));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map
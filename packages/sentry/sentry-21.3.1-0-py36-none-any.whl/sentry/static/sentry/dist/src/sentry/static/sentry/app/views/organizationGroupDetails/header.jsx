import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import PropTypes from 'prop-types';
import { fetchOrgMembers } from 'app/actionCreators/members';
import AssigneeSelector from 'app/components/assigneeSelector';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Badge from 'app/components/badge';
import Count from 'app/components/count';
import EventOrGroupTitle from 'app/components/eventOrGroupTitle';
import ErrorLevel from 'app/components/events/errorLevel';
import EventAnnotation from 'app/components/events/eventAnnotation';
import EventMessage from 'app/components/events/eventMessage';
import InboxReason from 'app/components/group/inboxBadges/inboxReason';
import UnhandledInboxTag from 'app/components/group/inboxBadges/unhandledTag';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import ExternalLink from 'app/components/links/externalLink';
import Link from 'app/components/links/link';
import ListLink from 'app/components/links/listLink';
import NavTabs from 'app/components/navTabs';
import SeenByList from 'app/components/seenByList';
import ShortId from 'app/components/shortId';
import Tooltip from 'app/components/tooltip';
import { IconChat } from 'app/icons';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import space from 'app/styles/space';
import { getMessage } from 'app/utils/events';
import withApi from 'app/utils/withApi';
import GroupActions from './actions';
import UnhandledTag, { TagAndMessageWrapper } from './unhandledTag';
import { ReprocessingStatus } from './utils';
var TAB = {
    DETAILS: 'details',
    ACTIVITY: 'activity',
    USER_FEEDBACK: 'user-feedback',
    ATTACHMENTS: 'attachments',
    TAGS: 'tags',
    EVENTS: 'events',
    MERGED: 'merged',
    SIMILAR_ISSUES: 'similar-issues',
};
var GroupHeader = /** @class */ (function (_super) {
    __extends(GroupHeader, _super);
    function GroupHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {};
        return _this;
    }
    GroupHeader.prototype.componentDidMount = function () {
        var _this = this;
        var organization = this.context.organization;
        var _a = this.props, group = _a.group, api = _a.api;
        var project = group.project;
        fetchOrgMembers(api, organization.slug, [project.id]).then(function (memberList) {
            var users = memberList.map(function (member) { return member.user; });
            _this.setState({ memberList: users });
        });
    };
    GroupHeader.prototype.getDisabledTabs = function () {
        var organization = this.context.organization;
        var hasReprocessingV2Feature = organization.features.includes('reprocessing-v2');
        if (!hasReprocessingV2Feature) {
            return [];
        }
        var groupReprocessingStatus = this.props.groupReprocessingStatus;
        if (groupReprocessingStatus === ReprocessingStatus.REPROCESSING) {
            return [
                TAB.ACTIVITY,
                TAB.USER_FEEDBACK,
                TAB.ATTACHMENTS,
                TAB.EVENTS,
                TAB.MERGED,
                TAB.SIMILAR_ISSUES,
                TAB.TAGS,
            ];
        }
        if (groupReprocessingStatus === ReprocessingStatus.REPROCESSED_AND_HASNT_EVENT) {
            return [
                TAB.DETAILS,
                TAB.ATTACHMENTS,
                TAB.EVENTS,
                TAB.MERGED,
                TAB.SIMILAR_ISSUES,
                TAB.TAGS,
                TAB.USER_FEEDBACK,
            ];
        }
        return [];
    };
    GroupHeader.prototype.render = function () {
        var _a;
        var _b = this.props, project = _b.project, group = _b.group, currentTab = _b.currentTab, baseUrl = _b.baseUrl, event = _b.event;
        var _c = this.context, organization = _c.organization, location = _c.location;
        var projectFeatures = new Set(project ? project.features : []);
        var organizationFeatures = new Set(organization ? organization.features : []);
        var userCount = group.userCount;
        var hasSimilarView = projectFeatures.has('similarity-view');
        var hasEventAttachments = organizationFeatures.has('event-attachments');
        var className = 'group-detail';
        if (group.isBookmarked) {
            className += ' isBookmarked';
        }
        if (group.hasSeen) {
            className += ' hasSeen';
        }
        if (group.status === 'resolved') {
            className += ' isResolved';
        }
        var memberList = this.state.memberList;
        var orgId = organization.slug;
        var message = getMessage(group);
        var hasInbox = (_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('inbox');
        var searchTermWithoutQuery = omit(location.query, 'query');
        var eventRouteToObject = {
            pathname: baseUrl + "events/",
            query: searchTermWithoutQuery,
        };
        var disabledTabs = this.getDisabledTabs();
        var disableActions = !!disabledTabs.length;
        return (<div className={className}>
        <div className="row">
          <div className="col-sm-7">
            <TitleWrapper>
              <h3>
                <EventOrGroupTitle hasGuideAnchor data={group}/>
              </h3>
              {hasInbox && group.inbox && (<InboxReasonWrapper>
                  <InboxReason inbox={group.inbox} fontSize="md"/>
                </InboxReasonWrapper>)}
            </TitleWrapper>
            <StyledTagAndMessageWrapper>
              {hasInbox && group.level && <ErrorLevel level={group.level} size="11px"/>}
              {group.isUnhandled && (hasInbox ? <UnhandledInboxTag /> : <UnhandledTag />)}
              <EventMessage message={message} level={hasInbox ? undefined : group.level} annotations={<React.Fragment>
                    {group.logger && (<EventAnnotationWithSpace>
                        <Link to={{
                        pathname: "/organizations/" + orgId + "/issues/",
                        query: { query: 'logger:' + group.logger },
                    }}>
                          {group.logger}
                        </Link>
                      </EventAnnotationWithSpace>)}
                    {group.annotations.map(function (annotation, i) { return (<EventAnnotationWithSpace key={i} dangerouslySetInnerHTML={{ __html: annotation }}/>); })}
                  </React.Fragment>}/>
            </StyledTagAndMessageWrapper>
          </div>

          <div className="col-sm-5 stats">
            <div className="flex flex-justify-right">
              {group.shortId && (<GuideAnchor target="issue_number" position="bottom">
                  <div className="short-id-box count align-right">
                    <h6 className="nav-header">
                      <Tooltip className="help-link" title={t('This identifier is unique across your organization, and can be used to reference an issue in various places, like commit messages.')} position="bottom">
                        <ExternalLink href="https://docs.sentry.io/product/integrations/github/#resolve-via-commit-or-pull-request">
                          {t('Issue #')}
                        </ExternalLink>
                      </Tooltip>
                    </h6>
                    <ShortId shortId={group.shortId} avatar={<StyledProjectBadge project={project} avatarSize={20} hideName/>}/>
                  </div>
                </GuideAnchor>)}
              <div className="count align-right m-l-1">
                <h6 className="nav-header">{t('Events')}</h6>
                {disableActions ? (<Count className="count" value={group.count}/>) : (<Link to={eventRouteToObject}>
                    <Count className="count" value={group.count}/>
                  </Link>)}
              </div>
              <div className="count align-right m-l-1">
                <h6 className="nav-header">{t('Users')}</h6>
                {userCount !== 0 ? (disableActions ? (<Count className="count" value={userCount}/>) : (<Link to={baseUrl + "tags/user/" + location.search}>
                      <Count className="count" value={userCount}/>
                    </Link>)) : (<span>0</span>)}
              </div>
              <div className="assigned-to m-l-1">
                <h6 className="nav-header">{t('Assignee')}</h6>
                <AssigneeSelector id={group.id} memberList={memberList} disabled={disableActions}/>
              </div>
            </div>
          </div>
        </div>
        <SeenByList seenBy={group.seenBy} iconTooltip={t('People who have viewed this issue')}/>
        <GroupActions group={group} project={project} disabled={disableActions} event={event}/>
        <NavTabs>
          <ListLink to={"" + baseUrl + location.search} isActive={function () { return currentTab === TAB.DETAILS; }} disabled={disabledTabs.includes(TAB.DETAILS)}>
            {t('Details')}
          </ListLink>
          <StyledListLink to={baseUrl + "activity/" + location.search} isActive={function () { return currentTab === TAB.ACTIVITY; }} disabled={disabledTabs.includes(TAB.ACTIVITY)}>
            {t('Activity')}
            <Badge>
              {group.numComments}
              <IconChat size="xs"/>
            </Badge>
          </StyledListLink>
          <StyledListLink to={baseUrl + "feedback/" + location.search} isActive={function () { return currentTab === TAB.USER_FEEDBACK; }} disabled={disabledTabs.includes(TAB.USER_FEEDBACK)}>
            {t('User Feedback')} <Badge text={group.userReportCount}/>
          </StyledListLink>
          {hasEventAttachments && (<ListLink to={baseUrl + "attachments/" + location.search} isActive={function () { return currentTab === TAB.ATTACHMENTS; }} disabled={disabledTabs.includes(TAB.ATTACHMENTS)}>
              {t('Attachments')}
            </ListLink>)}
          <ListLink to={baseUrl + "tags/" + location.search} isActive={function () { return currentTab === TAB.TAGS; }} disabled={disabledTabs.includes(TAB.TAGS)}>
            {t('Tags')}
          </ListLink>
          <ListLink to={eventRouteToObject} isActive={function () { return currentTab === TAB.EVENTS; }} disabled={disabledTabs.includes(TAB.EVENTS)}>
            {t('Events')}
          </ListLink>
          <ListLink to={baseUrl + "merged/" + location.search} isActive={function () { return currentTab === TAB.MERGED; }} disabled={disabledTabs.includes(TAB.MERGED)}>
            {t('Merged Issues')}
          </ListLink>
          {hasSimilarView && (<ListLink to={baseUrl + "similar/" + location.search} isActive={function () { return currentTab === TAB.SIMILAR_ISSUES; }} disabled={disabledTabs.includes(TAB.SIMILAR_ISSUES)}>
              {t('Similar Issues')}
            </ListLink>)}
        </NavTabs>
      </div>);
    };
    GroupHeader.contextTypes = {
        location: PropTypes.object,
        organization: SentryTypes.Organization,
    };
    return GroupHeader;
}(React.Component));
export { GroupHeader, TAB };
export default withApi(GroupHeader);
var TitleWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  line-height: 24px;\n"], ["\n  display: flex;\n  line-height: 24px;\n"])));
var InboxReasonWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var StyledTagAndMessageWrapper = styled(TagAndMessageWrapper)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  gap: ", ";\n  justify-content: flex-start;\n  line-height: 1.2;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  gap: ", ";\n  justify-content: flex-start;\n  line-height: 1.2;\n\n  @media (max-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; }, space(2));
var StyledListLink = styled(ListLink)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  svg {\n    margin-left: ", ";\n    margin-bottom: ", ";\n    vertical-align: middle;\n  }\n"], ["\n  svg {\n    margin-left: ", ";\n    margin-bottom: ", ";\n    vertical-align: middle;\n  }\n"])), space(0.5), space(0.25));
var StyledProjectBadge = styled(ProjectBadge)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var EventAnnotationWithSpace = styled(EventAnnotation)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=header.jsx.map
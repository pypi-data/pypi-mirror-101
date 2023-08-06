import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { bulkUpdate } from 'app/actionCreators/group';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import EventOrGroupTitle from 'app/components/eventOrGroupTitle';
import ErrorLevel from 'app/components/events/errorLevel';
import Link from 'app/components/links/link';
import { PanelItem } from 'app/components/panels';
import GroupChart from 'app/components/stream/groupChart';
import { IconChat, IconMute, IconStar } from 'app/icons';
import { t } from 'app/locale';
import GroupStore from 'app/stores/groupStore';
import space from 'app/styles/space';
import { getMessage } from 'app/utils/events';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
var CompactIssueHeader = /** @class */ (function (_super) {
    __extends(CompactIssueHeader, _super);
    function CompactIssueHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CompactIssueHeader.prototype.render = function () {
        var _a = this.props, data = _a.data, organization = _a.organization, projectId = _a.projectId, eventId = _a.eventId;
        var basePath = "/organizations/" + organization.slug + "/issues/";
        var issueLink = eventId
            ? "/organizations/" + organization.slug + "/projects/" + projectId + "/events/" + eventId + "/"
            : "" + basePath + data.id + "/";
        var commentColor = data.subscriptionDetails && data.subscriptionDetails.reason === 'mentioned'
            ? 'success'
            : 'textColor';
        return (<React.Fragment>
        <IssueHeaderMetaWrapper>
          <StyledErrorLevel size="12px" level={data.level} title={data.level}/>
          <h3 className="truncate">
            <IconLink to={issueLink || ''}>
              {data.status === 'ignored' && <IconMute size="xs"/>}
              {data.isBookmarked && <IconStar isSolid size="xs"/>}
              <EventOrGroupTitle data={data}/>
            </IconLink>
          </h3>
        </IssueHeaderMetaWrapper>
        <div className="event-extra">
          <span className="project-name">
            <strong>{data.project.slug}</strong>
          </span>
          {data.numComments !== 0 && (<span>
              <IconLink to={"" + basePath + data.id + "/activity/"} className="comments">
                <IconChat size="xs" color={commentColor}/>
                <span className="tag-count">{data.numComments}</span>
              </IconLink>
            </span>)}
          <span className="culprit">{getMessage(data)}</span>
        </div>
      </React.Fragment>);
    };
    return CompactIssueHeader;
}(React.Component));
var CompactIssue = createReactClass({
    displayName: 'CompactIssue',
    mixins: [Reflux.listenTo(GroupStore, 'onGroupChange')],
    getInitialState: function () {
        return {
            issue: this.props.data || GroupStore.get(this.props.id),
        };
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.id !== this.props.id) {
            this.setState({
                issue: GroupStore.get(this.props.id),
            });
        }
    },
    onGroupChange: function (itemIds) {
        if (!itemIds.has(this.props.id)) {
            return;
        }
        var id = this.props.id;
        var issue = GroupStore.get(id);
        this.setState({
            issue: issue,
        });
    },
    onSnooze: function (duration) {
        var data = {
            status: 'ignored',
        };
        if (duration) {
            data.ignoreDuration = duration;
        }
        this.onUpdate(data);
    },
    onUpdate: function (data) {
        var issue = this.state.issue;
        addLoadingMessage(t('Saving changes\u2026'));
        bulkUpdate(this.props.api, {
            orgId: this.props.organization.slug,
            projectId: issue.project.slug,
            itemIds: [issue.id],
            data: data,
        }, {
            complete: function () {
                clearIndicators();
            },
        });
    },
    render: function () {
        var issue = this.state.issue;
        var organization = this.props.organization;
        var className = 'issue';
        if (issue.isBookmarked) {
            className += ' isBookmarked';
        }
        if (issue.hasSeen) {
            className += ' hasSeen';
        }
        if (issue.status === 'resolved') {
            className += ' isResolved';
        }
        if (issue.status === 'ignored') {
            className += ' isIgnored';
        }
        if (this.props.statsPeriod) {
            className += ' with-graph';
        }
        return (<PanelItem className={className} onClick={this.toggleSelect} flexDirection="column" style={{ paddingTop: '12px', paddingBottom: '6px' }}>
        <CompactIssueHeader data={issue} organization={organization} projectId={issue.project.slug} eventId={this.props.eventId}/>
        {this.props.statsPeriod && (<div className="event-graph">
            <GroupChart statsPeriod={this.props.statsPeriod} data={this.props.data}/>
          </div>)}
        {this.props.children}
      </PanelItem>);
    },
});
export { CompactIssue };
export default withApi(withOrganization(CompactIssue));
var IssueHeaderMetaWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledErrorLevel = styled(ErrorLevel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: block;\n  margin-right: ", ";\n"], ["\n  display: block;\n  margin-right: ", ";\n"])), space(1));
var IconLink = styled(Link)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  & > svg {\n    margin-right: ", ";\n  }\n"], ["\n  & > svg {\n    margin-right: ", ";\n  }\n"])), space(0.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=compactIssue.jsx.map
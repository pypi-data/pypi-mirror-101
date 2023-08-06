import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment-timezone';
import { SectionHeading } from 'app/components/charts/styles';
import DateTime from 'app/components/dateTime';
import Duration from 'app/components/duration';
import EmptyStateWarning from 'app/components/emptyStateWarning';
import Link from 'app/components/links/link';
import { Panel, PanelBody } from 'app/components/panels';
import SeenByList from 'app/components/seenByList';
import TimeSince from 'app/components/timeSince';
import { IconEllipse } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { getTriggerName } from 'app/views/alerts/details/activity/statusItem';
import { IncidentActivityType, IncidentStatus, IncidentStatusMethod, } from 'app/views/alerts/types';
var TimelineIncident = /** @class */ (function (_super) {
    __extends(TimelineIncident, _super);
    function TimelineIncident() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TimelineIncident.prototype.renderActivity = function (activity, idx) {
        var _a, _b;
        var _c = this.props, incident = _c.incident, rule = _c.rule;
        var activities = incident.activities;
        var last = activities && idx === activities.length - 1;
        var authorName = (_b = (_a = activity.user) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Sentry';
        var isDetected = activity.type === IncidentActivityType.DETECTED;
        var isStarted = activity.type === IncidentActivityType.STARTED;
        var isClosed = activity.type === IncidentActivityType.STATUS_CHANGE &&
            activity.value === "" + IncidentStatus.CLOSED;
        var isTriggerChange = activity.type === IncidentActivityType.STATUS_CHANGE && !isClosed;
        // Unknown activity, don't render anything
        if ((!isStarted && !isDetected && !isClosed && !isTriggerChange) ||
            !activities ||
            !activities.length) {
            return null;
        }
        var currentTrigger = getTriggerName(activity.value);
        var title;
        var subtext;
        if (isTriggerChange) {
            var nextActivity = activities.find(function (_a) {
                var previousValue = _a.previousValue;
                return previousValue === activity.value;
            }) ||
                (activity.value &&
                    activity.value === "" + IncidentStatus.OPENED &&
                    activities.find(function (_a) {
                        var type = _a.type;
                        return type === IncidentActivityType.DETECTED;
                    }));
            var activityDuration = (nextActivity
                ? moment(nextActivity.dateCreated)
                : moment()).diff(moment(activity.dateCreated), 'milliseconds');
            title = t('Alert status changed');
            subtext =
                activityDuration !== null &&
                    tct("[currentTrigger]: [duration]", {
                        currentTrigger: currentTrigger,
                        duration: <Duration abbreviation seconds={activityDuration / 1000}/>,
                    });
        }
        else if (isClosed && (incident === null || incident === void 0 ? void 0 : incident.statusMethod) === IncidentStatusMethod.RULE_UPDATED) {
            title = t('Alert auto-resolved');
            subtext = t('Alert rule modified or deleted');
        }
        else if (isClosed && (incident === null || incident === void 0 ? void 0 : incident.statusMethod) !== IncidentStatusMethod.RULE_UPDATED) {
            title = t('Resolved');
            subtext = tct('by [authorName]', { authorName: authorName });
        }
        else if (isDetected) {
            title = (incident === null || incident === void 0 ? void 0 : incident.alertRule)
                ? t('Alert was created')
                : tct('[authorName] created an alert', { authorName: authorName });
            subtext = <DateTime timeOnly date={activity.dateCreated}/>;
        }
        else if (isStarted) {
            var dateEnded = moment(activity.dateCreated)
                .add(rule.timeWindow, 'minutes')
                .utc()
                .format();
            var timeOnly = Boolean(dateEnded && moment(activity.dateCreated).date() === moment(dateEnded).date());
            title = t('Trigger conditions were met');
            subtext = (<React.Fragment>
          <DateTime timeOnly={timeOnly} timeAndDate={!timeOnly} date={activity.dateCreated}/>
          {' — '}
          <DateTime timeOnly={timeOnly} timeAndDate={!timeOnly} date={dateEnded}/>
        </React.Fragment>);
        }
        else {
            return null;
        }
        return (<Activity key={activity.id}>
        <ActivityTrack>
          <IconEllipse size="sm" color="gray300"/>
          {!last && <VerticalDivider />}
        </ActivityTrack>

        <ActivityBody>
          <ActivityTime>
            <StyledTimeSince date={activity.dateCreated} suffix={t('ago')}/>
            <HorizontalDivider />
          </ActivityTime>
          <ActivityText>
            {title}
            {subtext && <ActivitySubText>{subtext}</ActivitySubText>}
          </ActivityText>
        </ActivityBody>
      </Activity>);
    };
    TimelineIncident.prototype.render = function () {
        var _this = this;
        var _a = this.props, incident = _a.incident, orgId = _a.orgId;
        return (<IncidentSection key={incident.identifier}>
        <IncidentHeader>
          <Link to={"/organizations/" + orgId + "/alerts/" + incident.identifier + "/?redirect=false"}>
            {tct('Alert #[id]', { id: incident.identifier })}
          </Link>
          <SeenByTab>
            {incident && (<StyledSeenByList iconPosition="right" seenBy={incident.seenBy} iconTooltip={t('People who have viewed this alert')}/>)}
          </SeenByTab>
        </IncidentHeader>
        {incident.activities && (<IncidentBody>
            {incident.activities
                    .filter(function (activity) { return activity.type !== IncidentActivityType.COMMENT; })
                    .map(function (activity, idx) { return _this.renderActivity(activity, idx); })}
          </IncidentBody>)}
      </IncidentSection>);
    };
    return TimelineIncident;
}(React.Component));
var Timeline = /** @class */ (function (_super) {
    __extends(Timeline, _super);
    function Timeline() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.renderEmptyMessage = function () {
            return (<StyledEmptyStateWarning small withIcon={false}>
        <p>{t('No alerts triggered during this time')}</p>
      </StyledEmptyStateWarning>);
        };
        return _this;
    }
    Timeline.prototype.render = function () {
        var _a = this.props, api = _a.api, incidents = _a.incidents, orgId = _a.orgId, rule = _a.rule;
        return (<History>
        <SectionHeading>{t('History')}</SectionHeading>
        <ScrollPanel>
          <PanelBody withPadding>
            {incidents && rule && incidents.length
                ? incidents.map(function (incident) { return (<TimelineIncident key={incident.identifier} api={api} orgId={orgId} incident={incident} rule={rule}/>); })
                : this.renderEmptyMessage()}
          </PanelBody>
        </ScrollPanel>
      </History>);
    };
    return Timeline;
}(React.Component));
export default Timeline;
var History = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 30px;\n"], ["\n  margin-bottom: 30px;\n"])));
var ScrollPanel = styled(Panel)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  max-height: 500px;\n  overflow: scroll;\n  -ms-overflow-style: none;\n  scrollbar-width: none;\n  &::-webkit-scrollbar {\n    display: none;\n  }\n\n  p {\n    font-size: ", ";\n  }\n"], ["\n  max-height: 500px;\n  overflow: scroll;\n  -ms-overflow-style: none;\n  scrollbar-width: none;\n  &::-webkit-scrollbar {\n    display: none;\n  }\n\n  p {\n    font-size: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; });
var StyledEmptyStateWarning = styled(EmptyStateWarning)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var IncidentSection = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  &:not(:first-of-type) {\n    margin-top: 15px;\n  }\n"], ["\n  &:not(:first-of-type) {\n    margin-top: 15px;\n  }\n"])));
var IncidentHeader = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  margin-bottom: ", ";\n"], ["\n  display: flex;\n  margin-bottom: ", ";\n"])), space(1.5));
var SeenByTab = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"], ["\n  flex: 1;\n  margin-left: ", ";\n  margin-right: 0;\n\n  .nav-tabs > & {\n    margin-right: 0;\n  }\n"])), space(2));
var StyledSeenByList = styled(SeenByList)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-top: 0;\n"], ["\n  margin-top: 0;\n"])));
var IncidentBody = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var Activity = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
var ActivityTrack = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-right: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin-right: ", ";\n"])), space(1));
var ActivityBody = styled('div')(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n"], ["\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n"])));
var ActivityTime = styled('li')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4;\n"], ["\n  display: flex;\n  align-items: center;\n  color: ", ";\n  font-size: ", ";\n  line-height: 1.4;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; });
var StyledTimeSince = styled(TimeSince)(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var ActivityText = styled('div')(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  flex-direction: row;\n  margin-bottom: ", ";\n  font-size: ", ";\n"], ["\n  flex-direction: row;\n  margin-bottom: ", ";\n  font-size: ", ";\n"])), space(1.5), function (p) { return p.theme.fontSizeMedium; });
var ActivitySubText = styled('span')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  display: inline-block;\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"], ["\n  display: inline-block;\n  color: ", ";\n  font-size: ", ";\n  margin-left: ", ";\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeMedium; }, space(0.5));
var HorizontalDivider = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  flex: 1;\n  height: 0;\n  border-bottom: 1px solid ", ";\n  margin: 5px 0;\n"], ["\n  flex: 1;\n  height: 0;\n  border-bottom: 1px solid ", ";\n  margin: 5px 0;\n"])), function (p) { return p.theme.innerBorder; });
var VerticalDivider = styled('div')(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  flex: 1;\n  width: 0;\n  margin: 0 5px;\n  border-left: 1px dashed ", ";\n"], ["\n  flex: 1;\n  width: 0;\n  margin: 0 5px;\n  border-left: 1px dashed ", ";\n"])), function (p) { return p.theme.innerBorder; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17;
//# sourceMappingURL=timeline.jsx.map
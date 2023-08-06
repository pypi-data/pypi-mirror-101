import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import { SectionHeading } from 'app/components/charts/styles';
import { getInterval } from 'app/components/charts/utils';
import DateTime from 'app/components/dateTime';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import Duration from 'app/components/duration';
import { KeyValueTable, KeyValueTableRow } from 'app/components/keyValueTable';
import * as Layout from 'app/components/layouts/thirds';
import { Panel, PanelBody } from 'app/components/panels';
import Placeholder from 'app/components/placeholder';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark, IconFire, IconInfo, IconUser, IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import Projects from 'app/utils/projects';
import theme from 'app/utils/theme';
import Timeline from 'app/views/alerts/rules/details/timeline';
import { DATASET_EVENT_TYPE_FILTERS } from 'app/views/settings/incidentRules/constants';
import { AlertRuleThresholdType, Dataset, } from 'app/views/settings/incidentRules/types';
import { extractEventTypeFilterFromRule } from 'app/views/settings/incidentRules/utils/getEventTypeFilter';
import { IncidentStatus } from '../../types';
import { API_INTERVAL_POINTS_LIMIT, TIME_OPTIONS } from './constants';
import MetricChart from './metricChart';
import RelatedIssues from './relatedIssues';
import RelatedTransactions from './relatedTransactions';
var DetailsBody = /** @class */ (function (_super) {
    __extends(DetailsBody, _super);
    function DetailsBody() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    DetailsBody.prototype.getMetricText = function () {
        var rule = this.props.rule;
        if (!rule) {
            return '';
        }
        var aggregate = rule.aggregate;
        return tct('[metric]', {
            metric: aggregate,
        });
    };
    DetailsBody.prototype.getTimeWindow = function () {
        var rule = this.props.rule;
        if (!rule) {
            return '';
        }
        var timeWindow = rule.timeWindow;
        return tct('[window]', {
            window: <Duration seconds={timeWindow * 60}/>,
        });
    };
    DetailsBody.prototype.getInterval = function () {
        var _a = this.props, _b = _a.timePeriod, start = _b.start, end = _b.end, rule = _a.rule;
        var startDate = moment.utc(start);
        var endDate = moment.utc(end);
        var timeWindow = rule === null || rule === void 0 ? void 0 : rule.timeWindow;
        if (timeWindow &&
            endDate.diff(startDate) < API_INTERVAL_POINTS_LIMIT * timeWindow * 60 * 1000) {
            return timeWindow + "m";
        }
        return getInterval({ start: start, end: end }, true);
    };
    DetailsBody.prototype.getFilter = function () {
        var rule = this.props.rule;
        if (!rule) {
            return null;
        }
        return (<Filters>
        <span>
          {(rule === null || rule === void 0 ? void 0 : rule.dataset) && <code>{DATASET_EVENT_TYPE_FILTERS[rule.dataset]}</code>}
        </span>
        <span>{(rule === null || rule === void 0 ? void 0 : rule.query) && <code>{rule === null || rule === void 0 ? void 0 : rule.query}</code>}</span>
      </Filters>);
    };
    DetailsBody.prototype.renderTrigger = function (trigger) {
        var rule = this.props.rule;
        if (!rule) {
            return null;
        }
        var icon = trigger.label === 'critical' ? (<IconFire color="red300" size="sm"/>) : trigger.label === 'warning' ? (<IconWarning color="yellow300" size="sm"/>) : (<IconCheckmark color="green300" size="sm" isCircled/>);
        var thresholdTypeText = rule.thresholdType === AlertRuleThresholdType.ABOVE ? t('Above') : t('Below');
        return (<TriggerCondition>
        {icon}
        <TriggerText>{thresholdTypeText + " " + trigger.alertThreshold}</TriggerText>
      </TriggerCondition>);
    };
    DetailsBody.prototype.renderRuleDetails = function () {
        var _a, _b, _c;
        var rule = this.props.rule;
        if (rule === undefined) {
            return <Placeholder height="200px"/>;
        }
        var criticalTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'critical';
        });
        var warningTrigger = rule === null || rule === void 0 ? void 0 : rule.triggers.find(function (_a) {
            var label = _a.label;
            return label === 'warning';
        });
        var ownerId = (_a = rule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        var teamActor = ownerId && { type: 'team', id: ownerId, name: '' };
        return (<React.Fragment>
        <SidebarHeading>{t('Metric')}</SidebarHeading>
        <RuleText>{this.getMetricText()}</RuleText>

        <SidebarHeading>{t('Environment')}</SidebarHeading>
        <RuleText>{(_b = rule.environment) !== null && _b !== void 0 ? _b : 'All'}</RuleText>

        <SidebarHeading>{t('Filters')}</SidebarHeading>
        {this.getFilter()}

        <SidebarHeading>{t('Conditions')}</SidebarHeading>
        {criticalTrigger && this.renderTrigger(criticalTrigger)}
        {warningTrigger && this.renderTrigger(warningTrigger)}

        <SidebarHeading>{t('Other Details')}</SidebarHeading>
        <KeyValueTable>
          <Feature features={['organizations:team-alerts-ownership']}>
            <KeyValueTableRow keyName={t('Team')} value={teamActor ? (<ActorAvatar actor={teamActor} size={24}/>) : (<IconUser size="20px" color="gray400"/>)}/>
          </Feature>

          {rule.createdBy && (<KeyValueTableRow keyName={t('Created By')} value={<CreatedBy>{(_c = rule.createdBy.name) !== null && _c !== void 0 ? _c : '-'}</CreatedBy>}/>)}

          {rule.dateModified && (<KeyValueTableRow keyName={t('Last Modified')} value={<TimeSince date={rule.dateModified} suffix={t('ago')}/>}/>)}
        </KeyValueTable>
      </React.Fragment>);
    };
    DetailsBody.prototype.renderMetricStatus = function () {
        var incidents = this.props.incidents;
        // get current status
        var activeIncident = incidents === null || incidents === void 0 ? void 0 : incidents.find(function (_a) {
            var dateClosed = _a.dateClosed;
            return !dateClosed;
        });
        var status = activeIncident ? activeIncident.status : IncidentStatus.CLOSED;
        var statusText = t('Okay');
        var Icon = IconCheckmark;
        var color = theme.green300;
        if (status === IncidentStatus.CRITICAL) {
            statusText = t('Critical');
            Icon = IconFire;
            color = theme.red300;
        }
        else if (status === IncidentStatus.WARNING) {
            statusText = t('Warning');
            Icon = IconWarning;
            color = theme.yellow300;
        }
        var latestIncident = (incidents === null || incidents === void 0 ? void 0 : incidents.length) ? incidents[0] : null;
        // The date at which the alert was triggered or resolved
        var activityDate = activeIncident
            ? activeIncident.dateStarted
            : latestIncident
                ? latestIncident.dateClosed
                : null;
        return (<StatusContainer>
        <div>
          <SidebarHeading noMargin>{t('Status')}</SidebarHeading>
          <ItemValue>
            <AlertBadge color={color} icon={Icon}>
              <AlertIconWrapper>
                <Icon color="white"/>
              </AlertIconWrapper>
            </AlertBadge>
            <IncidentStatusValue color={color}>{statusText}</IncidentStatusValue>
          </ItemValue>
        </div>
        <div>
          <SidebarHeading noMargin>
            {activeIncident ? t('Last Triggered') : t('Last Resolved')}
          </SidebarHeading>
          <ItemValue>{activityDate ? <TimeSince date={activityDate}/> : '-'}</ItemValue>
        </div>
      </StatusContainer>);
    };
    DetailsBody.prototype.renderLoading = function () {
        return (<Layout.Body>
        <Layout.Main>
          <Placeholder height="38px"/>
          <ChartPanel>
            <PanelBody withPadding>
              <Placeholder height="200px"/>
            </PanelBody>
          </ChartPanel>
        </Layout.Main>
        <Layout.Side>
          <Placeholder height="200px"/>
        </Layout.Side>
      </Layout.Body>);
    };
    DetailsBody.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, rule = _a.rule, incidents = _a.incidents, location = _a.location, organization = _a.organization, timePeriod = _a.timePeriod, orgId = _a.params.orgId;
        if (!rule) {
            return this.renderLoading();
        }
        var query = rule.query, projectSlugs = rule.projects;
        var queryWithTypeFilter = (query + " " + extractEventTypeFilterFromRule(rule)).trim();
        return (<Projects orgId={orgId} slugs={projectSlugs}>
        {function (_a) {
                var initiallyLoaded = _a.initiallyLoaded, projects = _a.projects;
                return initiallyLoaded ? (<React.Fragment>
              <StyledLayoutBody>
                <StyledAlert type="info" icon={<IconInfo size="md"/>}>
                  {t('You’re viewing the new alert details page. To view the old experience, select an alert on the chart or in the history.')}
                </StyledAlert>
              </StyledLayoutBody>
              <Layout.Body>
                <Layout.Main>
                  <HeaderContainer>
                    <div>
                      <SidebarHeading noMargin>{t('Display')}</SidebarHeading>
                      <ChartControls>
                        <DropdownControl label={timePeriod.label}>
                          {TIME_OPTIONS.map(function (_a) {
                        var label = _a.label, value = _a.value;
                        return (<DropdownItem key={value} eventKey={value} onSelect={_this.props.handleTimePeriodChange}>
                              {label}
                            </DropdownItem>);
                    })}
                        </DropdownControl>
                        {timePeriod.custom && (<StyledTimeRange>
                            <DateTime date={moment.utc(timePeriod.start)} timeAndDate/>
                            {' — '}
                            <DateTime date={moment.utc(timePeriod.end)} timeAndDate/>
                          </StyledTimeRange>)}
                      </ChartControls>
                    </div>
                    <div>
                      <SidebarHeading noMargin>
                        {t('Time Interval')}
                        <Tooltip title={t('This is the time period which the metric is evaluated by.')}>
                          <IconInfo size="xs"/>
                        </Tooltip>
                      </SidebarHeading>

                      <RuleText>{_this.getTimeWindow()}</RuleText>
                    </div>
                  </HeaderContainer>

                  <MetricChart api={api} rule={rule} incidents={incidents} timePeriod={timePeriod} organization={organization} projects={projects} metricText={_this.getMetricText()} interval={_this.getInterval()} filter={_this.getFilter()} query={queryWithTypeFilter} orgId={orgId}/>
                  <DetailWrapper>
                    <ActivityWrapper>
                      {(rule === null || rule === void 0 ? void 0 : rule.dataset) === Dataset.ERRORS && (<RelatedIssues organization={organization} rule={rule} projects={(projects || []).filter(function (project) {
                            return rule.projects.includes(project.slug);
                        })} timePeriod={timePeriod}/>)}
                      {(rule === null || rule === void 0 ? void 0 : rule.dataset) === Dataset.TRANSACTIONS && (<RelatedTransactions organization={organization} location={location} rule={rule} projects={(projects || []).filter(function (project) {
                            return rule.projects.includes(project.slug);
                        })} start={timePeriod.start} end={timePeriod.end} filter={DATASET_EVENT_TYPE_FILTERS[rule.dataset]}/>)}
                    </ActivityWrapper>
                  </DetailWrapper>
                </Layout.Main>
                <Layout.Side>
                  {_this.renderMetricStatus()}
                  <Timeline api={api} orgId={orgId} rule={rule} incidents={incidents}/>
                  {_this.renderRuleDetails()}
                </Layout.Side>
              </Layout.Body>
            </React.Fragment>) : (<Placeholder height="200px"/>);
            }}
      </Projects>);
    };
    return DetailsBody;
}(React.Component));
export default DetailsBody;
var DetailWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"], ["\n  display: flex;\n  flex: 1;\n\n  @media (max-width: ", ") {\n    flex-direction: column-reverse;\n  }\n"])), function (p) { return p.theme.breakpoints[0]; });
var HeaderContainer = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  gap: ", ";\n"], ["\n  display: flex;\n  gap: ", ";\n"])), space(4));
var StyledLayoutBody = styled(Layout.Body)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 0;\n  padding-bottom: 0 !important;\n  @media (min-width: ", ") {\n    grid-template-columns: auto;\n  }\n"], ["\n  flex-grow: 0;\n  padding-bottom: 0 !important;\n  @media (min-width: ", ") {\n    grid-template-columns: auto;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var StyledAlert = styled(Alert)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var ActivityWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  width: 100%;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  width: 100%;\n"])));
var ItemValue = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-start;\n  align-items: center;\n  position: relative;\n  font-size: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-start;\n  align-items: center;\n  position: relative;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var IncidentStatusValue = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-left: 30px;\n  color: ", ";\n"], ["\n  margin-left: 30px;\n  color: ", ";\n"])), function (p) { return p.color; });
var AlertBadge = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n  position: absolute;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n  left: 3px;\n\n  &:before {\n    content: '';\n    width: 20px;\n    height: 20px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"], ["\n  display: flex;\n  position: absolute;\n  align-items: center;\n  justify-content: center;\n  flex-shrink: 0;\n  /* icon warning needs to be treated differently to look visually centered */\n  line-height: ", ";\n  left: 3px;\n\n  &:before {\n    content: '';\n    width: 20px;\n    height: 20px;\n    border-radius: ", ";\n    background-color: ", ";\n    transform: rotate(45deg);\n  }\n"])), function (p) { return (p.icon === IconWarning ? undefined : 1); }, function (p) { return p.theme.borderRadius; }, function (p) { return p.color; });
var AlertIconWrapper = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  position: absolute;\n\n  svg {\n    width: 13px;\n    position: relative;\n    top: 1px;\n  }\n"], ["\n  position: absolute;\n\n  svg {\n    width: 13px;\n    position: relative;\n    top: 1px;\n  }\n"])));
var StatusContainer = styled('div')(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: 16px;\n  margin-bottom: 20px;\n"], ["\n  display: grid;\n  grid-template-columns: 50% 50%;\n  grid-row-gap: 16px;\n  margin-bottom: 20px;\n"])));
var SidebarHeading = styled(SectionHeading)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  margin-top: ", ";\n  line-height: 1;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  margin-top: ", ";\n  line-height: 1;\n"])), function (p) { return (p.noMargin ? 0 : space(2)); });
var ChartControls = styled('div')(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n"], ["\n  display: flex;\n  flex-direction: row;\n  align-items: center;\n"])));
var StyledTimeRange = styled('div')(templateObject_13 || (templateObject_13 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(2));
var ChartPanel = styled(Panel)(templateObject_14 || (templateObject_14 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
var RuleText = styled('div')(templateObject_15 || (templateObject_15 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeLarge; });
var Filters = styled('div')(templateObject_16 || (templateObject_16 = __makeTemplateObject(["\n  display: inline-flex;\n  width: 100%;\n  overflow-wrap: break-word;\n  font-size: ", ";\n  gap: ", ";\n"], ["\n  display: inline-flex;\n  width: 100%;\n  overflow-wrap: break-word;\n  font-size: ", ";\n  gap: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(1));
var TriggerCondition = styled('div')(templateObject_17 || (templateObject_17 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var TriggerText = styled('div')(templateObject_18 || (templateObject_18 = __makeTemplateObject(["\n  margin-left: ", ";\n  white-space: nowrap;\n"], ["\n  margin-left: ", ";\n  white-space: nowrap;\n"])), space(1));
var CreatedBy = styled('div')(templateObject_19 || (templateObject_19 = __makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12, templateObject_13, templateObject_14, templateObject_15, templateObject_16, templateObject_17, templateObject_18, templateObject_19;
//# sourceMappingURL=body.jsx.map
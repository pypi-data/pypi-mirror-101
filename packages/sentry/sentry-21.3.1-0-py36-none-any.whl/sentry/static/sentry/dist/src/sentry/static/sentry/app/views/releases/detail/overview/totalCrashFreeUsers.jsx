import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import moment from 'moment';
import AsyncComponent from 'app/components/asyncComponent';
import Count from 'app/components/count';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t, tn } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { displayCrashFreePercent } from '../../utils';
import { getInterval } from './chart/utils';
import { SectionHeading, Wrapper } from './styles';
var TotalCrashFreeUsers = /** @class */ (function (_super) {
    __extends(TotalCrashFreeUsers, _super);
    function TotalCrashFreeUsers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    TotalCrashFreeUsers.prototype.getEndpoints = function () {
        var _a = this.props, location = _a.location, defaultStatsPeriod = _a.defaultStatsPeriod, organization = _a.organization, projectSlug = _a.projectSlug, version = _a.version, selection = _a.selection;
        return [
            [
                'releaseStats',
                "/projects/" + organization.slug + "/" + projectSlug + "/releases/" + version + "/stats/",
                {
                    query: __assign(__assign({}, getParams(pick(location.query, __spreadArray([], __read(Object.values(URL_PARAM)))), {
                        defaultStatsPeriod: defaultStatsPeriod,
                    })), { interval: getInterval(selection.datetime), type: 'sessions' }),
                },
            ],
        ];
    };
    TotalCrashFreeUsers.prototype.renderLoading = function () {
        return this.renderBody();
    };
    TotalCrashFreeUsers.prototype.renderBody = function () {
        var _a;
        var crashFreeTimeBreakdown = (_a = this.state.releaseStats) === null || _a === void 0 ? void 0 : _a.usersBreakdown;
        if (!(crashFreeTimeBreakdown === null || crashFreeTimeBreakdown === void 0 ? void 0 : crashFreeTimeBreakdown.length)) {
            return null;
        }
        var timeline = crashFreeTimeBreakdown
            .map(function (_a, index, data) {
            var date = _a.date, crashFreeUsers = _a.crashFreeUsers, totalUsers = _a.totalUsers;
            // count number of crash free users from knowing percent and total
            var crashFreeUserCount = Math.round(((crashFreeUsers !== null && crashFreeUsers !== void 0 ? crashFreeUsers : 0) * totalUsers) / 100);
            // first item of timeline is release creation date, then we want to have relative date label
            var dateLabel = index === 0
                ? t('Release created')
                : moment(data[0].date).from(date, true) + " " + t('later');
            return { date: moment(date), dateLabel: dateLabel, crashFreeUsers: crashFreeUsers, crashFreeUserCount: crashFreeUserCount };
        })
            // remove those timeframes that are in the future
            .filter(function (item) { return item.date.isBefore(); })
            // we want timeline to go from bottom to up
            .reverse();
        if (!timeline.length) {
            return null;
        }
        return (<Wrapper>
        <SectionHeading>{t('Total Crash Free Users')}</SectionHeading>
        <Timeline>
          {timeline.map(function (row) { return (<Row key={row.date.toString()}>
              <InnerRow>
                <Text bold>{row.date.format('MMMM D')}</Text>
                <Text bold right>
                  <Count value={row.crashFreeUserCount}/>{' '}
                  {tn('user', 'users', row.crashFreeUserCount)}
                </Text>
              </InnerRow>
              <InnerRow>
                <Text>{row.dateLabel}</Text>
                <Text right>
                  {defined(row.crashFreeUsers)
                    ? displayCrashFreePercent(row.crashFreeUsers)
                    : '-'}
                </Text>
              </InnerRow>
            </Row>); })}
        </Timeline>
      </Wrapper>);
    };
    return TotalCrashFreeUsers;
}(AsyncComponent));
var Timeline = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  line-height: 1.2;\n"], ["\n  font-size: ", ";\n  line-height: 1.2;\n"])), function (p) { return p.theme.fontSizeMedium; });
var DOT_SIZE = 10;
var Row = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  border-left: 1px solid ", ";\n  padding-left: ", ";\n  padding-bottom: ", ";\n  margin-left: ", ";\n  position: relative;\n\n  &:before {\n    content: '';\n    width: ", "px;\n    height: ", "px;\n    border-radius: 100%;\n    background-color: ", ";\n    position: absolute;\n    top: 0;\n    left: -", "px;\n  }\n\n  &:last-child {\n    border-left: 0;\n  }\n"], ["\n  border-left: 1px solid ", ";\n  padding-left: ", ";\n  padding-bottom: ", ";\n  margin-left: ", ";\n  position: relative;\n\n  &:before {\n    content: '';\n    width: ", "px;\n    height: ", "px;\n    border-radius: 100%;\n    background-color: ", ";\n    position: absolute;\n    top: 0;\n    left: -", "px;\n  }\n\n  &:last-child {\n    border-left: 0;\n  }\n"])), function (p) { return p.theme.border; }, space(2), space(1), space(1), DOT_SIZE, DOT_SIZE, function (p) { return p.theme.purple300; }, Math.floor(DOT_SIZE / 2));
var InnerRow = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-column-gap: ", ";\n  grid-auto-flow: column;\n  grid-auto-columns: 1fr;\n\n  padding-bottom: ", ";\n"], ["\n  display: grid;\n  grid-column-gap: ", ";\n  grid-auto-flow: column;\n  grid-auto-columns: 1fr;\n\n  padding-bottom: ", ";\n"])), space(2), space(0.5));
var Text = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  text-align: ", ";\n  color: ", ";\n  padding-bottom: ", ";\n  ", ";\n"], ["\n  text-align: ", ";\n  color: ", ";\n  padding-bottom: ", ";\n  ", ";\n"])), function (p) { return (p.right ? 'right' : 'left'); }, function (p) { return (p.bold ? p.theme.textColor : p.theme.gray300); }, space(0.25), overflowEllipsis);
export default TotalCrashFreeUsers;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=totalCrashFreeUsers.jsx.map
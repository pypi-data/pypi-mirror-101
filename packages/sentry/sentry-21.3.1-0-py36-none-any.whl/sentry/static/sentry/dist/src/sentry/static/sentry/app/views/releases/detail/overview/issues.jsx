import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import pick from 'lodash/pick';
import Feature from 'app/components/acl/feature';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import DiscoverButton from 'app/components/discoverButton';
import DropdownButton from 'app/components/dropdownButton';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import GroupList from 'app/components/issues/groupList';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { Panel } from 'app/components/panels';
import { DEFAULT_RELATIVE_PERIODS } from 'app/constants';
import { URL_PARAM } from 'app/constants/globalSelectionHeader';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { QueryResults, stringifyQueryObject } from 'app/utils/tokenizeSearch';
import EmptyState from '../emptyState';
import { getReleaseEventView } from './chart/utils';
var IssuesType;
(function (IssuesType) {
    IssuesType["NEW"] = "new";
    IssuesType["UNHANDLED"] = "unhandled";
    IssuesType["RESOLVED"] = "resolved";
    IssuesType["ALL"] = "all";
})(IssuesType || (IssuesType = {}));
var Issues = /** @class */ (function (_super) {
    __extends(Issues, _super);
    function Issues() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            issuesType: IssuesType.NEW,
        };
        _this.handleIssuesTypeSelection = function (issuesType) {
            _this.setState({ issuesType: issuesType });
        };
        _this.renderEmptyMessage = function () {
            var selection = _this.props.selection;
            var issuesType = _this.state.issuesType;
            var selectedTimePeriod = DEFAULT_RELATIVE_PERIODS[selection.datetime.period];
            var displayedPeriod = selectedTimePeriod
                ? selectedTimePeriod.toLowerCase()
                : t('given timeframe');
            return (<EmptyState>
        <React.Fragment>
          {issuesType === IssuesType.NEW &&
                    tct('No new issues for the [timePeriod].', {
                        timePeriod: displayedPeriod,
                    })}
          {issuesType === IssuesType.UNHANDLED &&
                    tct('No unhandled issues for the [timePeriod].', {
                        timePeriod: displayedPeriod,
                    })}
          {issuesType === IssuesType.RESOLVED && t('No resolved issues.')}
          {issuesType === IssuesType.ALL &&
                    tct('No issues for the [timePeriod].', {
                        timePeriod: displayedPeriod,
                    })}
        </React.Fragment>
      </EmptyState>);
        };
        return _this;
    }
    Issues.prototype.getDiscoverUrl = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId, selection = _a.selection;
        var discoverView = getReleaseEventView(selection, version);
        return discoverView.getResultsViewUrlTarget(orgId);
    };
    Issues.prototype.getIssuesUrl = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId;
        var issuesType = this.state.issuesType;
        var queryParams = this.getIssuesEndpoint().queryParams;
        var query = new QueryResults([]);
        switch (issuesType) {
            case IssuesType.NEW:
                query.setTagValues('firstRelease', [version]);
                break;
            case IssuesType.UNHANDLED:
                query.setTagValues('release', [version]);
                query.setTagValues('error.handled', ['0']);
                break;
            case IssuesType.RESOLVED:
            case IssuesType.ALL:
            default:
                query.setTagValues('release', [version]);
        }
        return {
            pathname: "/organizations/" + orgId + "/issues/",
            query: __assign(__assign({}, queryParams), { limit: undefined, cursor: undefined, query: stringifyQueryObject(query) }),
        };
    };
    Issues.prototype.getIssuesEndpoint = function () {
        var _a = this.props, version = _a.version, orgId = _a.orgId, location = _a.location, defaultStatsPeriod = _a.defaultStatsPeriod;
        var issuesType = this.state.issuesType;
        var queryParams = __assign(__assign({}, getParams(pick(location.query, __spreadArray(__spreadArray([], __read(Object.values(URL_PARAM))), ['cursor'])), {
            defaultStatsPeriod: defaultStatsPeriod,
        })), { limit: 10, sort: 'new' });
        switch (issuesType) {
            case IssuesType.ALL:
                return {
                    path: "/organizations/" + orgId + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: stringifyQueryObject(new QueryResults(["release:" + version])) }),
                };
            case IssuesType.RESOLVED:
                return {
                    path: "/organizations/" + orgId + "/releases/" + version + "/resolved/",
                    queryParams: __assign(__assign({}, queryParams), { query: '' }),
                };
            case IssuesType.UNHANDLED:
                return {
                    path: "/organizations/" + orgId + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: stringifyQueryObject(new QueryResults(["release:" + version, 'error.handled:0'])) }),
                };
            case IssuesType.NEW:
            default:
                return {
                    path: "/organizations/" + orgId + "/issues/",
                    queryParams: __assign(__assign({}, queryParams), { query: stringifyQueryObject(new QueryResults(["first-release:" + version])) }),
                };
        }
    };
    Issues.prototype.render = function () {
        var _this = this;
        var issuesType = this.state.issuesType;
        var orgId = this.props.orgId;
        var _a = this.getIssuesEndpoint(), path = _a.path, queryParams = _a.queryParams;
        var issuesTypes = [
            { value: IssuesType.NEW, label: t('New Issues') },
            { value: IssuesType.RESOLVED, label: t('Resolved Issues') },
            { value: IssuesType.UNHANDLED, label: t('Unhandled Issues') },
            { value: IssuesType.ALL, label: t('All Issues') },
        ];
        return (<React.Fragment>
        <ControlsWrapper>
          <DropdownControl button={function (_a) {
                var _b;
                var isOpen = _a.isOpen, getActorProps = _a.getActorProps;
                return (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} prefix={t('Filter')} size="small">
                {(_b = issuesTypes.find(function (i) { return i.value === issuesType; })) === null || _b === void 0 ? void 0 : _b.label}
              </StyledDropdownButton>);
            }}>
            {issuesTypes.map(function (_a) {
                var value = _a.value, label = _a.label;
                return (<StyledDropdownItem key={value} onSelect={_this.handleIssuesTypeSelection} data-test-id={"filter-" + value} eventKey={value} isActive={value === issuesType}>
                {label}
              </StyledDropdownItem>);
            })}
          </DropdownControl>

          <OpenInButtonBar gap={1}>
            <Button to={this.getIssuesUrl()} size="small" data-test-id="issues-button">
              {t('Open in Issues')}
            </Button>

            <Feature features={['discover-basic']}>
              <GuideAnchor target="release_issues_open_in_discover">
                <DiscoverButton to={this.getDiscoverUrl()} size="small" data-test-id="discover-button">
                  {t('Open in Discover')}
                </DiscoverButton>
              </GuideAnchor>
            </Feature>
          </OpenInButtonBar>
        </ControlsWrapper>
        <TableWrapper data-test-id="release-wrapper">
          <GroupList orgId={orgId} endpointPath={path} queryParams={queryParams} query="" canSelectGroups={false} withChart={false} renderEmptyMessage={this.renderEmptyMessage}/>
        </TableWrapper>
      </React.Fragment>);
    };
    return Issues;
}(React.Component));
var ControlsWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space(1), function (p) { return p.theme.breakpoints[0]; });
var OpenInButtonBar = styled(ButtonBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"], ["\n  @media (max-width: ", ") {\n    margin-top: ", ";\n  }\n"])), function (p) { return p.theme.breakpoints[0]; }, space(1));
var StyledDropdownButton = styled(DropdownButton)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  min-width: 145px;\n"], ["\n  min-width: 145px;\n"])));
var StyledDropdownItem = styled(DropdownItem)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var TableWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"], ["\n  margin-bottom: ", ";\n  ", " {\n    /* smaller space between table and pagination */\n    margin-bottom: -", ";\n  }\n"])), space(4), Panel, space(1));
export default Issues;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=issues.jsx.map
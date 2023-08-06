import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import isEqual from 'lodash/isEqual';
import { createDashboard, deleteDashboard, updateDashboard, } from 'app/actionCreators/dashboards';
import { addSuccessMessage } from 'app/actionCreators/indicator';
import NotFound from 'app/components/errors/notFound';
import LoadingIndicator from 'app/components/loadingIndicator';
import GlobalSelectionHeader from 'app/components/organizations/globalSelectionHeader';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import Controls from './controls';
import Dashboard from './dashboard';
import { DEFAULT_STATS_PERIOD, EMPTY_DASHBOARD } from './data';
import OrgDashboards from './orgDashboards';
import DashboardTitle from './title';
import { cloneDashboard } from './utils';
var UNSAVED_MESSAGE = t('You have unsaved changes, are you sure you want to leave?');
var DashboardDetail = /** @class */ (function (_super) {
    __extends(DashboardDetail, _super);
    function DashboardDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            dashboardState: 'view',
            modifiedDashboard: null,
        };
        _this.onEdit = function (dashboard) { return function () {
            if (!dashboard) {
                return;
            }
            trackAnalyticsEvent({
                eventKey: 'dashboards2.edit.start',
                eventName: 'Dashboards2: Edit start',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState({
                dashboardState: 'edit',
                modifiedDashboard: cloneDashboard(dashboard),
            });
        }; };
        _this.onRouteLeave = function (nextLocation) {
            var organization = _this.props.organization;
            if ((nextLocation === null || nextLocation === void 0 ? void 0 : nextLocation.pathname) ===
                "/organizations/" + organization.slug + "/dashboards/widget/new/") {
                return undefined;
            }
            if (!['view', 'pending_delete'].includes(_this.state.dashboardState)) {
                return UNSAVED_MESSAGE;
            }
            return undefined;
        };
        _this.onUnload = function (event) {
            if (['view', 'pending_delete'].includes(_this.state.dashboardState)) {
                return;
            }
            event.preventDefault();
            event.returnValue = UNSAVED_MESSAGE;
        };
        _this.onCreate = function () {
            trackAnalyticsEvent({
                eventKey: 'dashboards2.create.start',
                eventName: 'Dashboards2: Create start',
                organization_id: parseInt(_this.props.organization.id, 10),
            });
            _this.setState({
                dashboardState: 'create',
                modifiedDashboard: cloneDashboard(EMPTY_DASHBOARD),
            });
        };
        _this.onCancel = function () {
            if (_this.state.dashboardState === 'create') {
                trackAnalyticsEvent({
                    eventKey: 'dashboards2.create.cancel',
                    eventName: 'Dashboards2: Create cancel',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
            }
            else if (_this.state.dashboardState === 'edit') {
                trackAnalyticsEvent({
                    eventKey: 'dashboards2.edit.cancel',
                    eventName: 'Dashboards2: Edit cancel',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
            }
            _this.setState({
                dashboardState: 'view',
                modifiedDashboard: null,
            });
        };
        _this.onDelete = function (dashboard) { return function () {
            var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location;
            if (!(dashboard === null || dashboard === void 0 ? void 0 : dashboard.id)) {
                return;
            }
            var previousDashboardState = _this.state.dashboardState;
            _this.setState({
                dashboardState: 'pending_delete',
            }, function () {
                trackAnalyticsEvent({
                    eventKey: 'dashboards2.delete',
                    eventName: 'Dashboards2: Delete',
                    organization_id: parseInt(_this.props.organization.id, 10),
                });
                deleteDashboard(api, organization.slug, dashboard.id)
                    .then(function () {
                    addSuccessMessage(t('Dashboard deleted'));
                    browserHistory.replace({
                        pathname: "/organizations/" + organization.slug + "/dashboards/",
                        query: __assign({}, location.query),
                    });
                })
                    .catch(function () {
                    _this.setState({
                        dashboardState: previousDashboardState,
                    });
                });
            });
        }; };
        _this.onCommit = function (_a) {
            var dashboard = _a.dashboard, reloadData = _a.reloadData;
            return function () {
                var _a = _this.props, api = _a.api, organization = _a.organization, location = _a.location;
                var _b = _this.state, dashboardState = _b.dashboardState, modifiedDashboard = _b.modifiedDashboard;
                switch (dashboardState) {
                    case 'create': {
                        if (modifiedDashboard) {
                            createDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                                addSuccessMessage(t('Dashboard created'));
                                trackAnalyticsEvent({
                                    eventKey: 'dashboards2.create.complete',
                                    eventName: 'Dashboards2: Create complete',
                                    organization_id: parseInt(organization.id, 10),
                                });
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                // redirect to new dashboard
                                browserHistory.replace({
                                    pathname: "/organizations/" + organization.slug + "/dashboards/" + newDashboard.id + "/",
                                    query: __assign({}, location.query),
                                });
                            });
                        }
                        break;
                    }
                    case 'edit': {
                        if (modifiedDashboard) {
                            // only update the dashboard if there are changes
                            if (isEqual(dashboard, modifiedDashboard)) {
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                return;
                            }
                            updateDashboard(api, organization.slug, modifiedDashboard).then(function (newDashboard) {
                                addSuccessMessage(t('Dashboard updated'));
                                trackAnalyticsEvent({
                                    eventKey: 'dashboards2.edit.complete',
                                    eventName: 'Dashboards2: Edit complete',
                                    organization_id: parseInt(organization.id, 10),
                                });
                                _this.setState({
                                    dashboardState: 'view',
                                    modifiedDashboard: null,
                                });
                                if (dashboard && newDashboard.id !== dashboard.id) {
                                    browserHistory.replace({
                                        pathname: "/organizations/" + organization.slug + "/dashboards/" + newDashboard.id + "/",
                                        query: __assign({}, location.query),
                                    });
                                    return;
                                }
                                reloadData();
                            });
                            return;
                        }
                        _this.setState({
                            dashboardState: 'view',
                            modifiedDashboard: null,
                        });
                        break;
                    }
                    case 'view':
                    default: {
                        _this.setState({
                            dashboardState: 'view',
                            modifiedDashboard: null,
                        });
                        break;
                    }
                }
            };
        };
        _this.onWidgetChange = function (widgets) {
            var modifiedDashboard = _this.state.modifiedDashboard;
            if (modifiedDashboard === null) {
                return;
            }
            _this.setState(function (prevState) {
                return __assign(__assign({}, prevState), { modifiedDashboard: __assign(__assign({}, prevState.modifiedDashboard), { widgets: widgets }) });
            });
        };
        _this.setModifiedDashboard = function (dashboard) {
            _this.setState({
                modifiedDashboard: dashboard,
            });
        };
        return _this;
    }
    DashboardDetail.prototype.componentDidMount = function () {
        var _a = this.props, route = _a.route, router = _a.router;
        router.setRouteLeaveHook(route, this.onRouteLeave);
        window.addEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.componentWillUnmount = function () {
        window.removeEventListener('beforeunload', this.onUnload);
    };
    DashboardDetail.prototype.render = function () {
        var _this = this;
        var _a = this.props, api = _a.api, location = _a.location, params = _a.params, organization = _a.organization;
        var _b = this.state, modifiedDashboard = _b.modifiedDashboard, dashboardState = _b.dashboardState;
        var isEditing = ['edit', 'create', 'pending_delete'].includes(dashboardState);
        return (<GlobalSelectionHeader skipLoadLastUsed={organization.features.includes('global-views')} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: DEFAULT_STATS_PERIOD,
                },
            }}>
        <OrgDashboards api={api} location={location} params={params} organization={organization}>
          {function (_a) {
                var dashboard = _a.dashboard, dashboards = _a.dashboards, error = _a.error, reloadData = _a.reloadData;
                return (<React.Fragment>
                <StyledPageHeader>
                  <DashboardTitle dashboard={modifiedDashboard || dashboard} onUpdate={_this.setModifiedDashboard} isEditing={isEditing}/>
                  <Controls organization={organization} dashboards={dashboards} dashboard={dashboard} onEdit={_this.onEdit(dashboard)} onCreate={_this.onCreate} onCancel={_this.onCancel} onCommit={_this.onCommit({ dashboard: dashboard, reloadData: reloadData })} onDelete={_this.onDelete(dashboard)} dashboardState={dashboardState}/>
                </StyledPageHeader>
                {error ? (<NotFound />) : dashboard ? (<Dashboard dashboard={modifiedDashboard || dashboard} organization={organization} isEditing={isEditing} onUpdate={_this.onWidgetChange}/>) : (<LoadingIndicator />)}
              </React.Fragment>);
            }}
        </OrgDashboards>
      </GlobalSelectionHeader>);
    };
    return DashboardDetail;
}(React.Component));
var StyledPageHeader = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: flex-start;\n    height: auto;\n  }\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: space-between;\n  font-size: ", ";\n  color: ", ";\n  height: 40px;\n  margin-bottom: ", ";\n\n  @media (max-width: ", ") {\n    flex-direction: column;\n    align-items: flex-start;\n    height: auto;\n  }\n"])), function (p) { return p.theme.headerFontSize; }, function (p) { return p.theme.textColor; }, space(2), function (p) { return p.theme.breakpoints[2]; });
export default withApi(withOrganization(DashboardDetail));
var templateObject_1;
//# sourceMappingURL=detail.jsx.map
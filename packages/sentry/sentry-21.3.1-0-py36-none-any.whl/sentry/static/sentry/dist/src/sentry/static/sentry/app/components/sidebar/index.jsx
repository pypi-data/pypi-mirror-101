import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import createReactClass from 'create-react-class';
import isEqual from 'lodash/isEqual';
import * as queryString from 'query-string';
import Reflux from 'reflux';
import { hideSidebar, showSidebar } from 'app/actionCreators/preferences';
import SidebarPanelActions from 'app/actions/sidebarPanelActions';
import Feature from 'app/components/acl/feature';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import { extractSelectionParameters } from 'app/components/organizations/globalSelectionHeader/utils';
import { IconActivity, IconChevron, IconGraph, IconIssues, IconLab, IconLightning, IconProject, IconReleases, IconSettings, IconSiren, IconStats, IconSupport, IconTelescope, } from 'app/icons';
import { t } from 'app/locale';
import ConfigStore from 'app/stores/configStore';
import HookStore from 'app/stores/hookStore';
import PreferencesStore from 'app/stores/preferencesStore';
import SidebarPanelStore from 'app/stores/sidebarPanelStore';
import space from 'app/styles/space';
import { getDiscoverLandingUrl } from 'app/utils/discover/urls';
import theme from 'app/utils/theme';
import withOrganization from 'app/utils/withOrganization';
import Broadcasts from './broadcasts';
import SidebarHelp from './help';
import OnboardingStatus from './onboardingStatus';
import ServiceIncidents from './serviceIncidents';
import SidebarDropdown from './sidebarDropdown';
import SidebarItem from './sidebarItem';
import { SidebarPanelKey } from './types';
var Sidebar = /** @class */ (function (_super) {
    __extends(Sidebar, _super);
    function Sidebar(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            horizontal: false,
        };
        _this.mq = null;
        _this.sidebarRef = React.createRef();
        _this.toggleSidebar = function () {
            var collapsed = _this.props.collapsed;
            if (!collapsed) {
                hideSidebar();
            }
            else {
                showSidebar();
            }
        };
        _this.checkHash = function () {
            if (window.location.hash === '#welcome') {
                _this.togglePanel(SidebarPanelKey.OnboardingWizard);
            }
        };
        _this.handleMediaQueryChange = function (changed) {
            _this.setState({
                horizontal: changed.matches,
            });
        };
        _this.togglePanel = function (panel) { return SidebarPanelActions.togglePanel(panel); };
        _this.hidePanel = function () { return SidebarPanelActions.hidePanel(); };
        // Keep the global selection querystring values in the path
        _this.navigateWithGlobalSelection = function (pathname, evt) {
            var _a;
            var globalSelectionRoutes = [
                'dashboards',
                'issues',
                'releases',
                'user-feedback',
                'discover',
                'discover/results',
                'performance',
            ].map(function (route) { return "/organizations/" + _this.props.organization.slug + "/" + route + "/"; });
            // Only keep the querystring if the current route matches one of the above
            if (globalSelectionRoutes.includes(pathname)) {
                var query = extractSelectionParameters((_a = _this.props.location) === null || _a === void 0 ? void 0 : _a.query);
                // Handle cmd-click (mac) and meta-click (linux)
                if (evt.metaKey) {
                    var q = queryString.stringify(query);
                    evt.currentTarget.href = evt.currentTarget.href + "?" + q;
                    return;
                }
                evt.preventDefault();
                browserHistory.push({ pathname: pathname, query: query });
            }
            _this.hidePanel();
        };
        if (!window.matchMedia) {
            return _this;
        }
        // TODO(billy): We should consider moving this into a component
        _this.mq = window.matchMedia("(max-width: " + theme.breakpoints[1] + ")");
        _this.mq.addListener(_this.handleMediaQueryChange);
        _this.state.horizontal = _this.mq.matches;
        return _this;
    }
    Sidebar.prototype.componentDidMount = function () {
        document.body.classList.add('body-sidebar');
        this.checkHash();
        this.doCollapse(this.props.collapsed);
    };
    // Sidebar doesn't use children, so don't use it to compare
    // Also ignore location, will re-render when routes change (instead of query params)
    //
    // NOTE(epurkhiser): The comment above is why I added `children?: never` as a
    // type to this component. I'm not sure the implications of removing this so
    // I've just left it for now.
    Sidebar.prototype.shouldComponentUpdate = function (_a, nextState) {
        var _children = _a.children, _location = _a.location, nextPropsToCompare = __rest(_a, ["children", "location"]);
        var _b = this.props, _childrenCurrent = _b.children, _locationCurrent = _b.location, currentPropsToCompare = __rest(_b, ["children", "location"]);
        return (!isEqual(currentPropsToCompare, nextPropsToCompare) ||
            !isEqual(this.state, nextState));
    };
    Sidebar.prototype.componentDidUpdate = function (prevProps) {
        var _a;
        var _b = this.props, collapsed = _b.collapsed, location = _b.location;
        // Close active panel if we navigated anywhere
        if ((location === null || location === void 0 ? void 0 : location.pathname) !== ((_a = prevProps.location) === null || _a === void 0 ? void 0 : _a.pathname)) {
            this.hidePanel();
        }
        // Collapse
        if (collapsed !== prevProps.collapsed) {
            this.doCollapse(collapsed);
        }
    };
    Sidebar.prototype.componentWillUnmount = function () {
        document.body.classList.remove('body-sidebar');
        if (this.mq) {
            this.mq.removeListener(this.handleMediaQueryChange);
            this.mq = null;
        }
    };
    Sidebar.prototype.doCollapse = function (collapsed) {
        if (collapsed) {
            document.body.classList.add('collapsed');
        }
        else {
            document.body.classList.remove('collapsed');
        }
    };
    Sidebar.prototype.render = function () {
        var _this = this;
        var _a = this.props, activePanel = _a.activePanel, organization = _a.organization, collapsed = _a.collapsed;
        var horizontal = this.state.horizontal;
        var config = ConfigStore.getConfig();
        var user = ConfigStore.get('user');
        var hasPanel = !!activePanel;
        var orientation = horizontal ? 'top' : 'left';
        var sidebarItemProps = {
            orientation: orientation,
            collapsed: collapsed,
            hasPanel: hasPanel,
        };
        var hasOrganization = !!organization;
        var projects = hasOrganization && (<SidebarItem {...sidebarItemProps} index onClick={this.hidePanel} icon={<IconProject size="md"/>} label={<GuideAnchor target="projects">{t('Projects')}</GuideAnchor>} to={"/organizations/" + organization.slug + "/projects/"} id="projects"/>);
        var issues = hasOrganization && (<SidebarItem {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/issues/", evt);
            }} icon={<IconIssues size="md"/>} label={<GuideAnchor target="issues">{t('Issues')}</GuideAnchor>} to={"/organizations/" + organization.slug + "/issues/"} id="issues"/>);
        var discover2 = hasOrganization && (<Feature hookName="feature-disabled:discover2-sidebar-item" features={['discover-basic']} organization={organization}>
        <SidebarItem {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection(getDiscoverLandingUrl(organization), evt);
            }} icon={<IconTelescope size="md"/>} label={<GuideAnchor target="discover">{t('Discover')}</GuideAnchor>} to={getDiscoverLandingUrl(organization)} id="discover-v2"/>
      </Feature>);
        var performance = hasOrganization && (<Feature hookName="feature-disabled:performance-sidebar-item" features={['performance-view']} organization={organization}>
        <SidebarItem {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/performance/", evt);
            }} icon={<IconLightning size="md"/>} label={<GuideAnchor target="performance">{t('Performance')}</GuideAnchor>} to={"/organizations/" + organization.slug + "/performance/"} id="performance"/>
      </Feature>);
        var releases = hasOrganization && (<SidebarItem {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/releases/", evt);
            }} icon={<IconReleases size="md"/>} label={<GuideAnchor target="releases">{t('Releases')}</GuideAnchor>} to={"/organizations/" + organization.slug + "/releases/"} id="releases"/>);
        var userFeedback = hasOrganization && (<SidebarItem {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/user-feedback/", evt);
            }} icon={<IconSupport size="md"/>} label={t('User Feedback')} to={"/organizations/" + organization.slug + "/user-feedback/"} id="user-feedback"/>);
        var alerts = hasOrganization && (<Feature features={['incidents']}>
        {function (_a) {
                var hasFeature = _a.hasFeature;
                var alertsPath = hasFeature
                    ? "/organizations/" + organization.slug + "/alerts/"
                    : "/organizations/" + organization.slug + "/alerts/rules/";
                return (<SidebarItem {...sidebarItemProps} onClick={function (_id, evt) { return _this.navigateWithGlobalSelection(alertsPath, evt); }} icon={<IconSiren size="md"/>} label={t('Alerts')} to={alertsPath} id="alerts"/>);
            }}
      </Feature>);
        var monitors = hasOrganization && (<Feature features={['monitors']} organization={organization}>
        <SidebarItem {...sidebarItemProps} onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/monitors/", evt);
            }} icon={<IconLab size="md"/>} label={t('Monitors')} to={"/organizations/" + organization.slug + "/monitors/"} id="monitors"/>
      </Feature>);
        var dashboards = hasOrganization && (<Feature features={['discover', 'discover-query', 'dashboards-basic', 'dashboards-edit']} organization={organization} requireAll={false}>
        <SidebarItem {...sidebarItemProps} index onClick={function (_id, evt) {
                return _this.navigateWithGlobalSelection("/organizations/" + organization.slug + "/dashboards/", evt);
            }} icon={<IconGraph size="md"/>} label={t('Dashboards')} to={"/organizations/" + organization.slug + "/dashboards/"} id="customizable-dashboards"/>
      </Feature>);
        var activity = hasOrganization && (<SidebarItem {...sidebarItemProps} onClick={this.hidePanel} icon={<IconActivity size="md"/>} label={t('Activity')} to={"/organizations/" + organization.slug + "/activity/"} id="activity"/>);
        var stats = hasOrganization && (<SidebarItem {...sidebarItemProps} onClick={this.hidePanel} icon={<IconStats size="md"/>} label={t('Stats')} to={"/organizations/" + organization.slug + "/stats/"} id="stats"/>);
        var settings = hasOrganization && (<SidebarItem {...sidebarItemProps} onClick={this.hidePanel} icon={<IconSettings size="md"/>} label={t('Settings')} to={"/settings/" + organization.slug + "/"} id="settings"/>);
        return (<StyledSidebar ref={this.sidebarRef} collapsed={collapsed}>
        <SidebarSectionGroupPrimary>
          <SidebarSection>
            <SidebarDropdown orientation={orientation} collapsed={collapsed} org={organization} user={user} config={config}/>
          </SidebarSection>

          <PrimaryItems>
            {hasOrganization && (<React.Fragment>
                <SidebarSection>
                  {projects}
                  {issues}
                  {performance}
                  {releases}
                  {userFeedback}
                  {alerts}
                  {discover2}
                </SidebarSection>

                <SidebarSection>
                  {dashboards}
                  {monitors}
                </SidebarSection>

                <SidebarSection>
                  {activity}
                  {stats}
                </SidebarSection>

                <SidebarSection>{settings}</SidebarSection>
              </React.Fragment>)}
          </PrimaryItems>
        </SidebarSectionGroupPrimary>

        {hasOrganization && (<SidebarSectionGroup>
            <SidebarSection noMargin noPadding>
              <OnboardingStatus org={organization} currentPanel={activePanel} onShowPanel={function () { return _this.togglePanel(SidebarPanelKey.OnboardingWizard); }} hidePanel={this.hidePanel} {...sidebarItemProps}/>
            </SidebarSection>

            <SidebarSection>
              {HookStore.get('sidebar:bottom-items').length > 0 &&
                    HookStore.get('sidebar:bottom-items')[0](__assign({ organization: organization }, sidebarItemProps))}
              <SidebarHelp orientation={orientation} collapsed={collapsed} hidePanel={this.hidePanel} organization={organization}/>
              <Broadcasts orientation={orientation} collapsed={collapsed} currentPanel={activePanel} onShowPanel={function () { return _this.togglePanel(SidebarPanelKey.Broadcasts); }} hidePanel={this.hidePanel} organization={organization}/>
              <ServiceIncidents orientation={orientation} collapsed={collapsed} currentPanel={activePanel} onShowPanel={function () { return _this.togglePanel(SidebarPanelKey.StatusUpdate); }} hidePanel={this.hidePanel}/>
            </SidebarSection>

            {!horizontal && (<SidebarSection>
                <SidebarCollapseItem id="collapse" data-test-id="sidebar-collapse" {...sidebarItemProps} icon={<StyledIconChevron collapsed={collapsed}/>} label={collapsed ? t('Expand') : t('Collapse')} onClick={this.toggleSidebar}/>
              </SidebarSection>)}
          </SidebarSectionGroup>)}
      </StyledSidebar>);
    };
    return Sidebar;
}(React.Component));
var SidebarContainer = createReactClass({
    displayName: 'SidebarContainer',
    mixins: [
        Reflux.listenTo(PreferencesStore, 'onPreferenceChange'),
        Reflux.listenTo(SidebarPanelStore, 'onSidebarPanelChange'),
    ],
    getInitialState: function () {
        return {
            collapsed: PreferencesStore.getInitialState().collapsed,
            activePanel: '',
        };
    },
    onPreferenceChange: function (preferences) {
        if (preferences.collapsed === this.state.collapsed) {
            return;
        }
        this.setState({ collapsed: preferences.collapsed });
    },
    onSidebarPanelChange: function (activePanel) {
        this.setState({ activePanel: activePanel });
    },
    render: function () {
        var _a = this.state, activePanel = _a.activePanel, collapsed = _a.collapsed;
        return <Sidebar {...this.props} {...{ activePanel: activePanel, collapsed: collapsed }}/>;
    },
});
export default withOrganization(SidebarContainer);
var responsiveFlex = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n\n  @media (max-width: ", ") {\n    flex-direction: row;\n  }\n"])), theme.breakpoints[1]);
var StyledSidebar = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  background: ", ";\n  background: ", ";\n  color: ", ";\n  line-height: 1;\n  padding: 12px 0 2px; /* Allows for 32px avatars  */\n  width: ", ";\n  position: fixed;\n  top: ", ";\n  left: 0;\n  bottom: 0;\n  justify-content: space-between;\n  z-index: ", ";\n  ", ";\n  ", ";\n\n  @media (max-width: ", ") {\n    top: 0;\n    left: 0;\n    right: 0;\n    height: ", ";\n    bottom: auto;\n    width: auto;\n    padding: 0 ", ";\n    align-items: center;\n  }\n"], ["\n  background: ", ";\n  background: ", ";\n  color: ", ";\n  line-height: 1;\n  padding: 12px 0 2px; /* Allows for 32px avatars  */\n  width: ", ";\n  position: fixed;\n  top: ", ";\n  left: 0;\n  bottom: 0;\n  justify-content: space-between;\n  z-index: ", ";\n  ", ";\n  ", ";\n\n  @media (max-width: ", ") {\n    top: 0;\n    left: 0;\n    right: 0;\n    height: ", ";\n    bottom: auto;\n    width: auto;\n    padding: 0 ", ";\n    align-items: center;\n  }\n"])), function (p) { return p.theme.sidebar.background; }, function (p) { return p.theme.sidebarGradient; }, function (p) { return p.theme.sidebar.color; }, function (p) { return p.theme.sidebar.expandedWidth; }, function (p) { return (ConfigStore.get('demoMode') ? p.theme.demo.headerSize : 0); }, function (p) { return p.theme.zIndex.sidebar; }, responsiveFlex, function (p) { return p.collapsed && "width: " + p.theme.sidebar.collapsedWidth + ";"; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.sidebar.mobileHeight; }, space(1));
var SidebarSectionGroup = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  flex-shrink: 0; /* prevents shrinking on Safari */\n"], ["\n  ", ";\n  flex-shrink: 0; /* prevents shrinking on Safari */\n"])), responsiveFlex);
var SidebarSectionGroupPrimary = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", ";\n  /* necessary for child flexing on msedge and ff */\n  min-height: 0;\n  min-width: 0;\n  flex: 1;\n  /* expand to fill the entire height on mobile */\n  @media (max-width: ", ") {\n    height: 100%;\n    align-items: center;\n  }\n"], ["\n  ", ";\n  /* necessary for child flexing on msedge and ff */\n  min-height: 0;\n  min-width: 0;\n  flex: 1;\n  /* expand to fill the entire height on mobile */\n  @media (max-width: ", ") {\n    height: 100%;\n    align-items: center;\n  }\n"])), responsiveFlex, function (p) { return p.theme.breakpoints[1]; });
var PrimaryItems = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  overflow: auto;\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n  -ms-overflow-style: -ms-autohiding-scrollbar;\n  @media (max-height: 675px) and (min-width: ", ") {\n    border-bottom: 1px solid ", ";\n    padding-bottom: ", ";\n    box-shadow: rgba(0, 0, 0, 0.15) 0px -10px 10px inset;\n    &::-webkit-scrollbar {\n      background-color: transparent;\n      width: 8px;\n    }\n    &::-webkit-scrollbar-thumb {\n      background: ", ";\n      border-radius: 8px;\n    }\n  }\n  @media (max-width: ", ") {\n    overflow-y: visible;\n    flex-direction: row;\n    height: 100%;\n    align-items: center;\n    border-right: 1px solid ", ";\n    padding-right: ", ";\n    margin-right: ", ";\n    box-shadow: rgba(0, 0, 0, 0.15) -10px 0px 10px inset;\n    ::-webkit-scrollbar {\n      display: none;\n    }\n  }\n"], ["\n  overflow: auto;\n  flex: 1;\n  display: flex;\n  flex-direction: column;\n  -ms-overflow-style: -ms-autohiding-scrollbar;\n  @media (max-height: 675px) and (min-width: ", ") {\n    border-bottom: 1px solid ", ";\n    padding-bottom: ", ";\n    box-shadow: rgba(0, 0, 0, 0.15) 0px -10px 10px inset;\n    &::-webkit-scrollbar {\n      background-color: transparent;\n      width: 8px;\n    }\n    &::-webkit-scrollbar-thumb {\n      background: ", ";\n      border-radius: 8px;\n    }\n  }\n  @media (max-width: ", ") {\n    overflow-y: visible;\n    flex-direction: row;\n    height: 100%;\n    align-items: center;\n    border-right: 1px solid ", ";\n    padding-right: ", ";\n    margin-right: ", ";\n    box-shadow: rgba(0, 0, 0, 0.15) -10px 0px 10px inset;\n    ::-webkit-scrollbar {\n      display: none;\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.gray400; }, space(1), function (p) { return p.theme.gray400; }, function (p) { return p.theme.breakpoints[1]; }, function (p) { return p.theme.gray400; }, space(1), space(0.5));
var SidebarSection = styled(SidebarSectionGroup)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  ", ";\n  ", ";\n\n  @media (max-width: ", ") {\n    margin: 0;\n    padding: 0;\n  }\n\n  &:empty {\n    display: none;\n  }\n"], ["\n  ", ";\n  ", ";\n\n  @media (max-width: ", ") {\n    margin: 0;\n    padding: 0;\n  }\n\n  &:empty {\n    display: none;\n  }\n"])), function (p) { return !p.noMargin && "margin: " + space(1) + " 0"; }, function (p) { return !p.noPadding && 'padding: 0 19px'; }, function (p) { return p.theme.breakpoints[0]; });
var ExpandedIcon = css(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  transition: 0.3s transform ease;\n  transform: rotate(270deg);\n"], ["\n  transition: 0.3s transform ease;\n  transform: rotate(270deg);\n"])));
var CollapsedIcon = css(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  transform: rotate(90deg);\n"], ["\n  transform: rotate(90deg);\n"])));
var StyledIconChevron = styled(function (_a) {
    var collapsed = _a.collapsed, props = __rest(_a, ["collapsed"]);
    return (<IconChevron direction="left" size="md" isCircled css={[ExpandedIcon, collapsed && CollapsedIcon]} {...props}/>);
})(templateObject_9 || (templateObject_9 = __makeTemplateObject([""], [""])));
var SidebarCollapseItem = styled(SidebarItem)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"], ["\n  @media (max-width: ", ") {\n    display: none;\n  }\n"])), function (p) { return p.theme.breakpoints[1]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10;
//# sourceMappingURL=index.jsx.map
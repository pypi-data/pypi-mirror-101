import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { openSudo } from 'app/actionCreators/modal';
import { fetchOrganizationDetails } from 'app/actionCreators/organization';
import ProjectActions from 'app/actions/projectActions';
import Alert from 'app/components/alert';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Sidebar from 'app/components/sidebar';
import { ORGANIZATION_FETCH_ERROR_TYPES } from 'app/constants';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import ConfigStore from 'app/stores/configStore';
import HookStore from 'app/stores/hookStore';
import OrganizationStore from 'app/stores/organizationStore';
import space from 'app/styles/space';
import { metric } from 'app/utils/analytics';
import { callIfFunction } from 'app/utils/callIfFunction';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import withApi from 'app/utils/withApi';
import withOrganizations from 'app/utils/withOrganizations';
var defaultProps = {
    detailed: true,
};
var OrganizationContext = /** @class */ (function (_super) {
    __extends(OrganizationContext, _super);
    function OrganizationContext(props) {
        var _this = _super.call(this, props) || this;
        _this.unlisteners = [
            ProjectActions.createSuccess.listen(function () { return _this.onProjectCreation(); }, undefined),
            OrganizationStore.listen(function (data) { return _this.loadOrganization(data); }, undefined),
        ];
        _this.remountComponent = function () {
            _this.setState(OrganizationContext.getDefaultState(_this.props), _this.fetchData);
        };
        _this.state = OrganizationContext.getDefaultState(props);
        return _this;
    }
    OrganizationContext.getDerivedStateFromProps = function (props, prevState) {
        var prevProps = prevState.prevProps;
        if (OrganizationContext.shouldRemount(prevProps, props)) {
            return OrganizationContext.getDefaultState(props);
        }
        var organizationsLoading = props.organizationsLoading, location = props.location, params = props.params;
        var orgId = params.orgId;
        return __assign(__assign({}, prevState), { prevProps: {
                orgId: orgId,
                organizationsLoading: organizationsLoading,
                location: location,
            } });
    };
    OrganizationContext.shouldRemount = function (prevProps, props) {
        var hasOrgIdAndChanged = prevProps.orgId && props.params.orgId && prevProps.orgId !== props.params.orgId;
        var hasOrgId = props.params.orgId ||
            (props.useLastOrganization && ConfigStore.get('lastOrganization'));
        // protect against the case where we finish fetching org details
        // and then `OrganizationsStore` finishes loading:
        // only fetch in the case where we don't have an orgId
        //
        // Compare `getOrganizationSlug`  because we may have a last used org from server
        // if there is no orgId in the URL
        var organizationLoadingChanged = prevProps.organizationsLoading !== props.organizationsLoading &&
            props.organizationsLoading === false;
        return (hasOrgIdAndChanged ||
            (!hasOrgId && organizationLoadingChanged) ||
            (props.location.state === 'refresh' && prevProps.location.state !== 'refresh'));
    };
    OrganizationContext.getDefaultState = function (props) {
        var prevProps = {
            orgId: props.params.orgId,
            organizationsLoading: props.organizationsLoading,
            location: props.location,
        };
        if (OrganizationContext.isOrgStorePopulatedCorrectly(props)) {
            // retrieve initial state from store
            return __assign(__assign({}, OrganizationStore.get()), { prevProps: prevProps });
        }
        return {
            loading: true,
            error: null,
            errorType: null,
            organization: null,
            prevProps: prevProps,
        };
    };
    OrganizationContext.getOrganizationSlug = function (props) {
        var _a, _b;
        return (props.params.orgId ||
            (props.useLastOrganization &&
                (ConfigStore.get('lastOrganization') ||
                    ((_b = (_a = props.organizations) === null || _a === void 0 ? void 0 : _a[0]) === null || _b === void 0 ? void 0 : _b.slug))));
    };
    OrganizationContext.isOrgChanging = function (props) {
        var organization = OrganizationStore.get().organization;
        if (!organization) {
            return false;
        }
        return organization.slug !== OrganizationContext.getOrganizationSlug(props);
    };
    OrganizationContext.isOrgStorePopulatedCorrectly = function (props) {
        var detailed = props.detailed;
        var _a = OrganizationStore.get(), organization = _a.organization, dirty = _a.dirty;
        return (!dirty &&
            organization &&
            !OrganizationContext.isOrgChanging(props) &&
            (!detailed || (detailed && organization.projects && organization.teams)));
    };
    OrganizationContext.prototype.getChildContext = function () {
        return {
            organization: this.state.organization,
        };
    };
    OrganizationContext.prototype.componentDidMount = function () {
        this.fetchData(true);
    };
    OrganizationContext.prototype.componentDidUpdate = function (prevProps) {
        var remountPrevProps = {
            orgId: prevProps.params.orgId,
            organizationsLoading: prevProps.organizationsLoading,
            location: prevProps.location,
        };
        if (OrganizationContext.shouldRemount(remountPrevProps, this.props)) {
            this.remountComponent();
        }
    };
    OrganizationContext.prototype.componentWillUnmount = function () {
        this.unlisteners.forEach(callIfFunction);
    };
    OrganizationContext.prototype.onProjectCreation = function () {
        // If a new project was created, we need to re-fetch the
        // org details endpoint, which will propagate re-rendering
        // for the entire component tree
        fetchOrganizationDetails(this.props.api, OrganizationContext.getOrganizationSlug(this.props), true, true);
    };
    OrganizationContext.prototype.isLoading = function () {
        // In the absence of an organization slug, the loading state should be
        // derived from this.props.organizationsLoading from OrganizationsStore
        if (!OrganizationContext.getOrganizationSlug(this.props)) {
            return this.props.organizationsLoading;
        }
        // The following loading logic exists because we could either be waiting for
        // the whole organization object to come in or just the teams and projects.
        var _a = this.state, loading = _a.loading, error = _a.error, organization = _a.organization;
        var detailed = this.props.detailed;
        return (loading ||
            (!error &&
                detailed &&
                (!organization || !organization.projects || !organization.teams)));
    };
    OrganizationContext.prototype.fetchData = function (isInitialFetch) {
        if (isInitialFetch === void 0) { isInitialFetch = false; }
        if (!OrganizationContext.getOrganizationSlug(this.props)) {
            return;
        }
        // fetch from the store, then fetch from the API if necessary
        if (OrganizationContext.isOrgStorePopulatedCorrectly(this.props)) {
            return;
        }
        metric.mark({ name: 'organization-details-fetch-start' });
        fetchOrganizationDetails(this.props.api, OrganizationContext.getOrganizationSlug(this.props), this.props.detailed, !OrganizationContext.isOrgChanging(this.props), // if true, will preserve a lightweight org that was fetched,
        isInitialFetch);
    };
    OrganizationContext.prototype.loadOrganization = function (orgData) {
        var _this = this;
        var organization = orgData.organization, error = orgData.error;
        var hooks = [];
        if (organization && !error) {
            HookStore.get('organization:header').forEach(function (cb) {
                hooks.push(cb(organization));
            });
            // Configure scope to have organization tag
            Sentry.configureScope(function (scope) {
                // XXX(dcramer): this is duplicated in sdk.py on the backend
                scope.setTag('organization', organization.id);
                scope.setTag('organization.slug', organization.slug);
                scope.setContext('organization', { id: organization.id, slug: organization.slug });
            });
        }
        else if (error) {
            // If user is superuser, open sudo window
            var user = ConfigStore.get('user');
            if (!user || !user.isSuperuser || error.status !== 403) {
                // This `catch` can swallow up errors in development (and tests)
                // So let's log them. This may create some noise, especially the test case where
                // we specifically test this branch
                console.error(error); // eslint-disable-line no-console
            }
            else {
                openSudo({
                    retryRequest: function () { return Promise.resolve(_this.fetchData()); },
                });
            }
        }
        this.setState(__assign(__assign({}, orgData), { hooks: hooks }), function () {
            // Take a measurement for when organization details are done loading and the new state is applied
            if (organization) {
                metric.measure({
                    name: 'app.component.perf',
                    start: 'organization-details-fetch-start',
                    data: {
                        name: 'org-details',
                        route: getRouteStringFromRoutes(_this.props.routes),
                        organization_id: parseInt(organization.id, 10),
                    },
                });
            }
        });
    };
    OrganizationContext.prototype.getOrganizationDetailsEndpoint = function () {
        return "/organizations/" + OrganizationContext.getOrganizationSlug(this.props) + "/";
    };
    OrganizationContext.prototype.getTitle = function () {
        if (this.state.organization) {
            return this.state.organization.name;
        }
        return 'Sentry';
    };
    OrganizationContext.prototype.renderSidebar = function () {
        if (!this.props.includeSidebar) {
            return null;
        }
        var _a = this.props, _ = _a.children, props = __rest(_a, ["children"]);
        return <Sidebar {...props} organization={this.state.organization}/>;
    };
    OrganizationContext.prototype.renderError = function () {
        var errorComponent;
        switch (this.state.errorType) {
            case ORGANIZATION_FETCH_ERROR_TYPES.ORG_NO_ACCESS:
                // We can still render when an org can't be loaded due to 401. The
                // backend will handle redirects when this is a problem.
                return this.renderBody();
            case ORGANIZATION_FETCH_ERROR_TYPES.ORG_NOT_FOUND:
                errorComponent = (<Alert type="error">
            {t('The organization you were looking for was not found.')}
          </Alert>);
                break;
            default:
                errorComponent = <LoadingError onRetry={this.remountComponent}/>;
        }
        return <ErrorWrapper>{errorComponent}</ErrorWrapper>;
    };
    OrganizationContext.prototype.renderBody = function () {
        return (<DocumentTitle title={this.getTitle()}>
        <div className="app">
          {this.state.hooks}
          {this.renderSidebar()}
          {this.props.children}
        </div>
      </DocumentTitle>);
    };
    OrganizationContext.prototype.render = function () {
        if (this.isLoading()) {
            return (<LoadingIndicator triangle>
          {t('Loading data for your organization.')}
        </LoadingIndicator>);
        }
        if (this.state.error) {
            return (<React.Fragment>
          {this.renderSidebar()}
          {this.renderError()}
        </React.Fragment>);
        }
        return this.renderBody();
    };
    OrganizationContext.childContextTypes = {
        organization: SentryTypes.Organization,
    };
    OrganizationContext.defaultProps = defaultProps;
    return OrganizationContext;
}(React.Component));
export default withApi(withOrganizations(Sentry.withProfiler(OrganizationContext)));
export { OrganizationContext };
var ErrorWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", ";\n"], ["\n  padding: ", ";\n"])), space(3));
var templateObject_1;
//# sourceMappingURL=organizationContext.jsx.map
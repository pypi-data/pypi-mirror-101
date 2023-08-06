import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import isString from 'lodash/isString';
import Alert from 'app/components/alert';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
import Redirect from 'app/utils/redirect';
import withApi from 'app/utils/withApi';
var ProjectDetailsInner = /** @class */ (function (_super) {
    __extends(ProjectDetailsInner, _super);
    function ProjectDetailsInner() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: null,
            project: null,
        };
        _this.fetchData = function () { return __awaiter(_this, void 0, void 0, function () {
            var _a, orgId, projectSlug, project, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        this.setState({
                            loading: true,
                            error: null,
                        });
                        _a = this.props, orgId = _a.orgId, projectSlug = _a.projectSlug;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.props.api.requestPromise("/projects/" + orgId + "/" + projectSlug + "/")];
                    case 2:
                        project = _b.sent();
                        this.setState({
                            loading: false,
                            error: null,
                            project: project,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({
                            loading: false,
                            error: error_1,
                            project: null,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectDetailsInner.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ProjectDetailsInner.prototype.getProjectId = function () {
        if (this.state.project) {
            return this.state.project.id;
        }
        return null;
    };
    ProjectDetailsInner.prototype.hasProjectId = function () {
        var projectID = this.getProjectId();
        return isString(projectID) && projectID.length > 0;
    };
    ProjectDetailsInner.prototype.getOrganizationId = function () {
        if (this.state.project) {
            return this.state.project.organization.id;
        }
        return null;
    };
    ProjectDetailsInner.prototype.render = function () {
        var childrenProps = __assign(__assign({}, this.state), { projectId: this.getProjectId(), hasProjectId: this.hasProjectId(), organizationId: this.getOrganizationId() });
        return this.props.children(childrenProps);
    };
    return ProjectDetailsInner;
}(React.Component));
var ProjectDetails = withApi(ProjectDetailsInner);
var redirectDeprecatedProjectRoute = function (generateRedirectRoute) {
    var RedirectDeprecatedProjectRoute = /** @class */ (function (_super) {
        __extends(RedirectDeprecatedProjectRoute, _super);
        function RedirectDeprecatedProjectRoute() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.trackRedirect = function (organizationId, nextRoute) {
                var payload = {
                    feature: 'global_views',
                    url: getRouteStringFromRoutes(_this.props.routes),
                    org_id: parseInt(organizationId, 10),
                };
                // track redirects of deprecated URLs for analytics
                analytics('deprecated_urls.redirect', payload);
                return nextRoute;
            };
            return _this;
        }
        RedirectDeprecatedProjectRoute.prototype.render = function () {
            var _this = this;
            var params = this.props.params;
            var orgId = params.orgId;
            return (<Wrapper>
          <ProjectDetails orgId={orgId} projectSlug={params.projectId}>
            {function (_a) {
                    var loading = _a.loading, error = _a.error, hasProjectId = _a.hasProjectId, projectId = _a.projectId, organizationId = _a.organizationId;
                    if (loading) {
                        return <LoadingIndicator />;
                    }
                    if (!hasProjectId || !organizationId) {
                        if (error && error.status === 404) {
                            return (<Alert type="error">
                      {t('The project you were looking for was not found.')}
                    </Alert>);
                        }
                        return <LoadingError />;
                    }
                    var routeProps = {
                        orgId: orgId,
                        projectId: projectId,
                        router: { params: params },
                    };
                    return (<Redirect router={_this.props.router} to={_this.trackRedirect(organizationId, generateRedirectRoute(routeProps))}/>);
                }}
          </ProjectDetails>
        </Wrapper>);
        };
        return RedirectDeprecatedProjectRoute;
    }(React.Component));
    return RedirectDeprecatedProjectRoute;
};
export default redirectDeprecatedProjectRoute;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  flex: 1;\n  padding: ", ";\n"], ["\n  flex: 1;\n  padding: ", ";\n"])), space(3));
var templateObject_1;
//# sourceMappingURL=redirectDeprecatedProjectRoute.jsx.map
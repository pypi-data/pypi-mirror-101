import { __assign, __awaiter, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import styled from '@emotion/styled';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { fetchOrgMembers } from 'app/actionCreators/members';
import { setActiveProject } from 'app/actionCreators/projects';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import MissingProjectMembership from 'app/components/projects/missingProjectMembership';
import { t } from 'app/locale';
import SentryTypes from 'app/sentryTypes';
import MemberListStore from 'app/stores/memberListStore';
import ProjectsStore from 'app/stores/projectsStore';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import withProjects from 'app/utils/withProjects';
var ErrorTypes;
(function (ErrorTypes) {
    ErrorTypes["MISSING_MEMBERSHIP"] = "MISSING_MEMBERSHIP";
    ErrorTypes["PROJECT_NOT_FOUND"] = "PROJECT_NOT_FOUND";
    ErrorTypes["UNKNOWN"] = "UNKNOWN";
})(ErrorTypes || (ErrorTypes = {}));
/**
 * Higher-order component that sets `project` as a child context
 * value to be accessed by child elements.
 *
 * Additionally delays rendering of children until project XHR has finished
 * and context is populated.
 */
var ProjectContext = createReactClass({
    displayName: 'ProjectContext',
    childContextTypes: {
        project: SentryTypes.Project,
    },
    mixins: [
        Reflux.connect(MemberListStore, 'memberList'),
        Reflux.listenTo(ProjectsStore, 'onProjectChange'),
    ],
    getInitialState: function () {
        return {
            loading: true,
            error: false,
            errorType: null,
            memberList: [],
            project: null,
        };
    },
    getChildContext: function () {
        return {
            project: this.state.project,
        };
    },
    componentWillMount: function () {
        this.fetchData();
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.projectId === this.props.projectId) {
            return;
        }
        if (!nextProps.skipReload) {
            this.remountComponent();
        }
    },
    componentDidUpdate: function (prevProps, prevState) {
        if (prevProps.projectId !== this.props.projectId) {
            this.fetchData();
        }
        // Project list has changed. Likely indicating that a new project has been
        // added. Re-fetch project details in case that the new project is the active
        // project.
        //
        // For now, only compare lengths. It is possible that project slugs within
        // the list could change, but it doesn't seem to be broken anywhere else at
        // the moment that would require deeper checks.
        if (prevProps.projects.length !== this.props.projects.length) {
            this.fetchData();
        }
        // Call forceUpdate() on <DocumentTitle/> if either project or organization
        // state has changed. This is because <DocumentTitle/>'s shouldComponentUpdate()
        // returns false unless props differ; meaning context changes for project/org
        // do NOT trigger renders for <DocumentTitle/> OR any subchildren. The end result
        // being that child elements that listen for context changes on project/org will
        // NOT update (without this hack).
        // See: https://github.com/gaearon/react-document-title/issues/35
        // intentionally shallow comparing references
        if (prevState.project !== this.state.project) {
            if (!this.docTitle) {
                return;
            }
            var docTitle = this.docTitleRef.docTitle;
            if (docTitle) {
                docTitle.forceUpdate();
            }
        }
    },
    remountComponent: function () {
        this.setState(this.getInitialState());
    },
    getTitle: function () {
        var _a, _b;
        return (_b = (_a = this.state.project) === null || _a === void 0 ? void 0 : _a.slug) !== null && _b !== void 0 ? _b : 'Sentry';
    },
    onProjectChange: function (projectIds) {
        if (!this.state.project) {
            return;
        }
        if (!projectIds.has(this.state.project.id)) {
            return;
        }
        this.setState({
            project: __assign({}, ProjectsStore.getById(this.state.project.id)),
        });
    },
    identifyProject: function () {
        var _a = this.props, projects = _a.projects, projectId = _a.projectId;
        var projectSlug = projectId;
        return projects.find(function (_a) {
            var slug = _a.slug;
            return slug === projectSlug;
        }) || null;
    },
    fetchData: function () {
        return __awaiter(this, void 0, void 0, function () {
            var _a, orgId, projectId, skipReload, activeProject, hasAccess, projectRequest, project, error_1, error_2;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, orgId = _a.orgId, projectId = _a.projectId, skipReload = _a.skipReload;
                        activeProject = this.identifyProject();
                        hasAccess = activeProject && activeProject.hasAccess;
                        this.setState(function (state) { return ({
                            // if `skipReload` is true, then don't change loading state
                            loading: skipReload ? state.loading : true,
                            // we bind project initially, but it'll rebind
                            project: activeProject,
                        }); });
                        if (!(activeProject && hasAccess)) return [3 /*break*/, 5];
                        setActiveProject(null);
                        projectRequest = this.props.api.requestPromise("/projects/" + orgId + "/" + projectId + "/");
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, projectRequest];
                    case 2:
                        project = _b.sent();
                        this.setState({
                            loading: false,
                            project: project,
                            error: false,
                            errorType: null,
                        });
                        // assuming here that this means the project is considered the active project
                        setActiveProject(project);
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({
                            loading: false,
                            error: false,
                            errorType: ErrorTypes.UNKNOWN,
                        });
                        return [3 /*break*/, 4];
                    case 4:
                        fetchOrgMembers(this.props.api, orgId, activeProject.id);
                        return [2 /*return*/];
                    case 5:
                        // User is not a memberof the active project
                        if (activeProject && !activeProject.isMember) {
                            this.setState({
                                loading: false,
                                error: true,
                                errorType: ErrorTypes.MISSING_MEMBERSHIP,
                            });
                            return [2 /*return*/];
                        }
                        _b.label = 6;
                    case 6:
                        _b.trys.push([6, 8, , 9]);
                        return [4 /*yield*/, this.props.api.requestPromise("/projects/" + orgId + "/" + projectId + "/")];
                    case 7:
                        _b.sent();
                        return [3 /*break*/, 9];
                    case 8:
                        error_2 = _b.sent();
                        this.setState({
                            loading: false,
                            error: true,
                            errorType: ErrorTypes.PROJECT_NOT_FOUND,
                        });
                        return [3 /*break*/, 9];
                    case 9: return [2 /*return*/];
                }
            });
        });
    },
    renderBody: function () {
        if (this.state.loading) {
            return (<div className="loading-full-layout">
          <LoadingIndicator />
        </div>);
        }
        if (!this.state.error) {
            return this.props.children;
        }
        switch (this.state.errorType) {
            case ErrorTypes.PROJECT_NOT_FOUND:
                // TODO(chrissy): use scale for margin values
                return (<div className="container">
            <div className="alert alert-block" style={{ margin: '30px 0 10px' }}>
              {t('The project you were looking for was not found.')}
            </div>
          </div>);
            case ErrorTypes.MISSING_MEMBERSHIP:
                // TODO(dcramer): add various controls to improve this flow and break it
                // out into a reusable missing access error component
                return (<ErrorWrapper>
            <MissingProjectMembership organization={this.props.organization} projectSlug={this.state.project.slug}/>
          </ErrorWrapper>);
            default:
                return <LoadingError onRetry={this.remountComponent}/>;
        }
    },
    render: function () {
        var _this = this;
        return (<DocumentTitle ref={function (ref) { return (_this.docTitleRef = ref); }} title={this.getTitle()}>
        {this.renderBody()}
      </DocumentTitle>);
    },
});
export { ProjectContext };
export default withApi(withOrganization(withProjects(ProjectContext)));
var ErrorWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  width: 100%;\n  margin: ", " ", ";\n"], ["\n  width: 100%;\n  margin: ", " ", ";\n"])), space(2), space(4));
var templateObject_1;
//# sourceMappingURL=projectContext.jsx.map
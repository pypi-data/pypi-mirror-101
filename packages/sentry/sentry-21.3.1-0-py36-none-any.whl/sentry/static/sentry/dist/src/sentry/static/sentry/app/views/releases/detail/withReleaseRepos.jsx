import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import { Body, Main } from 'app/components/layouts/thirds';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel } from 'app/components/panels';
import { IconCommit } from 'app/icons';
import { t } from 'app/locale';
import getDisplayName from 'app/utils/getDisplayName';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
import withRepositories from 'app/utils/withRepositories';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import { ReleaseContext } from '.';
var withReleaseRepos = function (WrappedComponent) {
    var _a;
    return withApi(withOrganization(withRepositories((_a = /** @class */ (function (_super) {
            __extends(class_1, _super);
            function class_1() {
                var _this = _super !== null && _super.apply(this, arguments) || this;
                _this.state = {
                    releaseRepos: [],
                    isLoading: true,
                };
                return _this;
            }
            class_1.prototype.componentDidMount = function () {
                this.fetchReleaseRepos();
            };
            class_1.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
                this.setActiveReleaseRepo(nextProps);
            };
            class_1.prototype.componentDidUpdate = function (prevProps, prevState) {
                if (!!prevProps.repositoriesLoading && !this.props.repositoriesLoading) {
                    this.fetchReleaseRepos();
                    return;
                }
                if (prevState.releaseRepos.length !== this.state.releaseRepos.length) {
                    this.setActiveReleaseRepo(this.props);
                }
            };
            class_1.prototype.setActiveReleaseRepo = function (props) {
                var _a, _b;
                var _c = this.state, releaseRepos = _c.releaseRepos, activeReleaseRepo = _c.activeReleaseRepo;
                if (!releaseRepos.length) {
                    return;
                }
                var activeCommitRepo = (_a = props.location.query) === null || _a === void 0 ? void 0 : _a.activeRepo;
                if (!activeCommitRepo) {
                    this.setState({
                        activeReleaseRepo: (_b = releaseRepos[0]) !== null && _b !== void 0 ? _b : null,
                    });
                    return;
                }
                if (activeCommitRepo === (activeReleaseRepo === null || activeReleaseRepo === void 0 ? void 0 : activeReleaseRepo.name)) {
                    return;
                }
                var matchedRepository = releaseRepos.find(function (commitRepo) { return commitRepo.name === activeCommitRepo; });
                if (matchedRepository) {
                    this.setState({
                        activeReleaseRepo: matchedRepository,
                    });
                    return;
                }
                addErrorMessage(t('The repository you were looking for was not found.'));
            };
            class_1.prototype.fetchReleaseRepos = function () {
                return __awaiter(this, void 0, void 0, function () {
                    var _a, params, api, repositories, repositoriesLoading, release, orgId, project, releaseRepos, error_1;
                    return __generator(this, function (_b) {
                        switch (_b.label) {
                            case 0:
                                _a = this.props, params = _a.params, api = _a.api, repositories = _a.repositories, repositoriesLoading = _a.repositoriesLoading;
                                if (repositoriesLoading === undefined || repositoriesLoading === true) {
                                    return [2 /*return*/];
                                }
                                if (!(repositories === null || repositories === void 0 ? void 0 : repositories.length)) {
                                    this.setState({ isLoading: false });
                                    return [2 /*return*/];
                                }
                                release = params.release, orgId = params.orgId;
                                project = this.context.project;
                                this.setState({ isLoading: true });
                                _b.label = 1;
                            case 1:
                                _b.trys.push([1, 3, , 4]);
                                return [4 /*yield*/, api.requestPromise("/projects/" + orgId + "/" + project.slug + "/releases/" + encodeURIComponent(release) + "/repositories/")];
                            case 2:
                                releaseRepos = _b.sent();
                                this.setState({ releaseRepos: releaseRepos, isLoading: false });
                                return [3 /*break*/, 4];
                            case 3:
                                error_1 = _b.sent();
                                Sentry.captureException(error_1);
                                addErrorMessage(t('An error occured while trying to fetch the repositories of the release: %s', release));
                                return [3 /*break*/, 4];
                            case 4: return [2 /*return*/];
                        }
                    });
                });
            };
            class_1.prototype.render = function () {
                var _a = this.state, isLoading = _a.isLoading, activeReleaseRepo = _a.activeReleaseRepo, releaseRepos = _a.releaseRepos;
                var _b = this.props, repositoriesLoading = _b.repositoriesLoading, repositories = _b.repositories, params = _b.params, router = _b.router, location = _b.location, organization = _b.organization;
                if (isLoading || repositoriesLoading) {
                    return <LoadingIndicator />;
                }
                var noRepositoryOrgRelatedFound = !(repositories === null || repositories === void 0 ? void 0 : repositories.length);
                if (noRepositoryOrgRelatedFound) {
                    var orgId = params.orgId;
                    return (<Body>
                  <Main fullWidth>
                    <Panel dashedBorder>
                      <EmptyMessage icon={<IconCommit size="xl"/>} title={t('Releases are better with commit data!')} description={t('Connect a repository to see commit info, files changed, and authors involved in future releases.')} action={<Button priority="primary" to={"/settings/" + orgId + "/repos/"}>
                            {t('Connect a repository')}
                          </Button>}/>
                    </Panel>
                  </Main>
                </Body>);
                }
                var noReleaseReposFound = !releaseRepos.length;
                if (noReleaseReposFound) {
                    return (<Body>
                  <Main fullWidth>
                    <Panel dashedBorder>
                      <EmptyMessage icon={<IconCommit size="xl"/>} title={t('Releases are better with commit data!')} description={t('No commits associated with this release have been found.')}/>
                    </Panel>
                  </Main>
                </Body>);
                }
                if (activeReleaseRepo === undefined) {
                    return <LoadingIndicator />;
                }
                var release = params.release;
                var orgSlug = organization.slug;
                return (<WrappedComponent {...this.props} // this is just to satisfy the compiler
                 orgSlug={orgSlug} projectSlug={this.context.project.slug} release={release} router={router} location={location} releaseRepos={releaseRepos} activeReleaseRepo={activeReleaseRepo}/>);
            };
            return class_1;
        }(React.Component)),
        _a.displayName = "withReleaseRepos(" + getDisplayName(WrappedComponent) + ")",
        _a.contextType = ReleaseContext,
        _a))));
};
export default withReleaseRepos;
//# sourceMappingURL=withReleaseRepos.jsx.map
import { __assign, __extends } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { changeProjectSlug, removeProject, transferProject, } from 'app/actionCreators/projects';
import ProjectActions from 'app/actions/projectActions';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import { Panel, PanelAlert, PanelHeader } from 'app/components/panels';
import { fields } from 'app/data/forms/projectGeneralSettings';
import { t, tct } from 'app/locale';
import ProjectsStore from 'app/stores/projectsStore';
import handleXhrErrorResponse from 'app/utils/handleXhrErrorResponse';
import recreateRoute from 'app/utils/recreateRoute';
import routeTitleGen from 'app/utils/routeTitle';
import withOrganization from 'app/utils/withOrganization';
import AsyncView from 'app/views/asyncView';
import Field from 'app/views/settings/components/forms/field';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import TextField from 'app/views/settings/components/forms/textField';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
var ProjectGeneralSettings = /** @class */ (function (_super) {
    __extends(ProjectGeneralSettings, _super);
    function ProjectGeneralSettings() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this._form = {};
        _this.handleTransferFieldChange = function (id, value) {
            _this._form[id] = value;
        };
        _this.handleRemoveProject = function () {
            var orgId = _this.props.params.orgId;
            var project = _this.state.data;
            if (!project) {
                return;
            }
            removeProject(_this.api, orgId, project).then(function () {
                // Need to hard reload because lots of components do not listen to Projects Store
                window.location.assign('/');
            }, handleXhrErrorResponse('Unable to remove project'));
        };
        _this.handleTransferProject = function () {
            var orgId = _this.props.params.orgId;
            var project = _this.state.data;
            if (!project) {
                return;
            }
            if (typeof _this._form.email !== 'string' || _this._form.email.length < 1) {
                return;
            }
            transferProject(_this.api, orgId, project, _this._form.email).then(function () {
                // Need to hard reload because lots of components do not listen to Projects Store
                window.location.assign('/');
            }, handleXhrErrorResponse('Unable to transfer project'));
        };
        _this.isProjectAdmin = function () { return new Set(_this.props.organization.access).has('project:admin'); };
        return _this;
    }
    ProjectGeneralSettings.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('Project Settings'), projectId, false);
    };
    ProjectGeneralSettings.prototype.getEndpoints = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return [['data', "/projects/" + orgId + "/" + projectId + "/"]];
    };
    ProjectGeneralSettings.prototype.renderRemoveProject = function () {
        var project = this.state.data;
        var isProjectAdmin = this.isProjectAdmin();
        var isInternal = project.isInternal;
        return (<Field label={t('Remove Project')} help={tct('Remove the [project] project and all related data. [linebreak] Careful, this action cannot be undone.', {
                project: <strong>{project.slug}</strong>,
                linebreak: <br />,
            })}>
        {!isProjectAdmin &&
                t('You do not have the required permission to remove this project.')}

        {isInternal &&
                t('This project cannot be removed. It is used internally by the Sentry server.')}

        {isProjectAdmin && !isInternal && (<Confirm onConfirm={this.handleRemoveProject} priority="danger" confirmText={t('Remove project')} message={<div>
                <TextBlock>
                  <strong>
                    {t('Removing this project is permanent and cannot be undone!')}
                  </strong>
                </TextBlock>
                <TextBlock>
                  {t('This will also remove all associated event data.')}
                </TextBlock>
              </div>}>
            <div>
              <Button className="ref-remove-project" type="button" priority="danger">
                {t('Remove Project')}
              </Button>
            </div>
          </Confirm>)}
      </Field>);
    };
    ProjectGeneralSettings.prototype.renderTransferProject = function () {
        var _this = this;
        var project = this.state.data;
        var isProjectAdmin = this.isProjectAdmin();
        var isInternal = project.isInternal;
        return (<Field label={t('Transfer Project')} help={tct('Transfer the [project] project and all related data. [linebreak] Careful, this action cannot be undone.', {
                project: <strong>{project.slug}</strong>,
                linebreak: <br />,
            })}>
        {!isProjectAdmin &&
                t('You do not have the required permission to transfer this project.')}

        {isInternal &&
                t('This project cannot be transferred. It is used internally by the Sentry server.')}

        {isProjectAdmin && !isInternal && (<Confirm onConfirm={this.handleTransferProject} priority="danger" confirmText={t('Transfer project')} renderMessage={function (_a) {
                    var confirm = _a.confirm;
                    return (<div>
                <TextBlock>
                  <strong>
                    {t('Transferring this project is permanent and cannot be undone!')}
                  </strong>
                </TextBlock>
                <TextBlock>
                  {t('Please enter the email of an organization owner to whom you would like to transfer this project.')}
                </TextBlock>
                <Panel>
                  <Form hideFooter onFieldChange={_this.handleTransferFieldChange} onSubmit={function (_data, _onSuccess, _onError, e) {
                            e.stopPropagation();
                            confirm();
                        }}>
                    <TextField name="email" label={t('Organization Owner')} placeholder="admin@example.com" required help={t('A request will be emailed to this address, asking the organization owner to accept the project transfer.')}/>
                  </Form>
                </Panel>
              </div>);
                }}>
            <div>
              <Button className="ref-transfer-project" type="button" priority="danger">
                {t('Transfer Project')}
              </Button>
            </div>
          </Confirm>)}
      </Field>);
    };
    ProjectGeneralSettings.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var organization = this.props.organization;
        var project = this.state.data;
        var _b = this.props.params, orgId = _b.orgId, projectId = _b.projectId;
        var endpoint = "/projects/" + orgId + "/" + projectId + "/";
        var access = new Set(organization.access);
        var jsonFormProps = {
            additionalFieldProps: {
                organization: organization,
            },
            features: new Set(organization.features),
            access: access,
            disabled: !access.has('project:write'),
        };
        var team = project.teams.length ? (_a = project.teams) === null || _a === void 0 ? void 0 : _a[0] : undefined;
        return (<div>
        <SettingsPageHeader title={t('Project Settings')}/>
        <PermissionAlert />

        <Form saveOnBlur allowUndo initialData={__assign(__assign({}, project), { team: team })} apiMethod="PUT" apiEndpoint={endpoint} onSubmitSuccess={function (resp) {
                _this.setState({ data: resp });
                if (projectId !== resp.slug) {
                    changeProjectSlug(projectId, resp.slug);
                    // Container will redirect after stores get updated with new slug
                    _this.props.onChangeSlug(resp.slug);
                }
                // This will update our project context
                ProjectActions.updateSuccess(resp);
            }}>
          <JsonForm {...jsonFormProps} title={t('Project Details')} fields={[fields.slug, fields.platform]}/>

          <JsonForm {...jsonFormProps} title={t('Email')} fields={[fields.subjectPrefix]}/>

          <JsonForm {...jsonFormProps} title={t('Event Settings')} fields={[fields.resolveAge]}/>

          <JsonForm {...jsonFormProps} title={t('Client Security')} fields={[
                fields.allowedDomains,
                fields.scrapeJavaScript,
                fields.securityToken,
                fields.securityTokenHeader,
                fields.verifySSL,
            ]} renderHeader={function () { return (<PanelAlert type="info">
                <TextBlock noMargin>
                  {tct('Configure origin URLs which Sentry should accept events from. This is used for communication with clients like [link].', {
                    link: (<a href="https://github.com/getsentry/sentry-javascript">
                          sentry-javascript
                        </a>),
                })}{' '}
                  {tct('This will restrict requests based on the [Origin] and [Referer] headers.', {
                    Origin: <code>Origin</code>,
                    Referer: <code>Referer</code>,
                })}
                </TextBlock>
              </PanelAlert>); }}/>
        </Form>

        <Panel>
          <PanelHeader>{t('Project Administration')}</PanelHeader>
          {this.renderRemoveProject()}
          {this.renderTransferProject()}
        </Panel>
      </div>);
    };
    return ProjectGeneralSettings;
}(AsyncView));
var ProjectGeneralSettingsContainer = createReactClass({
    mixins: [Reflux.listenTo(ProjectsStore, 'onProjectsUpdate')],
    changedSlug: undefined,
    onProjectsUpdate: function () {
        if (!this.changedSlug) {
            return;
        }
        var project = ProjectsStore.getBySlug(this.changedSlug);
        if (!project) {
            return;
        }
        browserHistory.replace(recreateRoute('', __assign(__assign({}, this.props), { params: __assign(__assign({}, this.props.params), { projectId: this.changedSlug }) })));
    },
    render: function () {
        var _this = this;
        return (<ProjectGeneralSettings onChangeSlug={function (newSlug) { return (_this.changedSlug = newSlug); }} {...this.props}/>);
    },
});
export default withOrganization(ProjectGeneralSettingsContainer);
//# sourceMappingURL=projectGeneralSettings.jsx.map
import { __assign, __extends } from "tslib";
import React from 'react';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import IssueSyncListElement from 'app/components/issueSyncListElement';
import NavTabs from 'app/components/navTabs';
import { t, tct } from 'app/locale';
import plugins from 'app/plugins';
import withApi from 'app/utils/withApi';
import withOrganization from 'app/utils/withOrganization';
var PluginActions = /** @class */ (function (_super) {
    __extends(PluginActions, _super);
    function PluginActions() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            issue: null,
            pluginLoading: false,
        };
        _this.deleteIssue = function () {
            var plugin = __assign(__assign({}, _this.props.plugin), { issue: null });
            // override plugin.issue so that 'create/link' Modal
            // doesn't think the plugin still has an issue linked
            var endpoint = "/issues/" + _this.props.group.id + "/plugins/" + plugin.slug + "/unlink/";
            _this.props.api.request(endpoint, {
                success: function () {
                    _this.loadPlugin(plugin);
                    addSuccessMessage(t('Successfully unlinked issue.'));
                },
                error: function () {
                    addErrorMessage(t('Unable to unlink issue'));
                },
            });
        };
        _this.loadPlugin = function (data) {
            _this.setState({
                pluginLoading: true,
            }, function () {
                plugins.load(data, function () {
                    var issue = data.issue || null;
                    _this.setState({ pluginLoading: false, issue: issue });
                });
            });
        };
        _this.handleModalClose = function (data) {
            return _this.setState({
                issue: (data === null || data === void 0 ? void 0 : data.id) && (data === null || data === void 0 ? void 0 : data.link)
                    ? { issue_id: data.id, url: data.link, label: data.label }
                    : null,
            });
        };
        _this.openModal = function () {
            var issue = _this.state.issue;
            var _a = _this.props, project = _a.project, group = _a.group, organization = _a.organization;
            var plugin = __assign(__assign({}, _this.props.plugin), { issue: issue });
            openModal(function (deps) { return (<PluginActionsModal {...deps} project={project} group={group} organization={organization} plugin={plugin} onSuccess={_this.handleModalClose}/>); }, { onClose: _this.handleModalClose });
        };
        return _this;
    }
    PluginActions.prototype.componentDidMount = function () {
        this.loadPlugin(this.props.plugin);
    };
    PluginActions.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
        if (this.props.plugin.id !== nextProps.plugin.id) {
            this.loadPlugin(nextProps.plugin);
        }
    };
    PluginActions.prototype.render = function () {
        var issue = this.state.issue;
        var plugin = __assign(__assign({}, this.props.plugin), { issue: issue });
        return (<IssueSyncListElement onOpen={this.openModal} externalIssueDisplayName={issue ? issue.label : null} externalIssueId={issue ? issue.issue_id : null} externalIssueLink={issue ? issue.url : null} onClose={this.deleteIssue} integrationType={plugin.id}/>);
    };
    return PluginActions;
}(React.Component));
var PluginActionsModal = /** @class */ (function (_super) {
    __extends(PluginActionsModal, _super);
    function PluginActionsModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            actionType: 'create',
        };
        return _this;
    }
    PluginActionsModal.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Body = _a.Body, group = _a.group, project = _a.project, organization = _a.organization, plugin = _a.plugin, onSuccess = _a.onSuccess;
        var actionType = this.state.actionType;
        return (<React.Fragment>
        <Header closeButton>
          {tct('[name] Issue', { name: plugin.name || plugin.title })}
        </Header>
        <NavTabs underlined>
          <li className={actionType === 'create' ? 'active' : ''}>
            <a onClick={function () { return _this.setState({ actionType: 'create' }); }}>{t('Create')}</a>
          </li>
          <li className={actionType === 'link' ? 'active' : ''}>
            <a onClick={function () { return _this.setState({ actionType: 'link' }); }}>{t('Link')}</a>
          </li>
        </NavTabs>
        {actionType && (
            // need the key here so React will re-render
            // with new action prop
            <Body key={actionType}>
            {plugins.get(plugin).renderGroupActions({
                    plugin: plugin,
                    group: group,
                    project: project,
                    organization: organization,
                    actionType: actionType,
                    onSuccess: onSuccess,
                })}
          </Body>)}
      </React.Fragment>);
    };
    return PluginActionsModal;
}(React.Component));
export { PluginActions };
export default withApi(withOrganization(PluginActions));
//# sourceMappingURL=pluginActions.jsx.map
import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import { openModal } from 'app/actionCreators/modal';
import Button from 'app/components/button';
import { t } from 'app/locale';
import space from 'app/styles/space';
import AsyncView from 'app/views/asyncView';
import RadioGroup from 'app/views/settings/components/forms/controls/radioGroup';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import FormModel from 'app/views/settings/components/forms/model';
var userEditForm = {
    title: 'User details',
    fields: [
        {
            name: 'name',
            type: 'string',
            required: true,
            label: t('Name'),
        },
        {
            name: 'username',
            type: 'string',
            required: true,
            label: t('Username'),
            help: t('The username is the unique id of the user in the system'),
        },
        {
            name: 'email',
            type: 'string',
            required: true,
            label: t('Email'),
            help: t('The users primary email address'),
        },
        {
            name: 'isActive',
            type: 'boolean',
            required: true,
            label: t('Active'),
            help: t('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),
        },
        {
            name: 'isStaff',
            type: 'boolean',
            required: true,
            label: t('Admin'),
            help: t('Designates whether this user can perform administrative functions.'),
        },
        {
            name: 'isSuperuser',
            type: 'boolean',
            required: true,
            label: t('Superuser'),
            help: t('Designates whether this user has all permissions without explicitly assigning them.'),
        },
    ],
};
var REMOVE_BUTTON_LABEL = {
    disable: t('Disable User'),
    delete: t('Permanently Delete User'),
};
var RemoveUserModal = /** @class */ (function (_super) {
    __extends(RemoveUserModal, _super);
    function RemoveUserModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            deleteType: 'disable',
        };
        _this.onRemove = function () {
            _this.props.onRemove(_this.state.deleteType);
            _this.props.closeModal();
        };
        return _this;
    }
    RemoveUserModal.prototype.render = function () {
        var _this = this;
        var user = this.props.user;
        var deleteType = this.state.deleteType;
        return (<React.Fragment>
        <RadioGroup value={deleteType} label={t('Remove user %s', user.email)} onChange={function (type) { return _this.setState({ deleteType: type }); }} choices={[
                ['disable', t('Disable the account.')],
                ['delete', t('Permanently remove the user and their data.')],
            ]}/>
        <ModalFooter>
          <Button priority="danger" onClick={this.onRemove}>
            {REMOVE_BUTTON_LABEL[deleteType]}
          </Button>
          <Button onClick={this.props.closeModal}>{t('Cancel')}</Button>
        </ModalFooter>
      </React.Fragment>);
    };
    return RemoveUserModal;
}(React.Component));
var AdminUserEdit = /** @class */ (function (_super) {
    __extends(AdminUserEdit, _super);
    function AdminUserEdit() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.removeUser = function (actionTypes) {
            return actionTypes === 'delete' ? _this.deleteUser() : _this.deactivateUser();
        };
        _this.formModel = new FormModel();
        return _this;
    }
    Object.defineProperty(AdminUserEdit.prototype, "userEndpoint", {
        get: function () {
            var params = this.props.params;
            return "/users/" + params.id + "/";
        },
        enumerable: false,
        configurable: true
    });
    AdminUserEdit.prototype.getEndpoints = function () {
        return [['user', this.userEndpoint]];
    };
    AdminUserEdit.prototype.deleteUser = function () {
        var _a;
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0: return [4 /*yield*/, this.api.requestPromise(this.userEndpoint, {
                            method: 'DELETE',
                            data: { hardDelete: true, organizations: [] },
                        })];
                    case 1:
                        _b.sent();
                        addSuccessMessage(t("%s's account has been deleted.", (_a = this.state.user) === null || _a === void 0 ? void 0 : _a.email));
                        browserHistory.replace('/manage/users/');
                        return [2 /*return*/];
                }
            });
        });
    };
    AdminUserEdit.prototype.deactivateUser = function () {
        return __awaiter(this, void 0, void 0, function () {
            var response;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.api.requestPromise(this.userEndpoint, {
                            method: 'PUT',
                            data: { isActive: false },
                        })];
                    case 1:
                        response = _a.sent();
                        this.setState({ user: response });
                        this.formModel.setInitialData(response);
                        addSuccessMessage(t("%s's account has been deactivated.", response.email));
                        return [2 /*return*/];
                }
            });
        });
    };
    AdminUserEdit.prototype.renderBody = function () {
        var _this = this;
        var user = this.state.user;
        if (user === null) {
            return null;
        }
        var openDeleteModal = function () {
            return openModal(function (opts) { return (<RemoveUserModal user={user} onRemove={_this.removeUser} {...opts}/>); });
        };
        return (<React.Fragment>
        <h3>{t('Users')}</h3>
        <p>{t('Editing user: %s', user.email)}</p>
        <Form model={this.formModel} initialData={user} apiMethod="PUT" apiEndpoint={this.userEndpoint} requireChanges onSubmitError={addErrorMessage} onSubmitSuccess={function (data) {
                _this.setState({ user: data });
                addSuccessMessage('User account updated.');
            }} extraButton={<Button type="button" onClick={openDeleteModal} style={{ marginLeft: space(1) }} priority="danger">
              {t('Remove User')}
            </Button>}>
          <JsonForm forms={[userEditForm]}/>
        </Form>
      </React.Fragment>);
    };
    return AdminUserEdit;
}(AsyncView));
var ModalFooter = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: end;\n  padding: 20px 30px;\n  margin: 20px -30px -30px;\n  border-top: 1px solid ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  justify-content: end;\n  padding: 20px 30px;\n  margin: 20px -30px -30px;\n  border-top: 1px solid ", ";\n"])), space(1), function (p) { return p.theme.border; });
export default AdminUserEdit;
var templateObject_1;
//# sourceMappingURL=adminUserEdit.jsx.map
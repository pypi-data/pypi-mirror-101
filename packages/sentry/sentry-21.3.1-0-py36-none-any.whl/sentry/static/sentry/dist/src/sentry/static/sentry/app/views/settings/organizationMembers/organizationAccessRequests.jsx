import { __assign, __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { addErrorMessage, addSuccessMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
var OrganizationAccessRequests = /** @class */ (function (_super) {
    __extends(OrganizationAccessRequests, _super);
    function OrganizationAccessRequests() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            accessRequestBusy: {},
        };
        _this.handleApprove = function (id, e) {
            e.stopPropagation();
            _this.handleAction({
                id: id,
                isApproved: true,
                successMessage: t('Team request approved'),
                errorMessage: t('Error approving team request'),
            });
        };
        _this.handleDeny = function (id, e) {
            e.stopPropagation();
            _this.handleAction({
                id: id,
                isApproved: false,
                successMessage: t('Team request denied'),
                errorMessage: t('Error denying team request'),
            });
        };
        return _this;
    }
    OrganizationAccessRequests.prototype.handleAction = function (_a) {
        var id = _a.id, isApproved = _a.isApproved, successMessage = _a.successMessage, errorMessage = _a.errorMessage;
        return __awaiter(this, void 0, void 0, function () {
            var _b, api, orgId, onRemoveAccessRequest, _c;
            return __generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _b = this.props, api = _b.api, orgId = _b.orgId, onRemoveAccessRequest = _b.onRemoveAccessRequest;
                        this.setState(function (state) {
                            var _a;
                            return ({
                                accessRequestBusy: __assign(__assign({}, state.accessRequestBusy), (_a = {}, _a[id] = true, _a)),
                            });
                        });
                        _d.label = 1;
                    case 1:
                        _d.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/access-requests/" + id + "/", {
                                method: 'PUT',
                                data: { isApproved: isApproved },
                            })];
                    case 2:
                        _d.sent();
                        onRemoveAccessRequest(id);
                        addSuccessMessage(successMessage);
                        return [3 /*break*/, 4];
                    case 3:
                        _c = _d.sent();
                        addErrorMessage(errorMessage);
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState(function (state) {
                            var _a;
                            return ({
                                accessRequestBusy: __assign(__assign({}, state.accessRequestBusy), (_a = {}, _a[id] = false, _a)),
                            });
                        });
                        return [2 /*return*/];
                }
            });
        });
    };
    OrganizationAccessRequests.prototype.render = function () {
        var _this = this;
        var requestList = this.props.requestList;
        var accessRequestBusy = this.state.accessRequestBusy;
        if (!requestList || !requestList.length) {
            return null;
        }
        return (<Panel>
        <PanelHeader>{t('Pending Team Requests')}</PanelHeader>

        <PanelBody>
          {requestList.map(function (_a) {
                var id = _a.id, member = _a.member, team = _a.team, requester = _a.requester;
                var memberName = member.user &&
                    (member.user.name || member.user.email || member.user.username);
                var requesterName = requester && (requester.name || requester.email || requester.username);
                return (<StyledPanelItem key={id}>
                <div data-test-id="request-message">
                  {requesterName
                        ? tct('[requesterName] requests to add [name] to the [team] team.', {
                            requesterName: requesterName,
                            name: <strong>{memberName}</strong>,
                            team: <strong>#{team.slug}</strong>,
                        })
                        : tct('[name] requests access to the [team] team.', {
                            name: <strong>{memberName}</strong>,
                            team: <strong>#{team.slug}</strong>,
                        })}
                </div>
                <div>
                  <StyledButton priority="primary" size="small" onClick={function (e) { return _this.handleApprove(id, e); }} busy={accessRequestBusy[id]}>
                    {t('Approve')}
                  </StyledButton>
                  <Button busy={accessRequestBusy[id]} onClick={function (e) { return _this.handleDeny(id, e); }} size="small">
                    {t('Deny')}
                  </Button>
                </div>
              </StyledPanelItem>);
            })}
        </PanelBody>
      </Panel>);
    };
    return OrganizationAccessRequests;
}(React.Component));
var StyledPanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto max-content;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: grid;\n  grid-template-columns: auto max-content;\n  grid-gap: ", ";\n  align-items: center;\n"])), space(2));
var StyledButton = styled(Button)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
export default withApi(OrganizationAccessRequests);
var templateObject_1, templateObject_2;
//# sourceMappingURL=organizationAccessRequests.jsx.map
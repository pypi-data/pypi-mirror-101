import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { loadIncidents } from 'app/actionCreators/serviceIncidents';
import Button from 'app/components/button';
import { IconWarning } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import List from '../list';
import ListItem from '../list/listItem';
import SidebarItem from './sidebarItem';
import SidebarPanel from './sidebarPanel';
import SidebarPanelEmpty from './sidebarPanelEmpty';
import SidebarPanelItem from './sidebarPanelItem';
var ServiceIncidents = /** @class */ (function (_super) {
    __extends(ServiceIncidents, _super);
    function ServiceIncidents() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            status: null,
        };
        return _this;
    }
    ServiceIncidents.prototype.componentDidMount = function () {
        this.fetchData();
    };
    ServiceIncidents.prototype.fetchData = function () {
        return __awaiter(this, void 0, void 0, function () {
            var status_1, e_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, loadIncidents()];
                    case 1:
                        status_1 = _a.sent();
                        this.setState({ status: status_1 });
                        return [3 /*break*/, 3];
                    case 2:
                        e_1 = _a.sent();
                        Sentry.withScope(function (scope) {
                            scope.setLevel(Sentry.Severity.Warning);
                            scope.setFingerprint(['ServiceIncidents-fetchData']);
                            Sentry.captureException(e_1);
                        });
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    };
    ServiceIncidents.prototype.render = function () {
        var _a = this.props, currentPanel = _a.currentPanel, onShowPanel = _a.onShowPanel, hidePanel = _a.hidePanel, collapsed = _a.collapsed, orientation = _a.orientation;
        var status = this.state.status;
        if (!status) {
            return null;
        }
        var active = currentPanel === 'statusupdate';
        var isEmpty = !status.incidents || status.incidents.length === 0;
        if (isEmpty) {
            return null;
        }
        return (<React.Fragment>
        <SidebarItem id="statusupdate" orientation={orientation} collapsed={collapsed} active={active} icon={<IconWarning className="animated pulse infinite"/>} label={t('Service status')} onClick={onShowPanel}/>
        {active && status && (<SidebarPanel orientation={orientation} title={t('Recent service updates')} hidePanel={hidePanel} collapsed={collapsed}>
            {isEmpty && (<SidebarPanelEmpty>
                {t('There are no incidents to report')}
              </SidebarPanelEmpty>)}
            <IncidentList className="incident-list">
              {status.incidents.map(function (incident) { return (<SidebarPanelItem title={incident.name} message={t('Latest updates')} key={incident.id}>
                  {incident.updates ? (<List>
                      {incident.updates.map(function (update, key) { return (<ListItem key={key}>{update}</ListItem>); })}
                    </List>) : null}
                  <ActionBar>
                    <Button href={incident.url} size="small" external>
                      {t('Learn more')}
                    </Button>
                  </ActionBar>
                </SidebarPanelItem>); })}
            </IncidentList>
          </SidebarPanel>)}
      </React.Fragment>);
    };
    return ServiceIncidents;
}(React.Component));
export default ServiceIncidents;
var IncidentList = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var ActionBar = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(2));
var templateObject_1, templateObject_2;
//# sourceMappingURL=serviceIncidents.jsx.map
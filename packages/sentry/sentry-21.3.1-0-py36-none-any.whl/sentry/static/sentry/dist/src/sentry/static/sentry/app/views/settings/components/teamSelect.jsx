import { __awaiter, __extends, __generator, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import DropdownAutoComplete from 'app/components/dropdownAutoComplete';
import DropdownButton from 'app/components/dropdownButton';
import Link from 'app/components/links/link';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { DEFAULT_DEBOUNCE_DURATION, TEAMS_PER_PAGE } from 'app/constants';
import { IconSubtract } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var TeamSelect = /** @class */ (function (_super) {
    __extends(TeamSelect, _super);
    function TeamSelect() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            teams: null,
        };
        _this.fetchTeams = debounce(function (query) { return __awaiter(_this, void 0, void 0, function () {
            var _a, api, organization, teams;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, organization = _a.organization;
                        return [4 /*yield*/, api.requestPromise("/organizations/" + organization.slug + "/teams/", {
                                query: { query: query, per_page: TEAMS_PER_PAGE },
                            })];
                    case 1:
                        teams = _b.sent();
                        this.setState({ teams: teams, loading: false });
                        return [2 /*return*/];
                }
            });
        }); }, DEFAULT_DEBOUNCE_DURATION);
        _this.handleQueryUpdate = function (event) {
            _this.setState({ loading: true });
            _this.fetchTeams(event.target.value);
        };
        _this.handleAddTeam = function (option) {
            var _a;
            var team = (_a = _this.state.teams) === null || _a === void 0 ? void 0 : _a.find(function (tm) { return tm.slug === option.value; });
            if (team) {
                _this.props.onAddTeam(team);
            }
        };
        _this.handleRemove = function (teamSlug) {
            _this.props.onRemoveTeam(teamSlug);
        };
        return _this;
    }
    TeamSelect.prototype.componentDidMount = function () {
        this.fetchTeams();
    };
    TeamSelect.prototype.renderTeamAddDropDown = function () {
        var _a = this.props, disabled = _a.disabled, selectedTeams = _a.selectedTeams, menuHeader = _a.menuHeader;
        var teams = this.state.teams;
        var isDisabled = disabled;
        var options = [];
        if (teams === null || teams.length === 0) {
            options = [];
        }
        else {
            options = teams
                .filter(function (team) { return !selectedTeams.includes(team.slug); })
                .map(function (team, index) { return ({
                index: index,
                value: team.slug,
                searchKey: team.slug,
                label: <TeamDropdownElement>#{team.slug}</TeamDropdownElement>,
            }); });
        }
        return (<DropdownAutoComplete items={options} busyItemsStillVisible={this.state.loading} onChange={this.handleQueryUpdate} onSelect={this.handleAddTeam} emptyMessage={t('No teams')} menuHeader={menuHeader} disabled={isDisabled} alignMenu="right">
        {function (_a) {
                var isOpen = _a.isOpen;
                return (<DropdownButton aria-label={t('Add Team')} isOpen={isOpen} size="xsmall" disabled={isDisabled}>
            {t('Add Team')}
          </DropdownButton>);
            }}
      </DropdownAutoComplete>);
    };
    TeamSelect.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, selectedTeams = _a.selectedTeams, disabled = _a.disabled, confirmLastTeamRemoveMessage = _a.confirmLastTeamRemoveMessage;
        if (selectedTeams.length === 0) {
            return <EmptyMessage>{t('No Teams assigned')}</EmptyMessage>;
        }
        var confirmMessage = selectedTeams.length === 1 && confirmLastTeamRemoveMessage
            ? confirmLastTeamRemoveMessage
            : null;
        return selectedTeams.map(function (team) { return (<TeamRow key={team} orgId={organization.slug} team={team} onRemove={_this.handleRemove} disabled={disabled} confirmMessage={confirmMessage}/>); });
    };
    TeamSelect.prototype.render = function () {
        return (<Panel>
        <PanelHeader hasButtons>
          {t('Team')}
          {this.renderTeamAddDropDown()}
        </PanelHeader>

        <PanelBody>{this.renderBody()}</PanelBody>
      </Panel>);
    };
    return TeamSelect;
}(React.Component));
var TeamRow = function (props) {
    var orgId = props.orgId, team = props.team, onRemove = props.onRemove, disabled = props.disabled, confirmMessage = props.confirmMessage;
    return (<TeamPanelItem>
      <StyledLink to={"/settings/" + orgId + "/teams/" + team + "/"}>{"#" + team}</StyledLink>
      <Confirm message={confirmMessage} bypass={!confirmMessage} onConfirm={function () { return onRemove(team); }} disabled={disabled}>
        <Button size="xsmall" icon={<IconSubtract isCircled size="xs"/>} disabled={disabled}>
          {t('Remove')}
        </Button>
      </Confirm>
    </TeamPanelItem>);
};
var TeamDropdownElement = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: ", " 0px;\n  text-transform: none;\n"], ["\n  padding: ", " 0px;\n  text-transform: none;\n"])), space(0.5));
var TeamPanelItem = styled(PanelItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", ";\n  align-items: center;\n"], ["\n  padding: ", ";\n  align-items: center;\n"])), space(2));
var StyledLink = styled(Link)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex: 1;\n  margin-right: ", ";\n"], ["\n  flex: 1;\n  margin-right: ", ";\n"])), space(1));
export default withApi(TeamSelect);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=teamSelect.jsx.map
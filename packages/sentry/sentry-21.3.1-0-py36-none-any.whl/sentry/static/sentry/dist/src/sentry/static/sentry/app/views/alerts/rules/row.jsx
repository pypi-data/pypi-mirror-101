import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import memoize from 'lodash/memoize';
import moment from 'moment';
import Access from 'app/components/acl/access';
import Feature from 'app/components/acl/feature';
import ActorAvatar from 'app/components/avatar/actorAvatar';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import ErrorBoundary from 'app/components/errorBoundary';
import IdBadge from 'app/components/idBadge';
import Link from 'app/components/links/link';
import { IconDelete, IconSettings, IconUser } from 'app/icons';
import { t, tct } from 'app/locale';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { isIssueAlert } from '../utils';
var RuleListRow = /** @class */ (function (_super) {
    __extends(RuleListRow, _super);
    function RuleListRow() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        /**
         * Memoized function to find a project from a list of projects
         */
        _this.getProject = memoize(function (slug, projects) {
            return projects.find(function (project) { return project.slug === slug; });
        });
        return _this;
    }
    RuleListRow.prototype.render = function () {
        var _a, _b, _c;
        var _d = this.props, rule = _d.rule, projectsLoaded = _d.projectsLoaded, projects = _d.projects, organization = _d.organization, orgId = _d.orgId, onDelete = _d.onDelete, userTeams = _d.userTeams;
        var dateCreated = moment(rule.dateCreated).format('ll');
        var slug = rule.projects[0];
        var editLink = "/organizations/" + orgId + "/alerts/" + (isIssueAlert(rule) ? 'rules' : 'metric-rules') + "/" + slug + "/" + rule.id + "/";
        var hasRedesign = !isIssueAlert(rule) && organization.features.includes('alert-details-redesign');
        var detailsLink = "/organizations/" + orgId + "/alerts/rules/details/" + rule.id + "/";
        var ownerId = (_a = rule.owner) === null || _a === void 0 ? void 0 : _a.split(':')[1];
        var teamActor = ownerId
            ? { type: 'team', id: ownerId, name: '' }
            : null;
        var canEdit = ownerId ? userTeams.has(ownerId) : true;
        return (<ErrorBoundary>
        <RuleType>{isIssueAlert(rule) ? t('Issue') : t('Metric')}</RuleType>
        <Title>
          <Link to={hasRedesign ? detailsLink : editLink}>{rule.name}</Link>
        </Title>
        <ProjectBadge avatarSize={18} project={!projectsLoaded ? { slug: slug } : this.getProject(slug, projects)}/>
        <Feature features={['organizations:team-alerts-ownership']}>
          <TeamIcon>
            {teamActor ? (<ActorAvatar actor={teamActor} size={24}/>) : (<IconUser size="20px" color="gray400"/>)}
          </TeamIcon>
        </Feature>
        <CreatedBy>{(_c = (_b = rule === null || rule === void 0 ? void 0 : rule.createdBy) === null || _b === void 0 ? void 0 : _b.name) !== null && _c !== void 0 ? _c : '-'}</CreatedBy>
        <div>{dateCreated}</div>
        <RightColumn>
          <Access access={['alerts:write']}>
            {function (_a) {
                var hasAccess = _a.hasAccess;
                return (<ButtonBar gap={1}>
                <Confirm disabled={!hasAccess || !canEdit} message={tct("Are you sure you want to delete [name]? You won't be able to view the history of this alert once it's deleted.", {
                        name: rule.name,
                    })} header={t('Delete Alert Rule?')} priority="danger" confirmText={t('Delete Rule')} onConfirm={function () { return onDelete(slug, rule); }}>
                  <Button type="button" icon={<IconDelete />} size="small" title={t('Delete')}/>
                </Confirm>
                <Button size="small" type="button" icon={<IconSettings />} title={t('Edit')} to={editLink}/>
              </ButtonBar>);
            }}
          </Access>
        </RightColumn>
      </ErrorBoundary>);
    };
    return RuleListRow;
}(React.Component));
var columnCss = css(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  height: 100%;\n"], ["\n  display: flex;\n  flex-direction: column;\n  align-items: flex-start;\n  height: 100%;\n"])));
var RightColumn = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-start;\n  align-items: center;\n  padding: ", " ", ";\n"], ["\n  display: flex;\n  justify-content: flex-start;\n  align-items: center;\n  padding: ", " ", ";\n"])), space(1.5), space(2));
var RuleType = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  text-transform: uppercase;\n  ", "\n"], ["\n  font-size: ", ";\n  font-weight: 400;\n  color: ", ";\n  text-transform: uppercase;\n  ", "\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, columnCss);
var Title = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  ", "\n  ", "\n"], ["\n  ", "\n  ", "\n"])), overflowEllipsis, columnCss);
var CreatedBy = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  ", "\n  ", "\n"], ["\n  ", "\n  ", "\n"])), overflowEllipsis, columnCss);
var ProjectBadge = styled(IdBadge)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var TeamIcon = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
export default RuleListRow;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=row.jsx.map
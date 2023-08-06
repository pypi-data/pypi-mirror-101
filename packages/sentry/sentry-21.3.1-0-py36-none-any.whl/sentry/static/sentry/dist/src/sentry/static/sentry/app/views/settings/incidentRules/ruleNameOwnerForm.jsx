import { __extends } from "tslib";
import React from 'react';
import Feature from 'app/components/acl/feature';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import SelectMembers from 'app/components/selectMembers';
import { t } from 'app/locale';
import FormField from 'app/views/settings/components/forms/formField';
import TextField from 'app/views/settings/components/forms/textField';
var RuleNameOwnerForm = /** @class */ (function (_super) {
    __extends(RuleNameOwnerForm, _super);
    function RuleNameOwnerForm() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    RuleNameOwnerForm.prototype.render = function () {
        var _a = this.props, disabled = _a.disabled, project = _a.project, organization = _a.organization, userTeamIds = _a.userTeamIds;
        return (<Panel>
        <PanelHeader>{t('Give your rule a name')}</PanelHeader>
        <PanelBody>
          <TextField disabled={disabled} name="name" label={t('Rule Name')} help={t('Give your rule a name so it is easy to manage later')} placeholder={t('Something really bad happened')} required/>
          <Feature features={['organizations:team-alerts-ownership']}>
            <FormField name="owner" label={t('Team')} help={t('The team that owns this alert')}>
              {function (_a) {
                var model = _a.model;
                var owner = model.getValue('owner');
                var ownerId = owner && owner.split(':')[1];
                return (<SelectMembers showTeam project={project} organization={organization} value={ownerId} onChange={function (_a) {
                        var value = _a.value;
                        var ownerValue = value && "team:" + value;
                        model.setValue('owner', ownerValue);
                    }} filteredTeamIds={userTeamIds} includeUnassigned/>);
            }}
            </FormField>
          </Feature>
        </PanelBody>
      </Panel>);
    };
    return RuleNameOwnerForm;
}(React.PureComponent));
export default RuleNameOwnerForm;
//# sourceMappingURL=ruleNameOwnerForm.jsx.map
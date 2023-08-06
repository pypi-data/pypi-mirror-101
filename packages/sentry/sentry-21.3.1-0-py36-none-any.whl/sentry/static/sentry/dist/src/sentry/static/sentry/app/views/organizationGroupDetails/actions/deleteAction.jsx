import { __assign, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openModal } from 'app/actionCreators/modal';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import ActionButton from 'app/components/actions/button';
import MenuHeader from 'app/components/actions/menuHeader';
import MenuItemActionLink from 'app/components/actions/menuItemActionLink';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import Confirm from 'app/components/confirm';
import DropdownLink from 'app/components/dropdownLink';
import { IconChevron, IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { analytics } from 'app/utils/analytics';
function DeleteAction(_a) {
    var disabled = _a.disabled, project = _a.project, organization = _a.organization, onDiscard = _a.onDiscard, onDelete = _a.onDelete;
    function renderDiscardDisabled(_a) {
        var children = _a.children, props = __rest(_a, ["children"]);
        return children(__assign(__assign({}, props), { renderDisabled: function (_a) {
                var features = _a.features;
                return (<FeatureDisabled alert featureName="Discard and Delete" features={features}/>);
            } }));
    }
    function renderDiscardModal(_a) {
        var Body = _a.Body, Footer = _a.Footer, closeModal = _a.closeModal;
        return (<Feature features={['projects:discard-groups']} hookName="feature-disabled:discard-groups" organization={organization} project={project} renderDisabled={renderDiscardDisabled}>
        {function (_a) {
                var hasFeature = _a.hasFeature, renderDisabled = _a.renderDisabled, props = __rest(_a, ["hasFeature", "renderDisabled"]);
                return (<React.Fragment>
            <Body>
              {!hasFeature &&
                        typeof renderDisabled === 'function' &&
                        renderDisabled(__assign(__assign({}, props), { hasFeature: hasFeature, children: null }))}
              {t("Discarding this event will result in the deletion of most data associated with this issue and future events being discarded before reaching your stream. Are you sure you wish to continue?")}
            </Body>
            <Footer>
              <Button onClick={closeModal}>{t('Cancel')}</Button>
              <Button style={{ marginLeft: space(1) }} priority="primary" onClick={onDiscard} disabled={!hasFeature}>
                {t('Discard Future Events')}
              </Button>
            </Footer>
          </React.Fragment>);
            }}
      </Feature>);
    }
    function openDiscardModal() {
        openModal(renderDiscardModal);
        analytics('feature.discard_group.modal_opened', {
            org_id: parseInt(organization.id, 10),
        });
    }
    return (<ButtonBar merged>
      <Confirm message={t('Deleting this issue is permanent. Are you sure you wish to continue?')} onConfirm={onDelete} disabled={disabled}>
        <DeleteButton disabled={disabled} label={t('Delete issue')} icon={<IconDelete size="xs"/>}/>
      </Confirm>
      <DropdownLink caret={false} disabled={disabled} customTitle={<ActionButton disabled={disabled} label={t('More delete options')} icon={<IconChevron direction="down" size="xs"/>}/>}>
        <MenuHeader>{t('Delete & Discard')}</MenuHeader>
        <MenuItemActionLink title="" onAction={openDiscardModal}>
          {t('Delete and discard future events')}
        </MenuItemActionLink>
      </DropdownLink>
    </ButtonBar>);
}
var DeleteButton = styled(ActionButton)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", "\n"], ["\n  ",
    "\n"])), function (p) {
    return !p.disabled &&
        "\n  &:hover {\n    background-color: " + p.theme.button.danger.background + ";\n    color: " + p.theme.button.danger.color + ";\n    border-color: " + p.theme.button.danger.border + ";\n  }\n  ";
});
export default DeleteAction;
var templateObject_1;
//# sourceMappingURL=deleteAction.jsx.map
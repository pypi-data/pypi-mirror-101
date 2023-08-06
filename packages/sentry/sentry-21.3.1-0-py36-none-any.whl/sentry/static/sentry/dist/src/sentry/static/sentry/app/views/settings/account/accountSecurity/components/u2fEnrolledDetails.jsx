import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import Confirm from 'app/components/confirm';
import DateTime from 'app/components/dateTime';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import Tooltip from 'app/components/tooltip';
import { IconDelete } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import ConfirmHeader from 'app/views/settings/account/accountSecurity/components/confirmHeader';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
import TextBlock from 'app/views/settings/components/text/textBlock';
/**
 * List u2f devices w/ ability to remove a single device
 */
function U2fEnrolledDetails(_a) {
    var className = _a.className, isEnrolled = _a.isEnrolled, devices = _a.devices, id = _a.id, onRemoveU2fDevice = _a.onRemoveU2fDevice;
    if (id !== 'u2f' || !isEnrolled) {
        return null;
    }
    var hasDevices = devices === null || devices === void 0 ? void 0 : devices.length;
    // Note Tooltip doesn't work because of bootstrap(?) pointer events for disabled buttons
    var isLastDevice = hasDevices === 1;
    return (<Panel className={className}>
      <PanelHeader>{t('Device name')}</PanelHeader>

      <PanelBody>
        {!hasDevices && (<EmptyMessage>{t('You have not added any U2F devices')}</EmptyMessage>)}
        {hasDevices &&
            (devices === null || devices === void 0 ? void 0 : devices.map(function (device) { return (<DevicePanelItem key={device.name}>
              <DeviceInformation>
                <Name>{device.name}</Name>
                <FadedDateTime date={device.timestamp}/>
              </DeviceInformation>

              <Actions>
                <Confirm onConfirm={function () { return onRemoveU2fDevice(device); }} disabled={isLastDevice} message={<React.Fragment>
                      <ConfirmHeader>
                        {t('Do you want to remove U2F device?')}
                      </ConfirmHeader>
                      <TextBlock>
                        {t("Are you sure you want to remove the U2F device \"" + device.name + "\"?")}
                      </TextBlock>
                    </React.Fragment>}>
                  <Button size="small" priority="danger">
                    <Tooltip disabled={!isLastDevice} title={t('Can not remove last U2F device')}>
                      <IconDelete size="xs"/>
                    </Tooltip>
                  </Button>
                </Confirm>
              </Actions>
            </DevicePanelItem>); }))}
        <AddAnotherPanelItem>
          <Button type="button" to="/settings/account/security/mfa/u2f/enroll/" size="small">
            {t('Add Another Device')}
          </Button>
        </AddAnotherPanelItem>
      </PanelBody>
    </Panel>);
}
var DevicePanelItem = styled(PanelItem)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var DeviceInformation = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex: 1;\n\n  padding: ", ";\n  padding-right: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  flex: 1;\n\n  padding: ", ";\n  padding-right: 0;\n"])), space(2));
var FadedDateTime = styled(DateTime)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  opacity: 0.6;\n"], ["\n  font-size: ", ";\n  opacity: 0.6;\n"])), function (p) { return p.theme.fontSizeRelativeSmall; });
var Name = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex: 1;\n"], ["\n  flex: 1;\n"])));
var Actions = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space(2));
var AddAnotherPanelItem = styled(PanelItem)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  justify-content: flex-end;\n  padding: ", ";\n"], ["\n  justify-content: flex-end;\n  padding: ", ";\n"])), space(2));
export default styled(U2fEnrolledDetails)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(4));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=u2fEnrolledDetails.jsx.map
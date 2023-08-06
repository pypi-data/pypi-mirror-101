import { __assign, __extends, __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import * as Sentry from '@sentry/react';
import { addErrorMessage } from 'app/actionCreators/indicator';
import Button from 'app/components/button';
import SelectControl from 'app/components/forms/selectControl';
import LoadingIndicator from 'app/components/loadingIndicator';
import { Panel, PanelBody, PanelHeader, PanelItem } from 'app/components/panels';
import { IconAdd } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { uniqueId } from 'app/utils/guid';
import { removeAtArrayIndex } from 'app/utils/removeAtArrayIndex';
import { replaceAtArrayIndex } from 'app/utils/replaceAtArrayIndex';
import withOrganization from 'app/utils/withOrganization';
import FieldHelp from 'app/views/settings/components/forms/field/fieldHelp';
import FieldLabel from 'app/views/settings/components/forms/field/fieldLabel';
import ActionTargetSelector from 'app/views/settings/incidentRules/triggers/actionsPanel/actionTargetSelector';
import DeleteActionButton from 'app/views/settings/incidentRules/triggers/actionsPanel/deleteActionButton';
import { ActionLabel, TargetLabel, } from 'app/views/settings/incidentRules/types';
/**
 * When a new action is added, all of it's settings should be set to their default values.
 * @param actionConfig
 * @param dateCreated kept to maintain order of unsaved actions
 */
var getCleanAction = function (actionConfig, dateCreated) {
    return {
        unsavedId: uniqueId(),
        unsavedDateCreated: dateCreated !== null && dateCreated !== void 0 ? dateCreated : new Date().toISOString(),
        type: actionConfig.type,
        targetType: actionConfig &&
            actionConfig.allowedTargetTypes &&
            actionConfig.allowedTargetTypes.length > 0
            ? actionConfig.allowedTargetTypes[0]
            : null,
        targetIdentifier: actionConfig.sentryAppId || '',
        integrationId: actionConfig.integrationId,
        sentryAppId: actionConfig.sentryAppId,
        options: actionConfig.options || null,
    };
};
/**
 * Actions have a type (e.g. email, slack, etc), but only some have
 * an integrationId (e.g. email is null). This helper creates a unique
 * id based on the type and integrationId so that we know what action
 * a user's saved action corresponds to.
 */
var getActionUniqueKey = function (_a) {
    var type = _a.type, integrationId = _a.integrationId, sentryAppId = _a.sentryAppId;
    if (integrationId) {
        return type + "-" + integrationId;
    }
    else if (sentryAppId) {
        return type + "-" + sentryAppId;
    }
    return type;
};
/**
 * Creates a human-friendly display name for the integration based on type and
 * server provided `integrationName`
 *
 * e.g. for slack we show that it is slack and the `integrationName` is the workspace name
 */
var getFullActionTitle = function (_a) {
    var type = _a.type, integrationName = _a.integrationName, sentryAppName = _a.sentryAppName, status = _a.status;
    if (sentryAppName) {
        if (status) {
            return sentryAppName + " (" + status + ")";
        }
        return "" + sentryAppName;
    }
    var label = ActionLabel[type];
    if (integrationName) {
        return label + " - " + integrationName;
    }
    return label;
};
/**
 * Lists saved actions as well as control to add a new action
 */
var ActionsPanel = /** @class */ (function (_super) {
    __extends(ActionsPanel, _super);
    function ActionsPanel() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleAddAction = function () {
            var _a = _this.props, availableActions = _a.availableActions, onAdd = _a.onAdd;
            var actionConfig = availableActions === null || availableActions === void 0 ? void 0 : availableActions[0];
            if (!actionConfig) {
                addErrorMessage(t('There was a problem adding an action'));
                Sentry.captureException(new Error('Unable to add an action'));
                return;
            }
            var action = getCleanAction(actionConfig);
            // Add new actions to critical by default
            var triggerIndex = 0;
            onAdd(triggerIndex, action);
        };
        _this.handleDeleteAction = function (triggerIndex, index) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var actions = triggers[triggerIndex].actions;
            onChange(triggerIndex, triggers, removeAtArrayIndex(actions, index));
        };
        _this.handleChangeActionLevel = function (triggerIndex, index, value) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            // Convert saved action to unsaved by removing id
            var _b = triggers[triggerIndex].actions[index], _ = _b.id, action = __rest(_b, ["id"]);
            action.unsavedId = uniqueId();
            triggers[value.value].actions.push(action);
            onChange(value.value, triggers, triggers[value.value].actions);
            _this.handleDeleteAction(triggerIndex, index);
        };
        _this.handleChangeActionType = function (triggerIndex, index, value) {
            var _a;
            var _b = _this.props, triggers = _b.triggers, onChange = _b.onChange, availableActions = _b.availableActions;
            var actions = triggers[triggerIndex].actions;
            var actionConfig = availableActions === null || availableActions === void 0 ? void 0 : availableActions.find(function (availableAction) { return getActionUniqueKey(availableAction) === value.value; });
            if (!actionConfig) {
                addErrorMessage(t('There was a problem changing an action'));
                Sentry.captureException(new Error('Unable to change an action type'));
                return;
            }
            var existingDateCreated = (_a = actions[index].dateCreated) !== null && _a !== void 0 ? _a : actions[index].unsavedDateCreated;
            var newAction = getCleanAction(actionConfig, existingDateCreated);
            onChange(triggerIndex, triggers, replaceAtArrayIndex(actions, index, newAction));
        };
        _this.handleChangeTarget = function (triggerIndex, index, value) {
            var _a = _this.props, triggers = _a.triggers, onChange = _a.onChange;
            var actions = triggers[triggerIndex].actions;
            var newAction = __assign(__assign({}, actions[index]), { targetType: value.value, targetIdentifier: '' });
            onChange(triggerIndex, triggers, replaceAtArrayIndex(actions, index, newAction));
        };
        return _this;
    }
    ActionsPanel.prototype.handleChangeTargetIdentifier = function (triggerIndex, index, value) {
        var _a = this.props, triggers = _a.triggers, onChange = _a.onChange;
        var actions = triggers[triggerIndex].actions;
        var newAction = __assign(__assign({}, actions[index]), { targetIdentifier: value });
        onChange(triggerIndex, triggers, replaceAtArrayIndex(actions, index, newAction));
    };
    ActionsPanel.prototype.render = function () {
        var _this = this;
        var _a = this.props, availableActions = _a.availableActions, currentProject = _a.currentProject, disabled = _a.disabled, loading = _a.loading, organization = _a.organization, projects = _a.projects, triggers = _a.triggers;
        var project = projects.find(function (_a) {
            var slug = _a.slug;
            return slug === currentProject;
        });
        var items = availableActions === null || availableActions === void 0 ? void 0 : availableActions.map(function (availableAction) { return ({
            value: getActionUniqueKey(availableAction),
            label: getFullActionTitle(availableAction),
        }); });
        var levels = [
            { value: 0, label: 'Critical Status' },
            { value: 1, label: 'Warning Status' },
        ];
        // Create single array of unsaved and saved trigger actions
        // Sorted by date created ascending
        var actions = triggers
            .flatMap(function (trigger, triggerIndex) {
            return trigger.actions.map(function (action, actionIdx) {
                var _a;
                var availableAction = availableActions === null || availableActions === void 0 ? void 0 : availableActions.find(function (a) { return getActionUniqueKey(a) === getActionUniqueKey(action); });
                return {
                    dateCreated: new Date((_a = action.dateCreated) !== null && _a !== void 0 ? _a : action.unsavedDateCreated).getTime(),
                    triggerIndex: triggerIndex,
                    action: action,
                    actionIdx: actionIdx,
                    availableAction: availableAction,
                };
            });
        })
            .sort(function (a, b) { return a.dateCreated - b.dateCreated; });
        return (<Panel>
        <PanelHeader>{t('Actions')}</PanelHeader>
        <PanelBody withPadding>
          <FieldLabel>{t('Add an action')}</FieldLabel>
          <FieldHelp>
            {t('We can send you an email or activate an integration when any of the thresholds above are met.')}
          </FieldHelp>
        </PanelBody>
        <PanelBody>
          {loading && <LoadingIndicator />}
          {actions.map(function (_a) {
                var _b, _c;
                var action = _a.action, actionIdx = _a.actionIdx, triggerIndex = _a.triggerIndex, availableAction = _a.availableAction;
                return (<PanelItemWrapper key={(_b = action.id) !== null && _b !== void 0 ? _b : action.unsavedId}>
                <RuleRowContainer>
                  <PanelItemGrid>
                    <PanelItemSelects>
                      <SelectControl name="select-level" aria-label={t('Select a status level')} isDisabled={disabled || loading} placeholder={t('Select Level')} onChange={_this.handleChangeActionLevel.bind(_this, triggerIndex, actionIdx)} value={triggerIndex} options={levels}/>

                      <SelectControl name="select-action" aria-label={t('Select an Action')} isDisabled={disabled || loading} placeholder={t('Select Action')} onChange={_this.handleChangeActionType.bind(_this, triggerIndex, actionIdx)} value={getActionUniqueKey(action)} options={items !== null && items !== void 0 ? items : []}/>

                      {availableAction &&
                        availableAction.allowedTargetTypes.length > 1 ? (<SelectControl isDisabled={disabled || loading} value={action.targetType} options={(_c = availableAction === null || availableAction === void 0 ? void 0 : availableAction.allowedTargetTypes) === null || _c === void 0 ? void 0 : _c.map(function (allowedType) { return ({
                            value: allowedType,
                            label: TargetLabel[allowedType],
                        }); })} onChange={_this.handleChangeTarget.bind(_this, triggerIndex, actionIdx)}/>) : null}
                      <ActionTargetSelector action={action} availableAction={availableAction} disabled={disabled} loading={loading} onChange={_this.handleChangeTargetIdentifier.bind(_this, triggerIndex, actionIdx)} organization={organization} project={project}/>
                    </PanelItemSelects>
                    <DeleteActionButton triggerIndex={triggerIndex} index={actionIdx} onClick={_this.handleDeleteAction} disabled={disabled}/>
                  </PanelItemGrid>
                </RuleRowContainer>
              </PanelItemWrapper>);
            })}
          <StyledPanelItem>
            <Button type="button" disabled={disabled || loading} size="small" icon={<IconAdd isCircled color="gray300"/>} onClick={this.handleAddAction}>
              {t('Add New Action')}
            </Button>
          </StyledPanelItem>
        </PanelBody>
      </Panel>);
    };
    return ActionsPanel;
}(React.PureComponent));
var ActionsPanelWithSpace = styled(ActionsPanel)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space(4));
var PanelItemWrapper = styled("div")(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding: ", " ", " ", ";\n"], ["\n  padding: ", " ", " ", ";\n"])), space(0.5), space(2), space(1));
var PanelItemGrid = styled(PanelItem)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  border-bottom: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  padding: ", ";\n  border-bottom: 0;\n"])), space(1));
var PanelItemSelects = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  width: 100%;\n  margin-right: ", ";\n  > * {\n    flex: 0 1 200px;\n\n    &:not(:last-child) {\n      margin-right: ", ";\n    }\n  }\n"], ["\n  display: flex;\n  width: 100%;\n  margin-right: ", ";\n  > * {\n    flex: 0 1 200px;\n\n    &:not(:last-child) {\n      margin-right: ", ";\n    }\n  }\n"])), space(1), space(1));
var StyledPanelItem = styled(PanelItem)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", " ", " ", ";\n"], ["\n  padding: ", " ", " ", ";\n"])), space(1), space(2), space(2));
var RuleRowContainer = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  background-color: ", ";\n  border-radius: ", ";\n  border: 1px ", " solid;\n"], ["\n  background-color: ", ";\n  border-radius: ", ";\n  border: 1px ", " solid;\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.border; });
export default withOrganization(ActionsPanelWithSpace);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map
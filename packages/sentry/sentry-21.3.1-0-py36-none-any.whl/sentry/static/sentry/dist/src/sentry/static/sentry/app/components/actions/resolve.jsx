import { __extends } from "tslib";
import React from 'react';
import { openModal } from 'app/actionCreators/modal';
import ActionLink from 'app/components/actions/actionLink';
import ButtonBar from 'app/components/buttonBar';
import CustomResolutionModal from 'app/components/customResolutionModal';
import DropdownLink from 'app/components/dropdownLink';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark, IconChevron } from 'app/icons';
import { t } from 'app/locale';
import { ResolutionStatus, } from 'app/types';
import { formatVersion } from 'app/utils/formatters';
import ActionButton from './button';
import MenuHeader from './menuHeader';
import MenuItemActionLink from './menuItemActionLink';
var defaultProps = {
    isResolved: false,
    isAutoResolved: false,
    confirmLabel: t('Resolve'),
    hasInbox: false,
};
var ResolveActions = /** @class */ (function (_super) {
    __extends(ResolveActions, _super);
    function ResolveActions() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ResolveActions.prototype.onCustomResolution = function (statusDetails) {
        this.props.onUpdate({
            status: ResolutionStatus.RESOLVED,
            statusDetails: statusDetails,
        });
    };
    ResolveActions.prototype.renderResolved = function () {
        var _a = this.props, isAutoResolved = _a.isAutoResolved, onUpdate = _a.onUpdate;
        return (<Tooltip title={isAutoResolved
                ? t('This event is resolved due to the Auto Resolve configuration for this project')
                : t('Unresolve')}>
        <ActionButton priority="primary" icon={<IconCheckmark size="xs"/>} label={t('Unresolve')} disabled={isAutoResolved} onClick={function () { return onUpdate({ status: ResolutionStatus.UNRESOLVED }); }}/>
      </Tooltip>);
    };
    ResolveActions.prototype.renderDropdownMenu = function () {
        var _this = this;
        var _a = this.props, projectSlug = _a.projectSlug, isResolved = _a.isResolved, hasRelease = _a.hasRelease, latestRelease = _a.latestRelease, onUpdate = _a.onUpdate, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, disableDropdown = _a.disableDropdown, hasInbox = _a.hasInbox;
        if (isResolved) {
            return this.renderResolved();
        }
        var actionTitle = !hasRelease
            ? t('Set up release tracking in order to use this feature.')
            : '';
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled || !hasRelease,
        };
        return (<DropdownLink customTitle={!hasInbox && (<ActionButton label={t('More resolve options')} disabled={!projectSlug ? disabled : disableDropdown} icon={<IconChevron direction="down" size="xs"/>}/>)} caret={false} title={hasInbox && t('Resolve In\u2026')} alwaysRenderMenu disabled={!projectSlug ? disabled : disableDropdown} anchorRight={hasInbox} isNestedDropdown={hasInbox}>
        <MenuHeader>{t('Resolved In')}</MenuHeader>

        <MenuItemActionLink {...actionLinkProps} title={t('The next release')} onAction={function () {
                return hasRelease &&
                    onUpdate({
                        status: ResolutionStatus.RESOLVED,
                        statusDetails: {
                            inNextRelease: true,
                        },
                    });
            }}>
          <Tooltip disabled={hasRelease} title={actionTitle}>
            {t('The next release')}
          </Tooltip>
        </MenuItemActionLink>

        <MenuItemActionLink {...actionLinkProps} title={t('The current release')} onAction={function () {
                return hasRelease &&
                    onUpdate({
                        status: ResolutionStatus.RESOLVED,
                        statusDetails: {
                            inRelease: latestRelease ? latestRelease.version : 'latest',
                        },
                    });
            }}>
          <Tooltip disabled={hasRelease} title={actionTitle}>
            {latestRelease
                ? t('The current release (%s)', formatVersion(latestRelease.version))
                : t('The current release')}
          </Tooltip>
        </MenuItemActionLink>

        <MenuItemActionLink {...actionLinkProps} title={t('Another version')} onAction={function () { return hasRelease && _this.openCustomReleaseModal(); }} shouldConfirm={false}>
          <Tooltip disabled={hasRelease} title={actionTitle}>
            {t('Another version\u2026')}
          </Tooltip>
        </MenuItemActionLink>
      </DropdownLink>);
    };
    ResolveActions.prototype.openCustomReleaseModal = function () {
        var _this = this;
        var _a = this.props, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug;
        openModal(function (deps) { return (<CustomResolutionModal {...deps} onSelected={function (statusDetails) {
                return _this.onCustomResolution(statusDetails);
            }} orgSlug={orgSlug} projectSlug={projectSlug}/>); });
    };
    ResolveActions.prototype.render = function () {
        var _a = this.props, isResolved = _a.isResolved, onUpdate = _a.onUpdate, confirmMessage = _a.confirmMessage, shouldConfirm = _a.shouldConfirm, disabled = _a.disabled, confirmLabel = _a.confirmLabel, projectFetchError = _a.projectFetchError, hasInbox = _a.hasInbox;
        if (isResolved) {
            return this.renderResolved();
        }
        var actionLinkProps = {
            shouldConfirm: shouldConfirm,
            message: confirmMessage,
            confirmLabel: confirmLabel,
            disabled: disabled,
        };
        return (<Tooltip disabled={!projectFetchError} title={t('Error fetching project')}>
        {hasInbox ? (<div style={{ width: '100%' }}>
            <div className="dropdown-submenu flex expand-left">
              {this.renderDropdownMenu()}
            </div>
          </div>) : (<ButtonBar merged>
            <ActionLink {...actionLinkProps} type="button" title={t('Resolve')} icon={<IconCheckmark size="xs"/>} onAction={function () { return onUpdate({ status: ResolutionStatus.RESOLVED }); }}>
              {t('Resolve')}
            </ActionLink>
            {this.renderDropdownMenu()}
          </ButtonBar>)}
      </Tooltip>);
    };
    ResolveActions.defaultProps = defaultProps;
    return ResolveActions;
}(React.Component));
export default ResolveActions;
//# sourceMappingURL=resolve.jsx.map
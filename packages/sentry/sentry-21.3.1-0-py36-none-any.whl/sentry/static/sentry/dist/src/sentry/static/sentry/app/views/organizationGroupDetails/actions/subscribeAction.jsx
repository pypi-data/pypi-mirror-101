import React from 'react';
import ActionButton from 'app/components/actions/button';
import { IconBell } from 'app/icons';
import { t } from 'app/locale';
import { getSubscriptionReason } from '../utils';
function SubscribeAction(_a) {
    var _b, _c;
    var disabled = _a.disabled, group = _a.group, onClick = _a.onClick;
    var canChangeSubscriptionState = !((_c = (_b = group.subscriptionDetails) === null || _b === void 0 ? void 0 : _b.disabled) !== null && _c !== void 0 ? _c : false);
    if (!canChangeSubscriptionState) {
        return null;
    }
    return (<ActionButton disabled={disabled} title={getSubscriptionReason(group, true)} priority={group.isSubscribed ? 'primary' : 'default'} size="zero" label={t('Subscribe')} onClick={onClick} icon={<IconBell size="xs"/>}/>);
}
export default SubscribeAction;
//# sourceMappingURL=subscribeAction.jsx.map
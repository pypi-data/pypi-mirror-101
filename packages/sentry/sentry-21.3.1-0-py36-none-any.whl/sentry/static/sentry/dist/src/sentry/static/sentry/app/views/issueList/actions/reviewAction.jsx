import React from 'react';
import ActionLink from 'app/components/actions/actionLink';
import { IconIssues } from 'app/icons';
import { t } from 'app/locale';
function ReviewAction(_a) {
    var disabled = _a.disabled, onUpdate = _a.onUpdate;
    return (<ActionLink type="button" disabled={disabled} onAction={function () { return onUpdate({ inbox: false }); }} title={t('Mark Reviewed')} icon={<IconIssues size="xs"/>}>
      {t('Mark Reviewed')}
    </ActionLink>);
}
export default ReviewAction;
//# sourceMappingURL=reviewAction.jsx.map
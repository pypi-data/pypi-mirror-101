import React from 'react';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
export default function PlatformHeaderButtonBar(_a) {
    var gettingStartedLink = _a.gettingStartedLink, docsLink = _a.docsLink;
    return (<ButtonBar gap={1}>
      <Button size="small" to={gettingStartedLink}>
        {t('< Back')}
      </Button>
      <Button size="small" href={docsLink} external>
        {t('Full Documentation')}
      </Button>
    </ButtonBar>);
}
//# sourceMappingURL=platformHeaderButtonBar.jsx.map
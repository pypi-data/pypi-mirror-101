import React from 'react';
import * as Sentry from '@sentry/react';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark, IconClose, IconWarning } from 'app/icons';
import { CandidateProcessingStatus } from 'app/types/debugImage';
function ProcessingIcon(_a) {
    var processingInfo = _a.processingInfo;
    switch (processingInfo.status) {
        case CandidateProcessingStatus.OK:
            return <IconCheckmark color="green300" size="xs"/>;
        case CandidateProcessingStatus.ERROR: {
            var details = processingInfo.details;
            return (<Tooltip title={details} disabled={!details}>
          <IconClose color="red300" size="xs"/>
        </Tooltip>);
        }
        case CandidateProcessingStatus.MALFORMED: {
            var details = processingInfo.details;
            return (<Tooltip title={details} disabled={!details}>
          <IconWarning color="yellow300" size="xs"/>
        </Tooltip>);
        }
        default: {
            Sentry.withScope(function (scope) {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image candidate ProcessingIcon status'));
            });
            return null; //this shall never happen
        }
    }
}
export default ProcessingIcon;
//# sourceMappingURL=processingIcon.jsx.map
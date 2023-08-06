import * as Sentry from '@sentry/react';
import { t } from 'app/locale';
import { CandidateDownloadStatus, ImageFeature, } from 'app/types/debugImage';
import { INTERNAL_SOURCE } from '../utils';
export function getImageFeatureDescription(type) {
    switch (type) {
        case ImageFeature.has_debug_info:
            return {
                label: t('debug'),
                description: t('Debug information provides function names and resolves inlined frames during symbolication'),
            };
        case ImageFeature.has_sources:
            return {
                label: t('sources'),
                description: t('Source code information allows Sentry to display source code context for stack frames'),
            };
        case ImageFeature.has_symbols:
            return {
                label: t('symtab'),
                description: t('Symbol tables are used as a fallback when full debug information is not available'),
            };
        case ImageFeature.has_unwind_info:
            return {
                label: t('unwind'),
                description: t('Stack unwinding information improves the quality of stack traces extracted from minidumps'),
            };
        default: {
            Sentry.withScope(function (scope) {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image candidate feature'));
            });
            return {}; // this shall not happen
        }
    }
}
export function getSourceTooltipDescription(source, builtinSymbolSources) {
    if (source === INTERNAL_SOURCE) {
        return t("This debug information file is from Sentry's internal symbol server for this project");
    }
    if (builtinSymbolSources === null || builtinSymbolSources === void 0 ? void 0 : builtinSymbolSources.find(function (builtinSymbolSource) { return builtinSymbolSource.id === source; })) {
        return t('This debug information file is from a built-in symbol server');
    }
    return t('This debug information file is from a custom symbol server');
}
export function getStatusTooltipDescription(candidate, hasReprocessWarning) {
    var download = candidate.download, location = candidate.location, source = candidate.source;
    switch (download.status) {
        case CandidateDownloadStatus.OK: {
            return {
                label: t('Download Details'),
                description: location,
                disabled: !location || source === INTERNAL_SOURCE,
            };
        }
        case CandidateDownloadStatus.ERROR:
        case CandidateDownloadStatus.MALFORMED: {
            var details = download.details;
            return {
                label: t('Download Details'),
                description: details,
                disabled: !details,
            };
        }
        case CandidateDownloadStatus.NOT_FOUND: {
            return {};
        }
        case CandidateDownloadStatus.NO_PERMISSION: {
            var details = download.details;
            return {
                label: t('Permission Error'),
                description: details,
                disabled: !details,
            };
        }
        case CandidateDownloadStatus.DELETED: {
            return {
                label: t('This file was deleted after the issue was processed.'),
            };
        }
        case CandidateDownloadStatus.UNAPPLIED: {
            return {
                label: hasReprocessWarning
                    ? t('This issue was processed before this debug information file was available. To apply new debug information, reprocess this issue.')
                    : t('This issue was processed before this debug information file was available'),
            };
        }
        default: {
            Sentry.withScope(function (scope) {
                scope.setLevel(Sentry.Severity.Warning);
                Sentry.captureException(new Error('Unknown image candidate download status'));
            });
            return {}; // This shall not happen
        }
    }
}
//# sourceMappingURL=utils.jsx.map
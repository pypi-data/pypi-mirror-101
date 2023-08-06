import React from 'react';
import DocumentTitle from 'react-document-title';
function SentryDocumentTitle(_a) {
    var title = _a.title, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, children = _a.children;
    function getDocTitle() {
        if (!orgSlug && !projectSlug) {
            return title;
        }
        if (orgSlug && projectSlug) {
            return title + " - " + orgSlug + " - " + projectSlug;
        }
        if (orgSlug) {
            return title + " - " + orgSlug;
        }
        return title + " - " + projectSlug;
    }
    var docTitle = getDocTitle();
    return <DocumentTitle title={docTitle + " - Sentry"}>{children}</DocumentTitle>;
}
export default SentryDocumentTitle;
//# sourceMappingURL=sentryDocumentTitle.jsx.map
function routeTitleGen(routeName, orgSlug, withSentry, projectSlug) {
    if (withSentry === void 0) { withSentry = true; }
    var tmplBase = routeName + " - " + orgSlug;
    var tmpl = projectSlug ? tmplBase + " - " + projectSlug : tmplBase;
    return withSentry ? tmpl + " - Sentry" : tmpl;
}
export default routeTitleGen;
//# sourceMappingURL=routeTitle.jsx.map
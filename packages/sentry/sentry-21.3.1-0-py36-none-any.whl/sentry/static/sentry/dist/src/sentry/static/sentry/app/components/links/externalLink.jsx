import { __rest } from "tslib";
import React from 'react';
var ExternalLink = React.forwardRef(function ExternalLink(_a, ref) {
    var _b = _a.openInNewTab, openInNewTab = _b === void 0 ? true : _b, props = __rest(_a, ["openInNewTab"]);
    var anchorProps = openInNewTab ? { target: '_blank', rel: 'noreferrer noopener' } : {};
    return <a ref={ref} {...anchorProps} {...props}/>;
});
export default ExternalLink;
//# sourceMappingURL=externalLink.jsx.map
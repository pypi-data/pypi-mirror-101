import { __rest } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
var SvgIcon = React.forwardRef(function SvgIcon(_a, ref) {
    var _b, _c;
    var theme = _a.theme, _d = _a.color, providedColor = _d === void 0 ? 'currentColor' : _d, _e = _a.size, providedSize = _e === void 0 ? 'sm' : _e, _f = _a.viewBox, viewBox = _f === void 0 ? '0 0 16 16' : _f, props = __rest(_a, ["theme", "color", "size", "viewBox"]);
    var color = (_b = theme[providedColor]) !== null && _b !== void 0 ? _b : providedColor;
    var size = (_c = theme.iconSizes[providedSize]) !== null && _c !== void 0 ? _c : providedSize;
    return (<svg {...props} viewBox={viewBox} fill={color} height={size} width={size} ref={ref}/>);
});
export default withTheme(SvgIcon);
//# sourceMappingURL=svgIcon.jsx.map
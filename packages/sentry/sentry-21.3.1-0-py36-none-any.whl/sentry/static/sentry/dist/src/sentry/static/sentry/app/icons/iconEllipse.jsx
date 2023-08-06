import React from 'react';
import SvgIcon from './svgIcon';
var IconEllipse = React.forwardRef(function IconEllipse(props, ref) {
    return (<SvgIcon {...props} ref={ref}>
      <circle cx="8" cy="8" r="4"/>
    </SvgIcon>);
});
IconEllipse.displayName = 'IconEllipse';
export { IconEllipse };
//# sourceMappingURL=iconEllipse.jsx.map
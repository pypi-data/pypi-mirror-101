import { __rest } from "tslib";
import React from 'react';
import classnames from 'classnames';
function NavTabs(props) {
    var underlined = props.underlined, className = props.className, tabProps = __rest(props, ["underlined", "className"]);
    var mergedClassName = classnames('nav nav-tabs', className, {
        'border-bottom': underlined,
    });
    return <ul className={mergedClassName} {...tabProps}/>;
}
export default NavTabs;
//# sourceMappingURL=navTabs.jsx.map
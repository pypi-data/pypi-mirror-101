import React from 'react';
import { formatAbbreviatedNumber } from 'app/utils/formatters';
function Count(props) {
    var value = props.value, className = props.className;
    return (<span className={className} title={value.toLocaleString()}>
      {formatAbbreviatedNumber(value)}
    </span>);
}
export default Count;
//# sourceMappingURL=count.jsx.map
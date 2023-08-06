import { __rest } from "tslib";
import React from 'react';
import { getDuration, getExactDuration } from 'app/utils/formatters';
var Duration = function (_a) {
    var seconds = _a.seconds, fixedDigits = _a.fixedDigits, abbreviation = _a.abbreviation, exact = _a.exact, props = __rest(_a, ["seconds", "fixedDigits", "abbreviation", "exact"]);
    return (<span {...props}>
    {exact
            ? getExactDuration(seconds, abbreviation)
            : getDuration(seconds, fixedDigits, abbreviation)}
  </span>);
};
export default Duration;
//# sourceMappingURL=duration.jsx.map
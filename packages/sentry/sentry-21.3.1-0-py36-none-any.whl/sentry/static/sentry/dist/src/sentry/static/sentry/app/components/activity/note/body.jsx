import React from 'react';
import marked from 'app/utils/marked';
var NoteBody = function (_a) {
    var className = _a.className, text = _a.text;
    return (<div className={className} data-test-id="activity-note-body" dangerouslySetInnerHTML={{ __html: marked(text) }}/>);
};
export default NoteBody;
//# sourceMappingURL=body.jsx.map
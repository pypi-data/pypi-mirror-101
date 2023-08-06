import { __read } from "tslib";
import React from 'react';
import { objectIsEmpty } from 'app/utils';
import Chunk from './chunk';
function Contexts(_a) {
    var event = _a.event, group = _a.group;
    var user = event.user, contexts = event.contexts;
    return (<React.Fragment>
      {!objectIsEmpty(user) && (<Chunk key="user" type="user" alias="user" group={group} event={event} value={user}/>)}
      {Object.entries(contexts).map(function (_a) {
            var _b;
            var _c = __read(_a, 2), key = _c[0], value = _c[1];
            return (<Chunk key={key} type={(_b = value === null || value === void 0 ? void 0 : value.type) !== null && _b !== void 0 ? _b : ''} alias={key} group={group} event={event} value={value}/>);
        })}
    </React.Fragment>);
}
export default Contexts;
//# sourceMappingURL=index.jsx.map
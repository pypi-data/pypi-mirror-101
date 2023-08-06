import React from 'react';
import Breadcrumbs from 'app/components/events/interfaces/breadcrumbs';
import Csp from 'app/components/events/interfaces/csp';
import DebugMeta from 'app/components/events/interfaces/debugMeta';
import DebugMetaV2 from 'app/components/events/interfaces/debugMeta-v2';
import Exception from 'app/components/events/interfaces/exception';
import Generic from 'app/components/events/interfaces/generic';
import Message from 'app/components/events/interfaces/message';
import Request from 'app/components/events/interfaces/request';
import Spans from 'app/components/events/interfaces/spans';
import Stacktrace from 'app/components/events/interfaces/stacktrace';
import Template from 'app/components/events/interfaces/template';
import Threads from 'app/components/events/interfaces/threads';
import { EntryType } from 'app/types/event';
function EventEntry(_a) {
    var _b;
    var entry = _a.entry, projectSlug = _a.projectSlug, event = _a.event, organization = _a.organization, groupId = _a.groupId;
    switch (entry.type) {
        case EntryType.EXCEPTION: {
            var data_1 = entry.data, type = entry.type;
            return <Exception type={type} event={event} data={data_1} projectId={projectSlug}/>;
        }
        case EntryType.MESSAGE: {
            var data_2 = entry.data;
            return <Message data={data_2}/>;
        }
        case EntryType.REQUEST: {
            var data_3 = entry.data, type = entry.type;
            return <Request type={type} event={event} data={data_3}/>;
        }
        case EntryType.STACKTRACE: {
            var data_4 = entry.data, type = entry.type;
            return <Stacktrace type={type} event={event} data={data_4} projectId={projectSlug}/>;
        }
        case EntryType.TEMPLATE: {
            var data_5 = entry.data, type = entry.type;
            return <Template type={type} event={event} data={data_5}/>;
        }
        case EntryType.CSP: {
            var data_6 = entry.data;
            return <Csp event={event} data={data_6}/>;
        }
        case EntryType.EXPECTCT:
        case EntryType.EXPECTSTAPLE:
        case EntryType.HPKP: {
            var data_7 = entry.data, type = entry.type;
            return <Generic type={type} data={data_7}/>;
        }
        case EntryType.BREADCRUMBS: {
            var data_8 = entry.data, type = entry.type;
            return (<Breadcrumbs type={type} data={data_8} organization={organization} event={event}/>);
        }
        case EntryType.THREADS: {
            var data_9 = entry.data, type = entry.type;
            return <Threads type={type} event={event} data={data_9} projectId={projectSlug}/>;
        }
        case EntryType.DEBUGMETA:
            var data = entry.data;
            var hasImagesLoadedV2Feature = !!((_b = organization.features) === null || _b === void 0 ? void 0 : _b.includes('images-loaded-v2'));
            if (hasImagesLoadedV2Feature) {
                return (<DebugMetaV2 event={event} projectId={projectSlug} groupId={groupId} organization={organization} data={data}/>);
            }
            return (<DebugMeta event={event} projectId={projectSlug} organization={organization} data={data}/>);
        case EntryType.SPANS:
            return (<Spans event={event} organization={organization}/>);
        default:
            // this should not happen
            /*eslint no-console:0*/
            window.console &&
                console.error &&
                console.error('Unregistered interface: ' + entry.type);
            return null;
    }
}
export default EventEntry;
//# sourceMappingURL=eventEntry.jsx.map
import * as Sentry from '@sentry/react';
import isNil from 'lodash/isNil';
import GroupActions from 'app/actions/groupActions';
import { Client } from 'app/api';
import GroupStore from 'app/stores/groupStore';
import { buildTeamId, buildUserId } from 'app/utils';
import { uniqueId } from 'app/utils/guid';
export function assignToUser(params) {
    var api = new Client();
    var endpoint = "/issues/" + params.id + "/";
    var id = uniqueId();
    GroupActions.assignTo(id, params.id, {
        email: (params.member && params.member.email) || '',
    });
    var request = api.requestPromise(endpoint, {
        method: 'PUT',
        // Sending an empty value to assignedTo is the same as "clear",
        // so if no member exists, that implies that we want to clear the
        // current assignee.
        data: {
            assignedTo: params.user ? buildUserId(params.user.id) : '',
        },
    });
    request
        .then(function (data) {
        GroupActions.assignToSuccess(id, params.id, data);
    })
        .catch(function (data) {
        GroupActions.assignToError(id, params.id, data);
    });
    return request;
}
export function clearAssignment(groupId) {
    var api = new Client();
    var endpoint = "/issues/" + groupId + "/";
    var id = uniqueId();
    GroupActions.assignTo(id, groupId, {
        email: '',
    });
    var request = api.requestPromise(endpoint, {
        method: 'PUT',
        // Sending an empty value to assignedTo is the same as "clear"
        data: {
            assignedTo: '',
        },
    });
    request
        .then(function (data) {
        GroupActions.assignToSuccess(id, groupId, data);
    })
        .catch(function (data) {
        GroupActions.assignToError(id, groupId, data);
    });
    return request;
}
export function assignToActor(_a) {
    var id = _a.id, actor = _a.actor;
    var api = new Client();
    var endpoint = "/issues/" + id + "/";
    var guid = uniqueId();
    var actorId;
    GroupActions.assignTo(guid, id, { email: '' });
    switch (actor.type) {
        case 'user':
            actorId = buildUserId(actor.id);
            break;
        case 'team':
            actorId = buildTeamId(actor.id);
            break;
        default:
            Sentry.withScope(function (scope) {
                scope.setExtra('actor', actor);
                Sentry.captureException('Unknown assignee type');
            });
    }
    return api
        .requestPromise(endpoint, {
        method: 'PUT',
        data: { assignedTo: actorId },
    })
        .then(function (data) {
        GroupActions.assignToSuccess(guid, id, data);
    })
        .catch(function (data) {
        GroupActions.assignToError(guid, id, data);
    });
}
export function deleteNote(api, group, id, _oldText) {
    var restore = group.activity.find(function (activity) { return activity.id === id; });
    var index = GroupStore.removeActivity(group.id, id);
    if (index === -1) {
        // I dunno, the id wasn't found in the GroupStore
        return Promise.reject(new Error('Group was not found in store'));
    }
    var promise = api.requestPromise("/issues/" + group.id + "/comments/" + id + "/", {
        method: 'DELETE',
    });
    promise.catch(function () { return GroupStore.addActivity(group.id, restore, index); });
    return promise;
}
export function createNote(api, group, note) {
    var promise = api.requestPromise("/issues/" + group.id + "/comments/", {
        method: 'POST',
        data: note,
    });
    promise.then(function (data) { return GroupStore.addActivity(group.id, data); });
    return promise;
}
export function updateNote(api, group, note, id, oldText) {
    GroupStore.updateActivity(group.id, id, { text: note.text });
    var promise = api.requestPromise("/issues/" + group.id + "/comments/" + id + "/", {
        method: 'PUT',
        data: note,
    });
    promise.catch(function () { return GroupStore.updateActivity(group.id, id, { text: oldText }); });
    return promise;
}
/**
 * Converts input parameters to API-compatible query arguments
 */
export function paramsToQueryArgs(params) {
    var _a;
    var p = params.itemIds
        ? { id: params.itemIds } // items matching array of itemids
        : params.query
            ? { query: params.query } // items matching search query
            : {}; // all items
    // only include environment if it is not null/undefined
    if (params.query && !isNil(params.environment)) {
        p.environment = params.environment;
    }
    // only include projects if it is not null/undefined/an empty array
    if ((_a = params.project) === null || _a === void 0 ? void 0 : _a.length) {
        p.project = params.project;
    }
    // only include date filters if they are not null/undefined
    if (params.query) {
        ['start', 'end', 'period', 'utc'].forEach(function (prop) {
            if (!isNil(params[prop])) {
                p[prop === 'period' ? 'statsPeriod' : prop] = params[prop];
            }
        });
    }
    return p;
}
function getUpdateUrl(_a) {
    var projectId = _a.projectId, orgId = _a.orgId;
    return projectId
        ? "/projects/" + orgId + "/" + projectId + "/issues/"
        : "/organizations/" + orgId + "/issues/";
}
function chainUtil() {
    var funcs = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        funcs[_i] = arguments[_i];
    }
    var filteredFuncs = funcs.filter(function (f) { return typeof f === 'function'; });
    return function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        filteredFuncs.forEach(function (func) {
            func.apply(funcs, args);
        });
    };
}
function wrapRequest(api, path, options, extraParams) {
    if (extraParams === void 0) { extraParams = {}; }
    options.success = chainUtil(options.success, extraParams.success);
    options.error = chainUtil(options.error, extraParams.error);
    options.complete = chainUtil(options.complete, extraParams.complete);
    return api.request(path, options);
}
export function bulkDelete(api, params, options) {
    var itemIds = params.itemIds;
    var path = getUpdateUrl(params);
    var query = paramsToQueryArgs(params);
    var id = uniqueId();
    GroupActions.delete(id, itemIds);
    return wrapRequest(api, path, {
        query: query,
        method: 'DELETE',
        success: function (response) {
            GroupActions.deleteSuccess(id, itemIds, response);
        },
        error: function (error) {
            GroupActions.deleteError(id, itemIds, error);
        },
    }, options);
}
export function bulkUpdate(api, params, options) {
    var itemIds = params.itemIds, failSilently = params.failSilently, data = params.data;
    var path = getUpdateUrl(params);
    var query = paramsToQueryArgs(params);
    var id = uniqueId();
    GroupActions.update(id, itemIds, data);
    return wrapRequest(api, path, {
        query: query,
        method: 'PUT',
        data: data,
        success: function (response) {
            GroupActions.updateSuccess(id, itemIds, response);
        },
        error: function (error) {
            GroupActions.updateError(id, itemIds, error, failSilently);
        },
    }, options);
}
export function mergeGroups(api, params, options) {
    var itemIds = params.itemIds;
    var path = getUpdateUrl(params);
    var query = paramsToQueryArgs(params);
    var id = uniqueId();
    GroupActions.merge(id, itemIds);
    return wrapRequest(api, path, {
        query: query,
        method: 'PUT',
        data: { merge: 1 },
        success: function (response) {
            GroupActions.mergeSuccess(id, itemIds, response);
        },
        error: function (error) {
            GroupActions.mergeError(id, itemIds, error);
        },
    }, options);
}
//# sourceMappingURL=group.jsx.map
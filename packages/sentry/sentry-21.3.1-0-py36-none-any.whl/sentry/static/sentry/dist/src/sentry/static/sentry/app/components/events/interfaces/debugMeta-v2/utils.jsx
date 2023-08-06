import { __read } from "tslib";
import React from 'react';
import { formatAddress, getImageRange } from 'app/components/events/interfaces/utils';
import { ImageStatus } from 'app/types/debugImage';
import { defined } from 'app/utils';
var IMAGE_ADDR_LEN = 12;
export var IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT = 400;
export function getStatusWeight(status) {
    switch (status) {
        case null:
        case undefined:
        case ImageStatus.UNUSED:
            return 0;
        case ImageStatus.FOUND:
            return 1;
        default:
            return 2;
    }
}
export function combineStatus(debugStatus, unwindStatus) {
    var debugWeight = getStatusWeight(debugStatus);
    var unwindWeight = getStatusWeight(unwindStatus);
    var combined = debugWeight >= unwindWeight ? debugStatus : unwindStatus;
    return combined || ImageStatus.UNUSED;
}
export function getFileName(path) {
    if (!path) {
        return undefined;
    }
    var directorySeparator = /^([a-z]:\\|\\\\)/i.test(path) ? '\\' : '/';
    return path.split(directorySeparator).pop();
}
export function normalizeId(id) {
    var _a;
    return (_a = id === null || id === void 0 ? void 0 : id.trim().toLowerCase().replace(/[- ]/g, '')) !== null && _a !== void 0 ? _a : '';
}
// TODO(ts): When replacing debugMeta with debugMetaV2, also replace {type: string} with the Image type defined in 'app/types/debugImage'
export function shouldSkipSection(filteredImages, images) {
    if (!!filteredImages.length) {
        return false;
    }
    var definedImages = images.filter(function (image) { return defined(image); });
    if (!definedImages.length) {
        return true;
    }
    if (definedImages.every(function (image) { return image.type === 'proguard'; })) {
        return true;
    }
    return false;
}
export function getImageAddress(image) {
    var _a = __read(getImageRange(image), 2), startAddress = _a[0], endAddress = _a[1];
    if (startAddress && endAddress) {
        return (<React.Fragment>
        <span>{formatAddress(startAddress, IMAGE_ADDR_LEN)}</span>
        {' \u2013 '}
        <span>{formatAddress(endAddress, IMAGE_ADDR_LEN)}</span>
      </React.Fragment>);
    }
    return undefined;
}
//# sourceMappingURL=utils.jsx.map
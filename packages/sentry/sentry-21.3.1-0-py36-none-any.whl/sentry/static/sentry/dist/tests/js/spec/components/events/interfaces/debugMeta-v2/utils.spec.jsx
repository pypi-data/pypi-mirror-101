import { __values } from "tslib";
import { combineStatus, getFileName, getStatusWeight, } from 'app/components/events/interfaces/debugMeta-v2/utils';
import { ImageStatus } from 'app/types/debugImage';
describe('DebugMeta  - utils', function () {
    describe('getStatusWeight function', function () {
        var data = [
            {
                parameter: ImageStatus.FOUND,
                result: 1,
            },
            {
                parameter: ImageStatus.UNUSED,
                result: 0,
            },
            {
                parameter: null,
                result: 0,
            },
            {
                parameter: ImageStatus.MISSING,
                result: 2,
            },
            {
                parameter: ImageStatus.MALFORMED,
                result: 2,
            },
            {
                parameter: ImageStatus.FETCHING_FAILED,
                result: 2,
            },
            {
                parameter: ImageStatus.TIMEOUT,
                result: 2,
            },
            {
                parameter: ImageStatus.OTHER,
                result: 2,
            },
        ];
        it('should return a number according to the passed parameter', function () {
            var e_1, _a;
            try {
                for (var data_1 = __values(data), data_1_1 = data_1.next(); !data_1_1.done; data_1_1 = data_1.next()) {
                    var _b = data_1_1.value, parameter = _b.parameter, result = _b.result;
                    var statusWeight = getStatusWeight(parameter);
                    expect(statusWeight).toEqual(result);
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (data_1_1 && !data_1_1.done && (_a = data_1.return)) _a.call(data_1);
                }
                finally { if (e_1) throw e_1.error; }
            }
        });
    });
    describe('getFileName function', function () {
        var filePaths = [
            {
                fileName: 'libsystem_kernel.dylib',
                directory: '/usr/lib/system/',
            },
            {
                fileName: 'libsentry.dylib',
                directory: '/Users/user/Coding/sentry-native/build/',
            },
        ];
        it('should return the file name of a provided filepath', function () {
            var e_2, _a;
            try {
                for (var filePaths_1 = __values(filePaths), filePaths_1_1 = filePaths_1.next(); !filePaths_1_1.done; filePaths_1_1 = filePaths_1.next()) {
                    var _b = filePaths_1_1.value, directory = _b.directory, fileName = _b.fileName;
                    var result = getFileName("" + directory + fileName);
                    expect(result).toEqual(fileName);
                }
            }
            catch (e_2_1) { e_2 = { error: e_2_1 }; }
            finally {
                try {
                    if (filePaths_1_1 && !filePaths_1_1.done && (_a = filePaths_1.return)) _a.call(filePaths_1);
                }
                finally { if (e_2) throw e_2.error; }
            }
        });
    });
    describe('combineStatus function', function () {
        var status = [
            {
                debugStatus: ImageStatus.MISSING,
                unwindStatus: ImageStatus.UNUSED,
                combinedStatus: ImageStatus.MISSING,
            },
            {
                debugStatus: ImageStatus.FOUND,
                unwindStatus: ImageStatus.MISSING,
                combinedStatus: ImageStatus.MISSING,
            },
            {
                debugStatus: ImageStatus.FOUND,
                unwindStatus: ImageStatus.UNUSED,
                combinedStatus: ImageStatus.FOUND,
            },
            {
                debugStatus: ImageStatus.FOUND,
                unwindStatus: null,
                combinedStatus: ImageStatus.FOUND,
            },
            {
                debugStatus: undefined,
                unwindStatus: undefined,
                combinedStatus: ImageStatus.UNUSED,
            },
            {
                debugStatus: undefined,
                unwindStatus: null,
                combinedStatus: ImageStatus.UNUSED,
            },
            {
                debugStatus: null,
                unwindStatus: null,
                combinedStatus: ImageStatus.UNUSED,
            },
        ];
        it('should return the status according to the passed parameters', function () {
            var e_3, _a;
            try {
                for (var status_1 = __values(status), status_1_1 = status_1.next(); !status_1_1.done; status_1_1 = status_1.next()) {
                    var _b = status_1_1.value, debugStatus = _b.debugStatus, unwindStatus = _b.unwindStatus, combinedStatus = _b.combinedStatus;
                    var result = combineStatus(debugStatus, unwindStatus);
                    expect(result).toEqual(combinedStatus);
                }
            }
            catch (e_3_1) { e_3 = { error: e_3_1 }; }
            finally {
                try {
                    if (status_1_1 && !status_1_1.done && (_a = status_1.return)) _a.call(status_1);
                }
                finally { if (e_3) throw e_3.error; }
            }
        });
    });
});
//# sourceMappingURL=utils.spec.jsx.map
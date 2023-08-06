import { __read } from "tslib";
import { t } from 'app/locale';
function handleXhrErrorResponse(error, currentRuleIndex) {
    var _a, _b, _c;
    var responseErrors = (_c = (_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.dynamicSampling) === null || _b === void 0 ? void 0 : _b.rules[currentRuleIndex]) !== null && _c !== void 0 ? _c : {};
    var _d = __read(Object.entries(responseErrors)[0], 2), type = _d[0], value = _d[1];
    if (type === 'sampleRate') {
        var message = Array.isArray(value) ? value[0] : value;
        if (message === 'Ensure this value is less than or equal to 1.') {
            return {
                type: 'sampleRate',
                message: t('Ensure this value is a floating number between 0 and 100'),
            };
        }
    }
    return {
        type: 'unknown',
        message: t('An internal error occurred while saving dynamic sampling rule'),
    };
}
export default handleXhrErrorResponse;
//# sourceMappingURL=handleXhrErrorResponse.jsx.map
import { DataCategory } from 'app/types';
import { formatBytesBase10 } from 'app/utils';
export var MILLION = Math.pow(10, 6);
export var BILLION = Math.pow(10, 9);
export var GIGABYTE = Math.pow(10, 9);
/**
 * This expects usage values/quantities for the data categories that we sell.
 *
 * Note: usageQuantity for Attachments should be in BYTES
 */
export function formatUsageWithUnits(usageQuantity, dataCategory, options) {
    if (usageQuantity === void 0) { usageQuantity = 0; }
    if (options === void 0) { options = { isAbbreviated: false, useUnitScaling: false }; }
    if (dataCategory !== DataCategory.ATTACHMENTS) {
        return options.isAbbreviated
            ? abbreviateUsageNumber(usageQuantity)
            : usageQuantity.toLocaleString();
    }
    if (options.useUnitScaling) {
        return formatBytesBase10(usageQuantity);
    }
    var usageGb = usageQuantity / GIGABYTE;
    return options.isAbbreviated
        ? abbreviateUsageNumber(usageGb) + " GB"
        : usageGb.toLocaleString(undefined, { maximumFractionDigits: 2 }) + " GB";
}
/**
 * Instead of using this function directly, use formatReservedWithUnits or
 * formatUsageWithUnits with options.isAbbreviated to true instead.
 *
 * This function display different precision for billion/million/thousand to
 * provide clarity on usage of errors/transactions/attachments to the user.
 *
 * If you are not displaying usage numbers, it might be better to use
 * `formatAbbreviatedNumber` in 'app/utils/formatters'
 */
export function abbreviateUsageNumber(n) {
    if (n >= BILLION) {
        return (n / BILLION).toLocaleString(undefined, { maximumFractionDigits: 2 }) + 'B';
    }
    if (n >= MILLION) {
        return (n / MILLION).toLocaleString(undefined, { maximumFractionDigits: 1 }) + 'M';
    }
    if (n >= 1000) {
        return (n / 1000).toFixed().toLocaleString() + 'K';
    }
    // Do not show decimals
    return n.toFixed().toLocaleString();
}
//# sourceMappingURL=utils.jsx.map
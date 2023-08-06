import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import DateTime from 'app/components/dateTime';
import Tag from 'app/components/tag';
import TimeSince, { getRelativeDate } from 'app/components/timeSince';
import { t, tct } from 'app/locale';
import { getDuration } from 'app/utils/formatters';
import getDynamicText from 'app/utils/getDynamicText';
var GroupInboxReason = {
    NEW: 0,
    UNIGNORED: 1,
    REGRESSION: 2,
    MANUAL: 3,
    REPROCESSED: 4,
};
var EVENT_ROUND_LIMIT = 1000;
function InboxReason(_a) {
    var inbox = _a.inbox, _b = _a.fontSize, fontSize = _b === void 0 ? 'sm' : _b, showDateAdded = _a.showDateAdded;
    var reason = inbox.reason, reason_details = inbox.reason_details, dateAdded = inbox.date_added;
    var relativeDateAdded = getDynamicText({
        value: dateAdded && getRelativeDate(dateAdded, 'ago', true),
        fixed: '3s ago',
    });
    var getCountText = function (count) {
        return count > EVENT_ROUND_LIMIT
            ? "More than " + Math.round(count / EVENT_ROUND_LIMIT) + "k"
            : "" + count;
    };
    function getTooltipDescription() {
        var until = reason_details.until, count = reason_details.count, window = reason_details.window, user_count = reason_details.user_count, user_window = reason_details.user_window;
        if (until) {
            // Was ignored until `until` has passed.
            //`until` format: "2021-01-20T03:59:03+00:00"
            return tct('Was ignored until [window]', {
                window: <DateTime date={until} dateOnly/>,
            });
        }
        if (count) {
            // Was ignored until `count` events occurred
            // If `window` is defined, than `count` events occurred in `window` minutes.
            // else `count` events occurred since it was ignored.
            if (window) {
                return tct('Occurred [count] time(s) in [duration]', {
                    count: getCountText(count),
                    duration: getDuration(window * 60, 0, true),
                });
            }
            return tct('Occurred [count] time(s)', {
                count: getCountText(count),
            });
        }
        if (user_count) {
            // Was ignored until `user_count` users were affected
            // If `user_window` is defined, than `user_count` users affected in `user_window` minutes.
            // else `user_count` events occurred since it was ignored.
            if (user_window) {
                return t('Affected [count] user(s) in [duration]', {
                    count: getCountText(user_count),
                    duration: getDuration(user_window * 60, 0, true),
                });
            }
            return t('Affected [count] user(s)', {
                count: getCountText(user_count),
            });
        }
        return undefined;
    }
    function getReasonDetails() {
        switch (reason) {
            case GroupInboxReason.UNIGNORED:
                return {
                    tagType: 'default',
                    reasonBadgeText: t('Unignored'),
                    tooltipText: dateAdded &&
                        t('Unignored %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                    tooltipDescription: getTooltipDescription(),
                };
            case GroupInboxReason.REGRESSION:
                return {
                    tagType: 'error',
                    reasonBadgeText: t('Regression'),
                    tooltipText: dateAdded &&
                        t('Regressed %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                    // TODO: Add tooltip description for regression move when resolver is added to reason
                    // Resolved by {full_name} {time} ago.
                };
            // TODO: Manual moves will go away, remove this then
            case GroupInboxReason.MANUAL:
                return {
                    tagType: 'highlight',
                    reasonBadgeText: t('Manual'),
                    tooltipText: dateAdded && t('Moved %(relative)s', { relative: relativeDateAdded }),
                    // TODO: IF manual moves stay then add tooltip description for manual move
                    // Moved to inbox by {full_name}.
                };
            case GroupInboxReason.REPROCESSED:
                return {
                    tagType: 'info',
                    reasonBadgeText: t('Reprocessed'),
                    tooltipText: dateAdded &&
                        t('Reprocessed %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                };
            case GroupInboxReason.NEW:
            default:
                return {
                    tagType: 'warning',
                    reasonBadgeText: t('New Issue'),
                    tooltipText: dateAdded &&
                        t('Created %(relative)s', {
                            relative: relativeDateAdded,
                        }),
                };
        }
    }
    var _c = getReasonDetails(), tooltipText = _c.tooltipText, tooltipDescription = _c.tooltipDescription, reasonBadgeText = _c.reasonBadgeText, tagType = _c.tagType;
    var tooltip = (tooltipText || tooltipDescription) && (<TooltipWrapper>
      {tooltipText && <div>{tooltipText}</div>}
      {tooltipDescription && (<TooltipDescription>{tooltipDescription}</TooltipDescription>)}
      <TooltipDescription>Mark Reviewed to remove this label</TooltipDescription>
    </TooltipWrapper>);
    return (<StyledTag type={tagType} tooltipText={tooltip} fontSize={fontSize}>
      {reasonBadgeText}
      {showDateAdded && dateAdded && (<React.Fragment>
          <Separator type={tagType !== null && tagType !== void 0 ? tagType : 'default'}>{' | '}</Separator>
          <TimeSince date={dateAdded} suffix="" extraShort disabledAbsoluteTooltip/>
        </React.Fragment>)}
    </StyledTag>);
}
export default InboxReason;
var TooltipWrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  text-align: left;\n"], ["\n  text-align: left;\n"])));
var TooltipDescription = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  color: ", ";\n"], ["\n  color: ", ";\n"])), function (p) { return p.theme.subText; });
var Separator = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  color: ", ";\n  opacity: 80%;\n"], ["\n  color: ", ";\n  opacity: 80%;\n"])), function (p) { return p.theme.tag[p.type].iconColor; });
var StyledTag = styled(Tag, {
    shouldForwardProp: function (p) { return p !== 'fontSize'; },
})(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n"], ["\n  font-size: ",
    ";\n"])), function (p) {
    return p.fontSize === 'sm' ? p.theme.fontSizeSmall : p.theme.fontSizeMedium;
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=inboxReason.jsx.map
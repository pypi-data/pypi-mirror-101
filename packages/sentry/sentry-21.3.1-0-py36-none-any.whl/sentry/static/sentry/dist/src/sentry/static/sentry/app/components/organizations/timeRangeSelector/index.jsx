import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import moment from 'moment-timezone';
import PropTypes from 'prop-types';
import DropdownMenu from 'app/components/dropdownMenu';
import HookOrDefault from 'app/components/hookOrDefault';
import HeaderItem from 'app/components/organizations/headerItem';
import MultipleSelectorSubmitRow from 'app/components/organizations/multipleSelectorSubmitRow';
import DateRange from 'app/components/organizations/timeRangeSelector/dateRange';
import SelectorItems from 'app/components/organizations/timeRangeSelector/dateRange/selectorItems';
import DateSummary from 'app/components/organizations/timeRangeSelector/dateSummary';
import { getRelativeSummary } from 'app/components/organizations/timeRangeSelector/utils';
import { DEFAULT_STATS_PERIOD } from 'app/constants';
import { IconCalendar } from 'app/icons';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import { analytics } from 'app/utils/analytics';
import { getLocalToSystem, getPeriodAgo, getUserTimezone, getUtcToSystem, parsePeriodToHours, } from 'app/utils/dates';
import getDynamicText from 'app/utils/getDynamicText';
import getRouteStringFromRoutes from 'app/utils/getRouteStringFromRoutes';
// Strips timezone from local date, creates a new moment date object with timezone
// Then returns as a Date object
var getDateWithTimezoneInUtc = function (date, utc) {
    return moment
        .tz(moment(date).local().format('YYYY-MM-DD HH:mm:ss'), utc ? 'UTC' : getUserTimezone())
        .utc()
        .toDate();
};
var getInternalDate = function (date, utc) {
    if (utc) {
        return getUtcToSystem(date);
    }
    else {
        return new Date(moment.tz(moment.utc(date), getUserTimezone()).format('YYYY/MM/DD HH:mm:ss'));
    }
};
var DateRangeHook = HookOrDefault({
    hookName: 'component:header-date-range',
    defaultComponent: DateRange,
});
var SelectorItemsHook = HookOrDefault({
    hookName: 'component:header-selector-items',
    defaultComponent: SelectorItems,
});
var defaultProps = {
    /**
     * Show absolute date selectors
     */
    showAbsolute: true,
    /**
     * Show relative date selectors
     */
    showRelative: true,
};
var TimeRangeSelector = /** @class */ (function (_super) {
    __extends(TimeRangeSelector, _super);
    function TimeRangeSelector(props) {
        var _this = _super.call(this, props) || this;
        _this.callCallback = function (callback, datetime) {
            if (typeof callback !== 'function') {
                return;
            }
            if (!datetime.start && !datetime.end) {
                callback(datetime);
                return;
            }
            // Change local date into either UTC or local time (local time defined by user preference)
            callback(__assign(__assign({}, datetime), { start: getDateWithTimezoneInUtc(datetime.start, _this.state.utc), end: getDateWithTimezoneInUtc(datetime.end, _this.state.utc) }));
        };
        _this.handleCloseMenu = function () {
            var _a = _this.state, relative = _a.relative, start = _a.start, end = _a.end, utc = _a.utc;
            if (_this.state.hasChanges) {
                // Only call update if we close when absolute date is selected
                _this.handleUpdate({ relative: relative, start: start, end: end, utc: utc });
            }
            else {
                _this.setState({ isOpen: false });
            }
        };
        _this.handleUpdate = function (datetime) {
            var onUpdate = _this.props.onUpdate;
            _this.setState({
                isOpen: false,
                hasChanges: false,
            }, function () {
                _this.callCallback(onUpdate, datetime);
            });
        };
        _this.handleAbsoluteClick = function () {
            var _a = _this.props, relative = _a.relative, onChange = _a.onChange;
            // Set default range to equivalent of last relative period,
            // or use default stats period
            var newDateTime = {
                relative: null,
                start: getPeriodAgo('hours', parsePeriodToHours(relative || DEFAULT_STATS_PERIOD)).toDate(),
                end: new Date(),
            };
            if (defined(_this.props.utc)) {
                newDateTime.utc = _this.state.utc;
            }
            _this.setState(__assign(__assign({ hasChanges: true }, newDateTime), { start: newDateTime.start, end: newDateTime.end }));
            _this.callCallback(onChange, newDateTime);
        };
        _this.handleSelectRelative = function (value) {
            var onChange = _this.props.onChange;
            var newDateTime = {
                relative: value,
                start: undefined,
                end: undefined,
            };
            _this.setState(newDateTime);
            _this.callCallback(onChange, newDateTime);
            _this.handleUpdate(newDateTime);
        };
        _this.handleClear = function () {
            var onChange = _this.props.onChange;
            var newDateTime = {
                relative: DEFAULT_STATS_PERIOD,
                start: undefined,
                end: undefined,
                utc: null,
            };
            _this.setState(newDateTime);
            _this.callCallback(onChange, newDateTime);
            _this.handleUpdate(newDateTime);
        };
        _this.handleSelectDateRange = function (_a) {
            var start = _a.start, end = _a.end, _b = _a.hasDateRangeErrors, hasDateRangeErrors = _b === void 0 ? false : _b;
            if (hasDateRangeErrors) {
                _this.setState({ hasDateRangeErrors: hasDateRangeErrors });
                return;
            }
            var onChange = _this.props.onChange;
            var newDateTime = {
                relative: null,
                start: start,
                end: end,
            };
            if (defined(_this.props.utc)) {
                newDateTime.utc = _this.state.utc;
            }
            _this.setState(__assign({ hasChanges: true, hasDateRangeErrors: hasDateRangeErrors }, newDateTime));
            _this.callCallback(onChange, newDateTime);
        };
        _this.handleUseUtc = function () {
            var onChange = _this.props.onChange;
            var _a = _this.props, start = _a.start, end = _a.end;
            _this.setState(function (state) {
                var utc = !state.utc;
                if (!start) {
                    start = getDateWithTimezoneInUtc(state.start, state.utc);
                }
                if (!end) {
                    end = getDateWithTimezoneInUtc(state.end, state.utc);
                }
                analytics('dateselector.utc_changed', {
                    utc: utc,
                    path: getRouteStringFromRoutes(_this.context.router.routes),
                    org_id: parseInt(_this.props.organization.id, 10),
                });
                var newDateTime = {
                    relative: null,
                    start: utc ? getLocalToSystem(start) : getUtcToSystem(start),
                    end: utc ? getLocalToSystem(end) : getUtcToSystem(end),
                    utc: utc,
                };
                _this.callCallback(onChange, newDateTime);
                return __assign({ hasChanges: true }, newDateTime);
            });
        };
        _this.handleOpen = function () {
            _this.setState({ isOpen: true });
            // Start loading react-date-picker
            import(
            /* webpackChunkName: "DateRangePicker" */ '../timeRangeSelector/dateRange/index');
        };
        var start = undefined;
        var end = undefined;
        if (props.start && props.end) {
            start = getInternalDate(props.start, props.utc);
            end = getInternalDate(props.end, props.utc);
        }
        _this.state = {
            // if utc is not null and not undefined, then use value of `props.utc` (it can be false)
            // otherwise if no value is supplied, the default should be the user's timezone preference
            utc: defined(props.utc) ? props.utc : getUserTimezone() === 'UTC',
            isOpen: false,
            hasChanges: false,
            hasDateRangeErrors: false,
            start: start,
            end: end,
            relative: props.relative,
        };
        return _this;
    }
    TimeRangeSelector.prototype.render = function () {
        var _this = this;
        var _a = this.props, defaultPeriod = _a.defaultPeriod, showAbsolute = _a.showAbsolute, showRelative = _a.showRelative, organization = _a.organization, hint = _a.hint;
        var _b = this.state, start = _b.start, end = _b.end, relative = _b.relative;
        var shouldShowAbsolute = showAbsolute;
        var shouldShowRelative = showRelative;
        var isAbsoluteSelected = !!start && !!end;
        var summary = isAbsoluteSelected && start && end ? (<DateSummary start={start} end={end}/>) : (getRelativeSummary(relative || defaultPeriod));
        var relativeSelected = isAbsoluteSelected ? '' : relative || defaultPeriod;
        return (<DropdownMenu isOpen={this.state.isOpen} onOpen={this.handleOpen} onClose={this.handleCloseMenu} keepMenuOpen>
        {function (_a) {
                var isOpen = _a.isOpen, getRootProps = _a.getRootProps, getActorProps = _a.getActorProps, getMenuProps = _a.getMenuProps;
                return (<TimeRangeRoot {...getRootProps()}>
            <StyledHeaderItem data-test-id="global-header-timerange-selector" icon={<IconCalendar />} isOpen={isOpen} hasSelected={(!!_this.props.relative && _this.props.relative !== defaultPeriod) ||
                        isAbsoluteSelected} hasChanges={_this.state.hasChanges} onClear={_this.handleClear} allowClear hint={hint} {...getActorProps()}>
              {getDynamicText({ value: summary, fixed: 'start to end' })}
            </StyledHeaderItem>

            {isOpen && (<Menu {...getMenuProps()} isAbsoluteSelected={isAbsoluteSelected}>
                <SelectorList isAbsoluteSelected={isAbsoluteSelected}>
                  <SelectorItemsHook isAbsoluteSelected={isAbsoluteSelected} relativeSelected={relativeSelected} shouldShowRelative={shouldShowRelative} shouldShowAbsolute={shouldShowAbsolute} handleAbsoluteClick={_this.handleAbsoluteClick} handleSelectRelative={_this.handleSelectRelative}/>
                </SelectorList>
                {isAbsoluteSelected && (<div>
                    <DateRangeHook start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} organization={organization} showTimePicker utc={_this.state.utc} onChange={_this.handleSelectDateRange} onChangeUtc={_this.handleUseUtc}/>
                    <SubmitRow>
                      <MultipleSelectorSubmitRow onSubmit={_this.handleCloseMenu} disabled={!_this.state.hasChanges || _this.state.hasDateRangeErrors}/>
                    </SubmitRow>
                  </div>)}
              </Menu>)}
          </TimeRangeRoot>);
            }}
      </DropdownMenu>);
    };
    TimeRangeSelector.contextTypes = {
        router: PropTypes.object,
    };
    TimeRangeSelector.defaultProps = defaultProps;
    return TimeRangeSelector;
}(React.PureComponent));
var TimeRangeRoot = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledHeaderItem = styled(HeaderItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  height: 100%;\n"], ["\n  height: 100%;\n"])));
var Menu = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  ", ";\n  ", ";\n\n  display: flex;\n  background: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: 100%;\n  min-width: 100%;\n  z-index: ", ";\n  box-shadow: ", ";\n  border-radius: ", ";\n  font-size: 0.8em;\n  overflow: hidden;\n"], ["\n  ", ";\n  ", ";\n\n  display: flex;\n  background: ", ";\n  border: 1px solid ", ";\n  position: absolute;\n  top: 100%;\n  min-width: 100%;\n  z-index: ", ";\n  box-shadow: ", ";\n  border-radius: ", ";\n  font-size: 0.8em;\n  overflow: hidden;\n"])), function (p) { return !p.isAbsoluteSelected && 'left: -1px'; }, function (p) { return p.isAbsoluteSelected && 'right: -1px'; }, function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.zIndex.dropdown; }, function (p) { return p.theme.dropShadowLight; }, function (p) { return p.theme.borderRadiusBottom; });
var SelectorList = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  flex-shrink: 0;\n  width: ", ";\n  min-height: 305px;\n"], ["\n  display: flex;\n  flex: 1;\n  flex-direction: column;\n  flex-shrink: 0;\n  width: ", ";\n  min-height: 305px;\n"])), function (p) { return (p.isAbsoluteSelected ? '160px' : '220px'); });
var SubmitRow = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding: ", " ", ";\n  border-top: 1px solid ", ";\n  border-left: 1px solid ", ";\n"], ["\n  padding: ", " ", ";\n  border-top: 1px solid ", ";\n  border-left: 1px solid ", ";\n"])), space(0.5), space(1), function (p) { return p.theme.innerBorder; }, function (p) { return p.theme.border; });
export default TimeRangeSelector;
export { TimeRangeRoot };
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map
import { __assign, __rest } from "tslib";
import React from 'react';
import ReactSelect, { components as selectComponents, mergeStyles, } from 'react-select';
import Async from 'react-select/async';
import AsyncCreatable from 'react-select/async-creatable';
import Creatable from 'react-select/creatable';
import { withTheme } from 'emotion-theming';
import { IconChevron, IconClose } from 'app/icons';
import space from 'app/styles/space';
import convertFromSelect2Choices from 'app/utils/convertFromSelect2Choices';
import SelectControlLegacy from './selectControlLegacy';
function isGroupedOptions(maybe) {
    if (!maybe || maybe.length === 0) {
        return false;
    }
    return maybe[0].options !== undefined;
}
var ClearIndicator = function (props) { return (<selectComponents.ClearIndicator {...props}>
    <IconClose size="10px"/>
  </selectComponents.ClearIndicator>); };
var DropdownIndicator = function (props) { return (<selectComponents.DropdownIndicator {...props}>
    <IconChevron direction="down" size="14px"/>
  </selectComponents.DropdownIndicator>); };
var MultiValueRemove = function (props) { return (<selectComponents.MultiValueRemove {...props}>
    <IconClose size="8px"/>
  </selectComponents.MultiValueRemove>); };
function SelectControl(props) {
    // TODO(epurkhiser): We should remove all SelectControls (and SelectFields,
    // SelectAsyncFields, etc) that are using this prop, before we can remove the
    // v1 react-select component.
    if (props.deprecatedSelectControl) {
        var _1 = props.deprecatedSelectControl, legacyProps = __rest(props, ["deprecatedSelectControl"]);
        return <SelectControlLegacy {...legacyProps}/>;
    }
    var theme = props.theme;
    // TODO(epurkhiser): The loading indicator should probably also be our loading
    // indicator.
    // Unfortunately we cannot use emotions `css` helper here, since react-select
    // *requires* object styles, which the css helper cannot produce.
    var indicatorStyles = function (_a) {
        var _padding = _a.padding, provided = __rest(_a, ["padding"]);
        return (__assign(__assign({}, provided), { padding: '4px', alignItems: 'center', cursor: 'pointer', color: theme.subText }));
    };
    var defaultStyles = {
        control: function (_, state) { return (__assign(__assign(__assign(__assign(__assign(__assign({ height: '100%', fontSize: theme.fontSizeLarge, lineHeight: theme.text.lineHeightBody, display: 'flex' }, {
            color: theme.formText,
            background: theme.background,
            border: "1px solid " + theme.border,
            boxShadow: "inset " + theme.dropShadowLight,
        }), { borderRadius: theme.borderRadius, transition: 'border 0.1s linear', alignItems: 'center', minHeight: '40px', '&:hover': {
                borderColor: theme.border,
            } }), (state.isFocused && {
            border: "1px solid " + theme.border,
            boxShadow: 'rgba(209, 202, 216, 0.5) 0 0 0 3px',
        })), (state.menuIsOpen && {
            borderBottomLeftRadius: '0',
            borderBottomRightRadius: '0',
            boxShadow: 'none',
        })), (state.isDisabled && {
            borderColor: theme.border,
            background: theme.backgroundSecondary,
            color: theme.disabled,
            cursor: 'not-allowed',
        })), (!state.isSearchable && {
            cursor: 'pointer',
        }))); },
        menu: function (provided) { return (__assign(__assign({}, provided), { zIndex: theme.zIndex.dropdown, marginTop: '-1px', background: theme.background, border: "1px solid " + theme.border, borderRadius: "0 0 " + theme.borderRadius + " " + theme.borderRadius, borderTop: "1px solid " + theme.border, boxShadow: theme.dropShadowLight })); },
        option: function (provided, state) { return (__assign(__assign({}, provided), { lineHeight: '1.5', fontSize: theme.fontSizeMedium, cursor: 'pointer', color: state.isFocused
                ? theme.textColor
                : state.isSelected
                    ? theme.background
                    : theme.textColor, backgroundColor: state.isFocused
                ? theme.focus
                : state.isSelected
                    ? theme.active
                    : 'transparent', '&:active': {
                backgroundColor: theme.active,
            } })); },
        valueContainer: function (provided) { return (__assign(__assign({}, provided), { alignItems: 'center' })); },
        input: function (provided) { return (__assign(__assign({}, provided), { color: theme.formText })); },
        singleValue: function (provided) { return (__assign(__assign({}, provided), { color: theme.formText })); },
        placeholder: function (provided) { return (__assign(__assign({}, provided), { color: theme.formPlaceholder })); },
        multiValue: function (provided) { return (__assign(__assign({}, provided), { color: '#007eff', backgroundColor: '#ebf5ff', borderRadius: '2px', border: '1px solid #c2e0ff', display: 'flex' })); },
        multiValueLabel: function (provided) { return (__assign(__assign({}, provided), { color: '#007eff', padding: '0', paddingLeft: '6px', lineHeight: '1.8' })); },
        multiValueRemove: function () { return ({
            cursor: 'pointer',
            alignItems: 'center',
            borderLeft: '1px solid #c2e0ff',
            borderRadius: '0 2px 2px 0',
            display: 'flex',
            padding: '0 4px',
            marginLeft: '4px',
            '&:hover': {
                color: '#6284b9',
                background: '#cce5ff',
            },
        }); },
        indicatorsContainer: function () { return ({
            display: 'grid',
            gridAutoFlow: 'column',
            gridGap: '2px',
            marginRight: '6px',
        }); },
        clearIndicator: indicatorStyles,
        dropdownIndicator: indicatorStyles,
        loadingIndicator: indicatorStyles,
        groupHeading: function (provided) { return (__assign(__assign({}, provided), { lineHeight: '1.5', fontWeight: 600, backgroundColor: theme.backgroundSecondary, color: theme.textColor, marginBottom: 0, padding: space(1) + " " + space(1.5) })); },
        group: function (provided) { return (__assign(__assign({}, provided), { padding: 0 })); },
    };
    var getFieldLabelStyle = function (label) { return ({
        ':before': {
            content: "\"" + label + "\"",
            color: theme.gray300,
            fontWeight: 600,
        },
    }); };
    var async = props.async, creatable = props.creatable, options = props.options, choices = props.choices, clearable = props.clearable, components = props.components, styles = props.styles, value = props.value, inFieldLabel = props.inFieldLabel, rest = __rest(props, ["async", "creatable", "options", "choices", "clearable", "components", "styles", "value", "inFieldLabel"]);
    // Compatibility with old select2 API
    var choicesOrOptions = convertFromSelect2Choices(typeof choices === 'function' ? choices(props) : choices) ||
        options;
    // It's possible that `choicesOrOptions` does not exist (e.g. in the case of AsyncSelect)
    var mappedValue = value;
    if (choicesOrOptions) {
        /**
         * Value is expected to be object like the options list, we map it back from the options list.
         * Note that if the component doesn't have options or choices passed in
         * because the select component fetches the options finding the mappedValue will fail
         * and the component won't work
         */
        var flatOptions_1 = [];
        if (isGroupedOptions(choicesOrOptions)) {
            flatOptions_1 = choicesOrOptions.flatMap(function (option) { return option.options; });
        }
        else {
            // @ts-ignore The types used in react-select generics (OptionType) don't
            // line up well with our option type (SelectValue). We need to do more work
            // to get these types to align.
            flatOptions_1 = choicesOrOptions.flatMap(function (option) { return option; });
        }
        mappedValue =
            props.multiple && Array.isArray(value)
                ? value.map(function (val) { return flatOptions_1.find(function (option) { return option.value === val; }); })
                : flatOptions_1.find(function (opt) { return opt.value === value; }) || value;
    }
    // Override the default style with in-field labels if they are provided
    var inFieldLabelStyles = {
        singleValue: function (base) { return (__assign(__assign({}, base), getFieldLabelStyle(inFieldLabel))); },
        placeholder: function (base) { return (__assign(__assign({}, base), getFieldLabelStyle(inFieldLabel))); },
    };
    var labelOrDefaultStyles = inFieldLabel
        ? mergeStyles(defaultStyles, inFieldLabelStyles)
        : defaultStyles;
    // Allow the provided `styles` prop to override default styles using the same
    // function interface provided by react-styled. This ensures the `provided`
    // styles include our overridden default styles
    var mappedStyles = styles
        ? mergeStyles(labelOrDefaultStyles, styles)
        : labelOrDefaultStyles;
    var replacedComponents = {
        ClearIndicator: ClearIndicator,
        DropdownIndicator: DropdownIndicator,
        MultiValueRemove: MultiValueRemove,
        IndicatorSeparator: null,
    };
    return (<SelectPicker styles={mappedStyles} components={__assign(__assign({}, replacedComponents), components)} async={async} creatable={creatable} isClearable={clearable} backspaceRemovesValue={clearable} value={mappedValue} isMulti={props.multiple || props.multi} isDisabled={props.isDisabled || props.disabled} options={options || choicesOrOptions} openMenuOnFocus={props.openMenuOnFocus === undefined ? true : props.openMenuOnFocus} {...rest}/>);
}
SelectControl.propTypes = SelectControlLegacy.propTypes;
var SelectControlWithTheme = withTheme(SelectControl);
function SelectPicker(_a) {
    var async = _a.async, creatable = _a.creatable, forwardedRef = _a.forwardedRef, props = __rest(_a, ["async", "creatable", "forwardedRef"]);
    // Pick the right component to use
    // Using any here as react-select types also use any
    var Component;
    if (async && creatable) {
        Component = AsyncCreatable;
    }
    else if (async && !creatable) {
        Component = Async;
    }
    else if (creatable) {
        Component = Creatable;
    }
    else {
        Component = ReactSelect;
    }
    return <Component ref={forwardedRef} {...props}/>;
}
SelectPicker.propTypes = SelectControl.propTypes;
// The generics need to be filled here as forwardRef can't expose generics.
var RefForwardedSelectControl = React.forwardRef(function RefForwardedSelectControl(props, ref) {
    return <SelectControlWithTheme forwardedRef={ref} {...props}/>;
});
// TODO(ts): Needed because <SelectField> uses this
RefForwardedSelectControl.propTypes = SelectControl.propTypes;
export default RefForwardedSelectControl;
//# sourceMappingURL=selectControl.jsx.map
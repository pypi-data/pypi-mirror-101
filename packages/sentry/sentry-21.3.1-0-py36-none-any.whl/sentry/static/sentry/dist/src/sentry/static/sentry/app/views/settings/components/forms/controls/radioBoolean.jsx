import React from 'react';
var Option = React.forwardRef(function Option(_a, ref) {
    var name = _a.name, disabled = _a.disabled, label = _a.label, value = _a.value, checked = _a.checked, onChange = _a.onChange;
    function handleChange(e) {
        var isTrue = e.target.value === 'true';
        onChange === null || onChange === void 0 ? void 0 : onChange(isTrue, e);
    }
    return (<div className="radio">
      <label style={{ fontWeight: 'normal' }}>
        <input ref={ref} type="radio" value={value} name={name} checked={checked} onChange={handleChange} disabled={disabled}/>{' '}
        {label}
      </label>
    </div>);
});
var RadioBoolean = React.forwardRef(function RadioBoolean(_a, ref) {
    var disabled = _a.disabled, name = _a.name, onChange = _a.onChange, value = _a.value, _b = _a.yesFirst, yesFirst = _b === void 0 ? true : _b, _c = _a.yesLabel, yesLabel = _c === void 0 ? 'Yes' : _c, _d = _a.noLabel, noLabel = _d === void 0 ? 'No' : _d;
    var yesOption = (<Option ref={ref} value="true" checked={value === true} name={name} disabled={disabled} label={yesLabel} onChange={onChange}/>);
    var noOption = (<Option value="false" checked={value === false} name={name} disabled={disabled} label={noLabel} onChange={onChange}/>);
    return (<div>
      {yesFirst ? yesOption : noOption}
      {yesFirst ? noOption : yesOption}
    </div>);
});
export default RadioBoolean;
//# sourceMappingURL=radioBoolean.jsx.map
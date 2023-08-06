import { __makeTemplateObject, __read } from "tslib";
import React, { useCallback, useEffect, useRef, useState } from 'react';
import styled from '@emotion/styled';
import TextOverflow from 'app/components/textOverflow';
import { IconEdit } from 'app/icons/iconEdit';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import useKeypress from 'app/utils/useKeyPress';
import useOnClickOutside from 'app/utils/useOnClickOutside';
import Input from 'app/views/settings/components/forms/controls/input';
import Field from 'app/views/settings/components/forms/field';
function EditableText(_a) {
    var value = _a.value, onChange = _a.onChange;
    var _b = __read(useState(false), 2), isEditing = _b[0], setIsEditing = _b[1];
    var _c = __read(useState(value), 2), inputValue = _c[0], setInputValue = _c[1];
    var isEmpty = !inputValue.trim();
    var wrapperRef = useRef(null);
    var contentRef = useRef(null);
    var inputRef = useRef(null);
    var enter = useKeypress('Enter');
    var esc = useKeypress('Escape');
    // check to see if the user clicked outside of this component
    useOnClickOutside(wrapperRef, function () {
        if (isEditing && !isEmpty) {
            onChange(inputValue);
            setIsEditing(false);
        }
    });
    var onEnter = useCallback(function () {
        if (enter && !isEmpty) {
            onChange(inputValue);
            setIsEditing(false);
        }
    }, [enter, inputValue, onChange]);
    var onEsc = useCallback(function () {
        if (esc) {
            setInputValue(value);
            setIsEditing(false);
        }
    }, [esc, value]);
    // focus the cursor in the input field on edit start
    useEffect(function () {
        if (isEditing) {
            var inputElement = inputRef.current;
            if (defined(inputElement)) {
                inputElement.focus();
            }
        }
    }, [isEditing]);
    useEffect(function () {
        if (isEditing) {
            // if Enter is pressed, save the text and close the editor
            onEnter();
            // if Escape is pressed, revert the text and close the editor
            onEsc();
        }
    }, [onEnter, onEsc, isEditing]); // watch the Enter and Escape key presses
    function handleInputChange(event) {
        setInputValue(event.target.value);
    }
    function handleContentClick() {
        setIsEditing(true);
    }
    return (<Wrapper ref={wrapperRef}>
      {isEditing ? (<InputWrapper isEmpty={isEmpty}>
          <StyledField error={isEmpty ? t('Text required') : undefined} inline={false} flexibleControlStateSize stacked required>
            <StyledInput ref={inputRef} value={inputValue} onChange={handleInputChange}/>
          </StyledField>
          <InputLabel>{inputValue}</InputLabel>
        </InputWrapper>) : (<Content onClick={handleContentClick} ref={contentRef}>
          <Label>
            <InnerLabel>{inputValue}</InnerLabel>
          </Label>
          <StyledIconEdit />
        </Content>)}
    </Wrapper>);
}
export default EditableText;
var Content = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  height: 40px;\n  position: relative;\n  max-width: calc(100% - 22px);\n  padding-right: 22px;\n"], ["\n  height: 40px;\n  position: relative;\n  max-width: calc(100% - 22px);\n  padding-right: 22px;\n"])));
var Label = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: inline-block;\n  border: 1px solid transparent;\n  border-radius: ", ";\n  transition: border 150ms;\n  text-align: left;\n  padding: 0 10px;\n  height: 40px;\n  max-width: 100%;\n"], ["\n  display: inline-block;\n  border: 1px solid transparent;\n  border-radius: ", ";\n  transition: border 150ms;\n  text-align: left;\n  padding: 0 10px;\n  height: 40px;\n  max-width: 100%;\n"])), function (p) { return p.theme.borderRadius; });
var InnerLabel = styled(TextOverflow)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  border-bottom: 1px dotted ", ";\n  transition: border 150ms;\n  height: 39px;\n  line-height: 39px;\n"], ["\n  border-bottom: 1px dotted ", ";\n  transition: border 150ms;\n  height: 39px;\n  line-height: 39px;\n"])), function (p) { return p.theme.gray200; });
var StyledIconEdit = styled(IconEdit)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  opacity: 0;\n  transition: opacity 150ms;\n  margin-left: ", ";\n  height: 40px;\n  position: absolute;\n  right: 0;\n"], ["\n  opacity: 0;\n  transition: opacity 150ms;\n  margin-left: ", ";\n  height: 40px;\n  position: absolute;\n  right: 0;\n"])), space(0.75));
var Wrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-start;\n  height: 40px;\n  :hover {\n    ", " {\n      opacity: 1;\n    }\n    ", " {\n      border-color: ", ";\n    }\n    ", " {\n      border-bottom-color: transparent;\n    }\n  }\n"], ["\n  display: flex;\n  justify-content: flex-start;\n  height: 40px;\n  :hover {\n    ", " {\n      opacity: 1;\n    }\n    ", " {\n      border-color: ", ";\n    }\n    ", " {\n      border-bottom-color: transparent;\n    }\n  }\n"])), StyledIconEdit, Label, function (p) { return p.theme.gray300; }, InnerLabel);
var InputWrapper = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  position: relative;\n  max-width: 100%;\n  min-width: ", ";\n"], ["\n  position: relative;\n  max-width: 100%;\n  min-width: ", ";\n"])), function (p) { return (p.isEmpty ? '100px' : '50px'); });
var StyledField = styled(Field)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  width: 100%;\n  padding: 0;\n  position: absolute;\n  right: 0;\n"], ["\n  width: 100%;\n  padding: 0;\n  position: absolute;\n  right: 0;\n"])));
var StyledInput = styled(Input)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    box-shadow: none;\n  }\n"], ["\n  &,\n  &:focus,\n  &:active,\n  &:hover {\n    box-shadow: none;\n  }\n"])));
var InputLabel = styled('div')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  width: auto;\n  opacity: 0;\n  padding: ", ";\n  height: 40px;\n  position: relative;\n  z-index: -1;\n"], ["\n  width: auto;\n  opacity: 0;\n  padding: ", ";\n  height: 40px;\n  position: relative;\n  z-index: -1;\n"])), space(1.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=editableText.jsx.map
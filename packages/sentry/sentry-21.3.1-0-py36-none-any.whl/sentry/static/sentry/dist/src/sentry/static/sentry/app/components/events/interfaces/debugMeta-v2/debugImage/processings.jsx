import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import space from 'app/styles/space';
import ProcessingItem from '../processing/item';
import ProcessingList from '../processing/list';
import ProcessingIcon from './processingIcon';
function Processings(_a) {
    var unwind_status = _a.unwind_status, debug_status = _a.debug_status;
    var items = [];
    if (debug_status) {
        items.push(<StyledProcessingItem key="symbolication" type="symbolication" icon={<ProcessingIcon status={debug_status}/>}/>);
    }
    if (unwind_status) {
        items.push(<StyledProcessingItem key="stack_unwinding" type="stack_unwinding" icon={<ProcessingIcon status={unwind_status}/>}/>);
    }
    return <StyledProcessingList items={items}/>;
}
export default Processings;
var StyledProcessingList = styled(ProcessingList)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-wrap: wrap;\n  margin-bottom: -", ";\n"], ["\n  display: flex;\n  flex-wrap: wrap;\n  margin-bottom: -", ";\n"])), space(1));
var StyledProcessingItem = styled(ProcessingItem)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  :not(:last-child) {\n    padding-right: ", ";\n  }\n  padding-bottom: ", ";\n"], ["\n  :not(:last-child) {\n    padding-right: ", ";\n  }\n  padding-bottom: ", ";\n"])), space(2), space(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=processings.jsx.map
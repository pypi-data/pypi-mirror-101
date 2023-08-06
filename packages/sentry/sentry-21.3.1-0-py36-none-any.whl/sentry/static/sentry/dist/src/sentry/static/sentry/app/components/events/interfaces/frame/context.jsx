import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ClippedBox from 'app/components/clippedBox';
import ErrorBoundary from 'app/components/errorBoundary';
import { Assembly } from 'app/components/events/interfaces/assembly';
import ContextLine from 'app/components/events/interfaces/contextLine';
import FrameRegisters from 'app/components/events/interfaces/frameRegisters';
import FrameVariables from 'app/components/events/interfaces/frameVariables';
import { OpenInContextLine } from 'app/components/events/interfaces/openInContextLine';
import StacktraceLink from 'app/components/events/interfaces/stacktraceLink';
import { parseAssembly } from 'app/components/events/interfaces/utils';
import { IconFlag } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { defined } from 'app/utils';
import withOrganization from 'app/utils/withOrganization';
var Context = function (_a) {
    var _b, _c;
    var _d = _a.hasContextVars, hasContextVars = _d === void 0 ? false : _d, _e = _a.hasContextSource, hasContextSource = _e === void 0 ? false : _e, _f = _a.hasContextRegisters, hasContextRegisters = _f === void 0 ? false : _f, _g = _a.isExpanded, isExpanded = _g === void 0 ? false : _g, _h = _a.hasAssembly, hasAssembly = _h === void 0 ? false : _h, _j = _a.expandable, expandable = _j === void 0 ? false : _j, _k = _a.emptySourceNotation, emptySourceNotation = _k === void 0 ? false : _k, _l = _a.isHoverPreviewed, isHoverPreviewed = _l === void 0 ? false : _l, registers = _a.registers, components = _a.components, frame = _a.frame, event = _a.event, organization = _a.organization;
    if (!hasContextSource && !hasContextVars && !hasContextRegisters && !hasAssembly) {
        return emptySourceNotation ? (<div className="empty-context">
        <StyledIconFlag size="xs"/>
        <p>{t('No additional details are available for this frame.')}</p>
      </div>) : null;
    }
    var getContextLines = function () {
        if (isExpanded) {
            return frame.context;
        }
        return frame.context.filter(function (l) { return l[0] === frame.lineNo; });
    };
    var contextLines = getContextLines();
    var startLineNo = hasContextSource ? frame.context[0][0] : undefined;
    return (<ol start={startLineNo} className={"context " + (isExpanded ? 'expanded' : '')}>
      {defined(frame.errors) && (<li className={expandable ? 'expandable error' : 'error'} key="errors">
          {frame.errors.join(', ')}
        </li>)}

      {frame.context &&
            contextLines.map(function (line, index) {
                var isActive = frame.lineNo === line[0];
                var hasComponents = isActive && components.length > 0;
                return (<StyledContextLine key={index} line={line} isActive={isActive}>
              {!isHoverPreviewed && hasComponents && (<ErrorBoundary mini>
                  <OpenInContextLine key={index} lineNo={line[0]} filename={frame.filename || ''} components={components}/>
                </ErrorBoundary>)}
              {(organization === null || organization === void 0 ? void 0 : organization.features.includes('integrations-stacktrace-link')) &&
                        !isHoverPreviewed &&
                        isActive &&
                        isExpanded &&
                        frame.filename && (<ErrorBoundary customComponent={null}>
                    <StacktraceLink key={index} lineNo={line[0]} frame={frame} event={event}/>
                  </ErrorBoundary>)}
            </StyledContextLine>);
            })}

      {(hasContextRegisters || hasContextVars) && (<StyledClippedBox clipHeight={100}>
          {hasContextRegisters && (<FrameRegisters registers={registers} deviceArch={(_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.device) === null || _c === void 0 ? void 0 : _c.arch}/>)}
          {hasContextVars && <FrameVariables data={frame.vars || {}}/>}
        </StyledClippedBox>)}

      {hasAssembly && (<Assembly {...parseAssembly(frame.package)} filePath={frame.absPath}/>)}
    </ol>);
};
export default withOrganization(Context);
var StyledClippedBox = styled(ClippedBox)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-left: 0;\n  margin-right: 0;\n\n  &:first-of-type {\n    margin-top: 0;\n  }\n\n  :first-child {\n    margin-top: -", ";\n  }\n\n  > *:first-child {\n    padding-top: 0;\n    border-top: none;\n  }\n"], ["\n  margin-left: 0;\n  margin-right: 0;\n\n  &:first-of-type {\n    margin-top: 0;\n  }\n\n  :first-child {\n    margin-top: -", ";\n  }\n\n  > *:first-child {\n    padding-top: 0;\n    border-top: none;\n  }\n"])), space(3));
var StyledIconFlag = styled(IconFlag)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space(1));
var StyledContextLine = styled(ContextLine)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  background: inherit;\n  padding: 0;\n  text-indent: 20px;\n  z-index: 1000;\n"], ["\n  background: inherit;\n  padding: 0;\n  text-indent: 20px;\n  z-index: 1000;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=context.jsx.map
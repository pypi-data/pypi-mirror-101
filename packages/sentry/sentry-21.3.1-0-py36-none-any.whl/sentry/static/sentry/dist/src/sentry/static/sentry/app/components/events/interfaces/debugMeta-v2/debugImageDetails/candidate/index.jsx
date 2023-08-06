import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { INTERNAL_SOURCE } from '../utils';
import StatusTooltip from './status/statusTooltip';
import Actions from './actions';
import Information from './information';
function Candidate(_a) {
    var candidate = _a.candidate, builtinSymbolSources = _a.builtinSymbolSources, organization = _a.organization, projectId = _a.projectId, baseUrl = _a.baseUrl, haveCandidatesAtLeastOneAction = _a.haveCandidatesAtLeastOneAction, hasReprocessWarning = _a.hasReprocessWarning, onDelete = _a.onDelete, eventDateReceived = _a.eventDateReceived;
    var source = candidate.source;
    var isInternalSource = source === INTERNAL_SOURCE;
    return (<React.Fragment>
      <Column>
        <StatusTooltip candidate={candidate} hasReprocessWarning={hasReprocessWarning}/>
      </Column>

      <InformationColumn>
        <Information candidate={candidate} builtinSymbolSources={builtinSymbolSources} isInternalSource={isInternalSource} eventDateReceived={eventDateReceived} hasReprocessWarning={hasReprocessWarning}/>
      </InformationColumn>

      {haveCandidatesAtLeastOneAction && (<ActionsColumn>
          <Actions onDelete={onDelete} baseUrl={baseUrl} projectId={projectId} organization={organization} candidate={candidate} isInternalSource={isInternalSource}/>
        </ActionsColumn>)}
    </React.Fragment>);
}
export default Candidate;
var Column = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var InformationColumn = styled(Column)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  flex-direction: column;\n  align-items: flex-start;\n"], ["\n  flex-direction: column;\n  align-items: flex-start;\n"])));
var ActionsColumn = styled(Column)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map
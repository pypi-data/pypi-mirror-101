import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import capitalize from 'lodash/capitalize';
import moment from 'moment-timezone';
import DateTime from 'app/components/dateTime';
import FileSize from 'app/components/fileSize';
import TimeSince from 'app/components/timeSince';
import Tooltip from 'app/components/tooltip';
import { IconWarning } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { CandidateDownloadStatus, SymbolType, } from 'app/types/debugImage';
import ProcessingItem from '../../../processing/item';
import ProcessingList from '../../../processing/list';
import { INTERNAL_SOURCE } from '../../utils';
import Divider from './divider';
import Features from './features';
import ProcessingIcon from './processingIcon';
function Information(_a) {
    var candidate = _a.candidate, isInternalSource = _a.isInternalSource, hasReprocessWarning = _a.hasReprocessWarning, eventDateReceived = _a.eventDateReceived;
    var source_name = candidate.source_name, source = candidate.source, location = candidate.location, download = candidate.download;
    function getFilenameOrLocation() {
        if (candidate.download.status === CandidateDownloadStatus.UNAPPLIED ||
            (candidate.download.status === CandidateDownloadStatus.OK && isInternalSource)) {
            var _a = candidate, symbolType = _a.symbolType, filename = _a.filename;
            return symbolType === SymbolType.PROGUARD && filename === 'proguard-mapping'
                ? null
                : filename;
        }
        if (location && !isInternalSource) {
            return location;
        }
        return null;
    }
    function getTimeSinceTooltipDescription(dateCreated) {
        var dateTime = <DateTime date={dateCreated}/>;
        if (candidate.download.status === CandidateDownloadStatus.OK) {
            return dateTime;
        }
        var uploadedBeforeEvent = moment(dateCreated).isBefore(eventDateReceived);
        if (uploadedBeforeEvent) {
            if (hasReprocessWarning) {
                return (<React.Fragment>
            {tct('This debug file was uploaded [when] before this event. It takes up to 1 hour for new files to propagate. To apply new debug information, reprocess this issue.', {
                        when: moment(eventDateReceived).from(dateCreated, true),
                    })}
            <DateTimeWrapper>{dateTime}</DateTimeWrapper>
          </React.Fragment>);
            }
            return (<React.Fragment>
          {tct('This debug file was uploaded [when] before this event. It takes up to 1 hour for new files to propagate.', {
                    when: moment(eventDateReceived).from(dateCreated, true),
                })}
          <DateTimeWrapper>{dateTime}</DateTimeWrapper>
        </React.Fragment>);
        }
        if (hasReprocessWarning) {
            <React.Fragment>
        {tct('This debug file was uploaded [when] after this event. To apply new debug information, reprocess this issue.', {
                    when: moment(dateCreated).from(eventDateReceived, true),
                })}
        <DateTimeWrapper>{dateTime}</DateTimeWrapper>
      </React.Fragment>;
        }
        return (<React.Fragment>
        {tct('This debug file was uploaded [when] after this event.', {
                when: moment(eventDateReceived).from(dateCreated, true),
            })}
        <DateTimeWrapper>{dateTime}</DateTimeWrapper>
      </React.Fragment>);
    }
    function renderProcessingInfo() {
        if (candidate.download.status !== CandidateDownloadStatus.OK &&
            candidate.download.status !== CandidateDownloadStatus.DELETED) {
            return null;
        }
        var items = [];
        var _a = candidate, debug = _a.debug, unwind = _a.unwind;
        if (debug) {
            items.push(<ProcessingItem key="symbolication" type="symbolication" icon={<ProcessingIcon processingInfo={debug}/>}/>);
        }
        if (unwind) {
            items.push(<ProcessingItem key="stack_unwinding" type="stack_unwinding" icon={<ProcessingIcon processingInfo={unwind}/>}/>);
        }
        if (!items.length) {
            return null;
        }
        return (<React.Fragment>
        <StyledProcessingList items={items}/>
        <Divider />
      </React.Fragment>);
    }
    function renderExtraDetails() {
        if ((candidate.download.status !== CandidateDownloadStatus.UNAPPLIED &&
            candidate.download.status !== CandidateDownloadStatus.OK) ||
            source !== INTERNAL_SOURCE) {
            return null;
        }
        var _a = candidate, symbolType = _a.symbolType, fileType = _a.fileType, cpuName = _a.cpuName, size = _a.size, dateCreated = _a.dateCreated;
        return (<React.Fragment>
        <Tooltip title={getTimeSinceTooltipDescription(dateCreated)}>
          <TimeSinceWrapper>
            {candidate.download.status === CandidateDownloadStatus.UNAPPLIED && (<IconWarning color="red300" size="xs"/>)}
            {tct('Uploaded [timesince]', {
                timesince: <TimeSince disabledAbsoluteTooltip date={dateCreated}/>,
            })}
          </TimeSinceWrapper>
        </Tooltip>
        <Divider />
        <FileSize bytes={size}/>
        <Divider />
        <span>
          {symbolType === SymbolType.PROGUARD && cpuName === 'any'
                ? t('proguard mapping')
                : "" + symbolType + (fileType ? " " + fileType : '')}
        </span>
        <Divider />
      </React.Fragment>);
    }
    var filenameOrLocation = getFilenameOrLocation();
    return (<Wrapper>
      <div>
        <strong data-test-id="source_name">
          {source_name ? capitalize(source_name) : t('Unknown')}
        </strong>
        {filenameOrLocation && (<FilenameOrLocation>{filenameOrLocation}</FilenameOrLocation>)}
      </div>
      <Details>
        {renderExtraDetails()}
        {renderProcessingInfo()}
        <Features download={download}/>
      </Details>
    </Wrapper>);
}
export default Information;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  white-space: pre-wrap;\n  word-break: break-all;\n  max-width: 100%;\n"], ["\n  white-space: pre-wrap;\n  word-break: break-all;\n  max-width: 100%;\n"])));
var FilenameOrLocation = styled('span')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  padding-left: ", ";\n  font-size: ", ";\n"], ["\n  padding-left: ", ";\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.fontSizeSmall; });
var Details = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n  color: ", ";\n  font-size: ", ";\n"])), space(1), function (p) { return p.theme.gray400; }, function (p) { return p.theme.fontSizeSmall; });
var TimeSinceWrapper = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"])), space(0.5));
var DateTimeWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space(1));
var StyledProcessingList = styled(ProcessingList)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content;\n  grid-gap: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map
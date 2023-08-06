import { __extends, __makeTemplateObject, __read } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { PlatformIcon } from 'platformicons';
import Line from 'app/components/events/interfaces/frame/line';
import { getImageRange, parseAddress, stackTracePlatformIcon, } from 'app/components/events/interfaces/utils';
import { t } from 'app/locale';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import withOrganization from 'app/utils/withOrganization';
var defaultProps = {
    includeSystemFrames: true,
    expandFirstFrame: true,
};
var StacktraceContent = /** @class */ (function (_super) {
    __extends(StacktraceContent, _super);
    function StacktraceContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showingAbsoluteAddresses: false,
            showCompleteFunctionName: false,
        };
        _this.renderOmittedFrames = function (firstFrameOmitted, lastFrameOmitted) {
            var props = {
                className: 'frame frames-omitted',
                key: 'omitted',
            };
            var text = t('Frames %d until %d were omitted and not available.', firstFrameOmitted, lastFrameOmitted);
            return <li {...props}>{text}</li>;
        };
        _this.frameIsVisible = function (frame, nextFrame) {
            var includeSystemFrames = _this.props.includeSystemFrames;
            return (includeSystemFrames ||
                frame.inApp ||
                (nextFrame && nextFrame.inApp) ||
                // the last non-app frame
                (!frame.inApp && !nextFrame));
        };
        _this.handleToggleAddresses = function (event) {
            event.stopPropagation(); // to prevent collapsing if collapsable
            _this.setState(function (prevState) { return ({
                showingAbsoluteAddresses: !prevState.showingAbsoluteAddresses,
            }); });
        };
        _this.handleToggleFunctionName = function (event) {
            event.stopPropagation(); // to prevent collapsing if collapsable
            _this.setState(function (prevState) { return ({
                showCompleteFunctionName: !prevState.showCompleteFunctionName,
            }); });
        };
        return _this;
    }
    StacktraceContent.prototype.componentDidMount = function () {
        var _a = this.props, isHoverPreviewed = _a.isHoverPreviewed, organization = _a.organization, event = _a.event;
        if (isHoverPreviewed) {
            trackAnalyticsEvent({
                eventKey: 'stacktrace.preview.open',
                eventName: 'Stack Trace Preview: Open',
                organization_id: (organization === null || organization === void 0 ? void 0 : organization.id) ? parseInt(organization.id, 10) : '',
                issue_id: event.groupID,
            });
        }
    };
    StacktraceContent.prototype.isFrameAfterLastNonApp = function () {
        var _a;
        var data = this.props.data;
        var frames = (_a = data.frames) !== null && _a !== void 0 ? _a : [];
        if (!frames.length || frames.length < 2) {
            return false;
        }
        var lastFrame = frames[frames.length - 1];
        var penultimateFrame = frames[frames.length - 2];
        return penultimateFrame.inApp && !lastFrame.inApp;
    };
    StacktraceContent.prototype.findImageForAddress = function (address, addrMode) {
        var _a, _b;
        var images = (_b = (_a = this.props.event.entries.find(function (entry) { return entry.type === 'debugmeta'; })) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.images;
        return images && address
            ? images.find(function (img, idx) {
                if (!addrMode || addrMode === 'abs') {
                    var _a = __read(getImageRange(img), 2), startAddress = _a[0], endAddress = _a[1];
                    return address >= startAddress && address < endAddress;
                }
                return addrMode === "rel:" + idx;
            })
            : null;
    };
    StacktraceContent.prototype.getClassName = function () {
        var _a = this.props, _b = _a.className, className = _b === void 0 ? '' : _b, includeSystemFrames = _a.includeSystemFrames;
        if (includeSystemFrames) {
            return className + " traceback full-traceback";
        }
        return className + " traceback in-app-traceback";
    };
    StacktraceContent.prototype.render = function () {
        var _this = this;
        var _a, _b, _c, _d, _e;
        var _f = this.props, data = _f.data, event = _f.event, newestFirst = _f.newestFirst, expandFirstFrame = _f.expandFirstFrame, platform = _f.platform, includeSystemFrames = _f.includeSystemFrames, isHoverPreviewed = _f.isHoverPreviewed;
        var _g = this.state, showingAbsoluteAddresses = _g.showingAbsoluteAddresses, showCompleteFunctionName = _g.showCompleteFunctionName;
        var firstFrameOmitted = null;
        var lastFrameOmitted = null;
        if (data.framesOmitted) {
            firstFrameOmitted = data.framesOmitted[0];
            lastFrameOmitted = data.framesOmitted[1];
        }
        var lastFrameIdx = null;
        ((_a = data.frames) !== null && _a !== void 0 ? _a : []).forEach(function (frame, frameIdx) {
            if (frame.inApp) {
                lastFrameIdx = frameIdx;
            }
        });
        if (lastFrameIdx === null) {
            lastFrameIdx = ((_b = data.frames) !== null && _b !== void 0 ? _b : []).length - 1;
        }
        var frames = [];
        var nRepeats = 0;
        var maxLengthOfAllRelativeAddresses = ((_c = data.frames) !== null && _c !== void 0 ? _c : []).reduce(function (maxLengthUntilThisPoint, frame) {
            var correspondingImage = _this.findImageForAddress(frame.instructionAddr, frame.addrMode);
            try {
                var relativeAddress = (parseAddress(frame.instructionAddr) -
                    parseAddress(correspondingImage.image_addr)).toString(16);
                return maxLengthUntilThisPoint > relativeAddress.length
                    ? maxLengthUntilThisPoint
                    : relativeAddress.length;
            }
            catch (_a) {
                return maxLengthUntilThisPoint;
            }
        }, 0);
        var isFrameAfterLastNonApp = this.isFrameAfterLastNonApp();
        ((_d = data.frames) !== null && _d !== void 0 ? _d : []).forEach(function (frame, frameIdx) {
            var _a, _b, _c;
            var prevFrame = ((_a = data.frames) !== null && _a !== void 0 ? _a : [])[frameIdx - 1];
            var nextFrame = ((_b = data.frames) !== null && _b !== void 0 ? _b : [])[frameIdx + 1];
            var repeatedFrame = nextFrame &&
                frame.lineNo === nextFrame.lineNo &&
                frame.instructionAddr === nextFrame.instructionAddr &&
                frame.package === nextFrame.package &&
                frame.module === nextFrame.module &&
                frame.function === nextFrame.function;
            if (repeatedFrame) {
                nRepeats++;
            }
            if (_this.frameIsVisible(frame, nextFrame) && !repeatedFrame) {
                var image = _this.findImageForAddress(frame.instructionAddr, frame.addrMode);
                frames.push(<Line key={frameIdx} event={event} data={frame} isExpanded={expandFirstFrame && lastFrameIdx === frameIdx} emptySourceNotation={lastFrameIdx === frameIdx && frameIdx === 0} isOnlyFrame={((_c = data.frames) !== null && _c !== void 0 ? _c : []).length === 1} nextFrame={nextFrame} prevFrame={prevFrame} platform={platform} timesRepeated={nRepeats} showingAbsoluteAddress={showingAbsoluteAddresses} onAddressToggle={_this.handleToggleAddresses} image={image} maxLengthOfRelativeAddress={maxLengthOfAllRelativeAddresses} registers={{}} //TODO: Fix registers
                 isFrameAfterLastNonApp={isFrameAfterLastNonApp} includeSystemFrames={includeSystemFrames} onFunctionNameToggle={_this.handleToggleFunctionName} showCompleteFunctionName={showCompleteFunctionName} isHoverPreviewed={isHoverPreviewed} isFirst={newestFirst ? frameIdx === lastFrameIdx : frameIdx === 0}/>);
            }
            if (!repeatedFrame) {
                nRepeats = 0;
            }
            if (frameIdx === firstFrameOmitted) {
                frames.push(_this.renderOmittedFrames(firstFrameOmitted, lastFrameOmitted));
            }
        });
        if (frames.length > 0 && data.registers) {
            var lastFrame = frames.length - 1;
            frames[lastFrame] = React.cloneElement(frames[lastFrame], {
                registers: data.registers,
            });
        }
        if (newestFirst) {
            frames.reverse();
        }
        var className = this.getClassName();
        return (<Wrapper className={className}>
        <StyledPlatformIcon platform={stackTracePlatformIcon(platform, (_e = data.frames) !== null && _e !== void 0 ? _e : [])} size="20px" style={{ borderRadius: '3px 0 0 3px' }}/>
        <StyledList>{frames}</StyledList>
      </Wrapper>);
    };
    StacktraceContent.defaultProps = {
        includeSystemFrames: true,
        expandFirstFrame: true,
    };
    return StacktraceContent;
}(React.Component));
export default withOrganization(StacktraceContent);
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var StyledPlatformIcon = styled(PlatformIcon)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: absolute;\n  top: -1px;\n  left: -20px;\n"], ["\n  position: absolute;\n  top: -1px;\n  left: -20px;\n"])));
var StyledList = styled('ul')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  list-style: none;\n"], ["\n  list-style: none;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=stacktraceContent.jsx.map
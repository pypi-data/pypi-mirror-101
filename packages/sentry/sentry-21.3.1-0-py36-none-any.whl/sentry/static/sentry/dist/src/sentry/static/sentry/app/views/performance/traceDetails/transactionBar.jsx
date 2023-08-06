import { __extends } from "tslib";
import React from 'react';
import { withTheme } from 'emotion-theming';
import Count from 'app/components/count';
import * as DividerHandlerManager from 'app/components/events/interfaces/spans/dividerHandlerManager';
import * as ScrollbarManager from 'app/components/events/interfaces/spans/scrollbarManager';
import ProjectBadge from 'app/components/idBadge/projectBadge';
import Projects from 'app/utils/projects';
import { ConnectorBar, DividerLine, DividerLineGhostContainer, DurationPill, OperationName, StyledIconChevron, TRANSACTION_ROW_HEIGHT, TransactionBarRectangle, TransactionBarTitle, TransactionBarTitleContainer, TransactionBarTitleContent, TransactionRow, TransactionRowCell, TransactionRowCellContainer, TransactionTreeConnector, TransactionTreeToggle, TransactionTreeToggleContainer, } from './styles';
import TransactionDetail from './transactionDetail';
import { getDurationDisplay, getHumanDuration, isTraceFullDetailed, toPercent, } from './utils';
var TOGGLE_BUTTON_MARGIN_RIGHT = 16;
var TOGGLE_BUTTON_MAX_WIDTH = 30;
export var TOGGLE_BORDER_BOX = TOGGLE_BUTTON_MAX_WIDTH + TOGGLE_BUTTON_MARGIN_RIGHT;
var MARGIN_LEFT = 0;
var TransactionBar = /** @class */ (function (_super) {
    __extends(TransactionBar, _super);
    function TransactionBar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            showDetail: false,
        };
        _this.toggleDisplayDetail = function () {
            var transaction = _this.props.transaction;
            if (isTraceFullDetailed(transaction)) {
                _this.setState(function (state) { return ({
                    showDetail: !state.showDetail,
                }); });
            }
        };
        return _this;
    }
    TransactionBar.prototype.getCurrentOffset = function () {
        var transaction = this.props.transaction;
        var generation = transaction.generation;
        return getOffset(generation);
    };
    TransactionBar.prototype.renderConnector = function (hasToggle) {
        var _a = this.props, continuingDepths = _a.continuingDepths, isExpanded = _a.isExpanded, isOrphan = _a.isOrphan, isLast = _a.isLast, transaction = _a.transaction;
        var generation = transaction.generation;
        var eventId = isTraceFullDetailed(transaction)
            ? transaction.event_id
            : transaction.traceSlug;
        if (generation === 0) {
            if (hasToggle) {
                return (<ConnectorBar style={{ right: '16px', height: '10px', bottom: '-5px', top: 'auto' }} orphanBranch={false}/>);
            }
            return null;
        }
        var connectorBars = continuingDepths.map(function (_a) {
            var depth = _a.depth, isOrphanDepth = _a.isOrphanDepth;
            if (generation - depth <= 1) {
                // If the difference is less than or equal to 1, then it means that the continued
                // bar is from its direct parent. In this case, do not render a connector bar
                // because the tree connector below will suffice.
                return null;
            }
            var left = -1 * getOffset(generation - depth - 1) - 1;
            return (<ConnectorBar style={{ left: left }} key={eventId + "-" + depth} orphanBranch={isOrphanDepth}/>);
        });
        if (hasToggle && isExpanded) {
            connectorBars.push(<ConnectorBar style={{
                    right: '16px',
                    height: '10px',
                    bottom: isLast ? "-" + TRANSACTION_ROW_HEIGHT / 2 + "px" : '0',
                    top: 'auto',
                }} key={eventId + "-last"} orphanBranch={false}/>);
        }
        return (<TransactionTreeConnector isLast={isLast} hasToggler={hasToggle} orphanBranch={isOrphan}>
        {connectorBars}
      </TransactionTreeConnector>);
    };
    TransactionBar.prototype.renderToggle = function () {
        var _a = this.props, isExpanded = _a.isExpanded, transaction = _a.transaction, toggleExpandedState = _a.toggleExpandedState;
        var children = transaction.children, generation = transaction.generation;
        var left = this.getCurrentOffset();
        if (children.length <= 0) {
            return (<TransactionTreeToggleContainer style={{ left: left + "px" }}>
          {this.renderConnector(false)}
        </TransactionTreeToggleContainer>);
        }
        var isRoot = generation === 0;
        return (<TransactionTreeToggleContainer style={{ left: left + "px" }} hasToggler>
        {this.renderConnector(true)}
        <TransactionTreeToggle disabled={isRoot} isExpanded={isExpanded} onClick={function (event) {
                event.stopPropagation();
                if (isRoot) {
                    return;
                }
                toggleExpandedState();
            }}>
          <Count value={children.length}/>
          {!isRoot && (<div>
              <StyledIconChevron direction={isExpanded ? 'up' : 'down'}/>
            </div>)}
        </TransactionTreeToggle>
      </TransactionTreeToggleContainer>);
    };
    TransactionBar.prototype.renderTitle = function (scrollbarManagerChildrenProps) {
        var generateContentSpanBarRef = scrollbarManagerChildrenProps.generateContentSpanBarRef;
        var _a = this.props, organization = _a.organization, transaction = _a.transaction;
        var left = this.getCurrentOffset();
        var content = isTraceFullDetailed(transaction) ? (<React.Fragment>
        <Projects orgId={organization.slug} slugs={[transaction.project_slug]}>
          {function (_a) {
                var projects = _a.projects;
                var project = projects.find(function (p) { return p.slug === transaction.project_slug; });
                return (<ProjectBadge project={project ? project : { slug: transaction.project_slug }} avatarSize={16} hideName/>);
            }}
        </Projects>
        <TransactionBarTitleContent>
          <strong>
            <OperationName spanErrors={transaction.errors}>
              {transaction['transaction.op']}
            </OperationName>
            {' \u2014 '}
          </strong>
          {transaction.transaction}
        </TransactionBarTitleContent>
      </React.Fragment>) : (<TransactionBarTitleContent>
        <strong>
          <OperationName spanErrors={[]}>Trace</OperationName>
          {' \u2014 '}
        </strong>
        {transaction.traceSlug}
      </TransactionBarTitleContent>);
        return (<TransactionBarTitleContainer ref={generateContentSpanBarRef()}>
        {this.renderToggle()}
        <TransactionBarTitle style={{
                left: left + "px",
                width: '100%',
            }}>
          {content}
        </TransactionBarTitle>
      </TransactionBarTitleContainer>);
    };
    TransactionBar.prototype.renderDivider = function (dividerHandlerChildrenProps) {
        if (this.state.showDetail) {
            // Mock component to preserve layout spacing
            return (<DividerLine showDetail style={{
                    position: 'relative',
                }}/>);
        }
        var addDividerLineRef = dividerHandlerChildrenProps.addDividerLineRef;
        return (<DividerLine ref={addDividerLineRef()} style={{
                position: 'relative',
            }} onMouseEnter={function () {
                dividerHandlerChildrenProps.setHover(true);
            }} onMouseLeave={function () {
                dividerHandlerChildrenProps.setHover(false);
            }} onMouseOver={function () {
                dividerHandlerChildrenProps.setHover(true);
            }} onMouseDown={dividerHandlerChildrenProps.onDragStart} onClick={function (event) {
                // we prevent the propagation of the clicks from this component to prevent
                // the span detail from being opened.
                event.stopPropagation();
            }}/>);
    };
    TransactionBar.prototype.renderGhostDivider = function (dividerHandlerChildrenProps) {
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition, addGhostDividerLineRef = dividerHandlerChildrenProps.addGhostDividerLineRef;
        return (<DividerLineGhostContainer style={{
                width: "calc(" + toPercent(dividerPosition) + " + 0.5px)",
                display: 'none',
            }}>
        <DividerLine ref={addGhostDividerLineRef()} style={{
                right: 0,
            }} className="hovering" onClick={function (event) {
                // the ghost divider line should not be interactive.
                // we prevent the propagation of the clicks from this component to prevent
                // the span detail from being opened.
                event.stopPropagation();
            }}/>
      </DividerLineGhostContainer>);
    };
    TransactionBar.prototype.renderRectangle = function () {
        var _a = this.props, transaction = _a.transaction, traceInfo = _a.traceInfo, theme = _a.theme;
        var showDetail = this.state.showDetail;
        var palette = theme.charts.getColorPalette(traceInfo.maxGeneration);
        // Use 1 as the difference in the event that startTimestamp === endTimestamp
        var delta = Math.abs(traceInfo.endTimestamp - traceInfo.startTimestamp) || 1;
        var startPosition = Math.abs(transaction.start_timestamp - traceInfo.startTimestamp);
        var startPercentage = startPosition / delta;
        var duration = Math.abs(transaction.timestamp - transaction.start_timestamp);
        var widthPercentage = duration / delta;
        return (<TransactionBarRectangle spanBarHatch={false} style={{
                backgroundColor: palette[transaction.generation % palette.length],
                left: "clamp(0%, " + toPercent(startPercentage || 0) + ", calc(100% - 1px))",
                width: toPercent(widthPercentage || 0),
            }}>
        <DurationPill durationDisplay={getDurationDisplay({
                left: startPercentage,
                width: widthPercentage,
            })} showDetail={showDetail} spanBarHatch={false}>
          {getHumanDuration(duration)}
        </DurationPill>
      </TransactionBarRectangle>);
    };
    TransactionBar.prototype.renderHeader = function (_a) {
        var dividerHandlerChildrenProps = _a.dividerHandlerChildrenProps, scrollbarManagerChildrenProps = _a.scrollbarManagerChildrenProps;
        var index = this.props.index;
        var showDetail = this.state.showDetail;
        var dividerPosition = dividerHandlerChildrenProps.dividerPosition;
        return (<TransactionRowCellContainer showDetail={showDetail}>
        <TransactionRowCell data-type="span-row-cell" style={{
                width: "calc(" + toPercent(dividerPosition) + " - 0.5px)",
                paddingTop: 0,
            }} showDetail={showDetail} onClick={this.toggleDisplayDetail}>
          {this.renderTitle(scrollbarManagerChildrenProps)}
        </TransactionRowCell>
        {this.renderDivider(dividerHandlerChildrenProps)}
        <TransactionRowCell data-type="span-row-cell" showStriping={index % 2 !== 0} style={{
                width: "calc(" + toPercent(1 - dividerPosition) + " - 0.5px)",
                paddingTop: 0,
            }} showDetail={showDetail} onClick={this.toggleDisplayDetail}>
          {this.renderRectangle()}
        </TransactionRowCell>
        {!showDetail && this.renderGhostDivider(dividerHandlerChildrenProps)}
      </TransactionRowCellContainer>);
    };
    TransactionBar.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, isVisible = _a.isVisible, transaction = _a.transaction;
        var showDetail = this.state.showDetail;
        return (<TransactionRow visible={isVisible} showBorder={showDetail} cursor={isTraceFullDetailed(transaction) ? 'pointer' : 'default'}>
        <ScrollbarManager.Consumer>
          {function (scrollbarManagerChildrenProps) {
                return (<DividerHandlerManager.Consumer>
                {function (dividerHandlerChildrenProps) {
                        return _this.renderHeader({
                            dividerHandlerChildrenProps: dividerHandlerChildrenProps,
                            scrollbarManagerChildrenProps: scrollbarManagerChildrenProps,
                        });
                    }}
              </DividerHandlerManager.Consumer>);
            }}
        </ScrollbarManager.Consumer>
        {isTraceFullDetailed(transaction) && isVisible && showDetail && (<TransactionDetail location={location} organization={organization} transaction={transaction}/>)}
      </TransactionRow>);
    };
    return TransactionBar;
}(React.Component));
function getOffset(generation) {
    return generation * (TOGGLE_BORDER_BOX / 2) + MARGIN_LEFT;
}
export default withTheme(TransactionBar);
//# sourceMappingURL=transactionBar.jsx.map
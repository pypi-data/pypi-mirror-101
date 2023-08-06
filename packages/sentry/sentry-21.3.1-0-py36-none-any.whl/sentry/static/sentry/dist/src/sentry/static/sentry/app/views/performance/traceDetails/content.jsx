import { __assign, __awaiter, __extends, __generator, __read, __spreadArray } from "tslib";
import React from 'react';
import * as Sentry from '@sentry/react';
import Alert from 'app/components/alert';
import * as DividerHandlerManager from 'app/components/events/interfaces/spans/dividerHandlerManager';
import * as ScrollbarManager from 'app/components/events/interfaces/spans/scrollbarManager';
import FeatureBadge from 'app/components/featureBadge';
import * as Layout from 'app/components/layouts/thirds';
import ExternalLink from 'app/components/links/externalLink';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import TimeSince from 'app/components/timeSince';
import { IconInfo } from 'app/icons';
import { t, tct, tn } from 'app/locale';
import { createFuzzySearch } from 'app/utils/createFuzzySearch';
import { getDuration } from 'app/utils/formatters';
import { reduceTrace } from 'app/utils/performance/quickTrace/utils';
import Breadcrumb from 'app/views/performance/breadcrumb';
import { MetaData } from 'app/views/performance/transactionDetails/styles';
import { DividerSpacer, ScrollbarContainer, SearchContainer, StyledPanel, StyledSearchBar, TraceDetailBody, TraceDetailHeader, TraceViewContainer, TraceViewHeaderContainer, TransactionRowMessage, VirtualScrollBar, VirtualScrollBarGrip, } from './styles';
import TransactionGroup from './transactionGroup';
import { getTraceInfo, isRootTransaction, toPercent } from './utils';
var TraceDetailsContent = /** @class */ (function (_super) {
    __extends(TraceDetailsContent, _super);
    function TraceDetailsContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchQuery: undefined,
            filteredTransactionIds: undefined,
        };
        _this.traceViewRef = React.createRef();
        _this.virtualScrollbarContainerRef = React.createRef();
        _this.handleTransactionFilter = function (searchQuery) {
            _this.setState({ searchQuery: searchQuery || undefined }, _this.filterTransactions);
        };
        _this.filterTransactions = function () { return __awaiter(_this, void 0, void 0, function () {
            var traces, _a, filteredTransactionIds, searchQuery, transformed, fuse, results, matched;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        traces = this.props.traces;
                        _a = this.state, filteredTransactionIds = _a.filteredTransactionIds, searchQuery = _a.searchQuery;
                        if (!searchQuery || traces === null || traces.length <= 0) {
                            if (filteredTransactionIds !== undefined) {
                                this.setState({
                                    filteredTransactionIds: undefined,
                                });
                            }
                            return [2 /*return*/];
                        }
                        transformed = traces.flatMap(function (trace) {
                            return reduceTrace(trace, function (acc, transaction) {
                                var _a;
                                var indexed = [
                                    transaction.event_id,
                                    transaction.span_id,
                                    transaction['transaction.op'],
                                    transaction.transaction,
                                    transaction.project_slug,
                                ];
                                var tags = (_a = transaction.tags) !== null && _a !== void 0 ? _a : [];
                                var tagKeys = tags.map(function (_a) {
                                    var key = _a.key;
                                    return key;
                                });
                                var tagValues = tags.map(function (_a) {
                                    var value = _a.value;
                                    return value;
                                });
                                acc.push({
                                    transaction: transaction,
                                    indexed: indexed,
                                    tagKeys: tagKeys,
                                    tagValues: tagValues,
                                });
                                return acc;
                            }, []);
                        });
                        return [4 /*yield*/, createFuzzySearch(transformed, {
                                keys: ['indexed', 'tagKeys', 'tagValues', 'dataKeys', 'dataValues'],
                                includeMatches: false,
                                threshold: 0.6,
                                location: 0,
                                distance: 100,
                                maxPatternLength: 32,
                            })];
                    case 1:
                        fuse = _b.sent();
                        results = fuse.search(searchQuery);
                        matched = results.map(function (result) { return result.item.transaction; });
                        this.setState({
                            filteredTransactionIds: new Set(matched.map(function (transaction) { return transaction.event_id; })),
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.isTransactionVisible = function (transaction) {
            var filteredTransactionIds = _this.state.filteredTransactionIds;
            return filteredTransactionIds
                ? filteredTransactionIds.has(transaction.event_id)
                : true;
        };
        return _this;
    }
    TraceDetailsContent.prototype.renderTraceLoading = function () {
        return <LoadingIndicator />;
    };
    TraceDetailsContent.prototype.renderTraceRequiresDateRangeSelection = function () {
        return <LoadingError message={t('Trace view requires a date range selection.')}/>;
    };
    TraceDetailsContent.prototype.renderTraceNotFound = function () {
        return <LoadingError message={t('The trace you are looking for was not found.')}/>;
    };
    TraceDetailsContent.prototype.renderSearchBar = function () {
        return (<SearchContainer>
        <StyledSearchBar defaultQuery="" query={this.state.searchQuery || ''} placeholder={t('Search for transactions')} onSearch={this.handleTransactionFilter}/>
      </SearchContainer>);
    };
    TraceDetailsContent.prototype.renderTraceHeader = function (traceInfo) {
        return (<TraceDetailHeader>
        <MetaData headingText={t('Event Breakdown')} tooltipText={t('The number of transactions and errors there are in this trace.')} bodyText={tct('[transactions]  |  [errors]', {
                transactions: tn('%s Transaction', '%s Transactions', traceInfo.transactions.size),
                errors: tn('%s Error', '%s Errors', traceInfo.errors.size),
            })} subtext={tn('Across %s project', 'Across %s projects', traceInfo.projects.size)}/>
        <MetaData headingText={t('Total Duration')} tooltipText={t('The time elapsed between the start and end of this trace.')} bodyText={getDuration(traceInfo.endTimestamp - traceInfo.startTimestamp, 2, true)} subtext={<TimeSince date={(traceInfo.endTimestamp || 0) * 1000}/>}/>
      </TraceDetailHeader>);
    };
    TraceDetailsContent.prototype.renderTraceWarnings = function () {
        var traces = this.props.traces;
        var _a = (traces !== null && traces !== void 0 ? traces : []).reduce(function (counts, trace) {
            if (isRootTransaction(trace)) {
                counts.roots++;
            }
            else {
                counts.orphans++;
            }
            return counts;
        }, { roots: 0, orphans: 0 }), roots = _a.roots, orphans = _a.orphans;
        var warning = null;
        if (roots === 0 && orphans > 0) {
            warning = (<Alert type="info" icon={<IconInfo size="sm"/>}>
          <ExternalLink href="https://docs.sentry.io/product/performance/trace-view/#orphan-traces-and-broken-subtraces">
            {t('A root transaction is missing. Transactions linked by a dashed line have been orphaned and cannot be directly linked to the root.')}
          </ExternalLink>
        </Alert>);
        }
        else if (roots === 1 && orphans > 0) {
            warning = (<Alert type="info" icon={<IconInfo size="sm"/>}>
          <ExternalLink href="https://docs.sentry.io/product/performance/trace-view/#orphan-traces-and-broken-subtraces">
            {t('This trace has broken subtraces. Transactions linked by a dashed line have been orphaned and cannot be directly linked to the root.')}
          </ExternalLink>
        </Alert>);
        }
        else if (roots > 1) {
            warning = (<Alert type="info" icon={<IconInfo size="sm"/>}>
          <ExternalLink href="https://docs.sentry.io/product/performance/trace-view/#multiple-roots">
            {t('Multiple root transactions have been found with this trace ID.')}
          </ExternalLink>
        </Alert>);
        }
        return warning;
    };
    TraceDetailsContent.prototype.renderInfoMessage = function (_a) {
        var isVisible = _a.isVisible, numberOfHiddenTransactionsAbove = _a.numberOfHiddenTransactionsAbove;
        var messages = [];
        if (isVisible) {
            if (numberOfHiddenTransactionsAbove === 1) {
                messages.push(<span key="stuff">
            {tct('[numOfTransaction] hidden transaction', {
                        numOfTransaction: <strong>{numberOfHiddenTransactionsAbove}</strong>,
                    })}
          </span>);
            }
            else if (numberOfHiddenTransactionsAbove > 1) {
                messages.push(<span key="stuff">
            {tct('[numOfTransaction] hidden transactions', {
                        numOfTransaction: <strong>{numberOfHiddenTransactionsAbove}</strong>,
                    })}
          </span>);
            }
        }
        if (messages.length <= 0) {
            return null;
        }
        return <TransactionRowMessage>{messages}</TransactionRowMessage>;
    };
    TraceDetailsContent.prototype.renderTransaction = function (transaction, _a) {
        var _this = this;
        var continuingDepths = _a.continuingDepths, isOrphan = _a.isOrphan, isLast = _a.isLast, index = _a.index, numberOfHiddenTransactionsAbove = _a.numberOfHiddenTransactionsAbove, traceInfo = _a.traceInfo;
        var _b = this.props, location = _b.location, organization = _b.organization;
        var children = transaction.children, eventId = transaction.event_id;
        // Add 1 to the generation to make room for the "root trace"
        var generation = transaction.generation + 1;
        var isVisible = this.isTransactionVisible(transaction);
        var accumulated = children.reduce(function (acc, child, idx) {
            var isLastChild = idx === children.length - 1;
            var hasChildren = child.children.length > 0;
            var result = _this.renderTransaction(child, {
                continuingDepths: !isLastChild && hasChildren
                    ? __spreadArray(__spreadArray([], __read(continuingDepths)), [{ depth: generation, isOrphanDepth: false }]) : continuingDepths,
                isOrphan: isOrphan,
                isLast: isLastChild,
                index: acc.lastIndex + 1,
                numberOfHiddenTransactionsAbove: acc.numberOfHiddenTransactionsAbove,
                traceInfo: traceInfo,
            });
            acc.lastIndex = result.lastIndex;
            acc.numberOfHiddenTransactionsAbove = result.numberOfHiddenTransactionsAbove;
            acc.renderedChildren.push(result.transactionGroup);
            return acc;
        }, {
            renderedChildren: [],
            lastIndex: index,
            numberOfHiddenTransactionsAbove: isVisible
                ? 0
                : numberOfHiddenTransactionsAbove + 1,
        });
        return {
            transactionGroup: (<React.Fragment key={eventId}>
          {this.renderInfoMessage({
                    isVisible: isVisible,
                    numberOfHiddenTransactionsAbove: numberOfHiddenTransactionsAbove,
                })}
          <TransactionGroup location={location} organization={organization} traceInfo={traceInfo} transaction={__assign(__assign({}, transaction), { generation: generation })} continuingDepths={continuingDepths} isOrphan={isOrphan} isLast={isLast} index={index} isVisible={isVisible} renderedChildren={accumulated.renderedChildren}/>
        </React.Fragment>),
            lastIndex: accumulated.lastIndex,
            numberOfHiddenTransactionsAbove: accumulated.numberOfHiddenTransactionsAbove,
        };
    };
    TraceDetailsContent.prototype.renderTraceView = function (traceInfo) {
        var _this = this;
        var _a;
        var sentryTransaction = (_a = Sentry.getCurrentHub().getScope()) === null || _a === void 0 ? void 0 : _a.getTransaction();
        var sentrySpan = sentryTransaction === null || sentryTransaction === void 0 ? void 0 : sentryTransaction.startChild({
            op: 'trace.render',
            description: 'trace-view-content',
        });
        var _b = this.props, location = _b.location, organization = _b.organization, traces = _b.traces, traceSlug = _b.traceSlug;
        if (traces === null || traces.length <= 0) {
            return this.renderTraceNotFound();
        }
        var accumulator = {
            index: 1,
            numberOfHiddenTransactionsAbove: 0,
            traceInfo: traceInfo,
            transactionGroups: [],
        };
        var _c = traces.reduce(function (acc, trace, index) {
            var isLastTransaction = index === traces.length - 1;
            var hasChildren = trace.children.length > 0;
            var isNextChildOrphaned = !isLastTransaction && traces[index + 1].parent_span_id !== null;
            var result = _this.renderTransaction(trace, __assign(__assign({}, acc), { 
                // if the root of a subtrace has a parent_span_idk, then it must be an orphan
                isOrphan: !isRootTransaction(trace), isLast: isLastTransaction, continuingDepths: !isLastTransaction && hasChildren
                    ? [{ depth: 0, isOrphanDepth: isNextChildOrphaned }]
                    : [] }));
            acc.index = result.lastIndex + 1;
            acc.numberOfHiddenTransactionsAbove = result.numberOfHiddenTransactionsAbove;
            acc.transactionGroups.push(result.transactionGroup);
            return acc;
        }, accumulator), transactionGroups = _c.transactionGroups, numberOfHiddenTransactionsAbove = _c.numberOfHiddenTransactionsAbove;
        var traceView = (<TraceDetailBody>
        <DividerHandlerManager.Provider interactiveLayerRef={this.traceViewRef}>
          <DividerHandlerManager.Consumer>
            {function (_a) {
                var dividerPosition = _a.dividerPosition;
                return (<ScrollbarManager.Provider dividerPosition={dividerPosition} interactiveLayerRef={_this.virtualScrollbarContainerRef}>
                <StyledPanel>
                  <TraceViewHeaderContainer>
                    <ScrollbarContainer ref={_this.virtualScrollbarContainerRef} style={{
                        // the width of this component is shrunk to compensate for half of the width of the divider line
                        width: "calc(" + toPercent(dividerPosition) + " - 0.5px)",
                    }}>
                      <ScrollbarManager.Consumer>
                        {function (_a) {
                        var virtualScrollbarRef = _a.virtualScrollbarRef, onDragStart = _a.onDragStart;
                        return (<VirtualScrollBar data-type="virtual-scrollbar" ref={virtualScrollbarRef} onMouseDown={onDragStart}>
                              <VirtualScrollBarGrip />
                            </VirtualScrollBar>);
                    }}
                      </ScrollbarManager.Consumer>
                    </ScrollbarContainer>
                    <DividerSpacer />
                  </TraceViewHeaderContainer>
                  <TraceViewContainer ref={_this.traceViewRef}>
                    <TransactionGroup location={location} organization={organization} traceInfo={traceInfo} transaction={{
                        traceSlug: traceSlug,
                        generation: 0,
                        'transaction.duration': traceInfo.endTimestamp - traceInfo.startTimestamp,
                        children: traces,
                        start_timestamp: traceInfo.startTimestamp,
                        timestamp: traceInfo.endTimestamp,
                    }} continuingDepths={[]} isOrphan={false} isLast={false} index={0} isVisible renderedChildren={transactionGroups}/>
                    {_this.renderInfoMessage({
                        isVisible: true,
                        numberOfHiddenTransactionsAbove: numberOfHiddenTransactionsAbove,
                    })}
                  </TraceViewContainer>
                </StyledPanel>
              </ScrollbarManager.Provider>);
            }}
          </DividerHandlerManager.Consumer>
        </DividerHandlerManager.Provider>
      </TraceDetailBody>);
        sentrySpan === null || sentrySpan === void 0 ? void 0 : sentrySpan.finish();
        return traceView;
    };
    TraceDetailsContent.prototype.renderContent = function () {
        var _a = this.props, start = _a.start, end = _a.end, statsPeriod = _a.statsPeriod, isLoading = _a.isLoading, error = _a.error, traces = _a.traces;
        if (!statsPeriod && (!start || !end)) {
            return this.renderTraceRequiresDateRangeSelection();
        }
        else if (isLoading) {
            return this.renderTraceLoading();
        }
        else if (error !== null || traces === null || traces.length <= 0) {
            return this.renderTraceNotFound();
        }
        else {
            var traceInfo = getTraceInfo(traces);
            return (<React.Fragment>
          {this.renderTraceWarnings()}
          {this.renderTraceHeader(traceInfo)}
          {this.renderSearchBar()}
          {this.renderTraceView(traceInfo)}
        </React.Fragment>);
        }
    };
    TraceDetailsContent.prototype.render = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, traceSlug = _a.traceSlug;
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumb organization={organization} location={location} traceSlug={traceSlug}/>
            <Layout.Title data-test-id="trace-header">
              {t('Trace ID: %s', traceSlug)}
              <FeatureBadge type="beta"/>
            </Layout.Title>
          </Layout.HeaderContent>
        </Layout.Header>
        <Layout.Body>
          <Layout.Main fullWidth>{this.renderContent()}</Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    };
    return TraceDetailsContent;
}(React.Component));
export default TraceDetailsContent;
//# sourceMappingURL=content.jsx.map
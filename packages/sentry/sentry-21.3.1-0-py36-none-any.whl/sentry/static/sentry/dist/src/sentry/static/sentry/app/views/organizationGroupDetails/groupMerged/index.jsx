import { __assign, __extends } from "tslib";
import React from 'react';
import * as queryString from 'query-string';
import GroupingActions from 'app/actions/groupingActions';
import Alert from 'app/components/alert';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t } from 'app/locale';
import GroupingStore from 'app/stores/groupingStore';
import { callIfFunction } from 'app/utils/callIfFunction';
import MergedList from './mergedList';
var GroupMergedView = /** @class */ (function (_super) {
    __extends(GroupMergedView, _super);
    function GroupMergedView() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            mergedItems: [],
            loading: true,
            error: false,
            query: _this.props.location.query.query || '',
        };
        _this.onGroupingChange = function (_a) {
            var mergedItems = _a.mergedItems, mergedLinks = _a.mergedLinks, loading = _a.loading, error = _a.error;
            if (mergedItems) {
                _this.setState({
                    mergedItems: mergedItems,
                    mergedLinks: mergedLinks,
                    loading: typeof loading !== 'undefined' ? loading : false,
                    error: typeof error !== 'undefined' ? error : false,
                });
            }
        };
        _this.listener = GroupingStore.listen(_this.onGroupingChange, undefined);
        _this.fetchData = function () {
            GroupingActions.fetch([
                {
                    endpoint: _this.getEndpoint(),
                    dataKey: 'merged',
                    queryParams: _this.props.location.query,
                },
            ]);
        };
        _this.handleUnmerge = function () {
            GroupingActions.unmerge({
                groupId: _this.props.params.groupId,
                loadingMessage: t('Unmerging events\u2026'),
                successMessage: t('Events successfully queued for unmerging.'),
                errorMessage: t('Unable to queue events for unmerging.'),
            });
        };
        return _this;
    }
    GroupMergedView.prototype.componentDidMount = function () {
        this.fetchData();
    };
    GroupMergedView.prototype.componentWillReceiveProps = function (nextProps) {
        if (nextProps.params.groupId !== this.props.params.groupId ||
            nextProps.location.search !== this.props.location.search) {
            var queryParams = nextProps.location.query;
            this.setState({
                query: queryParams.query,
            }, this.fetchData);
        }
    };
    GroupMergedView.prototype.componentWillUnmount = function () {
        callIfFunction(this.listener);
    };
    GroupMergedView.prototype.getEndpoint = function () {
        var params = this.props.params;
        var groupId = params.groupId;
        var queryParams = __assign(__assign({}, this.props.location.query), { limit: 50, query: this.state.query });
        return "/issues/" + groupId + "/hashes/?" + queryString.stringify(queryParams);
    };
    GroupMergedView.prototype.render = function () {
        var _a = this.props, project = _a.project, params = _a.params;
        var groupId = params.groupId;
        var _b = this.state, isLoading = _b.loading, error = _b.error, mergedItems = _b.mergedItems, mergedLinks = _b.mergedLinks;
        var isError = error && !isLoading;
        var isLoadedSuccessfully = !isError && !isLoading;
        return (<React.Fragment>
        <Alert type="warning">
          {t('This is an experimental feature. Data may not be immediately available while we process unmerges.')}
        </Alert>

        {isLoading && <LoadingIndicator />}
        {isError && (<LoadingError message={t('Unable to load merged events, please try again later')} onRetry={this.fetchData}/>)}

        {isLoadedSuccessfully && (<MergedList project={project} fingerprints={mergedItems} pageLinks={mergedLinks} groupId={groupId} onUnmerge={this.handleUnmerge} onToggleCollapse={GroupingActions.toggleCollapseFingerprints}/>)}
      </React.Fragment>);
    };
    return GroupMergedView;
}(React.Component));
export { GroupMergedView };
export default GroupMergedView;
//# sourceMappingURL=index.jsx.map
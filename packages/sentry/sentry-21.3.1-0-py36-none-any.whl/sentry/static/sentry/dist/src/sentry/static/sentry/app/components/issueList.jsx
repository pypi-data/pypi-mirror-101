import { __assign, __extends } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import CompactIssue from 'app/components/issues/compactIssue';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import Pagination from 'app/components/pagination';
import { Panel, PanelBody } from 'app/components/panels';
import { IconSearch } from 'app/icons';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import EmptyMessage from 'app/views/settings/components/emptyMessage';
var IssueList = /** @class */ (function (_super) {
    __extends(IssueList, _super);
    function IssueList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getInitialState();
        _this.fetchData = function () {
            var _a = _this.props, location = _a.location, api = _a.api, endpoint = _a.endpoint, query = _a.query;
            api.clear();
            api.request(endpoint, {
                method: 'GET',
                query: __assign({ cursor: (location && location.query && location.query.cursor) || '' }, query),
                success: function (data, _, jqXHR) {
                    var _a;
                    _this.setState({
                        data: data,
                        loading: false,
                        error: false,
                        issueIds: data.map(function (item) { return item.id; }),
                        pageLinks: (_a = jqXHR === null || jqXHR === void 0 ? void 0 : jqXHR.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null,
                    });
                },
                error: function () {
                    _this.setState({ loading: false, error: true });
                },
            });
        };
        return _this;
    }
    IssueList.prototype.getInitialState = function () {
        return {
            issueIds: [],
            loading: true,
            error: false,
            pageLinks: null,
            data: [],
        };
    };
    IssueList.prototype.componentWillMount = function () {
        this.fetchData();
    };
    IssueList.prototype.componentWillReceiveProps = function (nextProps) {
        var location = this.props.location;
        var nextLocation = nextProps.location;
        if (!location) {
            return;
        }
        if (location.pathname !== nextLocation.pathname ||
            location.search !== nextLocation.search) {
            this.remountComponent();
        }
    };
    IssueList.prototype.remountComponent = function () {
        this.setState(this.getInitialState(), this.fetchData);
    };
    IssueList.prototype.renderError = function () {
        return (<div style={{ margin: space(2) + " " + space(2) + " 0" }}>
        <LoadingError onRetry={this.fetchData}/>
      </div>);
    };
    IssueList.prototype.renderLoading = function () {
        return (<div style={{ margin: '18px 18px 0' }}>
        <LoadingIndicator />
      </div>);
    };
    IssueList.prototype.renderEmpty = function () {
        var emptyText = this.props.emptyText;
        var _a = this.props, noBorder = _a.noBorder, noMargin = _a.noMargin;
        var panelStyle = noBorder ? { border: 0, borderRadius: 0 } : {};
        if (noMargin) {
            panelStyle.marginBottom = 0;
        }
        return (<Panel style={panelStyle}>
        <EmptyMessage icon={<IconSearch size="xl"/>}>
          {emptyText ? emptyText : t('Nothing to show here, move along.')}
        </EmptyMessage>
      </Panel>);
    };
    IssueList.prototype.renderResults = function () {
        var _a = this.props, noBorder = _a.noBorder, noMargin = _a.noMargin, statsPeriod = _a.statsPeriod, renderEmpty = _a.renderEmpty;
        var _b = this.state, loading = _b.loading, error = _b.error, issueIds = _b.issueIds, data = _b.data;
        if (loading) {
            return this.renderLoading();
        }
        if (error) {
            return this.renderError();
        }
        if (issueIds.length > 0) {
            var panelStyle = noBorder
                ? { border: 0, borderRadius: 0 }
                : {};
            if (noMargin) {
                panelStyle.marginBottom = 0;
            }
            return (<Panel style={panelStyle}>
          <PanelBody className="issue-list">
            {data.map(function (issue) { return (<CompactIssue key={issue.id} id={issue.id} data={issue} statsPeriod={statsPeriod}/>); })}
          </PanelBody>
        </Panel>);
        }
        return (renderEmpty === null || renderEmpty === void 0 ? void 0 : renderEmpty()) || this.renderEmpty();
    };
    IssueList.prototype.render = function () {
        var pageLinks = this.state.pageLinks;
        var pagination = this.props.pagination;
        return (<React.Fragment>
        {this.renderResults()}
        {pagination && pageLinks && <Pagination pageLinks={pageLinks} {...this.props}/>}
      </React.Fragment>);
    };
    return IssueList;
}(React.Component));
export { IssueList };
export default withRouter(withApi(IssueList));
//# sourceMappingURL=issueList.jsx.map
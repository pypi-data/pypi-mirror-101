import { __extends } from "tslib";
import React from 'react';
import MiniBarChart from 'app/components/charts/miniBarChart';
import LoadingError from 'app/components/loadingError';
import LoadingIndicator from 'app/components/loadingIndicator';
import { t } from 'app/locale';
import theme from 'app/utils/theme';
import withApi from 'app/utils/withApi';
var initialState = {
    error: false,
    loading: true,
    rawData: {
        'events.total': [],
        'events.dropped': [],
    },
    stats: { received: [], rejected: [] },
};
var EventChart = /** @class */ (function (_super) {
    __extends(EventChart, _super);
    function EventChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = initialState;
        _this.fetchData = function () {
            var statNameList = ['events.total', 'events.dropped'];
            statNameList.forEach(function (statName) {
                // query the organization stats via a separate call as its possible the project stats
                // are too heavy
                _this.props.api.request('/internal/stats/', {
                    method: 'GET',
                    data: {
                        since: _this.props.since,
                        resolution: _this.props.resolution,
                        key: statName,
                    },
                    success: function (data) {
                        _this.setState(function (prevState) {
                            var rawData = prevState.rawData;
                            rawData[statName] = data;
                            return {
                                rawData: rawData,
                            };
                        }, _this.requestFinished);
                    },
                    error: function () {
                        _this.setState({
                            error: true,
                        });
                    },
                });
            });
        };
        return _this;
    }
    EventChart.prototype.componentWillMount = function () {
        this.fetchData();
    };
    EventChart.prototype.componentWillReceiveProps = function (nextProps) {
        if (this.props.since !== nextProps.since) {
            this.setState(initialState, this.fetchData);
        }
    };
    EventChart.prototype.requestFinished = function () {
        var rawData = this.state.rawData;
        if (rawData['events.total'] && rawData['events.dropped']) {
            this.processOrgData();
        }
    };
    EventChart.prototype.processOrgData = function () {
        var rawData = this.state.rawData;
        var sReceived = {};
        var sRejected = {};
        var aReceived = [0, 0]; // received, points
        rawData['events.total'].forEach(function (point, idx) {
            var dReceived = point[1];
            var dRejected = rawData['events.dropped'][idx][1];
            var ts = point[0];
            if (sReceived[ts] === undefined) {
                sReceived[ts] = dReceived;
                sRejected[ts] = dRejected;
            }
            else {
                sReceived[ts] += dReceived;
                sRejected[ts] += dRejected;
            }
            if (dReceived > 0) {
                aReceived[0] += dReceived;
                aReceived[1] += 1;
            }
        });
        this.setState({
            stats: {
                rejected: Object.keys(sRejected).map(function (ts) { return ({
                    name: parseInt(ts, 10) * 1000,
                    value: sRejected[ts] || 0,
                }); }),
                accepted: Object.keys(sReceived).map(function (ts) {
                    // total number of events accepted (received - rejected)
                    return ({ name: parseInt(ts, 10) * 1000, value: sReceived[ts] - sRejected[ts] });
                }),
            },
            loading: false,
        });
    };
    EventChart.prototype.getChartSeries = function () {
        var stats = this.state.stats;
        return [
            {
                seriesName: t('Accepted'),
                data: stats.accepted,
                color: theme.blue300,
            },
            {
                seriesName: t('Dropped'),
                data: stats.rejected,
                color: theme.red200,
            },
        ];
    };
    EventChart.prototype.render = function () {
        var _a = this.state, loading = _a.loading, error = _a.error;
        if (loading) {
            return <LoadingIndicator />;
        }
        else if (error) {
            return <LoadingError onRetry={this.fetchData}/>;
        }
        var series = this.getChartSeries();
        var colors = series.map(function (_a) {
            var color = _a.color;
            return color;
        });
        return (<MiniBarChart series={series} colors={colors} height={110} stacked isGroupedByDate showTimeInTooltip labelYAxisExtents/>);
    };
    return EventChart;
}(React.Component));
export default withApi(EventChart);
//# sourceMappingURL=eventChart.jsx.map
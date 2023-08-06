import { __assign, __extends, __read, __rest, __spreadArray } from "tslib";
import React from 'react';
import theme from 'app/utils/theme';
import PieSeries from './series/pieSeries';
import BaseChart from './baseChart';
var PieChart = /** @class */ (function (_super) {
    __extends(PieChart, _super);
    function PieChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.isInitialSelected = true;
        _this.selected = 0;
        _this.chart = React.createRef();
        // Select a series to highlight (e.g. shows details of series)
        // This is the same event as when you hover over a series in the chart
        _this.highlight = function (dataIndex) {
            if (!_this.chart.current) {
                return;
            }
            _this.chart.current.getEchartsInstance().dispatchAction({
                type: 'highlight',
                seriesIndex: 0,
                dataIndex: dataIndex,
            });
        };
        // Opposite of `highlight`
        _this.downplay = function (dataIndex) {
            if (!_this.chart.current) {
                return;
            }
            _this.chart.current.getEchartsInstance().dispatchAction({
                type: 'downplay',
                seriesIndex: 0,
                dataIndex: dataIndex,
            });
        };
        // echarts Legend does not have access to percentages (but tooltip does :/)
        _this.getSeriesPercentages = function (series) {
            var total = series.data.reduce(function (acc, _a) {
                var value = _a.value;
                return acc + value;
            }, 0);
            return series.data
                .map(function (_a) {
                var name = _a.name, value = _a.value;
                return [name, Math.round((value / total) * 10000) / 100];
            })
                .reduce(function (acc, _a) {
                var _b;
                var _c = __read(_a, 2), name = _c[0], value = _c[1];
                return (__assign(__assign({}, acc), (_b = {}, _b[name] = value, _b)));
            }, {});
        };
        return _this;
    }
    PieChart.prototype.componentDidMount = function () {
        var _this = this;
        var selectOnRender = this.props.selectOnRender;
        if (!selectOnRender) {
            return;
        }
        // Timeout is because we need to wait for rendering animation to complete
        // And I haven't found a callback for this
        setTimeout(function () { return _this.highlight(0); }, 1000);
    };
    PieChart.prototype.render = function () {
        var _this = this;
        var _a = this.props, series = _a.series, props = __rest(_a, ["series"]);
        if (!series || !series.length) {
            return null;
        }
        if (series.length > 1) {
            // eslint-disable-next-line no-console
            console.warn('PieChart only uses the first series!');
        }
        // Note, we only take the first series unit!
        var _b = __read(series, 1), firstSeries = _b[0];
        var seriesPercentages = this.getSeriesPercentages(firstSeries);
        return (<BaseChart ref={this.chart} colors={firstSeries &&
                firstSeries.data && __spreadArray([], __read(theme.charts.getColorPalette(firstSeries.data.length)))} 
        // when legend highlights it does NOT pass dataIndex :(
        onHighlight={function (_a) {
                var name = _a.name;
                if (!_this.isInitialSelected ||
                    !name ||
                    firstSeries.data[_this.selected].name === name) {
                    return;
                }
                // Unhighlight if not initial "highlight" event and
                // if name exists (i.e. not dispatched from cDM) and
                // highlighted series name is different than the initially selected series name
                _this.downplay(_this.selected);
                _this.isInitialSelected = false;
            }} onMouseOver={function (_a) {
                var dataIndex = _a.dataIndex;
                if (!_this.isInitialSelected) {
                    return;
                }
                if (dataIndex === _this.selected) {
                    return;
                }
                _this.downplay(_this.selected);
                _this.isInitialSelected = false;
            }} {...props} options={{
                legend: {
                    orient: 'vertical',
                    align: 'left',
                    show: true,
                    left: 10,
                    top: 10,
                    bottom: 10,
                    formatter: function (name) {
                        return name + " " + (typeof seriesPercentages[name] !== 'undefined'
                            ? "(" + seriesPercentages[name] + "%)"
                            : '');
                    },
                },
            }} series={[
                PieSeries({
                    name: firstSeries.seriesName,
                    data: firstSeries.data,
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            formatter: function (_a) {
                                var name = _a.name, percent = _a.percent;
                                return name + "\n" + percent + "%";
                            },
                            show: false,
                            position: 'center',
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: '18',
                            },
                        },
                    },
                    itemStyle: {
                        normal: {
                            label: {
                                show: false,
                            },
                            labelLine: {
                                show: false,
                            },
                        },
                    },
                }),
            ]} xAxis={null} yAxis={null}/>);
    };
    return PieChart;
}(React.Component));
export default PieChart;
//# sourceMappingURL=pieChart.jsx.map
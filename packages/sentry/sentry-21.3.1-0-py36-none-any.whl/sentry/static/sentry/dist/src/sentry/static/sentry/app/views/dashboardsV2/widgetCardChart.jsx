import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import isEqual from 'lodash/isEqual';
import AreaChart from 'app/components/charts/areaChart';
import BarChart from 'app/components/charts/barChart';
import ChartZoom from 'app/components/charts/chartZoom';
import ErrorPanel from 'app/components/charts/errorPanel';
import LineChart from 'app/components/charts/lineChart';
import SimpleTableChart from 'app/components/charts/simpleTableChart';
import TransitionChart from 'app/components/charts/transitionChart';
import TransparentLoadingMask from 'app/components/charts/transparentLoadingMask';
import { getSeriesSelection } from 'app/components/charts/utils';
import WorldMapChart from 'app/components/charts/worldMapChart';
import LoadingIndicator from 'app/components/loadingIndicator';
import Placeholder from 'app/components/placeholder';
import { IconWarning } from 'app/icons';
import space from 'app/styles/space';
import { axisLabelFormatter, tooltipFormatter } from 'app/utils/discover/charts';
import { getFieldFormatter } from 'app/utils/discover/fieldRenderers';
import { getAggregateArg, getMeasurementSlug } from 'app/utils/discover/fields';
import getDynamicText from 'app/utils/getDynamicText';
var WidgetCardChart = /** @class */ (function (_super) {
    __extends(WidgetCardChart, _super);
    function WidgetCardChart() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    WidgetCardChart.prototype.shouldComponentUpdate = function (nextProps) {
        // Widget title changes should not update the WidgetCardChart component tree
        var currentProps = __assign(__assign({}, this.props), { widget: __assign(__assign({}, this.props.widget), { title: '' }) });
        nextProps = __assign(__assign({}, nextProps), { widget: __assign(__assign({}, nextProps.widget), { title: '' }) });
        return !isEqual(currentProps, nextProps);
    };
    WidgetCardChart.prototype.tableResultComponent = function (_a) {
        var loading = _a.loading, errorMessage = _a.errorMessage, tableResults = _a.tableResults;
        var _b = this.props, location = _b.location, widget = _b.widget, organization = _b.organization;
        if (errorMessage) {
            return (<ErrorPanel>
          <IconWarning color="gray500" size="lg"/>
        </ErrorPanel>);
        }
        if (typeof tableResults === 'undefined' || loading) {
            // Align height to other charts.
            return <Placeholder height="200px"/>;
        }
        return tableResults.map(function (result, i) {
            var _a, _b;
            var fields = (_b = (_a = widget.queries[i]) === null || _a === void 0 ? void 0 : _a.fields) !== null && _b !== void 0 ? _b : [];
            return (<StyledSimpleTableChart key={"table:" + result.title} location={location} fields={fields} title={tableResults.length > 1 ? result.title : ''} loading={loading} metadata={result.meta} data={result.data} organization={organization}/>);
        });
    };
    WidgetCardChart.prototype.bigNumberComponent = function (_a) {
        var loading = _a.loading, errorMessage = _a.errorMessage, tableResults = _a.tableResults;
        if (errorMessage) {
            return (<ErrorPanel>
          <IconWarning color="gray500" size="lg"/>
        </ErrorPanel>);
        }
        if (typeof tableResults === 'undefined' || loading) {
            return <BigNumber>{'\u2014'}</BigNumber>;
        }
        return tableResults.map(function (result) {
            var _a;
            var tableMeta = (_a = result.meta) !== null && _a !== void 0 ? _a : {};
            var fields = Object.keys(tableMeta !== null && tableMeta !== void 0 ? tableMeta : {});
            var field = fields[0];
            if (!field || !result.data.length) {
                return <BigNumber key={"big_number:" + result.title}>{'\u2014'}</BigNumber>;
            }
            var dataRow = result.data[0];
            var fieldRenderer = getFieldFormatter(field, tableMeta);
            var rendered = fieldRenderer(dataRow);
            return <BigNumber key={"big_number:" + result.title}>{rendered}</BigNumber>;
        });
    };
    WidgetCardChart.prototype.chartComponent = function (chartProps) {
        var widget = this.props.widget;
        switch (widget.displayType) {
            case 'bar':
                return <BarChart {...chartProps}/>;
            case 'area':
                return <AreaChart stacked {...chartProps}/>;
            case 'world_map':
                return <WorldMapChart {...chartProps}/>;
            case 'line':
            default:
                return <LineChart {...chartProps}/>;
        }
    };
    WidgetCardChart.prototype.render = function () {
        var _this = this;
        var _a, _b, _c;
        var _d = this.props, theme = _d.theme, tableResults = _d.tableResults, timeseriesResults = _d.timeseriesResults, errorMessage = _d.errorMessage, loading = _d.loading, widget = _d.widget;
        if (widget.displayType === 'table') {
            return (<TransitionChart loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          {this.tableResultComponent({ tableResults: tableResults, loading: loading, errorMessage: errorMessage })}
        </TransitionChart>);
        }
        if (widget.displayType === 'big_number') {
            return (<TransitionChart loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          {this.bigNumberComponent({ tableResults: tableResults, loading: loading, errorMessage: errorMessage })}
        </TransitionChart>);
        }
        if (errorMessage) {
            return (<ErrorPanel>
          <IconWarning color="gray500" size="lg"/>
        </ErrorPanel>);
        }
        var _e = this.props, location = _e.location, router = _e.router, selection = _e.selection;
        var _f = selection.datetime, start = _f.start, end = _f.end, period = _f.period, utc = _f.utc;
        if (widget.displayType === 'world_map') {
            var DEFAULT_GEO_DATA_1 = {
                title: '',
                data: [],
            };
            var processTableResults = function () {
                var _a;
                if (!tableResults || !tableResults.length) {
                    return DEFAULT_GEO_DATA_1;
                }
                var tableResult = tableResults[0];
                var data = tableResult.data, meta = tableResult.meta;
                if (!data || !data.length || !meta) {
                    return DEFAULT_GEO_DATA_1;
                }
                var preAggregate = Object.keys(meta).find(function (column) {
                    return column !== 'geo.country_code';
                });
                if (!preAggregate) {
                    return DEFAULT_GEO_DATA_1;
                }
                return {
                    title: (_a = tableResult.title) !== null && _a !== void 0 ? _a : '',
                    data: data
                        .filter(function (row) { return row['geo.country_code']; })
                        .map(function (row) {
                        return { name: row['geo.country_code'], value: row[preAggregate] };
                    }),
                };
            };
            var _g = processTableResults(), data = _g.data, title = _g.title;
            var series = [
                {
                    seriesName: title,
                    data: data,
                },
            ];
            return (<TransitionChart loading={loading} reloading={loading}>
          <LoadingScreen loading={loading}/>
          <ChartWrapper>
            {getDynamicText({
                    value: this.chartComponent({
                        series: series,
                    }),
                    fixed: <Placeholder height="200px" testId="skeleton-ui"/>,
                })}
          </ChartWrapper>
        </TransitionChart>);
        }
        var legend = {
            left: 0,
            top: 0,
            selected: getSeriesSelection(location),
            formatter: function (seriesName) {
                var arg = getAggregateArg(seriesName);
                if (arg !== null) {
                    var slug = getMeasurementSlug(arg);
                    if (slug !== null) {
                        seriesName = slug.toUpperCase();
                    }
                }
                return seriesName;
            },
        };
        var axisField = (_c = (_b = (_a = widget.queries[0]) === null || _a === void 0 ? void 0 : _a.fields) === null || _b === void 0 ? void 0 : _b[0]) !== null && _c !== void 0 ? _c : 'count()';
        var chartOptions = {
            grid: {
                left: 0,
                right: 0,
                top: '40px',
                bottom: 0,
            },
            seriesOptions: {
                showSymbol: false,
            },
            tooltip: {
                trigger: 'axis',
                valueFormatter: tooltipFormatter,
            },
            yAxis: {
                axisLabel: {
                    color: theme.chartLabel,
                    formatter: function (value) { return axisLabelFormatter(value, axisField); },
                },
            },
        };
        return (<ChartZoom router={router} period={period} start={start} end={end} utc={utc}>
        {function (zoomRenderProps) {
                if (errorMessage) {
                    return (<ErrorPanel>
                <IconWarning color="gray500" size="lg"/>
              </ErrorPanel>);
                }
                var colors = timeseriesResults
                    ? theme.charts.getColorPalette(timeseriesResults.length - 2)
                    : [];
                // Create a list of series based on the order of the fields,
                var series = timeseriesResults
                    ? timeseriesResults.map(function (values, i) { return (__assign(__assign({}, values), { color: colors[i] })); })
                    : [];
                return (<TransitionChart loading={loading} reloading={loading}>
              <LoadingScreen loading={loading}/>
              <ChartWrapper>
                {getDynamicText({
                        value: _this.chartComponent(__assign(__assign(__assign({}, zoomRenderProps), chartOptions), { legend: legend,
                            series: series })),
                        fixed: <Placeholder height="200px" testId="skeleton-ui"/>,
                    })}
              </ChartWrapper>
            </TransitionChart>);
            }}
      </ChartZoom>);
    };
    return WidgetCardChart;
}(React.Component));
var StyledTransparentLoadingMask = styled(function (props) { return (<TransparentLoadingMask {...props} maskBackgroundColor="transparent"/>); })(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n"])));
var LoadingScreen = function (_a) {
    var loading = _a.loading;
    if (!loading) {
        return null;
    }
    return (<StyledTransparentLoadingMask visible={loading}>
      <LoadingIndicator mini/>
    </StyledTransparentLoadingMask>);
};
var BigNumber = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: 32px;\n  padding: ", " ", " ", " ", ";\n  * {\n    text-align: left !important;\n  }\n"], ["\n  font-size: 32px;\n  padding: ", " ", " ", " ", ";\n  * {\n    text-align: left !important;\n  }\n"])), space(1), space(3), space(3), space(3));
var ChartWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding: 0 ", " ", ";\n"], ["\n  padding: 0 ", " ", ";\n"])), space(3), space(3));
var StyledSimpleTableChart = styled(SimpleTableChart)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-top: ", ";\n  border-bottom-left-radius: ", ";\n  border-bottom-right-radius: ", ";\n  font-size: ", ";\n  box-shadow: none;\n\n  > div {\n    padding: ", " ", ";\n  }\n"], ["\n  margin-top: ", ";\n  border-bottom-left-radius: ", ";\n  border-bottom-right-radius: ", ";\n  font-size: ", ";\n  box-shadow: none;\n\n  > div {\n    padding: ", " ", ";\n  }\n"])), space(1.5), function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.fontSizeMedium; }, space(1), space(3));
export default withTheme(WidgetCardChart);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=widgetCardChart.jsx.map
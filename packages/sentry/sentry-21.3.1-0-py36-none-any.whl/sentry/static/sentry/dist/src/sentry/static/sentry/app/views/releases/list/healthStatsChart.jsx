import { __extends } from "tslib";
import React from 'react';
import LazyLoad from 'react-lazyload';
import { withTheme } from 'emotion-theming';
import MiniBarChart from 'app/components/charts/miniBarChart';
import { tn } from 'app/locale';
import { DisplayOption } from './utils';
var HealthStatsChart = /** @class */ (function (_super) {
    __extends(HealthStatsChart, _super);
    function HealthStatsChart() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.formatTooltip = function (value) {
            var activeDisplay = _this.props.activeDisplay;
            var suffix = activeDisplay === DisplayOption.USERS
                ? tn('user', 'users', value)
                : tn('session', 'sessions', value);
            return value.toLocaleString() + " " + suffix;
        };
        return _this;
    }
    HealthStatsChart.prototype.render = function () {
        var _a = this.props, height = _a.height, data = _a.data, theme = _a.theme;
        return (<LazyLoad debounce={50} height={height}>
        <MiniBarChart series={data} height={height} isGroupedByDate showTimeInTooltip hideDelay={50} tooltipFormatter={this.formatTooltip} colors={[theme.purple300, theme.gray200]}/>
      </LazyLoad>);
    };
    HealthStatsChart.defaultProps = {
        height: 24,
    };
    return HealthStatsChart;
}(React.Component));
export default withTheme(HealthStatsChart);
//# sourceMappingURL=healthStatsChart.jsx.map
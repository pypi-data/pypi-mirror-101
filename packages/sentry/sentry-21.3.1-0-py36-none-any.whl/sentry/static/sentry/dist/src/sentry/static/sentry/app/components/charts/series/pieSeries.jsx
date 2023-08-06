import { __assign, __rest } from "tslib";
import 'echarts/lib/chart/pie';
export default function PieSeries(props) {
    if (props === void 0) { props = {}; }
    var data = props.data, rest = __rest(props, ["data"]);
    return __assign(__assign({ radius: ['50%', '70%'], data: data }, rest), { type: 'pie' });
}
//# sourceMappingURL=pieSeries.jsx.map
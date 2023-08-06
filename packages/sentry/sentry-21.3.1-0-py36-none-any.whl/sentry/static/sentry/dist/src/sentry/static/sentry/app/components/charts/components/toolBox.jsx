import { __assign, __rest } from "tslib";
import 'echarts/lib/component/toolbox';
function getFeatures(_a) {
    var dataZoom = _a.dataZoom, features = __rest(_a, ["dataZoom"]);
    return __assign(__assign({}, (dataZoom
        ? {
            dataZoom: __assign({ yAxisIndex: 'none', title: {
                    zoom: 'zoom',
                    back: 'undo',
                    restore: 'reset',
                } }, dataZoom),
        }
        : {})), features);
}
export default function ToolBox(options, features) {
    return __assign({ right: 0, top: 0, itemSize: 16, 
        // Stack the toolbox under the legend.
        // so all series names are clickable.
        z: -1, feature: getFeatures(features) }, options);
}
//# sourceMappingURL=toolBox.jsx.map
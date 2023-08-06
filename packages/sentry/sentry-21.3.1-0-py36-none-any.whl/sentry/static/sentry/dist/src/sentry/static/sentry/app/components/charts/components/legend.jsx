import { __rest } from "tslib";
import 'echarts/lib/component/legend';
import 'echarts/lib/component/legendScroll';
import merge from 'lodash/merge';
import { truncationFormatter } from '../utils';
export default function Legend(props) {
    var _a = props !== null && props !== void 0 ? props : {}, truncate = _a.truncate, theme = _a.theme, rest = __rest(_a, ["truncate", "theme"]);
    var formatter = function (value) { return truncationFormatter(value, truncate !== null && truncate !== void 0 ? truncate : 0); };
    return merge({
        show: true,
        type: 'scroll',
        padding: 0,
        formatter: formatter,
        icon: 'circle',
        itemHeight: 14,
        itemWidth: 8,
        itemGap: 12,
        align: 'left',
        textStyle: {
            color: theme.textColor,
            verticalAlign: 'top',
            fontSize: 11,
            fontFamily: theme.text.family,
            lineHeight: 14,
        },
        inactiveColor: theme.inactive,
    }, rest);
}
//# sourceMappingURL=legend.jsx.map
import { __assign, __rest } from "tslib";
import React from 'react';
import omit from 'lodash/omit';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
function getHistogramRequestPayload(props) {
    var fields = props.fields, numBuckets = props.numBuckets, min = props.min, max = props.max, precision = props.precision, dataFilter = props.dataFilter, eventView = props.eventView, location = props.location;
    var baseApiPayload = {
        field: fields,
        numBuckets: numBuckets,
        min: min,
        max: max,
        precision: precision,
        dataFilter: dataFilter,
    };
    var additionalApiPayload = omit(eventView.getEventsAPIPayload(location), [
        'field',
        'sort',
        'per_page',
    ]);
    var apiPayload = Object.assign(baseApiPayload, additionalApiPayload);
    return apiPayload;
}
function beforeFetch(api) {
    api.clear();
}
function HistogramQuery(props) {
    var children = props.children, fields = props.fields;
    if (fields.length === 0) {
        return (<React.Fragment>
        {children({
                isLoading: false,
                error: null,
                pageLinks: null,
                histograms: {},
            })}
      </React.Fragment>);
    }
    return (<GenericDiscoverQuery route="events-histogram" getRequestPayload={getHistogramRequestPayload} beforeFetch={beforeFetch} {...omit(props, 'children')}>
      {function (_a) {
            var tableData = _a.tableData, rest = __rest(_a, ["tableData"]);
            return props.children(__assign({ histograms: tableData }, rest));
        }}
    </GenericDiscoverQuery>);
}
export default withApi(HistogramQuery);
//# sourceMappingURL=histogramQuery.jsx.map
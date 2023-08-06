import React from 'react';
import GenericDiscoverQuery from 'app/utils/discover/genericDiscoverQuery';
import withApi from 'app/utils/withApi';
export function getRequestFunction(_props) {
    var tagOrder = _props.tagOrder, aggregateColumn = _props.aggregateColumn;
    function getTagExplorerRequestPayload(props) {
        var eventView = props.eventView;
        var apiPayload = eventView.getEventsAPIPayload(props.location);
        apiPayload.order = tagOrder;
        apiPayload.aggregateColumn = aggregateColumn;
        return apiPayload;
    }
    return getTagExplorerRequestPayload;
}
function shouldRefetchData(prevProps, nextProps) {
    return (prevProps.tagOrder !== nextProps.tagOrder ||
        prevProps.aggregateColumn !== nextProps.aggregateColumn);
}
function SegmentExplorerQuery(props) {
    return (<GenericDiscoverQuery route="events-facets-performance" getRequestPayload={getRequestFunction(props)} shouldRefetchData={shouldRefetchData} {...props}/>);
}
export default withApi(SegmentExplorerQuery);
//# sourceMappingURL=segmentExplorerQuery.jsx.map
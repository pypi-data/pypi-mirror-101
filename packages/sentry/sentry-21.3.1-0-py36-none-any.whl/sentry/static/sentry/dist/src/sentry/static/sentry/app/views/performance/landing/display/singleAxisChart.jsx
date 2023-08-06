import React from 'react';
import DurationChart from '../chart/durationChart';
import HistogramChart from '../chart/histogramChart';
export function SingleAxisChart(props) {
    var axis = props.axis, onFilterChange = props.onFilterChange, eventView = props.eventView, organization = props.organization;
    return axis.isDistribution ? (<HistogramChart field={axis.field} {...props} onFilterChange={onFilterChange} title={axis.label} titleTooltip={axis.tooltip}/>) : (<DurationChart field={axis.field} eventView={eventView} organization={organization} title={axis.label} titleTooltip={axis.tooltip}/>);
}
//# sourceMappingURL=singleAxisChart.jsx.map
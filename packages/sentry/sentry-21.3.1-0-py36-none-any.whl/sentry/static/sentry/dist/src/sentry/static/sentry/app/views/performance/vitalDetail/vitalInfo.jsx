import React from 'react';
import VitalsCardDiscoverQuery from 'app/utils/performance/vitals/vitalsCardsDiscoverQuery';
import { VitalBar } from '../landing/vitalsCards';
export default function vitalInfo(props) {
    var vital = props.vital, eventView = props.eventView, organization = props.organization, location = props.location, hideBar = props.hideBar, hideStates = props.hideStates, hideVitalPercentNames = props.hideVitalPercentNames, hideDurationDetail = props.hideDurationDetail;
    return (<VitalsCardDiscoverQuery eventView={eventView} orgSlug={organization.slug} location={location} vitals={Array.isArray(vital) ? vital : [vital]}>
      {function (_a) {
            var isLoading = _a.isLoading, vitalsData = _a.vitalsData;
            return (<VitalBar isLoading={isLoading} data={vitalsData} vital={vital} showBar={!hideBar} showStates={!hideStates} showVitalPercentNames={!hideVitalPercentNames} showDurationDetail={!hideDurationDetail}/>);
        }}
    </VitalsCardDiscoverQuery>);
}
//# sourceMappingURL=vitalInfo.jsx.map
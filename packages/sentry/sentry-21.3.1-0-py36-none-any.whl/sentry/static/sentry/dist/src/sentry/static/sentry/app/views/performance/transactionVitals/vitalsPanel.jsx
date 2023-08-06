import { __extends } from "tslib";
import React from 'react';
import { Panel } from 'app/components/panels';
import HistogramQuery from 'app/utils/performance/histogram/histogramQuery';
import { WEB_VITAL_DETAILS } from 'app/utils/performance/vitals/constants';
import VitalsCardDiscoverQuery from 'app/utils/performance/vitals/vitalsCardsDiscoverQuery';
import { decodeScalar } from 'app/utils/queryString';
import { NUM_BUCKETS, VITAL_GROUPS } from './constants';
import VitalCard from './vitalCard';
var VitalsPanel = /** @class */ (function (_super) {
    __extends(VitalsPanel, _super);
    function VitalsPanel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    VitalsPanel.prototype.renderVitalCard = function (vital, isLoading, error, data, histogram, color, min, max, precision) {
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, dataFilter = _a.dataFilter;
        var vitalDetails = WEB_VITAL_DETAILS[vital];
        var zoomed = min !== undefined || max !== undefined;
        return (<HistogramQuery location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} fields={zoomed ? [vital] : []} min={min} max={max} precision={precision} dataFilter={dataFilter}>
        {function (results) {
                var _a, _b;
                var loading = zoomed ? results.isLoading : isLoading;
                var errored = zoomed ? results.error !== null : error;
                var chartData = zoomed ? (_b = (_a = results.histograms) === null || _a === void 0 ? void 0 : _a[vital]) !== null && _b !== void 0 ? _b : histogram : histogram;
                return (<VitalCard location={location} isLoading={loading} error={errored} vital={vital} vitalDetails={vitalDetails} summaryData={data} chartData={chartData} colors={color} eventView={eventView} organization={organization} min={min} max={max} precision={precision}/>);
            }}
      </HistogramQuery>);
    };
    VitalsPanel.prototype.renderVitalGroup = function (group, summaryResults) {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, dataFilter = _a.dataFilter;
        var vitals = group.vitals, colors = group.colors, min = group.min, max = group.max, precision = group.precision;
        var bounds = vitals.reduce(function (allBounds, vital) {
            var slug = WEB_VITAL_DETAILS[vital].slug;
            allBounds[vital] = {
                start: decodeScalar(location.query[slug + "Start"]),
                end: decodeScalar(location.query[slug + "End"]),
            };
            return allBounds;
        }, {});
        return (<HistogramQuery location={location} orgSlug={organization.slug} eventView={eventView} numBuckets={NUM_BUCKETS} fields={vitals} min={min} max={max} precision={precision} dataFilter={dataFilter}>
        {function (multiHistogramResults) {
                var isLoading = summaryResults.isLoading || multiHistogramResults.isLoading;
                var error = summaryResults.error !== null || multiHistogramResults.error !== null;
                return (<React.Fragment>
              {vitals.map(function (vital, index) {
                        var _a, _b, _c, _d, _e;
                        var data = (_b = (_a = summaryResults === null || summaryResults === void 0 ? void 0 : summaryResults.vitalsData) === null || _a === void 0 ? void 0 : _a[vital]) !== null && _b !== void 0 ? _b : null;
                        var histogram = (_d = (_c = multiHistogramResults.histograms) === null || _c === void 0 ? void 0 : _c[vital]) !== null && _d !== void 0 ? _d : [];
                        var _f = (_e = bounds[vital]) !== null && _e !== void 0 ? _e : {}, start = _f.start, end = _f.end;
                        return (<React.Fragment key={vital}>
                    {_this.renderVitalCard(vital, isLoading, error, data, histogram, [colors[index]], parseBound(start, precision), parseBound(end, precision), precision)}
                  </React.Fragment>);
                    })}
            </React.Fragment>);
            }}
      </HistogramQuery>);
    };
    VitalsPanel.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView;
        var allVitals = VITAL_GROUPS.reduce(function (keys, _a) {
            var vitals = _a.vitals;
            return keys.concat(vitals);
        }, []);
        return (<Panel>
        <VitalsCardDiscoverQuery eventView={eventView} orgSlug={organization.slug} location={location} vitals={allVitals}>
          {function (results) { return (<React.Fragment>
              {VITAL_GROUPS.map(function (vitalGroup) { return (<React.Fragment key={vitalGroup.vitals.join('')}>
                  {_this.renderVitalGroup(vitalGroup, results)}
                </React.Fragment>); })}
            </React.Fragment>); }}
        </VitalsCardDiscoverQuery>
      </Panel>);
    };
    return VitalsPanel;
}(React.Component));
function parseBound(boundString, precision) {
    if (boundString === undefined) {
        return undefined;
    }
    else if (precision === undefined || precision === 0) {
        return parseInt(boundString, 10);
    }
    return parseFloat(boundString);
}
export default VitalsPanel;
//# sourceMappingURL=vitalsPanel.jsx.map
import { __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Tag from 'app/components/tag';
import { CandidateDownloadStatus, ImageFeature, } from 'app/types/debugImage';
import { getImageFeatureDescription } from '../utils';
function Features(_a) {
    var download = _a.download;
    var features = [];
    if (download.status === CandidateDownloadStatus.OK ||
        download.status === CandidateDownloadStatus.DELETED ||
        download.status === CandidateDownloadStatus.UNAPPLIED) {
        features = Object.keys(download.features).filter(function (feature) { return download.features[feature]; });
    }
    return (<React.Fragment>
      {Object.keys(ImageFeature).map(function (imageFeature) {
            var _a = getImageFeatureDescription(imageFeature), label = _a.label, description = _a.description;
            var isDisabled = !features.includes(imageFeature);
            return (<StyledTag key={label} disabled={isDisabled} tooltipText={isDisabled ? undefined : description}>
            {label}
          </StyledTag>);
        })}
    </React.Fragment>);
}
export default Features;
var StyledTag = styled(Tag)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  opacity: ", ";\n"], ["\n  opacity: ", ";\n"])), function (p) { return (p.disabled ? '0.35' : 1); });
var templateObject_1;
//# sourceMappingURL=features.jsx.map
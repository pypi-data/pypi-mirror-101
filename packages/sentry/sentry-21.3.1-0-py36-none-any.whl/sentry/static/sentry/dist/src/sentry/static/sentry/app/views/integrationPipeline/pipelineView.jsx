import { __extends } from "tslib";
import React from 'react';
import Indicators from 'app/components/indicators';
import ThemeAndStyleProvider from 'app/themeAndStyleProvider';
import AwsLambdaCloudformation from './awsLambdaCloudformation';
import AwsLambdaFailureDetails from './awsLambdaFailureDetails';
import AwsLambdaFunctionSelect from './awsLambdaFunctionSelect';
import AwsLambdaProjectSelect from './awsLambdaProjectSelect';
/**
 * This component is a wrapper for specific pipeline views for integrations
 */
var pipelineMapper = {
    awsLambdaProjectSelect: [AwsLambdaProjectSelect, 'AWS Lambda Select Project'],
    awsLambdaFunctionSelect: [AwsLambdaFunctionSelect, 'AWS Lambda Select Lambdas'],
    awsLambdaCloudformation: [AwsLambdaCloudformation, 'AWS Lambda Create Cloudformation'],
    awsLambdaFailureDetails: [AwsLambdaFailureDetails, 'AWS Lambda View Failures'],
};
var PipelineView = /** @class */ (function (_super) {
    __extends(PipelineView, _super);
    function PipelineView() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    PipelineView.prototype.componentDidMount = function () {
        // update the title based on our mappings
        var title = this.mapping[1];
        document.title = title;
    };
    Object.defineProperty(PipelineView.prototype, "mapping", {
        get: function () {
            var pipelineName = this.props.pipelineName;
            var mapping = pipelineMapper[pipelineName];
            if (!mapping) {
                throw new Error("Invalid pipeline name " + pipelineName);
            }
            return mapping;
        },
        enumerable: false,
        configurable: true
    });
    PipelineView.prototype.render = function () {
        var Component = this.mapping[0];
        return (<ThemeAndStyleProvider>
        <Indicators className="indicators-container"/>
        <Component {...this.props}/>
      </ThemeAndStyleProvider>);
    };
    return PipelineView;
}(React.Component));
export default PipelineView;
//# sourceMappingURL=pipelineView.jsx.map
import React from 'react';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { loadSdkUpdates } from 'app/actionCreators/sdkUpdates';
import SdkUpdatesStore from 'app/stores/sdkUpdatesStore';
import withApi from './withApi';
import withOrganization from './withOrganization';
function withSdkUpdates(WrappedComponent) {
    var ProjectSdkSuggestions = createReactClass({
        mixins: [Reflux.listenTo(SdkUpdatesStore, 'onSdkUpdatesUpdate')],
        getInitialState: function () {
            return { sdkUpdates: [] };
        },
        componentDidMount: function () {
            var orgSlug = this.props.organization.slug;
            var updates = SdkUpdatesStore.getUpdates(orgSlug);
            // Load SdkUpdates
            if (updates !== undefined) {
                this.onSdkUpdatesUpdate();
                return;
            }
            loadSdkUpdates(this.props.api, orgSlug);
        },
        onSdkUpdatesUpdate: function () {
            var _a;
            var sdkUpdates = (_a = SdkUpdatesStore.getUpdates(this.props.organization.slug)) !== null && _a !== void 0 ? _a : null;
            this.setState({ sdkUpdates: sdkUpdates });
        },
        render: function () {
            return (<WrappedComponent {...this.props} sdkUpdates={this.state.sdkUpdates}/>);
        },
    });
    return withOrganization(withApi(ProjectSdkSuggestions));
}
export default withSdkUpdates;
//# sourceMappingURL=withSdkUpdates.jsx.map
import Reflux from 'reflux';
import SdkUpdatesActions from 'app/actions/sdkUpdatesActions';
var storeConfig = {
    orgSdkUpdates: new Map(),
    init: function () {
        this.listenTo(SdkUpdatesActions.load, this.onLoadSuccess);
    },
    onLoadSuccess: function (orgSlug, data) {
        this.orgSdkUpdates.set(orgSlug, data);
        this.trigger(this.orgSdkUpdates);
    },
    getUpdates: function (orgSlug) {
        return this.orgSdkUpdates.get(orgSlug);
    },
    isSdkUpdatesLoaded: function (orgSlug) {
        return this.orgSdkUpdates.has(orgSlug);
    },
};
var SdkUpdatesStore = Reflux.createStore(storeConfig);
export default SdkUpdatesStore;
//# sourceMappingURL=sdkUpdatesStore.jsx.map
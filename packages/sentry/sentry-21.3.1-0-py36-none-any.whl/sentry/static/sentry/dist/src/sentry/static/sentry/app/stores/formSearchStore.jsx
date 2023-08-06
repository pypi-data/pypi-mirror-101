import Reflux from 'reflux';
import FormSearchActions from 'app/actions/formSearchActions';
/**
 * Store for "form" searches, but probably will include more
 */
var formSearchStoreConfig = {
    searchMap: null,
    init: function () {
        this.reset();
        this.listenTo(FormSearchActions.loadSearchMap, this.onLoadSearchMap);
    },
    getInitialState: function () {
        return this.searchMap;
    },
    reset: function () {
        // `null` means it hasn't been loaded yet
        this.searchMap = null;
    },
    /**
     * Adds to search map
     */
    onLoadSearchMap: function (searchMap) {
        // Only load once
        if (this.searchMap !== null) {
            return;
        }
        this.searchMap = searchMap;
        this.trigger(this.searchMap);
    },
};
var FormSearchStore = Reflux.createStore(formSearchStoreConfig);
export default FormSearchStore;
//# sourceMappingURL=formSearchStore.jsx.map
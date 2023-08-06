import Reflux from 'reflux';
import SidebarPanelActions from '../actions/sidebarPanelActions';
var sidebarPanelStoreConfig = {
    activePanel: '',
    init: function () {
        this.listenTo(SidebarPanelActions.activatePanel, this.onActivatePanel);
        this.listenTo(SidebarPanelActions.hidePanel, this.onHidePanel);
        this.listenTo(SidebarPanelActions.togglePanel, this.onTogglePanel);
    },
    onActivatePanel: function (panel) {
        this.activePanel = panel;
        this.trigger(this.activePanel);
    },
    onTogglePanel: function (panel) {
        if (this.activePanel === panel) {
            this.onHidePanel();
        }
        else {
            this.onActivatePanel(panel);
        }
    },
    onHidePanel: function () {
        this.activePanel = '';
        this.trigger(this.activePanel);
    },
};
/**
 * This store is used to hold local user preferences
 * Side-effects (like reading/writing to cookies) are done in associated actionCreators
 */
var SidebarPanelStore = Reflux.createStore(sidebarPanelStoreConfig);
export default SidebarPanelStore;
//# sourceMappingURL=sidebarPanelStore.jsx.map
import Reflux from 'reflux';
import ModalActions from 'app/actions/modalActions';
var ModalStore = Reflux.createStore({
    init: function () {
        this.reset();
        this.listenTo(ModalActions.closeModal, this.onCloseModal);
        this.listenTo(ModalActions.openModal, this.onOpenModal);
    },
    reset: function () {
        this.state = {
            renderer: null,
            options: {},
        };
    },
    onCloseModal: function () {
        this.reset();
        this.trigger(this.state);
    },
    onOpenModal: function (renderer, options) {
        this.state = { renderer: renderer, options: options };
        this.trigger(this.state);
    },
});
// TODO(ts): This should be properly typed
export default ModalStore;
//# sourceMappingURL=modalStore.jsx.map
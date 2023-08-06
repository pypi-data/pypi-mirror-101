import React from 'react';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import Checkbox from 'app/components/checkbox';
import { t } from 'app/locale';
import SelectedGroupStore from 'app/stores/selectedGroupStore';
var GroupCheckBox = createReactClass({
    displayName: 'GroupCheckBox',
    mixins: [Reflux.listenTo(SelectedGroupStore, 'onSelectedGroupChange')],
    getInitialState: function () {
        return {
            isSelected: SelectedGroupStore.isSelected(this.props.id),
        };
    },
    componentWillReceiveProps: function (nextProps) {
        if (nextProps.id !== this.props.id) {
            this.setState({
                isSelected: SelectedGroupStore.isSelected(nextProps.id),
            });
        }
    },
    shouldComponentUpdate: function (_nextProps, nextState) {
        return nextState.isSelected !== this.state.isSelected;
    },
    onSelectedGroupChange: function () {
        var isSelected = SelectedGroupStore.isSelected(this.props.id);
        if (isSelected !== this.state.isSelected) {
            this.setState({
                isSelected: isSelected,
            });
        }
    },
    onSelect: function () {
        var id = this.props.id;
        SelectedGroupStore.toggleSelect(id);
    },
    render: function () {
        var _a = this.props, disabled = _a.disabled, id = _a.id;
        var isSelected = this.state.isSelected;
        return (<Checkbox aria-label={t('Select Issue')} value={id} checked={isSelected} onChange={this.onSelect} disabled={disabled}/>);
    },
});
export default GroupCheckBox;
//# sourceMappingURL=groupCheckBox.jsx.map
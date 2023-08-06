import ConfigStore from 'app/stores/configStore';
import withOrganization from 'app/utils/withOrganization';
/**
 * Component to handle demo mode switches
 */
function DemoModeGate(props) {
    var organization = props.organization, children = props.children, _a = props.demoComponent, demoComponent = _a === void 0 ? null : _a;
    if ((organization === null || organization === void 0 ? void 0 : organization.role) === 'member' && ConfigStore.get('demoMode')) {
        if (typeof demoComponent === 'function') {
            return demoComponent({ children: children });
        }
        return demoComponent;
    }
    return children;
}
export default withOrganization(DemoModeGate);
//# sourceMappingURL=demoModeGate.jsx.map
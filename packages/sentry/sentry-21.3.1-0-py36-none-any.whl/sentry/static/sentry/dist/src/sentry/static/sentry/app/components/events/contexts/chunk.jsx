import { __extends } from "tslib";
import React from 'react';
import EventDataSection from 'app/components/events/eventDataSection';
import { t } from 'app/locale';
import plugins from 'app/plugins';
import { defined, toTitleCase } from 'app/utils';
import { getContextComponent, getSourcePlugin } from './utils';
var Chunk = /** @class */ (function (_super) {
    __extends(Chunk, _super);
    function Chunk() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: false,
        };
        return _this;
    }
    Chunk.prototype.UNSAFE_componentWillMount = function () {
        this.syncPlugin();
    };
    Chunk.prototype.componentDidUpdate = function (prevProps) {
        var _a, _b;
        if (prevProps.type !== this.props.type ||
            ((_a = prevProps.group) === null || _a === void 0 ? void 0 : _a.id) !== ((_b = this.props.group) === null || _b === void 0 ? void 0 : _b.id)) {
            this.syncPlugin();
        }
    };
    Chunk.prototype.syncPlugin = function () {
        var _this = this;
        var _a = this.props, group = _a.group, type = _a.type, alias = _a.alias;
        // If we don't have a grouped event we can't sync with plugins.
        if (!group) {
            return;
        }
        // Search using `alias` first because old plugins rely on it and type is set to "default"
        // e.g. sessionstack
        var sourcePlugin = type === 'default'
            ? getSourcePlugin(group.pluginContexts, alias) ||
                getSourcePlugin(group.pluginContexts, type)
            : getSourcePlugin(group.pluginContexts, type);
        if (!sourcePlugin) {
            this.setState({ pluginLoading: false });
            return;
        }
        this.setState({
            pluginLoading: true,
        }, function () {
            plugins.load(sourcePlugin, function () {
                _this.setState({ pluginLoading: false });
            });
        });
    };
    Chunk.prototype.getTitle = function () {
        var _a = this.props, _b = _a.value, value = _b === void 0 ? {} : _b, alias = _a.alias, type = _a.type;
        if (defined(value.title) && typeof value.title !== 'object') {
            return value.title;
        }
        if (!defined(type)) {
            return toTitleCase(alias);
        }
        switch (type) {
            case 'app':
                return t('App');
            case 'device':
                return t('Device');
            case 'os':
                return t('Operating System');
            case 'user':
                return t('User');
            case 'gpu':
                return t('Graphics Processing Unit');
            case 'runtime':
                return t('Runtime');
            case 'trace':
                return t('Trace Details');
            case 'default':
                if (alias === 'state')
                    return t('Application State');
                return toTitleCase(alias);
            default:
                return toTitleCase(type);
        }
    };
    Chunk.prototype.render = function () {
        var pluginLoading = this.state.pluginLoading;
        // if we are currently loading the plugin, just render nothing for now.
        if (pluginLoading) {
            return null;
        }
        var _a = this.props, type = _a.type, alias = _a.alias, _b = _a.value, value = _b === void 0 ? {} : _b, event = _a.event;
        // we intentionally hide reprocessing context to not imply it was sent by the SDK.
        if (alias === 'reprocessing') {
            return null;
        }
        var Component = type === 'default'
            ? getContextComponent(alias) || getContextComponent(type)
            : getContextComponent(type);
        var isObjectValueEmpty = Object.values(value).filter(function (v) { return defined(v); }).length === 0;
        // this can happen if the component does not exist
        if (!Component || isObjectValueEmpty) {
            return null;
        }
        return (<EventDataSection key={"context-" + alias} type={"context-" + alias} title={<React.Fragment>
            {this.getTitle()}
            {defined(type) && type !== 'default' && alias !== type && (<small>({alias})</small>)}
          </React.Fragment>}>
        <Component alias={alias} event={event} data={value}/>
      </EventDataSection>);
    };
    return Chunk;
}(React.Component));
export default Chunk;
//# sourceMappingURL=chunk.jsx.map
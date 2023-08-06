/* global process */
/**
 * This module is used to define the look and feels for charts rendered via the
 * backend chart rendering service Chartcuterie.
 *
 * Be careful what you import into this file, as it will end up being bundled
 * into the configuration file loaded by the service.
 */
import { discoverCharts } from './discover';
/**
 * All registered style descriptors
 */
var renderConfig = new Map();
/**
 * Chartcuterie configuration object
 */
var config = {
    version: process.env.COMMIT_SHA,
    renderConfig: renderConfig,
};
/**
 * Register a style descriptor
 */
var register = function (renderDescriptor) {
    return renderConfig.set(renderDescriptor.key, renderDescriptor);
};
discoverCharts.forEach(register);
export default config;
//# sourceMappingURL=config.jsx.map
/* eslint no-native-reassign:0 */
var _a;
/**
 * Set the webpack public path at runtime. This is necessary so that imports can be resolved properly
 *
 * NOTE: This MUST be loaded before any other app modules in the entrypoint.
 *
 * XXX(epurkhiser): Currently we only boot with hydration in experimental SPA
 * mode, where assets are *currently not versioned*. We hardcode `/_assets/` here
 * for now as a quick workaround for the index.html being aware of versioned
 * asset paths.
 */
__webpack_public_path__ = ((_a = window.__initialData) === null || _a === void 0 ? void 0 : _a.distPrefix) || '/_assets/';
//# sourceMappingURL=statics-setup.jsx.map
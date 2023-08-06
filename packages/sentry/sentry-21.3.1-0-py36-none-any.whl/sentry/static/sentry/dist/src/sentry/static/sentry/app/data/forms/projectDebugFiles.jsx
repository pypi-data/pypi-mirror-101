import React from 'react';
import forEach from 'lodash/forEach';
import isObject from 'lodash/isObject';
import set from 'lodash/set';
import { openDebugFileSourceModal } from 'app/actionCreators/modal';
import Feature from 'app/components/acl/feature';
import FeatureDisabled from 'app/components/acl/featureDisabled';
import { DEBUG_SOURCE_TYPES } from 'app/data/debugFileSources';
import { t } from 'app/locale';
import TextBlock from 'app/views/settings/components/text/textBlock';
// Export route to make these forms searchable by label/help
export var route = '/settings/:orgId/projects/:projectId/debug-symbols/';
function flattenKeys(obj) {
    var result = {};
    forEach(obj, function (value, key) {
        if (isObject(value)) {
            forEach(value, function (innerValue, innerKey) {
                result[key + "." + innerKey] = innerValue;
            });
        }
        else {
            result[key] = value;
        }
    });
    return result;
}
function unflattenKeys(obj) {
    var result = {};
    forEach(obj, function (value, key) {
        set(result, key.split('.'), value);
    });
    return result;
}
export var fields = {
    builtinSymbolSources: {
        name: 'builtinSymbolSources',
        type: 'select',
        deprecatedSelectControl: false,
        multiple: true,
        label: t('Built-in Repositories'),
        help: t('Configures which built-in repositories Sentry should use to resolve debug files.'),
        formatMessageValue: function (value, _a) {
            var builtinSymbolSources = _a.builtinSymbolSources;
            var rv = [];
            value.forEach(function (key) {
                builtinSymbolSources.forEach(function (source) {
                    if (source.sentry_key === key) {
                        rv.push(source.name);
                    }
                });
            });
            return rv.length ? rv.join(', ') : '\u2014';
        },
        choices: function (_a) {
            var _b;
            var builtinSymbolSources = _a.builtinSymbolSources;
            return (_b = builtinSymbolSources) === null || _b === void 0 ? void 0 : _b.filter(function (source) { return !source.hidden; }).map(function (source) { return [source.sentry_key, t(source.name)]; });
        },
        getValue: function (value) { return (value === null ? [] : value); },
    },
    symbolSources: {
        name: 'symbolSources',
        type: 'rich_list',
        label: t('Custom Repositories'),
        /* eslint-disable-next-line react/prop-types */
        help: function (_a) {
            var organization = _a.organization;
            return (<Feature features={['organizations:custom-symbol-sources']} hookName="feature-disabled:custom-symbol-sources" organization={organization} renderDisabled={function (p) { return (<FeatureDisabled features={p.features} message={t('Custom repositories are disabled.')} featureName={t('custom repositories')}/>); }}>
        {t('Configures custom repositories containing debug files.')}
      </Feature>);
        },
        disabled: function (_a) {
            var features = _a.features;
            return !features.has('custom-symbol-sources');
        },
        formatMessageValue: false,
        addButtonText: t('Add Repository'),
        addDropdown: {
            items: [
                {
                    value: 's3',
                    label: t(DEBUG_SOURCE_TYPES.s3),
                    searchKey: t('aws amazon s3 bucket'),
                },
                {
                    value: 'gcs',
                    label: t(DEBUG_SOURCE_TYPES.gcs),
                    searchKey: t('gcs google cloud storage bucket'),
                },
                {
                    value: 'http',
                    label: t(DEBUG_SOURCE_TYPES.http),
                    searchKey: t('http symbol server ssqp symstore symsrv'),
                },
            ],
        },
        getValue: function (sources) { return JSON.stringify(sources.map(unflattenKeys)); },
        setValue: function (raw) {
            if (!raw) {
                return [];
            }
            return (JSON.parse(raw) || []).map(flattenKeys);
        },
        renderItem: function (item) {
            return item.name ? <span>{item.name}</span> : <em>{t('<Unnamed Repository>')}</em>;
        },
        onAddItem: function (item, addItem) {
            openDebugFileSourceModal({
                sourceType: item.value,
                onSave: addItem,
            });
        },
        onEditItem: function (item, updateItem) {
            openDebugFileSourceModal({
                sourceConfig: item,
                sourceType: item.type,
                onSave: updateItem,
            });
        },
        removeConfirm: {
            confirmText: t('Remove Repository'),
            message: (<React.Fragment>
          <TextBlock>
            <strong>
              {t('Removing this repository applies instantly to new events.')}
            </strong>
          </TextBlock>
          <TextBlock>
            {t('Debug files from this repository will not be used to symbolicate future events. This may create new issues and alert members in your organization.')}
          </TextBlock>
        </React.Fragment>),
        },
    },
};
//# sourceMappingURL=projectDebugFiles.jsx.map
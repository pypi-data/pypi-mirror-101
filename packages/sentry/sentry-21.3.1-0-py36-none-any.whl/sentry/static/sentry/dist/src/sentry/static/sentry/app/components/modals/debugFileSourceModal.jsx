import { __assign, __extends, __read } from "tslib";
import React from 'react';
import ExternalLink from 'app/components/links/externalLink';
import { AWS_REGIONS, DEBUG_SOURCE_CASINGS, DEBUG_SOURCE_LAYOUTS, getDebugSourceName, } from 'app/data/debugFileSources';
import { t, tct } from 'app/locale';
import FieldFromConfig from 'app/views/settings/components/forms/fieldFromConfig';
import Form from 'app/views/settings/components/forms/form';
function objectToChoices(obj) {
    return Object.entries(obj).map(function (_a) {
        var _b = __read(_a, 2), key = _b[0], value = _b[1];
        return [key, t(value)];
    });
}
var commonFields = {
    id: {
        name: 'id',
        type: 'hidden',
        required: true,
        defaultValue: function () { return Math.random().toString(36).substring(2); },
    },
    name: {
        name: 'name',
        type: 'string',
        required: true,
        label: t('Name'),
        placeholder: t('New Repository'),
        help: t('A display name for this repository'),
    },
    // filters are explicitly not exposed to the UI
    layoutType: {
        name: 'layout.type',
        type: 'select',
        label: t('Directory Layout'),
        help: t('The layout of the folder structure.'),
        defaultValue: 'native',
        choices: objectToChoices(DEBUG_SOURCE_LAYOUTS),
    },
    layoutCasing: {
        name: 'layout.casing',
        type: 'select',
        label: t('Path Casing'),
        help: t('The case of files and folders.'),
        defaultValue: 'default',
        choices: objectToChoices(DEBUG_SOURCE_CASINGS),
    },
    prefix: {
        name: 'prefix',
        type: 'string',
        label: 'Root Path',
        placeholder: '/',
        help: t('The path at which files are located within this repository.'),
    },
    separator: {
        name: '',
        type: 'separator',
    },
};
var httpFields = {
    url: {
        name: 'url',
        type: 'url',
        required: true,
        label: t('Download Url'),
        placeholder: 'https://msdl.microsoft.com/download/symbols/',
        help: t('Full URL to the symbol server'),
    },
    username: {
        name: 'username',
        type: 'string',
        required: false,
        label: t('User'),
        placeholder: 'admin',
        help: t('User for HTTP basic auth'),
    },
    password: {
        name: 'password',
        type: 'string',
        required: false,
        label: t('Password'),
        placeholder: 'open-sesame',
        help: t('Password for HTTP basic auth'),
    },
};
var s3Fields = {
    bucket: {
        name: 'bucket',
        type: 'string',
        required: true,
        label: t('Bucket'),
        placeholder: 's3-bucket-name',
        help: t('Name of the S3 bucket. Read permissions are required to download symbols.'),
    },
    region: {
        name: 'region',
        type: 'select',
        required: true,
        label: t('Region'),
        help: t('The AWS region and availability zone of the bucket.'),
        choices: AWS_REGIONS.map(function (_a) {
            var _b = __read(_a, 2), k = _b[0], v = _b[1];
            return [
                k,
                <span key={k}>
        <code>{k}</code> {v}
      </span>,
            ];
        }),
    },
    accessKey: {
        name: 'access_key',
        type: 'string',
        required: true,
        label: t('Access Key ID'),
        placeholder: 'AKIAIOSFODNN7EXAMPLE',
        help: tct('Access key to the AWS account. Credentials can be managed in the [link].', {
            link: (<ExternalLink href="https://console.aws.amazon.com/iam/">
            IAM console
          </ExternalLink>),
        }),
    },
    secretKey: {
        name: 'secret_key',
        type: 'string',
        required: true,
        label: t('Secret Access Key'),
        placeholder: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
    },
};
var gcsFields = {
    bucket: {
        name: 'bucket',
        type: 'string',
        required: true,
        label: t('Bucket'),
        placeholder: 'gcs-bucket-name',
        help: t('Name of the GCS bucket. Read permissions are required to download symbols.'),
    },
    clientEmail: {
        name: 'client_email',
        type: 'email',
        required: true,
        label: t('Client Email'),
        placeholder: 'user@project.iam.gserviceaccount.com',
        help: t('Email address of the GCS service account.'),
    },
    privateKey: {
        name: 'private_key',
        type: 'string',
        required: true,
        multiline: true,
        autosize: true,
        maxRows: 5,
        rows: 3,
        label: t('Private Key'),
        placeholder: '-----BEGIN PRIVATE KEY-----\n[PRIVATE-KEY]\n-----END PRIVATE KEY-----',
        help: tct('The service account key. Credentials can be managed on the [link].', {
            link: (<ExternalLink href="https://console.cloud.google.com/project/_/iam-admin">
          IAM &amp; Admin Page
        </ExternalLink>),
        }),
    },
};
function getFormFields(type) {
    switch (type) {
        case 'http':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                httpFields.url,
                httpFields.username,
                httpFields.password,
                commonFields.separator,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        case 's3':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                s3Fields.bucket,
                s3Fields.region,
                s3Fields.accessKey,
                s3Fields.secretKey,
                commonFields.separator,
                commonFields.prefix,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        case 'gcs':
            return [
                commonFields.id,
                commonFields.name,
                commonFields.separator,
                gcsFields.bucket,
                gcsFields.clientEmail,
                gcsFields.privateKey,
                commonFields.separator,
                commonFields.prefix,
                commonFields.layoutType,
                commonFields.layoutCasing,
            ];
        default:
            return null;
    }
}
var DebugFileSourceModal = /** @class */ (function (_super) {
    __extends(DebugFileSourceModal, _super);
    function DebugFileSourceModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSave = function (data) {
            var _a = _this.props, sourceType = _a.sourceType, onSave = _a.onSave, closeModal = _a.closeModal;
            onSave(__assign(__assign({}, data), { type: sourceType }));
            closeModal();
        };
        return _this;
    }
    DebugFileSourceModal.prototype.renderForm = function () {
        var _a = this.props, sourceConfig = _a.sourceConfig, sourceType = _a.sourceType;
        var fields = getFormFields(sourceType);
        if (!fields) {
            return null;
        }
        return (<Form allowUndo requireChanges initialData={sourceConfig} onSubmit={this.handleSave} footerClass="modal-footer">
        {fields.map(function (field, i) { return (<FieldFromConfig key={field.name || i} field={field} inline={false} stacked/>); })}
      </Form>);
    };
    DebugFileSourceModal.prototype.render = function () {
        var _a = this.props, closeModal = _a.closeModal, sourceType = _a.sourceType, sourceConfig = _a.sourceConfig, Header = _a.Header;
        var headerText = sourceConfig
            ? 'Update [name] Repository'
            : 'Add [name] Repository';
        return (<React.Fragment>
        <Header closeButton onHide={closeModal}>
          {tct(headerText, { name: getDebugSourceName(sourceType) })}
        </Header>

        {this.renderForm()}
      </React.Fragment>);
    };
    return DebugFileSourceModal;
}(React.Component));
export default DebugFileSourceModal;
//# sourceMappingURL=debugFileSourceModal.jsx.map
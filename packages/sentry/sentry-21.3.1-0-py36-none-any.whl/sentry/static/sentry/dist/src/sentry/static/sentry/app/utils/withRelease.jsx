import { __assign } from "tslib";
import React from 'react';
import createReactClass from 'create-react-class';
import Reflux from 'reflux';
import { getProjectRelease, getReleaseDeploys } from 'app/actionCreators/release';
import ReleaseStore from 'app/stores/releaseStore';
import getDisplayName from 'app/utils/getDisplayName';
var withRelease = function (WrappedComponent) {
    return createReactClass({
        displayName: "withRelease(" + getDisplayName(WrappedComponent) + ")",
        mixins: [Reflux.listenTo(ReleaseStore, 'onStoreUpdate')],
        getInitialState: function () {
            var _a = this.props, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = ReleaseStore.get(projectSlug, releaseVersion);
            return __assign({}, releaseData);
        },
        componentDidMount: function () {
            this.fetchRelease();
            this.fetchDeploys();
        },
        fetchRelease: function () {
            var _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = ReleaseStore.get(projectSlug, releaseVersion);
            var orgSlug = organization.slug;
            if ((!releaseData.release && !releaseData.releaseLoading) ||
                releaseData.releaseError) {
                getProjectRelease(api, { orgSlug: orgSlug, projectSlug: projectSlug, releaseVersion: releaseVersion });
            }
        },
        fetchDeploys: function () {
            var _a = this.props, api = _a.api, organization = _a.organization, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = ReleaseStore.get(projectSlug, releaseVersion);
            var orgSlug = organization.slug;
            if ((!releaseData.deploys && !releaseData.deploysLoading) ||
                releaseData.deploysError) {
                getReleaseDeploys(api, { orgSlug: orgSlug, projectSlug: projectSlug, releaseVersion: releaseVersion });
            }
        },
        onStoreUpdate: function () {
            var _a = this.props, projectSlug = _a.projectSlug, releaseVersion = _a.releaseVersion;
            var releaseData = ReleaseStore.get(projectSlug, releaseVersion);
            this.setState(__assign({}, releaseData));
        },
        render: function () {
            return (<WrappedComponent {...this.props} {...this.state}/>);
        },
    });
};
export default withRelease;
//# sourceMappingURL=withRelease.jsx.map
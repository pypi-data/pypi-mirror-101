import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import ExternalLink from 'app/components/links/externalLink';
import Pagination from 'app/components/pagination';
import { PanelTable } from 'app/components/panels';
import SearchBar from 'app/components/searchBar';
import { t, tct } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import ProjectProguardRow from './projectProguardRow';
var ProjectProguard = /** @class */ (function (_super) {
    __extends(ProjectProguard, _super);
    function ProjectProguard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (id) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                loading: true,
            });
            _this.api.request("/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + encodeURIComponent(id), {
                method: 'DELETE',
                complete: function () { return _this.fetchData(); },
            });
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        return _this;
    }
    ProjectProguard.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitleGen(t('ProGuard Mappings'), projectId, false);
    };
    ProjectProguard.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { mappings: [] });
    };
    ProjectProguard.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoints = [
            [
                'mappings',
                "/projects/" + orgId + "/" + projectId + "/files/dsyms/",
                { query: { query: location.query.query, file_formats: 'proguard' } },
            ],
        ];
        return endpoints;
    };
    ProjectProguard.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ProjectProguard.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return t('There are no mappings that match your search.');
        }
        return t('There are no mappings for this project.');
    };
    ProjectProguard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectProguard.prototype.renderMappings = function () {
        var _this = this;
        var mappings = this.state.mappings;
        var _a = this.props, organization = _a.organization, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        if (!(mappings === null || mappings === void 0 ? void 0 : mappings.length)) {
            return null;
        }
        return mappings.map(function (mapping) {
            var downloadUrl = _this.api.baseUrl + "/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + encodeURIComponent(mapping.id);
            return (<ProjectProguardRow mapping={mapping} downloadUrl={downloadUrl} onDelete={_this.handleDelete} downloadRole={organization.debugFilesRole} key={mapping.id}/>);
        });
    };
    ProjectProguard.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, mappings = _a.mappings, mappingsPageLinks = _a.mappingsPageLinks;
        return (<React.Fragment>
        <SettingsPageHeader title={t('ProGuard Mappings')} action={<SearchBar placeholder={t('Filter mappings')} onSearch={this.handleSearch} query={this.getQuery()} width="280px"/>}/>

        <TextBlock>
          {tct("ProGuard mapping files are used to convert minified classes, methods and field names into a human readable format. To learn more about proguard mapping files, [link: read the docs].", {
                link: (<ExternalLink href="https://docs.sentry.io/platforms/android/proguard/"/>),
            })}
        </TextBlock>

        <StyledPanelTable headers={[
                t('Mapping'),
                <SizeColumn key="size">{t('File Size')}</SizeColumn>,
                '',
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={(mappings === null || mappings === void 0 ? void 0 : mappings.length) === 0} isLoading={loading}>
          {this.renderMappings()}
        </StyledPanelTable>
        <Pagination pageLinks={mappingsPageLinks}/>
      </React.Fragment>);
    };
    return ProjectProguard;
}(AsyncView));
var StyledPanelTable = styled(PanelTable)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  grid-template-columns: minmax(220px, 1fr) max-content 120px;\n"], ["\n  grid-template-columns: minmax(220px, 1fr) max-content 120px;\n"])));
var SizeColumn = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
export default ProjectProguard;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectProguard.jsx.map
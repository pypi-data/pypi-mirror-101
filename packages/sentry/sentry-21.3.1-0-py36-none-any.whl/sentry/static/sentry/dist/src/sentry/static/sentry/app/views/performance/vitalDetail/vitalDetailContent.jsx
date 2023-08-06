import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { browserHistory } from 'react-router';
import styled from '@emotion/styled';
import omit from 'lodash/omit';
import Feature from 'app/components/acl/feature';
import Alert from 'app/components/alert';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { CreateAlertFromViewButton } from 'app/components/createAlertButton';
import SearchBar from 'app/components/events/searchBar';
import * as Layout from 'app/components/layouts/thirds';
import { getParams } from 'app/components/organizations/globalSelectionHeader/getParams';
import { IconChevron } from 'app/icons';
import { IconFlag } from 'app/icons/iconFlag';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { generateQueryWithTag } from 'app/utils';
import { WebVital } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import withProjects from 'app/utils/withProjects';
import Breadcrumb from '../breadcrumb';
import { getTransactionSearchQuery } from '../utils';
import Table from './table';
import { vitalDescription, vitalMap } from './utils';
import VitalChart from './vitalChart';
import VitalInfo from './vitalInfo';
var FRONTEND_VITALS = [WebVital.FCP, WebVital.LCP, WebVital.FID, WebVital.CLS];
function getSummaryConditions(query) {
    var parsed = tokenizeSearch(query);
    parsed.query = [];
    return stringifyQueryObject(parsed);
}
var VitalDetailContent = /** @class */ (function (_super) {
    __extends(VitalDetailContent, _super);
    function VitalDetailContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            incompatibleAlertNotice: null,
            error: undefined,
        };
        _this.handleSearch = function (query) {
            var location = _this.props.location;
            var queryParams = getParams(__assign(__assign({}, (location.query || {})), { query: query }));
            // do not propagate pagination when making a new search
            var searchQueryParams = omit(queryParams, 'cursor');
            browserHistory.push({
                pathname: location.pathname,
                query: searchQueryParams,
            });
        };
        _this.generateTagUrl = function (key, value) {
            var location = _this.props.location;
            var query = generateQueryWithTag(location.query, { key: key, value: value });
            return __assign(__assign({}, location), { query: query });
        };
        _this.handleIncompatibleQuery = function (incompatibleAlertNoticeFn, _errors) {
            var incompatibleAlertNotice = incompatibleAlertNoticeFn(function () {
                return _this.setState({ incompatibleAlertNotice: null });
            });
            _this.setState({ incompatibleAlertNotice: incompatibleAlertNotice });
        };
        _this.setError = function (error) {
            _this.setState({ error: error });
        };
        return _this;
    }
    VitalDetailContent.prototype.renderCreateAlertButton = function () {
        var _a = this.props, eventView = _a.eventView, organization = _a.organization, projects = _a.projects;
        return (<CreateAlertFromViewButton eventView={eventView} organization={organization} projects={projects} onIncompatibleQuery={this.handleIncompatibleQuery} onSuccess={function () { }} referrer="performance"/>);
    };
    VitalDetailContent.prototype.renderVitalSwitcher = function () {
        var _a = this.props, vitalName = _a.vitalName, location = _a.location;
        var position = FRONTEND_VITALS.indexOf(vitalName);
        if (position < 0) {
            return null;
        }
        var previousDisabled = position === 0;
        var nextDisabled = position === FRONTEND_VITALS.length - 1;
        var switchVital = function (newVitalName) {
            return function () {
                browserHistory.push({
                    pathname: location.pathname,
                    query: __assign(__assign({}, location.query), { vitalName: newVitalName }),
                });
            };
        };
        return (<ButtonBar merged>
        <Button icon={<IconChevron direction="left" size="sm"/>} aria-label={t('Previous')} disabled={previousDisabled} onClick={switchVital(FRONTEND_VITALS[position - 1])}/>
        <Button icon={<IconChevron direction="right" size="sm"/>} aria-label={t('Next')} disabled={nextDisabled} onClick={switchVital(FRONTEND_VITALS[position + 1])}/>
      </ButtonBar>);
    };
    VitalDetailContent.prototype.renderError = function () {
        var error = this.state.error;
        if (!error) {
            return null;
        }
        return (<Alert type="error" icon={<IconFlag size="md"/>}>
        {error}
      </Alert>);
    };
    VitalDetailContent.prototype.render = function () {
        var _this = this;
        var _a = this.props, location = _a.location, eventView = _a.eventView, organization = _a.organization, vitalName = _a.vitalName, projects = _a.projects;
        var incompatibleAlertNotice = this.state.incompatibleAlertNotice;
        var query = decodeScalar(location.query.query, '');
        var vital = vitalName || WebVital.LCP;
        var filterString = getTransactionSearchQuery(location);
        var summaryConditions = getSummaryConditions(filterString);
        var description = vitalDescription[vitalName];
        return (<React.Fragment>
        <Layout.Header>
          <Layout.HeaderContent>
            <Breadcrumb organization={organization} location={location} vitalName={vital}/>
            <Layout.Title>{vitalMap[vital]}</Layout.Title>
          </Layout.HeaderContent>
          <Layout.HeaderActions>
            <ButtonBar gap={1}>
              <Feature organization={organization} features={['incidents']}>
                {function (_a) {
            var hasFeature = _a.hasFeature;
            return hasFeature && _this.renderCreateAlertButton();
        }}
              </Feature>
              {this.renderVitalSwitcher()}
            </ButtonBar>
          </Layout.HeaderActions>
        </Layout.Header>
        <Layout.Body>
          {this.renderError()}
          {incompatibleAlertNotice && (<Layout.Main fullWidth>{incompatibleAlertNotice}</Layout.Main>)}
          <Layout.Main fullWidth>
            <StyledDescription>{description}</StyledDescription>
            <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={this.handleSearch}/>
            <VitalChart organization={organization} query={eventView.query} project={eventView.project} environment={eventView.environment} start={eventView.start} end={eventView.end} statsPeriod={eventView.statsPeriod}/>
            <StyledVitalInfo>
              <VitalInfo eventView={eventView} organization={organization} location={location} vital={vital}/>
            </StyledVitalInfo>
            <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={this.setError} summaryConditions={summaryConditions}/>
          </Layout.Main>
        </Layout.Body>
      </React.Fragment>);
    };
    return VitalDetailContent;
}(React.Component));
var StyledDescription = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  font-size: ", ";\n  margin-bottom: ", ";\n"], ["\n  font-size: ", ";\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, space(3));
var StyledSearchBar = styled(SearchBar)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
var StyledVitalInfo = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(3));
export default withProjects(VitalDetailContent);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=vitalDetailContent.jsx.map
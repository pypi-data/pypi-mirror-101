import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import { browserHistory, withRouter } from 'react-router';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import DropdownControl, { DropdownItem } from 'app/components/dropdownControl';
import SearchBar from 'app/components/events/searchBar';
import { MAX_QUERY_LENGTH } from 'app/constants';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import { generateAggregateFields } from 'app/utils/discover/fields';
import { decodeScalar } from 'app/utils/queryString';
import { stringifyQueryObject, tokenizeSearch } from 'app/utils/tokenizeSearch';
import Charts from '../charts/index';
import { getBackendAxisOptions, getFrontendAxisOptions, getFrontendOtherAxisOptions, } from '../data';
import Table from '../table';
import { getTransactionSearchQuery } from '../utils';
import DoubleAxisDisplay from './display/doubleAxisDisplay';
import { BACKEND_COLUMN_TITLES, FRONTEND_OTHER_COLUMN_TITLES, FRONTEND_PAGELOAD_COLUMN_TITLES, } from './data';
import { getCurrentLandingDisplay, getDefaultDisplayFieldForPlatform, getDisplayAxes, LANDING_DISPLAYS, LandingDisplayField, LEFT_AXIS_QUERY_KEY, RIGHT_AXIS_QUERY_KEY, } from './utils';
import { BackendCards, FrontendCards } from './vitalsCards';
var LandingContent = /** @class */ (function (_super) {
    __extends(LandingContent, _super);
    function LandingContent() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleLandingDisplayChange = function (field) {
            var _a = _this.props, location = _a.location, organization = _a.organization, eventView = _a.eventView, projects = _a.projects;
            var newQuery = __assign({}, location.query);
            delete newQuery[LEFT_AXIS_QUERY_KEY];
            delete newQuery[RIGHT_AXIS_QUERY_KEY];
            var defaultDisplay = getDefaultDisplayFieldForPlatform(projects, eventView);
            var currentDisplay = decodeScalar(location.query.landingDisplay);
            trackAnalyticsEvent({
                eventKey: 'performance_views.landingv2.display_change',
                eventName: 'Performance Views: Landing v2 Display Change',
                organization_id: parseInt(organization.id, 10),
                change_to_display: field,
                default_display: defaultDisplay,
                current_display: currentDisplay,
                is_default: defaultDisplay === currentDisplay,
            });
            browserHistory.push({
                pathname: location.pathname,
                query: __assign(__assign({}, newQuery), { landingDisplay: field }),
            });
        };
        _this.renderLandingFrontend = function (isPageload) {
            var _a = _this.props, organization = _a.organization, location = _a.location, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            var columnTitles = isPageload
                ? FRONTEND_PAGELOAD_COLUMN_TITLES
                : FRONTEND_OTHER_COLUMN_TITLES;
            var axisOptions = isPageload
                ? getFrontendAxisOptions(organization)
                : getFrontendOtherAxisOptions(organization);
            var _b = getDisplayAxes(axisOptions, location), leftAxis = _b.leftAxis, rightAxis = _b.rightAxis;
            return (<React.Fragment>
        {isPageload && (<FrontendCards eventView={eventView} organization={organization} location={location} projects={projects}/>)}
        <DoubleAxisDisplay eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </React.Fragment>);
        };
        _this.renderLandingBackend = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            var axisOptions = getBackendAxisOptions(organization);
            var _b = getDisplayAxes(axisOptions, location), leftAxis = _b.leftAxis, rightAxis = _b.rightAxis;
            var columnTitles = BACKEND_COLUMN_TITLES;
            return (<React.Fragment>
        <BackendCards eventView={eventView} organization={organization} location={location}/>
        <DoubleAxisDisplay eventView={eventView} organization={organization} location={location} axisOptions={axisOptions} leftAxis={leftAxis} rightAxis={rightAxis}/>
        <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()} columnTitles={columnTitles}/>
      </React.Fragment>);
        };
        _this.renderLandingAll = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, router = _a.router, projects = _a.projects, eventView = _a.eventView, setError = _a.setError;
            return (<React.Fragment>
        <Charts eventView={eventView} organization={organization} location={location} router={router}/>
        <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={eventView.getQueryWithAdditionalConditions()}/>
      </React.Fragment>);
        };
        _this.renderLandingV1 = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location, router = _a.router, projects = _a.projects, eventView = _a.eventView, setError = _a.setError, handleSearch = _a.handleSearch;
            var filterString = getTransactionSearchQuery(location, eventView.query);
            var summaryConditions = _this.getSummaryConditions(filterString);
            return (<React.Fragment>
        <StyledSearchBar organization={organization} projectIds={eventView.project} query={filterString} fields={generateAggregateFields(organization, __spreadArray(__spreadArray([], __read(eventView.fields)), [{ field: 'tps()' }]), ['epm()', 'eps()'])} onSearch={handleSearch} maxQueryLength={MAX_QUERY_LENGTH}/>
        <Feature features={['performance-vitals-overview']}>
          <FrontendCards eventView={eventView} organization={organization} location={location} projects={projects} frontendOnly/>
        </Feature>
        <Charts eventView={eventView} organization={organization} location={location} router={router}/>
        <Table eventView={eventView} projects={projects} organization={organization} location={location} setError={setError} summaryConditions={summaryConditions}/>
      </React.Fragment>);
        };
        return _this;
    }
    LandingContent.prototype.componentDidMount = function () {
        var organization = this.props.organization;
        trackAnalyticsEvent({
            eventKey: 'performance_views.landingv2.content',
            eventName: 'Performance Views: Landing V2 Content',
            organization_id: parseInt(organization.id, 10),
        });
    };
    LandingContent.prototype.getSummaryConditions = function (query) {
        var parsed = tokenizeSearch(query);
        parsed.query = [];
        return stringifyQueryObject(parsed);
    };
    LandingContent.prototype.renderLandingV2 = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, location = _a.location, eventView = _a.eventView, projects = _a.projects, handleSearch = _a.handleSearch;
        if (!this._haveTrackedLandingV2) {
            trackAnalyticsEvent({
                eventKey: 'performance_views.landingv2.new_landing',
                eventName: 'Performance Views: Landing V2 New Landing',
                organization_id: parseInt(organization.id, 10),
            });
            this._haveTrackedLandingV2 = true;
        }
        var currentLandingDisplay = getCurrentLandingDisplay(location, projects, eventView);
        var filterString = getTransactionSearchQuery(location, eventView.query);
        return (<React.Fragment>
        <SearchContainer>
          <StyledSearchBar organization={organization} projectIds={eventView.project} query={filterString} fields={generateAggregateFields(organization, __spreadArray(__spreadArray([], __read(eventView.fields)), [{ field: 'tps()' }]), ['epm()', 'eps()'])} onSearch={handleSearch} maxQueryLength={MAX_QUERY_LENGTH}/>
          <ProjectTypeDropdown>
            <DropdownControl buttonProps={{ prefix: t('Display') }} label={currentLandingDisplay.label}>
              {LANDING_DISPLAYS.map(function (_a) {
                var label = _a.label, field = _a.field;
                return (<DropdownItem key={field} onSelect={_this.handleLandingDisplayChange} eventKey={field} data-test-id={field} isActive={field === currentLandingDisplay.field}>
                  {label}
                </DropdownItem>);
            })}
            </DropdownControl>
          </ProjectTypeDropdown>
        </SearchContainer>
        {this.renderSelectedDisplay(currentLandingDisplay.field)}
      </React.Fragment>);
    };
    LandingContent.prototype.renderSelectedDisplay = function (display) {
        switch (display) {
            case LandingDisplayField.ALL:
                return this.renderLandingAll();
            case LandingDisplayField.FRONTEND_PAGELOAD:
                return this.renderLandingFrontend(true);
            case LandingDisplayField.FRONTEND_OTHER:
                return this.renderLandingFrontend(false);
            case LandingDisplayField.BACKEND:
                return this.renderLandingBackend();
            default:
                throw new Error("Unknown display: " + display);
        }
    };
    LandingContent.prototype.render = function () {
        var _this = this;
        var organization = this.props.organization;
        return (<div>
        <Feature organization={organization} features={['performance-landing-v2']}>
          {function (_a) {
                var hasFeature = _a.hasFeature;
                return hasFeature ? _this.renderLandingV2() : _this.renderLandingV1();
            }}
        </Feature>
      </div>);
    };
    return LandingContent;
}(React.Component));
var SearchContainer = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr min-content;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr min-content;\n"])));
var ProjectTypeDropdown = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  margin-left: ", ";\n"], ["\n  margin-left: ", ";\n"])), space(1));
var StyledSearchBar = styled(SearchBar)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  flex-grow: 1;\n  margin-bottom: ", ";\n"], ["\n  flex-grow: 1;\n  margin-bottom: ", ";\n"])), space(2));
export default withRouter(LandingContent);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=content.jsx.map
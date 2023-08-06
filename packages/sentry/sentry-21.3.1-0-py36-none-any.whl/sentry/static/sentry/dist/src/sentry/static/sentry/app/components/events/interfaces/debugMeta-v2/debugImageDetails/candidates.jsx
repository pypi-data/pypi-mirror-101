import { __assign, __extends, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';
import isEqual from 'lodash/isEqual';
import pick from 'lodash/pick';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import PanelTable from 'app/components/panels/panelTable';
import QuestionTooltip from 'app/components/questionTooltip';
import SearchBar from 'app/components/searchBar';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { CandidateDownloadStatus, ImageStatus } from 'app/types/debugImage';
import { defined } from 'app/utils';
import Filter from '../filter';
import Status from './candidate/status';
import Candidate from './candidate';
import { INTERNAL_SOURCE } from './utils';
var filterOptionCategories = {
    status: t('Status'),
    source: t('Source'),
};
var Candidates = /** @class */ (function (_super) {
    __extends(Candidates, _super);
    function Candidates() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            filterOptions: {},
            filteredCandidatesBySearch: [],
            filteredCandidatesByFilter: [],
        };
        _this.doSearch = debounce(_this.filterCandidatesBySearch, 300);
        _this.handleChangeSearchTerm = function (searchTerm) {
            if (searchTerm === void 0) { searchTerm = ''; }
            _this.setState({ searchTerm: searchTerm });
        };
        _this.handleChangeFilter = function (filterOptions) {
            var filteredCandidatesBySearch = _this.state.filteredCandidatesBySearch;
            var filteredCandidatesByFilter = _this.getFilteredCandidatedByFilter(filteredCandidatesBySearch, filterOptions);
            _this.setState({ filterOptions: filterOptions, filteredCandidatesByFilter: filteredCandidatesByFilter });
        };
        _this.handleResetFilter = function () {
            var filterOptions = _this.state.filterOptions;
            _this.setState({
                filterOptions: Object.keys(filterOptions).reduce(function (accumulator, currentValue) {
                    accumulator[currentValue] = filterOptions[currentValue].map(function (filterOption) { return (__assign(__assign({}, filterOption), { isChecked: false })); });
                    return accumulator;
                }, {}),
            }, _this.filterCandidatesBySearch);
        };
        _this.handleResetSearchBar = function () {
            var candidates = _this.props.candidates;
            _this.setState({
                searchTerm: '',
                filteredCandidatesByFilter: candidates,
                filteredCandidatesBySearch: candidates,
            });
        };
        return _this;
    }
    Candidates.prototype.componentDidMount = function () {
        this.getFilters();
    };
    Candidates.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (!isEqual(prevProps.candidates, this.props.candidates)) {
            this.getFilters();
            return;
        }
        if (prevState.searchTerm !== this.state.searchTerm) {
            this.doSearch();
        }
    };
    Candidates.prototype.filterCandidatesBySearch = function () {
        var _a = this.state, searchTerm = _a.searchTerm, filterOptions = _a.filterOptions;
        var candidates = this.props.candidates;
        if (!searchTerm.trim()) {
            var filteredCandidatesByFilter_1 = this.getFilteredCandidatedByFilter(candidates, filterOptions);
            this.setState({
                filteredCandidatesBySearch: candidates,
                filteredCandidatesByFilter: filteredCandidatesByFilter_1,
            });
            return;
        }
        // Slightly hacky, but it works
        // the string is being `stringfy`d here in order to match exactly the same `stringfy`d string of the loop
        var searchFor = JSON.stringify(searchTerm)
            // it replaces double backslash generate by JSON.stringfy with single backslash
            .replace(/((^")|("$))/g, '')
            .toLocaleLowerCase();
        var filteredCandidatesBySearch = candidates.filter(function (obj) {
            return Object.keys(pick(obj, ['source_name', 'location'])).some(function (key) {
                var info = obj[key];
                if (key === 'location' && typeof Number(info) === 'number') {
                    return false;
                }
                if (!defined(info) || !String(info).trim()) {
                    return false;
                }
                return JSON.stringify(info)
                    .replace(/((^")|("$))/g, '')
                    .toLocaleLowerCase()
                    .trim()
                    .includes(searchFor);
            });
        });
        var filteredCandidatesByFilter = this.getFilteredCandidatedByFilter(filteredCandidatesBySearch, filterOptions);
        this.setState({
            filteredCandidatesBySearch: filteredCandidatesBySearch,
            filteredCandidatesByFilter: filteredCandidatesByFilter,
        });
    };
    Candidates.prototype.getFilters = function () {
        var candidates = __spreadArray([], __read(this.props.candidates));
        var filterOptions = this.getFilterOptions(candidates);
        this.setState({
            filterOptions: filterOptions,
            filteredCandidatesBySearch: candidates,
            filteredCandidatesByFilter: this.getFilteredCandidatedByFilter(candidates, filterOptions),
        });
    };
    Candidates.prototype.getFilterOptions = function (candidates) {
        var imageStatus = this.props.imageStatus;
        var filterOptions = {};
        var candidateStatus = __spreadArray([], __read(new Set(candidates.map(function (candidate) { return candidate.download.status; }))));
        if (candidateStatus.length > 1) {
            filterOptions[filterOptionCategories.status] = candidateStatus.map(function (status) { return ({
                id: status,
                symbol: <Status status={status}/>,
                isChecked: status !== CandidateDownloadStatus.NOT_FOUND ||
                    imageStatus === ImageStatus.MISSING,
            }); });
        }
        var candidateSources = __spreadArray([], __read(new Set(candidates.map(function (candidate) { var _a; return (_a = candidate.source_name) !== null && _a !== void 0 ? _a : t('Unknown'); }))));
        if (candidateSources.length > 1) {
            filterOptions[filterOptionCategories.source] = candidateSources.map(function (sourceName) { return ({
                id: sourceName,
                symbol: sourceName,
                isChecked: false,
            }); });
        }
        return filterOptions;
    };
    Candidates.prototype.getFilteredCandidatedByFilter = function (candidates, filterOptions) {
        var _a, _b;
        var checkedStatusOptions = new Set((_a = filterOptions[filterOptionCategories.status]) === null || _a === void 0 ? void 0 : _a.filter(function (filterOption) { return filterOption.isChecked; }).map(function (option) { return option.id; }));
        var checkedSourceOptions = new Set((_b = filterOptions[filterOptionCategories.source]) === null || _b === void 0 ? void 0 : _b.filter(function (filterOption) { return filterOption.isChecked; }).map(function (option) { return option.id; }));
        if (checkedStatusOptions.size === 0 && checkedSourceOptions.size === 0) {
            return candidates;
        }
        if (checkedStatusOptions.size > 0) {
            var filteredByStatus = candidates.filter(function (candidate) {
                return checkedStatusOptions.has(candidate.download.status);
            });
            if (checkedSourceOptions.size === 0) {
                return filteredByStatus;
            }
            return filteredByStatus.filter(function (candidate) { var _a; return checkedSourceOptions.has((_a = candidate === null || candidate === void 0 ? void 0 : candidate.source_name) !== null && _a !== void 0 ? _a : ''); });
        }
        return candidates.filter(function (candidate) { var _a; return checkedSourceOptions.has((_a = candidate === null || candidate === void 0 ? void 0 : candidate.source_name) !== null && _a !== void 0 ? _a : ''); });
    };
    Candidates.prototype.getEmptyMessage = function () {
        var _a = this.state, searchTerm = _a.searchTerm, images = _a.filteredCandidatesByFilter, filterOptions = _a.filterOptions;
        if (!!images.length) {
            return {};
        }
        var hasActiveFilter = Object.values(filterOptions)
            .flatMap(function (filterOption) { return filterOption; })
            .find(function (filterOption) { return filterOption.isChecked; });
        if (searchTerm || hasActiveFilter) {
            return {
                emptyMessage: t('Sorry, no debug files match your search query'),
                emptyAction: hasActiveFilter ? (<Button onClick={this.handleResetFilter} priority="primary">
            {t('Reset filter')}
          </Button>) : (<Button onClick={this.handleResetSearchBar} priority="primary">
            {t('Clear search bar')}
          </Button>),
            };
        }
        return {
            emptyMessage: t('There are no debug files to be displayed'),
        };
    };
    Candidates.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projectId = _a.projectId, baseUrl = _a.baseUrl, builtinSymbolSources = _a.builtinSymbolSources, onDelete = _a.onDelete, isLoading = _a.isLoading, candidates = _a.candidates, eventDateReceived = _a.eventDateReceived, hasReprocessWarning = _a.hasReprocessWarning;
        var _b = this.state, searchTerm = _b.searchTerm, filterOptions = _b.filterOptions, filteredCandidatesByFilter = _b.filteredCandidatesByFilter;
        var haveCandidatesOkOrDeletedDebugFile = candidates.some(function (candidate) {
            return (candidate.download.status === CandidateDownloadStatus.OK &&
                candidate.source === INTERNAL_SOURCE) ||
                candidate.download.status === CandidateDownloadStatus.DELETED;
        });
        var haveCandidatesAtLeastOneAction = haveCandidatesOkOrDeletedDebugFile || hasReprocessWarning;
        return (<Wrapper>
        <Header>
          <Title>
            {t('Debug File Candidates')}
            <QuestionTooltip title={tct('These are the Debug Information Files (DIFs) corresponding to this image which have been looked up on [docLink:symbol servers] during the processing of the stacktrace.', {
                docLink: (<ExternalLink href="https://docs.sentry.io/platforms/native/data-management/debug-files/symbol-servers/"/>),
            })} size="xs" position="top" isHoverable/>
          </Title>
          {!!candidates.length && (<Search>
              <StyledFilter options={filterOptions} onFilter={this.handleChangeFilter}/>
              <StyledSearchBar query={searchTerm} onChange={function (value) { return _this.handleChangeSearchTerm(value); }} placeholder={t('Search debug file candidates')}/>
            </Search>)}
        </Header>
        <StyledPanelTable headers={haveCandidatesAtLeastOneAction
                ? [t('Status'), t('Information'), '']
                : [t('Status'), t('Information')]} isEmpty={!filteredCandidatesByFilter.length} isLoading={isLoading} {...this.getEmptyMessage()}>
          {filteredCandidatesByFilter.map(function (candidate, index) { return (<Candidate key={index} candidate={candidate} builtinSymbolSources={builtinSymbolSources} organization={organization} baseUrl={baseUrl} projectId={projectId} eventDateReceived={eventDateReceived} hasReprocessWarning={hasReprocessWarning} haveCandidatesAtLeastOneAction={haveCandidatesAtLeastOneAction} onDelete={onDelete}/>); })}
        </StyledPanelTable>
      </Wrapper>);
    };
    return Candidates;
}(React.Component));
export default Candidates;
var Wrapper = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n"], ["\n  display: grid;\n"])));
var Header = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  @media (min-width: ", ") {\n    flex-wrap: wrap;\n    flex-direction: row;\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  @media (min-width: ", ") {\n    flex-wrap: wrap;\n    flex-direction: row;\n  }\n"])), function (props) { return props.theme.breakpoints[0]; });
var Title = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  padding-right: ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  font-weight: 600;\n  color: ", ";\n  margin-bottom: ", ";\n"], ["\n  padding-right: ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  font-weight: 600;\n  color: ", ";\n  margin-bottom: ", ";\n"])), space(4), space(0.5), function (p) { return p.theme.gray400; }, space(2));
var Search = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  flex-grow: 1;\n  display: flex;\n  flex-direction: column;\n  justify-content: flex-start;\n  .drop-down-filter-menu {\n    border-top-right-radius: ", ";\n  }\n\n  @media (min-width: ", ") {\n    flex-direction: row;\n    justify-content: flex-end;\n  }\n"], ["\n  flex-grow: 1;\n  display: flex;\n  flex-direction: column;\n  justify-content: flex-start;\n  .drop-down-filter-menu {\n    border-top-right-radius: ", ";\n  }\n\n  @media (min-width: ", ") {\n    flex-direction: row;\n    justify-content: flex-end;\n  }\n"])), function (p) { return p.theme.borderRadius; }, function (props) { return props.theme.breakpoints[0]; });
var StyledFilter = styled(Filter)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space(2));
// TODO(matej): remove this once we refactor SearchBar to not use css classes
// - it could accept size as a prop
var StyledSearchBar = styled(SearchBar)(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  width: 100%;\n  margin-bottom: ", ";\n  position: relative;\n  .search-input {\n    height: 32px;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n\n  @media (min-width: ", ") {\n    max-width: 600px;\n    .search-input,\n    .search-input:focus {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n    }\n  }\n"], ["\n  width: 100%;\n  margin-bottom: ", ";\n  position: relative;\n  .search-input {\n    height: 32px;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n\n  @media (min-width: ", ") {\n    max-width: 600px;\n    .search-input,\n    .search-input:focus {\n      border-top-left-radius: 0;\n      border-bottom-left-radius: 0;\n    }\n  }\n"])), space(2), function (props) { return props.theme.breakpoints[0]; });
var StyledPanelTable = styled(PanelTable)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-template-columns: ", ";\n\n  height: 100%;\n\n  @media (min-width: ", ") {\n    overflow: visible;\n  }\n"], ["\n  grid-template-columns: ",
    ";\n\n  height: 100%;\n\n  @media (min-width: ", ") {\n    overflow: visible;\n  }\n"])), function (p) {
    return p.headers.length === 3 ? 'max-content 1fr max-content' : 'max-content 1fr';
}, function (props) { return props.theme.breakpoints[2]; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=candidates.jsx.map
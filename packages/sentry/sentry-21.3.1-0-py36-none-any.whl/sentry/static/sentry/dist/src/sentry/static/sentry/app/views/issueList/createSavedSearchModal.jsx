import { __extends, __read, __spreadArray } from "tslib";
import React from 'react';
import { addLoadingMessage, clearIndicators } from 'app/actionCreators/indicator';
import { createSavedSearch } from 'app/actionCreators/savedSearches';
import Button from 'app/components/button';
import { SelectField, TextField } from 'app/components/forms';
import { t } from 'app/locale';
import space from 'app/styles/space';
import withApi from 'app/utils/withApi';
import { getSortLabel, IssueSortOptions } from './utils';
var DEFAULT_SORT_OPTIONS = [
    IssueSortOptions.DATE,
    IssueSortOptions.NEW,
    IssueSortOptions.FREQ,
    IssueSortOptions.PRIORITY,
    IssueSortOptions.USER,
];
var CreateSavedSearchModal = /** @class */ (function (_super) {
    __extends(CreateSavedSearchModal, _super);
    function CreateSavedSearchModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isSaving: false,
            name: '',
            error: null,
            query: null,
            sort: null,
        };
        _this.onSubmit = function (e) {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            var query = _this.state.query || _this.props.query;
            var sort = _this.validateSortOption(_this.state.sort || _this.props.sort);
            e.preventDefault();
            _this.setState({ isSaving: true });
            addLoadingMessage(t('Saving Changes'));
            createSavedSearch(api, organization.slug, _this.state.name, query, sort)
                .then(function (_data) {
                _this.props.closeModal();
                _this.setState({
                    error: null,
                    isSaving: false,
                });
                clearIndicators();
            })
                .catch(function (err) {
                var error = t('Unable to save your changes.');
                if (err.responseJSON && err.responseJSON.detail) {
                    error = err.responseJSON.detail;
                }
                _this.setState({
                    error: error,
                    isSaving: false,
                });
                clearIndicators();
            });
        };
        _this.handleChangeName = function (val) {
            _this.setState({ name: String(val) });
        };
        _this.handleChangeQuery = function (val) {
            _this.setState({ query: String(val) });
        };
        _this.handleChangeSort = function (val) {
            _this.setState({ sort: val });
        };
        return _this;
    }
    /** Handle "date added" sort not being available for saved searches */
    CreateSavedSearchModal.prototype.validateSortOption = function (sort) {
        if (this.sortOptions().find(function (option) { return option === sort; })) {
            return sort;
        }
        return IssueSortOptions.DATE;
    };
    CreateSavedSearchModal.prototype.sortOptions = function () {
        var _a;
        var organization = this.props.organization;
        var options = __spreadArray([], __read(DEFAULT_SORT_OPTIONS));
        if ((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('issue-list-trend-sort')) {
            options.push(IssueSortOptions.TREND);
        }
        return options;
    };
    CreateSavedSearchModal.prototype.render = function () {
        var _a = this.state, isSaving = _a.isSaving, error = _a.error;
        var _b = this.props, Header = _b.Header, Footer = _b.Footer, Body = _b.Body, closeModal = _b.closeModal, query = _b.query, sort = _b.sort;
        var sortOptions = this.sortOptions().map(function (sortOption) { return ({
            value: sortOption,
            label: getSortLabel(sortOption),
        }); });
        return (<form onSubmit={this.onSubmit}>
        <Header>
          <h4>{t('Save Current Search')}</h4>
        </Header>

        <Body>
          {this.state.error && (<div className="alert alert-error alert-block">{error}</div>)}

          <p>{t('All team members will now have access to this search.')}</p>
          <TextField key="name" name="name" label={t('Name')} placeholder="e.g. My Search Results" required onChange={this.handleChangeName}/>
          <TextField key="query" name="query" label={t('Query')} value={query} required onChange={this.handleChangeQuery}/>
          <SelectField key="sort" name="sort" label={t('Sort By')} required clearable={false} defaultValue={this.validateSortOption(sort)} options={sortOptions} onChange={this.handleChangeSort}/>
        </Body>
        <Footer>
          <Button priority="default" size="small" disabled={isSaving} onClick={closeModal} style={{ marginRight: space(1) }}>
            {t('Cancel')}
          </Button>
          <Button priority="primary" size="small" disabled={isSaving}>
            {t('Save')}
          </Button>
        </Footer>
      </form>);
    };
    return CreateSavedSearchModal;
}(React.Component));
export default withApi(CreateSavedSearchModal);
//# sourceMappingURL=createSavedSearchModal.jsx.map
import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import styled from '@emotion/styled';
import debounce from 'lodash/debounce';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { navigateTo } from 'app/actionCreators/navigation';
import AutoComplete from 'app/components/autoComplete';
import LoadingIndicator from 'app/components/loadingIndicator';
import SearchResult from 'app/components/search/searchResult';
import SearchResultWrapper from 'app/components/search/searchResultWrapper';
import SearchSources from 'app/components/search/sources';
import ApiSource from 'app/components/search/sources/apiSource';
import CommandSource from 'app/components/search/sources/commandSource';
import FormSource from 'app/components/search/sources/formSource';
import RouteSource from 'app/components/search/sources/routeSource';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import replaceRouterParams from 'app/utils/replaceRouterParams';
// Not using typeof defaultProps because of the wrapping HOC which
// causes defaultProp magic to fall off.
var defaultProps = {
    renderItem: function (_a) {
        var item = _a.item, matches = _a.matches, itemProps = _a.itemProps, highlighted = _a.highlighted;
        return (<SearchResultWrapper {...itemProps} highlighted={highlighted}>
      <SearchResult highlighted={highlighted} item={item} matches={matches}/>
    </SearchResultWrapper>);
    },
    sources: [ApiSource, FormSource, RouteSource, CommandSource],
    closeOnSelect: true,
};
// "Omni" search
var Search = /** @class */ (function (_super) {
    __extends(Search, _super);
    function Search() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSelect = function (item, state) {
            if (!item) {
                return;
            }
            trackAnalyticsEvent({
                eventKey: _this.props.entryPoint + ".select",
                eventName: _this.props.entryPoint + " Select",
                query: state && state.inputValue,
                result_type: item.resultType,
                source_type: item.sourceType,
            });
            var to = item.to, action = item.action;
            // `action` refers to a callback function while
            // `to` is a react-router route
            if (action) {
                action(item, state);
                return;
            }
            if (!to) {
                return;
            }
            if (to.startsWith('http')) {
                var open_1 = window.open();
                if (open_1 === null) {
                    addErrorMessage(t('Unable to open search result (a popup blocker may have caused this).'));
                    return;
                }
                open_1.opener = null;
                open_1.location.href = to;
                return;
            }
            var _a = _this.props, params = _a.params, router = _a.router;
            var nextPath = replaceRouterParams(to, params);
            navigateTo(nextPath, router);
        };
        _this.saveQueryMetrics = debounce(function (query) {
            if (!query) {
                return;
            }
            trackAnalyticsEvent({
                eventKey: _this.props.entryPoint + ".query",
                eventName: _this.props.entryPoint + " Query",
                query: query,
            });
        }, 200);
        _this.renderItem = function (_a) {
            var resultObj = _a.resultObj, index = _a.index, highlightedIndex = _a.highlightedIndex, getItemProps = _a.getItemProps;
            // resultObj is a fuse.js result object with {item, matches, score}
            var renderItem = _this.props.renderItem;
            var highlighted = index === highlightedIndex;
            var item = resultObj.item, matches = resultObj.matches;
            var key = item.title + "-" + index;
            var itemProps = __assign({}, getItemProps({
                item: item,
                index: index,
            }));
            if (typeof renderItem !== 'function') {
                throw new Error('Invalid `renderItem`');
            }
            var renderedItem = renderItem({
                item: item,
                matches: matches,
                index: index,
                highlighted: highlighted,
                itemProps: itemProps,
            });
            return React.cloneElement(renderedItem, { key: key });
        };
        return _this;
    }
    Search.prototype.componentDidMount = function () {
        trackAnalyticsEvent({
            eventKey: this.props.entryPoint + ".open",
            eventName: this.props.entryPoint + " Open",
        });
    };
    Search.prototype.render = function () {
        var _this = this;
        var _a = this.props, params = _a.params, dropdownStyle = _a.dropdownStyle, searchOptions = _a.searchOptions, minSearch = _a.minSearch, maxResults = _a.maxResults, renderInput = _a.renderInput, sources = _a.sources, closeOnSelect = _a.closeOnSelect, resultFooter = _a.resultFooter;
        return (<AutoComplete defaultHighlightedIndex={0} onSelect={this.handleSelect} closeOnSelect={closeOnSelect}>
        {function (_a) {
                var getInputProps = _a.getInputProps, getItemProps = _a.getItemProps, isOpen = _a.isOpen, inputValue = _a.inputValue, highlightedIndex = _a.highlightedIndex;
                var searchQuery = inputValue.toLowerCase().trim();
                var isValidSearch = inputValue.length >= minSearch;
                _this.saveQueryMetrics(searchQuery);
                return (<SearchWrapper>
              {renderInput({ getInputProps: getInputProps })}

              {isValidSearch && isOpen ? (<SearchSources searchOptions={searchOptions} query={searchQuery} params={params} sources={sources !== null && sources !== void 0 ? sources : defaultProps.sources}>
                  {function (_a) {
                            var isLoading = _a.isLoading, results = _a.results, hasAnyResults = _a.hasAnyResults;
                            return (<DropdownBox className={dropdownStyle}>
                      {isLoading && (<LoadingWrapper>
                          <LoadingIndicator mini hideMessage relative/>
                        </LoadingWrapper>)}
                      {!isLoading &&
                                    results.slice(0, maxResults).map(function (resultObj, index) {
                                        return _this.renderItem({
                                            resultObj: resultObj,
                                            index: index,
                                            highlightedIndex: highlightedIndex,
                                            getItemProps: getItemProps,
                                        });
                                    })}
                      {!isLoading && !hasAnyResults && (<EmptyItem>{t('No results found')}</EmptyItem>)}
                      {!isLoading && resultFooter && (<ResultFooter>{resultFooter}</ResultFooter>)}
                    </DropdownBox>);
                        }}
                </SearchSources>) : null}
            </SearchWrapper>);
            }}
      </AutoComplete>);
    };
    Search.defaultProps = defaultProps;
    return Search;
}(React.Component));
export default withRouter(Search);
var DropdownBox = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  background: ", ";\n  border: 1px solid ", ";\n  box-shadow: ", ";\n  position: absolute;\n  top: 36px;\n  right: 0;\n  width: 400px;\n  border-radius: 5px;\n  overflow: auto;\n  max-height: 60vh;\n"], ["\n  background: ", ";\n  border: 1px solid ", ";\n  box-shadow: ", ";\n  position: absolute;\n  top: 36px;\n  right: 0;\n  width: 400px;\n  border-radius: 5px;\n  overflow: auto;\n  max-height: 60vh;\n"])), function (p) { return p.theme.background; }, function (p) { return p.theme.border; }, function (p) { return p.theme.dropShadowHeavy; });
var SearchWrapper = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var ResultFooter = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  position: sticky;\n  bottom: 0;\n  left: 0;\n  right: 0;\n"], ["\n  position: sticky;\n  bottom: 0;\n  left: 0;\n  right: 0;\n"])));
var EmptyItem = styled(SearchResultWrapper)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  text-align: center;\n  padding: 16px;\n  opacity: 0.5;\n"], ["\n  text-align: center;\n  padding: 16px;\n  opacity: 0.5;\n"])));
var LoadingWrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  padding: ", ";\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  padding: ", ";\n"])), space(1));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map
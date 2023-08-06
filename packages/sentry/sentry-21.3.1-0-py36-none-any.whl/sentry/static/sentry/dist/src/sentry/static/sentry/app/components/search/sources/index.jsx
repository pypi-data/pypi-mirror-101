import { __extends } from "tslib";
import React from 'react';
import flatten from 'lodash/flatten';
var SearchSources = /** @class */ (function (_super) {
    __extends(SearchSources, _super);
    function SearchSources() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    // `allSources` will be an array of all result objects from each source
    SearchSources.prototype.renderResults = function (allSources) {
        var children = this.props.children;
        // loading means if any result has `isLoading` OR any result is null
        var isLoading = !!allSources.find(function (arg) { return arg.isLoading || arg.results === null; });
        var foundResults = isLoading
            ? []
            : flatten(allSources.map(function (_a) {
                var results = _a.results;
                return results || [];
            })).sort(function (a, b) { return a.score - b.score; });
        var hasAnyResults = !!foundResults.length;
        return children({
            isLoading: isLoading,
            results: foundResults,
            hasAnyResults: hasAnyResults,
        });
    };
    SearchSources.prototype.renderSources = function (sources, results, idx) {
        var _this = this;
        if (idx >= sources.length) {
            return this.renderResults(results);
        }
        var Source = sources[idx];
        return (<Source {...this.props}>
        {function (args) {
                // Mutate the array instead of pushing because we don't know how often
                // this child function will be called and pushing will cause duplicate
                // results to be pushed for all calls down the chain.
                results[idx] = args;
                return _this.renderSources(sources, results, idx + 1);
            }}
      </Source>);
    };
    SearchSources.prototype.render = function () {
        var sources = this.props.sources;
        return this.renderSources(sources, new Array(sources.length), 0);
    };
    return SearchSources;
}(React.Component));
export default SearchSources;
//# sourceMappingURL=index.jsx.map
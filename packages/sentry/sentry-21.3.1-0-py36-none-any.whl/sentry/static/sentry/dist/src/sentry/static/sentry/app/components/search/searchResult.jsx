import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import styled from '@emotion/styled';
import IdBadge from 'app/components/idBadge';
import { IconInput, IconLink, IconSettings } from 'app/icons';
import PluginIcon from 'app/plugins/components/pluginIcon';
import space from 'app/styles/space';
import highlightFuseMatches from 'app/utils/highlightFuseMatches';
import { StyledSettingsSearch } from 'app/views/settings/components/settingsSearch';
var SearchResult = /** @class */ (function (_super) {
    __extends(SearchResult, _super);
    function SearchResult() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    SearchResult.prototype.renderContent = function () {
        var _a;
        var _b = this.props, highlighted = _b.highlighted, item = _b.item, matches = _b.matches, params = _b.params;
        var sourceType = item.sourceType, model = item.model, extra = item.extra;
        var title = item.title, description = item.description;
        if (matches) {
            // TODO(ts) Type this better.
            var HighlightedMarker = function (p) { return (<HighlightMarker highlighted={highlighted} {...p}/>); };
            var matchedTitle = matches && matches.find(function (_a) {
                var key = _a.key;
                return key === 'title';
            });
            var matchedDescription = matches && matches.find(function (_a) {
                var key = _a.key;
                return key === 'description';
            });
            title = matchedTitle
                ? highlightFuseMatches(matchedTitle, HighlightedMarker)
                : title;
            description = matchedDescription
                ? highlightFuseMatches(matchedDescription, HighlightedMarker)
                : description;
        }
        if (['organization', 'member', 'project', 'team'].includes(sourceType)) {
            var DescriptionNode = (<BadgeDetail highlighted={highlighted}>{description}</BadgeDetail>);
            var badgeProps = (_a = {
                    displayName: title,
                    displayEmail: DescriptionNode,
                    description: DescriptionNode,
                    useLink: false,
                    orgId: params.orgId,
                    avatarSize: 32
                },
                _a[sourceType] = model,
                _a);
            return <IdBadge {...badgeProps}/>;
        }
        return (<React.Fragment>
        <div>
          <SearchTitle>{title}</SearchTitle>
        </div>
        {description && <SearchDetail>{description}</SearchDetail>}
        {extra && <ExtraDetail>{extra}</ExtraDetail>}
      </React.Fragment>);
    };
    SearchResult.prototype.renderResultType = function () {
        var item = this.props.item;
        var resultType = item.resultType, model = item.model;
        var isSettings = resultType === 'settings';
        var isField = resultType === 'field';
        var isRoute = resultType === 'route';
        var isIntegration = resultType === 'integration';
        if (isSettings) {
            return <IconSettings />;
        }
        if (isField) {
            return <IconInput />;
        }
        if (isRoute) {
            return <IconLink />;
        }
        if (isIntegration) {
            return <StyledPluginIcon pluginId={model.slug}/>;
        }
        return null;
    };
    SearchResult.prototype.render = function () {
        return (<Wrapper>
        <Content>{this.renderContent()}</Content>
        <IconWrapper>{this.renderResultType()}</IconWrapper>
      </Wrapper>);
    };
    return SearchResult;
}(React.Component));
export default withRouter(SearchResult);
// This is for tests
var SearchTitle = styled('span')(templateObject_1 || (templateObject_1 = __makeTemplateObject([""], [""])));
var SearchDetail = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  font-size: 0.8em;\n  line-height: 1.3;\n  margin-top: 4px;\n  opacity: 0.8;\n"], ["\n  font-size: 0.8em;\n  line-height: 1.3;\n  margin-top: 4px;\n  opacity: 0.8;\n"])));
var ExtraDetail = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  margin-top: ", ";\n"], ["\n  font-size: ", ";\n  color: ", ";\n  margin-top: ", ";\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.gray300; }, space(0.5));
var BadgeDetail = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  line-height: 1.3;\n  color: ", ";\n"], ["\n  line-height: 1.3;\n  color: ", ";\n"])), function (p) { return (p.highlighted ? p.theme.purple300 : null); });
var Wrapper = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var Content = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n"], ["\n  display: flex;\n  flex-direction: column;\n"])));
var IconWrapper = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  ", " & {\n    color: inherit;\n  }\n"], ["\n  " /* sc-selector*/, " & {\n    color: inherit;\n  }\n"])), /* sc-selector*/ StyledSettingsSearch);
var StyledPluginIcon = styled(PluginIcon)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  flex-shrink: 0;\n"], ["\n  flex-shrink: 0;\n"])));
var HighlightMarker = styled('mark')(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  padding: 0;\n  background: transparent;\n  font-weight: bold;\n  color: ", ";\n"], ["\n  padding: 0;\n  background: transparent;\n  font-weight: bold;\n  color: ", ";\n"])), function (p) { return p.theme.active; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=searchResult.jsx.map
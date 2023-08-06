import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import TextareaAutosize from 'react-autosize-textarea';
import styled from '@emotion/styled';
import { withTheme } from 'emotion-theming';
import moment from 'moment';
import AsyncComponent from 'app/components/asyncComponent';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import Tag from 'app/components/tag';
import { IconGithub, IconGitlab } from 'app/icons';
import { inputStyles } from 'app/styles/input';
import space from 'app/styles/space';
var CodeOwners = /** @class */ (function (_super) {
    __extends(CodeOwners, _super);
    function CodeOwners() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    CodeOwners.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [
            [
                'codeowners',
                "/projects/" + organization.slug + "/" + project.slug + "/codeowners/?expand=codeMapping",
            ],
        ];
    };
    CodeOwners.prototype.renderIcon = function (provider) {
        switch (provider) {
            case 'github':
                return <IconGithub size="md"/>;
            case 'gitlab':
                return <IconGitlab size="md"/>;
            default:
                return null;
        }
    };
    CodeOwners.prototype.renderView = function (data) {
        var theme = this.props.theme;
        var raw = data.raw, dateUpdated = data.dateUpdated, provider = data.provider, repoName = data.codeMapping.repoName;
        return (<Container>
        <RulesHeader>
          <TitleContainer>
            {this.renderIcon(provider)}
            <Title>CODEOWNERS</Title>
          </TitleContainer>
          <ReadOnlyTag type="default">{'Read Only'}</ReadOnlyTag>
          <Repository>{repoName}</Repository>
          <Detail />
        </RulesHeader>
        <RulesView>
          <InnerPanel>
            <InnerPanelHeader>{"Last synced " + moment(dateUpdated).fromNow()}</InnerPanelHeader>
            <InnerPanelBody>
              <StyledTextArea value={raw} spellCheck="false" autoComplete="off" autoCorrect="off" autoCapitalize="off" theme={theme}/>
            </InnerPanelBody>
          </InnerPanel>
        </RulesView>
      </Container>);
    };
    CodeOwners.prototype.renderBody = function () {
        var _this = this;
        var codeowners = this.state.codeowners;
        return codeowners.map(function (codeowner) { return (<React.Fragment key={codeowner.id}>{_this.renderView(codeowner)}</React.Fragment>); });
    };
    return CodeOwners;
}(AsyncComponent));
export default withTheme(CodeOwners);
var Container = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr 2fr;\n  grid-template-areas: 'rules-header rules-view';\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 1fr 2fr;\n  grid-template-areas: 'rules-header rules-view';\n  margin-bottom: ", ";\n"])), space(3));
var RulesHeader = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  grid-area: rules-header;\n  display: grid;\n  grid-template-columns: 2fr 1fr;\n  grid-template-rows: 45px 1fr 1fr 1fr 1fr;\n  grid-template-areas: 'title tag' 'repository repository' '. .' '. .' 'detail detail';\n  border: 1px solid #c6becf;\n  border-radius: 4px 0 0 4px;\n  border-right: none;\n  box-shadow: 0 2px 0 rgb(37 11 54 / 4%);\n  background-color: #ffffff;\n"], ["\n  grid-area: rules-header;\n  display: grid;\n  grid-template-columns: 2fr 1fr;\n  grid-template-rows: 45px 1fr 1fr 1fr 1fr;\n  grid-template-areas: 'title tag' 'repository repository' '. .' '. .' 'detail detail';\n  border: 1px solid #c6becf;\n  border-radius: 4px 0 0 4px;\n  border-right: none;\n  box-shadow: 0 2px 0 rgb(37 11 54 / 4%);\n  background-color: #ffffff;\n"])));
var TitleContainer = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-area: title;\n  align-self: center;\n  padding-left: ", ";\n  display: flex;\n  * {\n    padding-right: ", ";\n  }\n"], ["\n  grid-area: title;\n  align-self: center;\n  padding-left: ", ";\n  display: flex;\n  * {\n    padding-right: ", ";\n  }\n"])), space(2), space(0.5));
var Title = styled('div')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  align-self: center;\n"], ["\n  align-self: center;\n"])));
var ReadOnlyTag = styled(Tag)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  grid-area: tag;\n  align-self: center;\n  justify-self: end;\n  padding-right: ", ";\n"], ["\n  grid-area: tag;\n  align-self: center;\n  justify-self: end;\n  padding-right: ", ";\n"])), space(1));
var Repository = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  grid-area: repository;\n  padding-left: calc(", " + ", ");\n  color: #9386a0;\n  font-size: 14px;\n"], ["\n  grid-area: repository;\n  padding-left: calc(", " + ", ");\n  color: #9386a0;\n  font-size: 14px;\n"])), space(2), space(3));
var Detail = styled('div')(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  grid-area: detail;\n  align-self: end;\n  padding: 0 0 ", " ", ";\n  color: #9386a0;\n  font-size: 14px;\n"], ["\n  grid-area: detail;\n  align-self: end;\n  padding: 0 0 ", " ", ";\n  color: #9386a0;\n  font-size: 14px;\n"])), space(2), space(2));
var RulesView = styled('div')(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  grid-area: rules-view;\n"], ["\n  grid-area: rules-view;\n"])));
var InnerPanel = styled(Panel)(templateObject_9 || (templateObject_9 = __makeTemplateObject(["\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0px;\n  margin: 0px;\n  height: 100%;\n"], ["\n  border-top-left-radius: 0;\n  border-bottom-left-radius: 0px;\n  margin: 0px;\n  height: 100%;\n"])));
var InnerPanelHeader = styled(PanelHeader)(templateObject_10 || (templateObject_10 = __makeTemplateObject(["\n  text-transform: none;\n  font-size: 16px;\n  font-weight: 400;\n"], ["\n  text-transform: none;\n  font-size: 16px;\n  font-weight: 400;\n"])));
var InnerPanelBody = styled(PanelBody)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  height: auto;\n"], ["\n  height: auto;\n"])));
var StyledTextArea = styled(TextareaAutosize)(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  ", ";\n  height: calc(400px - ", " - ", " - ", ") !important;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  line-height: ", ";\n  border: none;\n  box-shadow: none;\n  padding: ", ";\n  color: #9386a0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border: none;\n    box-shadow: none;\n  }\n"], ["\n  ", ";\n  height: calc(400px - ", " - ", " - ", ") !important;\n  overflow: auto;\n  outline: 0;\n  width: 100%;\n  resize: none;\n  margin: 0;\n  font-family: ", ";\n  word-break: break-all;\n  white-space: pre-wrap;\n  line-height: ", ";\n  border: none;\n  box-shadow: none;\n  padding: ", ";\n  color: #9386a0;\n\n  &:hover,\n  &:focus,\n  &:active {\n    border: none;\n    box-shadow: none;\n  }\n"])), inputStyles, space(2), space(1), space(3), function (p) { return p.theme.text.familyMono; }, space(3), space(2));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=codeowners.jsx.map
import { __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Feature from 'app/components/acl/feature';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import { t, tct } from 'app/locale';
import routeTitleGen from 'app/utils/routeTitle';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';
import TextBlock from 'app/views/settings/components/text/textBlock';
import PermissionAlert from 'app/views/settings/project/permissionAlert';
import CodeOwners from 'app/views/settings/project/projectOwnership/codeowners';
import OwnerInput from 'app/views/settings/project/projectOwnership/ownerInput';
var ProjectOwnership = /** @class */ (function (_super) {
    __extends(ProjectOwnership, _super);
    function ProjectOwnership() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectOwnership.prototype.getTitle = function () {
        var project = this.props.project;
        return routeTitleGen(t('Issue Owners'), project.slug, false);
    };
    ProjectOwnership.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [['ownership', "/projects/" + organization.slug + "/" + project.slug + "/ownership/"]];
    };
    ProjectOwnership.prototype.renderBody = function () {
        var _a = this.props, project = _a.project, organization = _a.organization;
        var ownership = this.state.ownership;
        var disabled = !organization.access.includes('project:write');
        return (<React.Fragment>
        <SettingsPageHeader title={t('Issue Owners')} action={<Button to={{
                    pathname: "/organizations/" + organization.slug + "/issues/",
                    query: { project: project.id },
                }} size="small">
              {t('View Issues')}
            </Button>}/>
        <TextBlock>
          {tct("Automatically assign issues and send alerts to the right people based on issue properties. To learn more about Issue Owners, [link:view the docs].", {
                link: (<ExternalLink href="https://docs.sentry.io/product/error-monitoring/issue-owners/"/>),
            })}
        </TextBlock>
        <PermissionAlert />
        <Panel>
          <PanelHeader>{t('Ownership Rules')}</PanelHeader>
          <PanelBody withPadding>
            <Block>
              {t('An owner for an issue can be a team such as ')}{' '}
              <code>#infrastructure</code>
              {t('or a member’s email like ')} <code>tom@sentry.io</code>
              {'. Here are some examples: '}
            </Block>
            <Block>
              <CodeBlock>
                path:src/example/pipeline/* person@sentry.io #infrastructure
                {'\n'}
                url:http://example.com/settings/* #product
                {'\n'}
                tags.sku_class:enterprise #enterprise
                {'\n'}
                module:example.api.base tom@sentry.io
              </CodeBlock>
            </Block>
            <Block>
              {t('These rules follow the pattern: ')}
              <code>matcher:pattern owner1 owner2 ...</code>{' '}
              {t('and the globbing syntax works like this:')}
            </Block>
            <Block>
              <CodeBlock>
                {"* matches everything\n? matches any single character"}
              </CodeBlock>
            </Block>
            <OwnerInput {...this.props} disabled={disabled} initialText={ownership.raw || ''}/>
          </PanelBody>
        </Panel>
        <Feature features={['import-codeowners']}>
          <CodeOwners {...this.props}/>
        </Feature>
        <Form apiEndpoint={"/projects/" + organization.slug + "/" + project.slug + "/ownership/"} apiMethod="PUT" saveOnBlur initialData={{ fallthrough: ownership.fallthrough }} hideFooter>
          <JsonForm forms={[
                {
                    title: t('If ownership cannot be determined for an issue...'),
                    fields: [
                        {
                            name: 'fallthrough',
                            type: 'boolean',
                            label: t('All users with access to this project are issue owners'),
                            help: t('Issue owners will receive notifications for issues they are responsible for.'),
                            disabled: disabled,
                        },
                    ],
                },
            ]}/>
        </Form>

        <Form apiEndpoint={"/projects/" + organization.slug + "/" + project.slug + "/ownership/"} apiMethod="PUT" saveOnBlur initialData={{ autoAssignment: ownership.autoAssignment }} hideFooter>
          <JsonForm forms={[
                {
                    title: t('If a new event matches any of the ownership rules...'),
                    fields: [
                        {
                            name: 'autoAssignment',
                            type: 'boolean',
                            label: t('The issue is assigned to the team or user'),
                            help: t('Issue owners will be automatically assigned.'),
                            disabled: disabled,
                        },
                    ],
                },
            ]}/>
        </Form>
      </React.Fragment>);
    };
    return ProjectOwnership;
}(AsyncView));
export default ProjectOwnership;
var Block = styled(TextBlock)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  margin-bottom: 16px;\n"], ["\n  margin-bottom: 16px;\n"])));
var CodeBlock = styled('pre')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  word-break: break-all;\n  white-space: pre-wrap;\n"], ["\n  word-break: break-all;\n  white-space: pre-wrap;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map
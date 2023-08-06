import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import DocumentTitle from 'react-document-title';
import styled from '@emotion/styled';
import SettingsLayout from 'app/views/settings/components/settingsLayout';
import SettingsNavigation from 'app/views/settings/components/settingsNavigation';
var AdminNavigation = function () { return (<SettingsNavigation stickyTop="0" navigationObjects={[
        {
            name: 'System Status',
            items: [
                { path: '/manage/', index: true, title: 'Overview' },
                { path: '/manage/buffer/', title: 'Buffer' },
                { path: '/manage/queue/', title: 'Queue' },
                { path: '/manage/quotas/', title: 'Quotas' },
                { path: '/manage/status/environment/', title: 'Environment' },
                { path: '/manage/status/packages/', title: 'Packages' },
                { path: '/manage/status/mail/', title: 'Mail' },
                { path: '/manage/status/warnings/', title: 'Warnings' },
                { path: '/manage/settings/', title: 'Settings' },
            ],
        },
        {
            name: 'Manage',
            items: [
                { path: '/manage/organizations/', title: 'Organizations' },
                { path: '/manage/projects/', title: 'Projects' },
                { path: '/manage/users/', title: 'Users' },
            ],
        },
    ]}/>); };
function AdminLayout(_a) {
    var children = _a.children, props = __rest(_a, ["children"]);
    return (<DocumentTitle title="Sentry Admin">
      <Page>
        <SettingsLayout renderNavigation={AdminNavigation} {...props}>
          {children}
        </SettingsLayout>
      </Page>
    </DocumentTitle>);
}
export default AdminLayout;
var Page = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  flex-grow: 1;\n  margin-bottom: -20px;\n"], ["\n  display: flex;\n  flex-grow: 1;\n  margin-bottom: -20px;\n"])));
var templateObject_1;
//# sourceMappingURL=adminLayout.jsx.map
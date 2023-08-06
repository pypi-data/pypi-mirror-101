import { __assign, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import { openInviteMembersModal } from 'app/actionCreators/modal';
import { taskIsDone } from 'app/components/onboardingWizard/utils';
import { sourceMaps } from 'app/data/platformCategories';
import { t } from 'app/locale';
import pulsingIndicatorStyles from 'app/styles/pulsingIndicator';
import space from 'app/styles/space';
import { OnboardingTaskKey, } from 'app/types';
import EventWaiter from 'app/utils/eventWaiter';
import withApi from 'app/utils/withApi';
import withProjects from 'app/utils/withProjects';
function hasPlatformWithSourceMaps(organization) {
    var projects = organization === null || organization === void 0 ? void 0 : organization.projects;
    if (!projects) {
        return false;
    }
    return projects.some(function (_a) {
        var platform = _a.platform;
        return platform && sourceMaps.includes(platform);
    });
}
export function getOnboardingTasks(organization) {
    return [
        {
            task: OnboardingTaskKey.FIRST_PROJECT,
            title: t('Create a project'),
            description: t("Monitor in seconds by adding a simple lines of code to your project. It's as easy as microwaving leftover pizza."),
            skippable: false,
            requisites: [],
            actionType: 'app',
            location: "/organizations/" + organization.slug + "/projects/new/",
            display: true,
        },
        {
            task: OnboardingTaskKey.FIRST_EVENT,
            title: t('Capture your first error'),
            description: t("Time to test it out. Now that you've created a project, capture your first error. We've got an example you can fiddle with."),
            skippable: false,
            requisites: [OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/install/",
            display: true,
            SupplementComponent: withProjects(withApi(function (_a) {
                var api = _a.api, task = _a.task, projects = _a.projects, onCompleteTask = _a.onCompleteTask;
                return projects.length > 0 &&
                    task.requisiteTasks.length === 0 &&
                    !task.completionSeen ? (<EventWaiter api={api} organization={organization} project={projects[0]} eventType="error" onIssueReceived={function () { return !taskIsDone(task) && onCompleteTask(); }}>
              {function () { return <EventWaitingIndicator />; }}
            </EventWaiter>) : null;
            })),
        },
        {
            task: OnboardingTaskKey.INVITE_MEMBER,
            title: t('Invite your team'),
            description: t('Assign issues and comment on shared errors with coworkers so you always know who to blame when sh*t hits the fan.'),
            skippable: true,
            requisites: [],
            actionType: 'action',
            action: function () { return openInviteMembersModal({ source: 'onboarding_widget' }); },
            display: true,
        },
        {
            task: OnboardingTaskKey.SECOND_PLATFORM,
            title: t('Create another project'),
            description: t('Easy, right? Don’t stop at one. Set up another project to keep things running smoothly in both the frontend and backend.'),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/organizations/" + organization.slug + "/projects/new/",
            display: true,
        },
        {
            task: OnboardingTaskKey.FIRST_TRANSACTION,
            title: t('Boost performance'),
            description: t("Don't keep users waiting. Trace transactions, investigate spans and cross-reference related issues for those mission-critical endpoints."),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'external',
            location: 'https://docs.sentry.io/product/performance/getting-started/',
            display: true,
            SupplementComponent: withProjects(withApi(function (_a) {
                var api = _a.api, task = _a.task, projects = _a.projects, onCompleteTask = _a.onCompleteTask;
                return projects.length > 0 &&
                    task.requisiteTasks.length === 0 &&
                    !task.completionSeen ? (<EventWaiter api={api} organization={organization} project={projects[0]} eventType="transaction" onIssueReceived={function () { return !taskIsDone(task) && onCompleteTask(); }}>
              {function () { return <EventWaitingIndicator />; }}
            </EventWaiter>) : null;
            })),
        },
        {
            task: OnboardingTaskKey.USER_CONTEXT,
            title: t('Get more user context'),
            description: t('Enable us to pinpoint which users are suffering from that bad code, so you can debug the problem more swiftly and maybe even apologize for it.'),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'external',
            location: 'https://docs.sentry.io/product/error-monitoring/issue-owners/',
            display: true,
        },
        {
            task: OnboardingTaskKey.RELEASE_TRACKING,
            title: t('Track releases'),
            description: t('Take an in-depth look at the health of each and every release with crash analytics, errors, related issues and suspect commits.'),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/release-tracking/",
            display: true,
        },
        {
            task: OnboardingTaskKey.SOURCEMAPS,
            title: t('Upload source maps'),
            description: t("Deminify Javascript source code to debug with context. Seeing code in it's original form will help you debunk the ghosts of errors past."),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'external',
            location: 'https://docs.sentry.io/platforms/javascript/sourcemaps/',
            display: hasPlatformWithSourceMaps(organization),
        },
        {
            task: OnboardingTaskKey.USER_REPORTS,
            title: 'User crash reports',
            description: t('Collect user feedback when your application crashes'),
            skippable: true,
            requisites: [
                OnboardingTaskKey.FIRST_PROJECT,
                OnboardingTaskKey.FIRST_EVENT,
                OnboardingTaskKey.USER_CONTEXT,
            ],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/user-reports/",
            display: false,
        },
        {
            task: OnboardingTaskKey.ISSUE_TRACKER,
            title: t('Set up issue tracking'),
            description: t('Link to Sentry issues within your issue tracker'),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT, OnboardingTaskKey.FIRST_EVENT],
            actionType: 'app',
            location: "/settings/" + organization.slug + "/projects/:projectId/plugins/",
            display: false,
        },
        {
            task: OnboardingTaskKey.ALERT_RULE,
            title: t('Get smarter alerts'),
            description: t("Customize alerting rules by issue or metric. You'll get the exact information you need precisely when you need it."),
            skippable: true,
            requisites: [OnboardingTaskKey.FIRST_PROJECT],
            actionType: 'app',
            location: "/organizations/" + organization.slug + "/alerts/rules/",
            display: true,
        },
    ];
}
export function getMergedTasks(organization) {
    var taskDescriptors = getOnboardingTasks(organization);
    var serverTasks = organization.onboardingTasks;
    // Map server task state (i.e. completed status) with tasks objects
    var allTasks = taskDescriptors.map(function (desc) {
        return (__assign(__assign(__assign({}, desc), serverTasks.find(function (serverTask) { return serverTask.task === desc.task; })), { requisiteTasks: [] }));
    });
    // Map incomplete requisiteTasks as full task objects
    return allTasks.map(function (task) { return (__assign(__assign({}, task), { requisiteTasks: task.requisites
            .map(function (key) { return allTasks.find(function (task2) { return task2.task === key; }); })
            .filter(function (reqTask) { return reqTask.status !== 'complete'; }) })); });
}
var PulsingIndicator = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  ", ";\n  margin-right: ", ";\n"], ["\n  ", ";\n  margin-right: ", ";\n"])), pulsingIndicatorStyles, space(1));
var EventWaitingIndicator = styled(function (p) { return (<div {...p}>
    <PulsingIndicator />
    {t('Waiting for event')}
  </div>); })(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-grow: 1;\n  font-size: ", ";\n  color: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  flex-grow: 1;\n  font-size: ", ";\n  color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.orange400; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=taskConfig.jsx.map
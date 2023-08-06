import { __makeTemplateObject, __rest } from "tslib";
import React from 'react';
import * as ReactRouter from 'react-router';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import moment from 'moment';
import { navigateTo } from 'app/actionCreators/navigation';
import Avatar from 'app/components/avatar';
import Button from 'app/components/button';
import Card from 'app/components/card';
import LetterAvatar from 'app/components/letterAvatar';
import Tooltip from 'app/components/tooltip';
import { IconCheckmark, IconClose, IconEvent, IconLock } from 'app/icons';
import { t, tct } from 'app/locale';
import space from 'app/styles/space';
import { trackAnalyticsEvent } from 'app/utils/analytics';
import testableTransition from 'app/utils/testableTransition';
import withOrganization from 'app/utils/withOrganization';
import SkipConfirm from './skipConfirm';
import { taskIsDone } from './utils';
var recordAnalytics = function (task, organization, action) {
    return trackAnalyticsEvent({
        eventKey: 'onboarding.wizard_clicked',
        eventName: 'Onboarding Wizard Clicked',
        organization_id: organization.id,
        todo_id: task.task,
        todo_title: task.title,
        action: action,
    });
};
function Task(_a) {
    var router = _a.router, task = _a.task, onSkip = _a.onSkip, onMarkComplete = _a.onMarkComplete, forwardedRef = _a.forwardedRef, organization = _a.organization;
    var handleSkip = function () {
        recordAnalytics(task, organization, 'skipped');
        onSkip(task.task);
    };
    var handleClick = function (e) {
        recordAnalytics(task, organization, 'clickthrough');
        e.stopPropagation();
        if (task.actionType === 'external') {
            window.open(task.location, '_blank');
        }
        if (task.actionType === 'action') {
            task.action();
        }
        if (task.actionType === 'app') {
            navigateTo(task.location + "?onboardingTask", router);
        }
    };
    if (taskIsDone(task) && task.completionSeen) {
        var completedOn = moment(task.dateCompleted);
        return (<TaskCard ref={forwardedRef} onClick={handleClick}>
        <CompleteTitle>
          <StatusIndicator>
            {task.status === 'complete' && <CompleteIndicator />}
            {task.status === 'skipped' && <SkippedIndicator />}
          </StatusIndicator>
          {task.title}
          <DateCompleted title={completedOn.toString()}>
            {completedOn.fromNow()}
          </DateCompleted>
          {task.user ? (<TaskUserAvatar hasTooltip user={task.user}/>) : (<Tooltip containerDisplayMode="inherit" title={t('No user was associated with completing this task')}>
              <TaskBlankAvatar round/>
            </Tooltip>)}
        </CompleteTitle>
      </TaskCard>);
    }
    var IncompleteMarker = task.requisiteTasks.length > 0 && (<Tooltip containerDisplayMode="block" title={tct('[requisite] before completing this task', {
            requisite: task.requisiteTasks[0].title,
        })}>
      <IconLock color="orange400"/>
    </Tooltip>);
    var SupplementComponent = task.SupplementComponent;
    var supplement = SupplementComponent && (<SupplementComponent task={task} onCompleteTask={function () { return onMarkComplete(task.task); }}/>);
    var skipAction = task.skippable && (<SkipConfirm onSkip={handleSkip}>
      {function (_a) {
        var skip = _a.skip;
        return <StyledIconClose size="xs" onClick={skip}/>;
    }}
    </SkipConfirm>);
    return (<TaskCard interactive ref={forwardedRef} onClick={handleClick} data-test-id={task.task}>
      <IncompleteTitle>
        {IncompleteMarker}
        {task.title}
      </IncompleteTitle>
      <Description>{"" + task.description}</Description>
      {task.requisiteTasks.length === 0 && (<ActionBar>
          {skipAction}
          {supplement}
          {task.status === 'pending' ? (<InProgressIndicator user={task.user}/>) : (<Button priority="primary" size="small">
              {t('Start')}
            </Button>)}
        </ActionBar>)}
    </TaskCard>);
}
var TaskCard = styled(Card)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  position: relative;\n  padding: ", " ", ";\n"], ["\n  position: relative;\n  padding: ", " ", ";\n"])), space(2), space(3));
var IncompleteTitle = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-weight: 600;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-weight: 600;\n"])), space(1));
var CompleteTitle = styled(IncompleteTitle)(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  grid-template-columns: min-content 1fr max-content min-content;\n"], ["\n  grid-template-columns: min-content 1fr max-content min-content;\n"])));
var Description = styled('p')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  font-size: ", ";\n  color: ", ";\n  margin: ", " 0 0 0;\n"], ["\n  font-size: ", ";\n  color: ", ";\n  margin: ", " 0 0 0;\n"])), function (p) { return p.theme.fontSizeSmall; }, function (p) { return p.theme.subText; }, space(0.5));
var ActionBar = styled('div')(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-end;\n  margin-top: ", ";\n"], ["\n  display: flex;\n  justify-content: flex-end;\n  align-items: flex-end;\n  margin-top: ", ";\n"])), space(1.5));
var InProgressIndicator = styled(function (_a) {
    var user = _a.user, props = __rest(_a, ["user"]);
    return (<div {...props}>
    <Tooltip disabled={!user} containerDisplayMode="flex" title={tct('This task has been started by [user]', {
            user: user === null || user === void 0 ? void 0 : user.name,
        })}>
      <IconEvent />
    </Tooltip>
    {t('Task in progress...')}
  </div>);
})(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  font-size: ", ";\n  font-weight: bold;\n  color: ", ";\n  display: grid;\n  grid-template-columns: max-content max-content;\n  align-items: center;\n  grid-gap: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.orange400; }, space(1));
var StyledIconClose = styled(IconClose)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  position: absolute;\n  right: ", ";\n  top: ", ";\n  color: ", ";\n"], ["\n  position: absolute;\n  right: ", ";\n  top: ", ";\n  color: ", ";\n"])), space(1.5), space(1.5), function (p) { return p.theme.gray300; });
var transition = testableTransition();
var StatusIndicator = styled(motion.div)(templateObject_8 || (templateObject_8 = __makeTemplateObject(["\n  display: flex;\n"], ["\n  display: flex;\n"])));
StatusIndicator.defaultProps = {
    variants: {
        initial: { opacity: 0, x: 10 },
        animate: { opacity: 1, x: 0 },
    },
    transition: transition,
};
var CompleteIndicator = styled(IconCheckmark)(templateObject_9 || (templateObject_9 = __makeTemplateObject([""], [""])));
CompleteIndicator.defaultProps = {
    isCircled: true,
    color: 'green300',
};
var SkippedIndicator = styled(IconClose)(templateObject_10 || (templateObject_10 = __makeTemplateObject([""], [""])));
SkippedIndicator.defaultProps = {
    isCircled: true,
    color: 'orange400',
};
var completedItemAnimation = {
    initial: { opacity: 0, x: -10 },
    animate: { opacity: 1, x: 0 },
};
var DateCompleted = styled(motion.div)(templateObject_11 || (templateObject_11 = __makeTemplateObject(["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 300;\n"], ["\n  color: ", ";\n  font-size: ", ";\n  font-weight: 300;\n"])), function (p) { return p.theme.subText; }, function (p) { return p.theme.fontSizeSmall; });
DateCompleted.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var TaskUserAvatar = motion.custom(Avatar);
TaskUserAvatar.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var TaskBlankAvatar = styled(motion.custom(LetterAvatar))(templateObject_12 || (templateObject_12 = __makeTemplateObject(["\n  position: unset;\n"], ["\n  position: unset;\n"])));
TaskBlankAvatar.defaultProps = {
    variants: completedItemAnimation,
    transition: transition,
};
var WrappedTask = withOrganization(ReactRouter.withRouter(Task));
export default React.forwardRef(function (props, ref) { return <WrappedTask forwardedRef={ref} {...props}/>; });
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9, templateObject_10, templateObject_11, templateObject_12;
//# sourceMappingURL=task.jsx.map
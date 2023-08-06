import { __assign, __extends, __makeTemplateObject } from "tslib";
import React from 'react';
import styled from '@emotion/styled';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { SelectField } from 'app/components/forms';
import InternalStatChart from 'app/components/internalStatChart';
import { Panel, PanelBody, PanelHeader } from 'app/components/panels';
import AsyncView from 'app/views/asyncView';
var TIME_WINDOWS = ['1h', '1d', '1w'];
var AdminQueue = /** @class */ (function (_super) {
    __extends(AdminQueue, _super);
    function AdminQueue() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminQueue.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { timeWindow: '1w', since: new Date().getTime() / 1000 - 3600 * 24 * 7, resolution: '1h', taskName: null });
    };
    AdminQueue.prototype.getEndpoints = function () {
        return [['taskList', '/internal/queue/tasks/']];
    };
    AdminQueue.prototype.changeWindow = function (timeWindow) {
        var seconds;
        if (timeWindow === '1h') {
            seconds = 3600;
        }
        else if (timeWindow === '1d') {
            seconds = 3600 * 24;
        }
        else if (timeWindow === '1w') {
            seconds = 3600 * 24 * 7;
        }
        else {
            throw new Error('Invalid time window');
        }
        this.setState({
            since: new Date().getTime() / 1000 - seconds,
            timeWindow: timeWindow,
        });
    };
    AdminQueue.prototype.changeTask = function (value) {
        this.setState({ activeTask: value });
    };
    AdminQueue.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, activeTask = _a.activeTask, taskList = _a.taskList;
        return (<div>
        <Header>
          <h3 className="no-border">Queue Overview</h3>

          <ButtonBar merged active={this.state.timeWindow}>
            {TIME_WINDOWS.map(function (r) { return (<Button size="small" barId={r} onClick={function () { return _this.changeWindow(r); }} key={r}>
                {r}
              </Button>); })}
          </ButtonBar>
        </Header>

        <Panel>
          <PanelHeader>Global Throughput</PanelHeader>
          <PanelBody withPadding>
            <InternalStatChart since={this.state.since} resolution={this.state.resolution} stat="jobs.all.started" label="jobs started"/>
          </PanelBody>
        </Panel>

        <h3 className="no-border">Task Details</h3>

        <div>
          <div className="m-b-1">
            <label>Show details for task:</label>
            <SelectField name="task" onChange={function (value) { return _this.changeTask(value); }} value={activeTask} clearable choices={taskList.map(function (t) { return [t, t]; })}/>
          </div>
          {activeTask ? (<div>
              <Panel key={"jobs.started." + activeTask}>
                <PanelHeader>
                  Jobs Started <small>{activeTask}</small>
                </PanelHeader>
                <PanelBody withPadding>
                  <InternalStatChart since={this.state.since} resolution={this.state.resolution} stat={"jobs.started." + activeTask} label="jobs" height={100}/>
                </PanelBody>
              </Panel>
              <Panel key={"jobs.finished." + activeTask}>
                <PanelHeader>
                  Jobs Finished <small>{activeTask}</small>
                </PanelHeader>
                <PanelBody withPadding>
                  <InternalStatChart since={this.state.since} resolution={this.state.resolution} stat={"jobs.finished." + activeTask} label="jobs" height={100}/>
                </PanelBody>
              </Panel>
            </div>) : null}
        </div>
      </div>);
    };
    return AdminQueue;
}(AsyncView));
export default AdminQueue;
var Header = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"], ["\n  display: flex;\n  justify-content: space-between;\n  align-items: center;\n"])));
var templateObject_1;
//# sourceMappingURL=adminQueue.jsx.map
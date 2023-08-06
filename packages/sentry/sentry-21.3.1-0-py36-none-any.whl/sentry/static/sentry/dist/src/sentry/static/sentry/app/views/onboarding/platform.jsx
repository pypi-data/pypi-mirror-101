import { __awaiter, __extends, __generator } from "tslib";
import React from 'react';
import { motion } from 'framer-motion';
import { addErrorMessage } from 'app/actionCreators/indicator';
import { createProject } from 'app/actionCreators/projects';
import ProjectActions from 'app/actions/projectActions';
import Button from 'app/components/button';
import ExternalLink from 'app/components/links/externalLink';
import PlatformPicker from 'app/components/platformPicker';
import { t, tct } from 'app/locale';
import withApi from 'app/utils/withApi';
import withTeams from 'app/utils/withTeams';
import StepHeading from './components/stepHeading';
var OnboardingPlatform = /** @class */ (function (_super) {
    __extends(OnboardingPlatform, _super);
    function OnboardingPlatform() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            firstProjectCreated: false,
            progressing: false,
        };
        _this.handleSetPlatform = function (platform) { return _this.props.onUpdate({ platform: platform }); };
        _this.handleContinue = function () { return __awaiter(_this, void 0, void 0, function () {
            var platform;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ progressing: true });
                        platform = this.props.platform;
                        if (platform === null) {
                            return [2 /*return*/];
                        }
                        // Create their first project if they don't already have one. This is a
                        // no-op if they already have a project.
                        return [4 /*yield*/, this.createFirstProject(platform)];
                    case 1:
                        // Create their first project if they don't already have one. This is a
                        // no-op if they already have a project.
                        _a.sent();
                        this.props.onComplete({});
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    OnboardingPlatform.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.active && !this.props.active) {
            // eslint-disable-next-line react/no-did-update-set-state
            this.setState({ progressing: false });
        }
    };
    Object.defineProperty(OnboardingPlatform.prototype, "hasFirstProject", {
        get: function () {
            return this.props.project || this.state.firstProjectCreated;
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(OnboardingPlatform.prototype, "contineButtonLabel", {
        get: function () {
            if (this.state.progressing) {
                return t('Creating Project...');
            }
            if (!this.hasFirstProject) {
                return t('Create Project');
            }
            if (!this.props.active) {
                return t('Project Created');
            }
            return t('Set Up Your Project');
        },
        enumerable: false,
        configurable: true
    });
    OnboardingPlatform.prototype.createFirstProject = function (platform) {
        return __awaiter(this, void 0, void 0, function () {
            var _a, api, orgId, teams, data, error_1;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, teams = _a.teams;
                        if (this.hasFirstProject) {
                            return [2 /*return*/];
                        }
                        if (teams.length < 1) {
                            return [2 /*return*/];
                        }
                        this.setState({ firstProjectCreated: true });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, createProject(api, orgId, teams[0].slug, orgId, platform, {
                                defaultRules: false,
                            })];
                    case 2:
                        data = _b.sent();
                        ProjectActions.createSuccess(data);
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        addErrorMessage(t('Failed to create project'));
                        throw error_1;
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    OnboardingPlatform.prototype.render = function () {
        var _this = this;
        var _a = this.props, active = _a.active, project = _a.project, platform = _a.platform;
        var selectedPlatform = platform || (project && project.platform);
        var continueDisabled = this.state.progressing || (this.hasFirstProject && !active);
        return (<div>
        <StepHeading step={1}>Choose your project’s platform</StepHeading>
        <motion.div variants={{
                initial: { y: 30, opacity: 0 },
                animate: { y: 0, opacity: 1 },
                exit: { opacity: 0 },
            }}>
          <p>
            {tct("Variety is the spice of application monitoring. Sentry SDKs integrate\n             with most languages and platforms your developer heart desires.\n             [link:View the full list].", { link: <ExternalLink href="https://docs.sentry.io/platforms/"/> })}
          </p>
          <PlatformPicker noAutoFilter platform={selectedPlatform} setPlatform={this.handleSetPlatform}/>
          <p>
            {tct("Don't see your platform-of-choice? Fear not. Select\n               [otherPlatformLink:other platform] when using a [communityClient:community client].\n               Need help? Learn more in [docs:our docs].", {
                otherPlatformLink: (<Button priority="link" onClick={function () { return _this.handleSetPlatform('other'); }}/>),
                communityClient: (<ExternalLink href="https://docs.sentry.io/platforms/#community-supported"/>),
                docs: <ExternalLink href="https://docs.sentry.io/platforms/"/>,
            })}
          </p>
          {selectedPlatform && (<Button data-test-id="platform-select-next" priority="primary" disabled={continueDisabled} onClick={this.handleContinue}>
              {this.contineButtonLabel}
            </Button>)}
        </motion.div>
      </div>);
    };
    return OnboardingPlatform;
}(React.Component));
export default withApi(withTeams(OnboardingPlatform));
//# sourceMappingURL=platform.jsx.map
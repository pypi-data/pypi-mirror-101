import { __awaiter, __generator } from "tslib";
import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import ModalActions from 'app/actions/modalActions';
import ConfigStore from 'app/stores/configStore';
import GroupActions from 'app/views/organizationGroupDetails/actions';
// @ts-expect-error
var group = TestStubs.Group({
    id: '1337',
    pluginActions: [],
    pluginIssues: [],
});
// @ts-expect-error
var project = TestStubs.ProjectDetails({
    id: '2448',
    name: 'project name',
    slug: 'project',
});
// @ts-expect-error
var organization = TestStubs.Organization({
    id: '4660',
    slug: 'org',
    features: ['reprocessing-v2'],
});
function renderComponent(event) {
    return mountWithTheme(<GroupActions group={group} project={project} organization={organization} event={event} disabled={false}/>);
}
describe('GroupActions', function () {
    beforeEach(function () {
        jest.spyOn(ConfigStore, 'get').mockImplementation(function () { return []; });
    });
    describe('render()', function () {
        it('renders correctly', function () {
            var wrapper = renderComponent();
            expect(wrapper).toSnapshot();
        });
    });
    describe('subscribing', function () {
        var issuesApi;
        beforeEach(function () {
            // @ts-expect-error
            issuesApi = MockApiClient.addMockResponse({
                url: '/projects/org/project/issues/',
                method: 'PUT',
                // @ts-expect-error
                body: TestStubs.Group({ isSubscribed: false }),
            });
        });
        it('can subscribe', function () {
            var wrapper = renderComponent();
            var btn = wrapper.find('button[aria-label="Subscribe"]');
            btn.simulate('click');
            expect(issuesApi).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
                data: { isSubscribed: true },
            }));
        });
    });
    describe('bookmarking', function () {
        var issuesApi;
        beforeEach(function () {
            // @ts-expect-error
            issuesApi = MockApiClient.addMockResponse({
                url: '/projects/org/project/issues/',
                method: 'PUT',
                // @ts-expect-error
                body: TestStubs.Group({ isBookmarked: false }),
            });
        });
        it('can bookmark', function () {
            var wrapper = renderComponent();
            var btn = wrapper.find('button[aria-label="Bookmark"]');
            btn.simulate('click');
            expect(issuesApi).toHaveBeenCalledWith(expect.anything(), expect.objectContaining({
                data: { isBookmarked: true },
            }));
        });
    });
    describe('reprocessing', function () {
        it('renders ReprocessAction component if org has feature flag reprocessing-v2', function () {
            var wrapper = renderComponent();
            var reprocessActionButton = wrapper.find('ReprocessAction');
            expect(reprocessActionButton).toBeTruthy();
        });
        it('open dialog by clicking on the ReprocessAction component', function () {
            return __awaiter(this, void 0, void 0, function () {
                var event, onReprocessEventFunc, wrapper, reprocessActionButton;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            event = TestStubs.EventStacktraceException({
                                platform: 'native',
                            });
                            onReprocessEventFunc = jest.spyOn(ModalActions, 'openModal');
                            wrapper = renderComponent(event);
                            reprocessActionButton = wrapper.find('ReprocessAction');
                            expect(reprocessActionButton).toBeTruthy();
                            reprocessActionButton.simulate('click');
                            // @ts-expect-error
                            return [4 /*yield*/, tick()];
                        case 1:
                            // @ts-expect-error
                            _a.sent();
                            expect(onReprocessEventFunc).toHaveBeenCalled();
                            return [2 /*return*/];
                    }
                });
            });
        });
    });
});
//# sourceMappingURL=actions.spec.jsx.map
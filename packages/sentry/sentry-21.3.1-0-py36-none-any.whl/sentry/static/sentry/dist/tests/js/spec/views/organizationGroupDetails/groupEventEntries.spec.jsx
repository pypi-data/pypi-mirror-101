import { __assign, __awaiter, __generator } from "tslib";
import React from 'react';
import { mountWithTheme } from 'sentry-test/enzyme';
import { initializeOrg } from 'sentry-test/initializeOrg';
import EventEntries from 'app/components/events/eventEntries';
import { EntryType } from 'app/types/event';
var _a = initializeOrg(), organization = _a.organization, project = _a.project;
// @ts-expect-error
var api = new MockApiClient();
function renderComponent(event, errors) {
    return __awaiter(this, void 0, void 0, function () {
        var wrapper, eventErrors, bannerSummary, bannerSummaryInfo, toggleButton, errorItem;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    wrapper = mountWithTheme(<EventEntries organization={organization} event={__assign(__assign({}, event), { errors: errors !== null && errors !== void 0 ? errors : event.errors })} project={project} location={location} api={api}/>);
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 1:
                    // @ts-expect-error
                    _a.sent();
                    wrapper.update();
                    eventErrors = wrapper.find('Errors');
                    bannerSummary = eventErrors.find('BannerSummary');
                    bannerSummaryInfo = bannerSummary.find('span[data-test-id="errors-banner-summary-info"]');
                    toggleButton = bannerSummary
                        .find('[data-test-id="event-error-toggle"]')
                        .hostNodes();
                    toggleButton.simulate('click');
                    // @ts-expect-error
                    return [4 /*yield*/, tick()];
                case 2:
                    // @ts-expect-error
                    _a.sent();
                    wrapper.update();
                    errorItem = wrapper.find('ErrorItem');
                    return [2 /*return*/, { bannerSummaryInfoText: bannerSummaryInfo.text(), errorItem: errorItem }];
            }
        });
    });
}
describe('GroupEventEntries', function () {
    // @ts-expect-error
    var event = TestStubs.Event();
    beforeEach(function () {
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: "/projects/" + organization.slug + "/" + project.slug + "/events/" + event.id + "/grouping-info/",
            body: {},
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: "/projects/" + organization.slug + "/" + project.slug + "/files/dsyms/",
            body: [],
        });
    });
    describe('EventError', function () {
        it('renders', function () {
            return __awaiter(this, void 0, void 0, function () {
                var errors, _a, bannerSummaryInfoText, errorItem;
                return __generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            errors = [
                                {
                                    type: 'invalid_data',
                                    data: {
                                        name: 'logentry',
                                    },
                                    message: 'no message present',
                                },
                                {
                                    type: 'invalid_data',
                                    data: {
                                        name: 'breadcrumbs.values.2.data',
                                    },
                                    message: 'expected an object',
                                },
                            ];
                            return [4 /*yield*/, renderComponent(event, errors)];
                        case 1:
                            _a = _b.sent(), bannerSummaryInfoText = _a.bannerSummaryInfoText, errorItem = _a.errorItem;
                            expect(bannerSummaryInfoText).toEqual("There were " + errors.length + " errors encountered while processing this event");
                            expect(errorItem.length).toBe(2);
                            expect(errorItem.at(0).props().error).toEqual(errors[0]);
                            expect(errorItem.at(1).props().error).toEqual(errors[1]);
                            return [2 /*return*/];
                    }
                });
            });
        });
        describe('Proguard erros', function () {
            var proGuardUuid = 'a59c8fcc-2f27-49f8-af9e-02661fc3e8d7';
            it('Missing mapping file', function () {
                return __awaiter(this, void 0, void 0, function () {
                    var newEvent, _a, errorItem, bannerSummaryInfoText;
                    return __generator(this, function (_b) {
                        switch (_b.label) {
                            case 0:
                                newEvent = __assign(__assign({}, event), { platform: 'java', entries: [
                                        {
                                            type: EntryType.DEBUGMETA,
                                            data: {
                                                images: [{ type: 'proguard', uuid: proGuardUuid }],
                                            },
                                        },
                                    ] });
                                return [4 /*yield*/, renderComponent(newEvent)];
                            case 1:
                                _a = _b.sent(), errorItem = _a.errorItem, bannerSummaryInfoText = _a.bannerSummaryInfoText;
                                expect(bannerSummaryInfoText).toEqual('There was 1 error encountered while processing this event');
                                expect(errorItem.length).toBe(1);
                                expect(errorItem.at(0).props().error).toEqual({
                                    type: 'proguard_missing_mapping',
                                    message: 'A proguard mapping file was missing.',
                                    data: { mapping_uuid: proGuardUuid },
                                });
                                return [2 /*return*/];
                        }
                    });
                });
            });
            it("Don't display extra proguard errors, if the entry error of an event has an error of type 'proguard_missing_mapping'", function () {
                return __awaiter(this, void 0, void 0, function () {
                    var newEvent, _a, bannerSummaryInfoText, errorItem;
                    return __generator(this, function (_b) {
                        switch (_b.label) {
                            case 0:
                                newEvent = __assign(__assign({}, event), { platform: 'java', entries: [
                                        {
                                            type: EntryType.DEBUGMETA,
                                            data: {
                                                images: [{ type: 'proguard', uuid: proGuardUuid }],
                                            },
                                        },
                                    ], errors: [
                                        {
                                            type: 'proguard_missing_mapping',
                                            message: 'A proguard mapping file was missing.',
                                            data: { mapping_uuid: proGuardUuid },
                                        },
                                    ] });
                                return [4 /*yield*/, renderComponent(newEvent)];
                            case 1:
                                _a = _b.sent(), bannerSummaryInfoText = _a.bannerSummaryInfoText, errorItem = _a.errorItem;
                                expect(bannerSummaryInfoText).toEqual('There was 1 error encountered while processing this event');
                                expect(errorItem.length).toBe(1);
                                expect(errorItem.at(0).props().error).toEqual({
                                    type: 'proguard_missing_mapping',
                                    message: 'A proguard mapping file was missing.',
                                    data: { mapping_uuid: proGuardUuid },
                                });
                                return [2 /*return*/];
                        }
                    });
                });
            });
            describe('ProGuard Plugin seems to not be correctly configured', function () {
                it('find minified data in the exception entry', function () {
                    return __awaiter(this, void 0, void 0, function () {
                        var newEvent, _a, bannerSummaryInfoText, errorItem, _b, type, message;
                        return __generator(this, function (_c) {
                            switch (_c.label) {
                                case 0:
                                    newEvent = __assign(__assign({}, event), { platform: 'java', entries: [
                                            {
                                                type: 'exception',
                                                data: {
                                                    values: [
                                                        {
                                                            stacktrace: {
                                                                frames: [
                                                                    {
                                                                        function: null,
                                                                        colNo: null,
                                                                        vars: {},
                                                                        symbol: null,
                                                                        module: 'a.$a.a.a',
                                                                    },
                                                                ],
                                                                framesOmitted: null,
                                                                registers: null,
                                                                hasSystemFrames: false,
                                                            },
                                                            module: null,
                                                            rawStacktrace: null,
                                                            mechanism: null,
                                                            threadId: null,
                                                            value: 'Unexpected token else',
                                                            type: 'SyntaxError',
                                                        },
                                                    ],
                                                    excOmitted: null,
                                                    hasSystemFrames: false,
                                                },
                                            },
                                        ] });
                                    return [4 /*yield*/, renderComponent(newEvent)];
                                case 1:
                                    _a = _c.sent(), bannerSummaryInfoText = _a.bannerSummaryInfoText, errorItem = _a.errorItem;
                                    expect(bannerSummaryInfoText).toEqual('There was 1 error encountered while processing this event');
                                    expect(errorItem.length).toBe(1);
                                    _b = errorItem.at(0).props().error, type = _b.type, message = _b.message;
                                    expect(type).toEqual('proguard_potentially_misconfigured_plugin');
                                    expect(message).toBeTruthy();
                                    return [2 /*return*/];
                            }
                        });
                    });
                });
                it('find minified data in the threads entry', function () {
                    return __awaiter(this, void 0, void 0, function () {
                        var newEvent, _a, bannerSummaryInfoText, errorItem, _b, type, message;
                        return __generator(this, function (_c) {
                            switch (_c.label) {
                                case 0:
                                    newEvent = __assign(__assign({}, event), { platform: 'java', entries: [
                                            {
                                                type: 'exception',
                                                data: {
                                                    values: [
                                                        {
                                                            stacktrace: {
                                                                frames: [
                                                                    {
                                                                        function: null,
                                                                        colNo: null,
                                                                        vars: {},
                                                                        symbol: null,
                                                                        module: 'a.$a.a.a',
                                                                    },
                                                                ],
                                                                framesOmitted: null,
                                                                registers: null,
                                                                hasSystemFrames: false,
                                                            },
                                                            module: null,
                                                            rawStacktrace: null,
                                                            mechanism: null,
                                                            threadId: null,
                                                            value: 'Unexpected token else',
                                                            type: 'SyntaxError',
                                                        },
                                                    ],
                                                    excOmitted: null,
                                                    hasSystemFrames: false,
                                                },
                                            },
                                            {
                                                type: 'threads',
                                                data: {
                                                    values: [
                                                        {
                                                            stacktrace: {
                                                                frames: [
                                                                    {
                                                                        function: 'start',
                                                                        package: 'libdyld.dylib',
                                                                        module: 'a.$a.a.a',
                                                                    },
                                                                    {
                                                                        function: 'main',
                                                                        package: 'iOS-Swift',
                                                                        module: '',
                                                                    },
                                                                ],
                                                            },
                                                        },
                                                    ],
                                                },
                                            },
                                        ] });
                                    return [4 /*yield*/, renderComponent(newEvent)];
                                case 1:
                                    _a = _c.sent(), bannerSummaryInfoText = _a.bannerSummaryInfoText, errorItem = _a.errorItem;
                                    expect(bannerSummaryInfoText).toEqual('There was 1 error encountered while processing this event');
                                    expect(errorItem.length).toBe(1);
                                    _b = errorItem.at(0).props().error, type = _b.type, message = _b.message;
                                    expect(type).toEqual('proguard_potentially_misconfigured_plugin');
                                    expect(message).toBeTruthy();
                                    return [2 /*return*/];
                            }
                        });
                    });
                });
            });
        });
    });
});
//# sourceMappingURL=groupEventEntries.spec.jsx.map
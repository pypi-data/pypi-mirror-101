import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __rest, __spreadArray } from "tslib";
import React from 'react';
import { css } from '@emotion/core';
import styled from '@emotion/styled';
import partition from 'lodash/partition';
import sortBy from 'lodash/sortBy';
import { addErrorMessage } from 'app/actionCreators/indicator';
import AlertLink from 'app/components/alertLink';
import AsyncComponent from 'app/components/asyncComponent';
import Button from 'app/components/button';
import ButtonBar from 'app/components/buttonBar';
import { t } from 'app/locale';
import space from 'app/styles/space';
import { DebugFileFeature } from 'app/types/debugFiles';
import { CandidateDownloadStatus } from 'app/types/debugImage';
import { displayReprocessEventAction } from 'app/utils/displayReprocessEventAction';
import theme from 'app/utils/theme';
import { getFileType } from 'app/views/settings/projectDebugFiles/utils';
import { getFileName } from '../utils';
import Candidates from './candidates';
import GeneralInfo from './generalInfo';
import { INTERNAL_SOURCE, INTERNAL_SOURCE_LOCATION } from './utils';
var DebugImageDetails = /** @class */ (function (_super) {
    __extends(DebugImageDetails, _super);
    function DebugImageDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (debugId) { return __awaiter(_this, void 0, void 0, function () {
            var _a, organization, projectId, _b;
            return __generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, projectId = _a.projectId;
                        this.setState({ loading: true });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?id=" + debugId, { method: 'DELETE' })];
                    case 2:
                        _c.sent();
                        this.fetchData();
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        addErrorMessage(t('An error occurred while deleting the debug file.'));
                        this.setState({ loading: false });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    DebugImageDetails.prototype.getDefaultState = function () {
        return __assign(__assign({}, _super.prototype.getDefaultState.call(this)), { debugFiles: [], builtinSymbolSources: [] });
    };
    DebugImageDetails.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (!prevProps.image && !!this.props.image) {
            this.remountComponent();
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    DebugImageDetails.prototype.getUplodedDebugFiles = function (candidates) {
        return candidates.find(function (candidate) { return candidate.source === INTERNAL_SOURCE; });
    };
    DebugImageDetails.prototype.getEndpoints = function () {
        var _a;
        var _b = this.props, organization = _b.organization, projectId = _b.projectId, image = _b.image;
        if (!image) {
            return [];
        }
        var debug_id = image.debug_id, _c = image.candidates, candidates = _c === void 0 ? [] : _c;
        var builtinSymbolSources = (this.state || {}).builtinSymbolSources;
        var uploadedDebugFiles = this.getUplodedDebugFiles(candidates);
        var endpoints = [];
        if (uploadedDebugFiles) {
            endpoints.push([
                'debugFiles',
                "/projects/" + organization.slug + "/" + projectId + "/files/dsyms/?debug_id=" + debug_id,
                {
                    query: {
                        file_formats: !!((_a = organization.features) === null || _a === void 0 ? void 0 : _a.includes('android-mappings'))
                            ? ['breakpad', 'macho', 'elf', 'pe', 'pdb', 'sourcebundle']
                            : undefined,
                    },
                },
            ]);
        }
        if (!(builtinSymbolSources === null || builtinSymbolSources === void 0 ? void 0 : builtinSymbolSources.length) &&
            organization.features.includes('symbol-sources')) {
            endpoints.push(['builtinSymbolSources', '/builtin-symbol-sources/', {}]);
        }
        return endpoints;
    };
    DebugImageDetails.prototype.sortCandidates = function (candidates, unAppliedCandidates) {
        var _a = __read(partition(candidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.NO_PERMISSION; }), 2), noPermissionCandidates = _a[0], restNoPermissionCandidates = _a[1];
        var _b = __read(partition(restNoPermissionCandidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.MALFORMED; }), 2), malFormedCandidates = _b[0], restMalFormedCandidates = _b[1];
        var _c = __read(partition(restMalFormedCandidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.ERROR; }), 2), errorCandidates = _c[0], restErrorCandidates = _c[1];
        var _d = __read(partition(restErrorCandidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.OK; }), 2), okCandidates = _d[0], restOKCandidates = _d[1];
        var _e = __read(partition(restOKCandidates, function (candidate) { return candidate.download.status === CandidateDownloadStatus.DELETED; }), 2), deletedCandidates = _e[0], notFoundCandidates = _e[1];
        return __spreadArray(__spreadArray(__spreadArray(__spreadArray(__spreadArray(__spreadArray(__spreadArray([], __read(sortBy(noPermissionCandidates, ['source_name', 'location']))), __read(sortBy(malFormedCandidates, ['source_name', 'location']))), __read(sortBy(errorCandidates, ['source_name', 'location']))), __read(sortBy(okCandidates, ['source_name', 'location']))), __read(sortBy(deletedCandidates, ['source_name', 'location']))), __read(sortBy(unAppliedCandidates, ['source_name', 'location']))), __read(sortBy(notFoundCandidates, ['source_name', 'location'])));
    };
    DebugImageDetails.prototype.getCandidates = function () {
        var _a = this.state, debugFiles = _a.debugFiles, loading = _a.loading;
        var image = this.props.image;
        var _b = (image !== null && image !== void 0 ? image : {}).candidates, candidates = _b === void 0 ? [] : _b;
        if (!debugFiles || loading) {
            return candidates;
        }
        var debugFileCandidates = candidates.map(function (_a) {
            var location = _a.location, candidate = __rest(_a, ["location"]);
            return (__assign(__assign({}, candidate), { location: (location === null || location === void 0 ? void 0 : location.includes(INTERNAL_SOURCE_LOCATION))
                    ? location.split(INTERNAL_SOURCE_LOCATION)[1]
                    : location }));
        });
        var candidateLocations = new Set(debugFileCandidates.map(function (_a) {
            var location = _a.location;
            return location;
        }).filter(function (location) { return !!location; }));
        var _c = __read(partition(debugFiles, function (debugFile) { return !candidateLocations.has(debugFile.id); }), 2), unAppliedDebugFiles = _c[0], appliedDebugFiles = _c[1];
        var unAppliedCandidates = unAppliedDebugFiles.map(function (debugFile) {
            var _a;
            var data = debugFile.data, symbolType = debugFile.symbolType, filename = debugFile.objectName, location = debugFile.id, size = debugFile.size, dateCreated = debugFile.dateCreated, cpuName = debugFile.cpuName;
            var features = (_a = data === null || data === void 0 ? void 0 : data.features) !== null && _a !== void 0 ? _a : [];
            return {
                download: {
                    status: CandidateDownloadStatus.UNAPPLIED,
                    features: {
                        has_sources: features.includes(DebugFileFeature.SOURCES),
                        has_debug_info: features.includes(DebugFileFeature.DEBUG),
                        has_unwind_info: features.includes(DebugFileFeature.UNWIND),
                        has_symbols: features.includes(DebugFileFeature.SYMTAB),
                    },
                },
                cpuName: cpuName,
                location: location,
                filename: filename,
                size: size,
                dateCreated: dateCreated,
                symbolType: symbolType,
                fileType: getFileType(debugFile),
                source: INTERNAL_SOURCE,
                source_name: t('Sentry'),
            };
        });
        var _d = __read(partition(debugFileCandidates, function (debugFileCandidate) {
            return debugFileCandidate.download.status === CandidateDownloadStatus.OK &&
                debugFileCandidate.source === INTERNAL_SOURCE;
        }), 2), debugFileInternalOkCandidates = _d[0], debugFileOtherCandidates = _d[1];
        var convertedDebugFileInternalOkCandidates = debugFileInternalOkCandidates.map(function (debugFileOkCandidate) {
            var internalDebugFileInfo = appliedDebugFiles.find(function (appliedDebugFile) { return appliedDebugFile.id === debugFileOkCandidate.location; });
            if (!internalDebugFileInfo) {
                return __assign(__assign({}, debugFileOkCandidate), { download: __assign(__assign({}, debugFileOkCandidate.download), { status: CandidateDownloadStatus.DELETED }) });
            }
            var symbolType = internalDebugFileInfo.symbolType, filename = internalDebugFileInfo.objectName, location = internalDebugFileInfo.id, size = internalDebugFileInfo.size, dateCreated = internalDebugFileInfo.dateCreated, cpuName = internalDebugFileInfo.cpuName;
            return __assign(__assign({}, debugFileOkCandidate), { cpuName: cpuName,
                location: location,
                filename: filename,
                size: size,
                dateCreated: dateCreated,
                symbolType: symbolType, fileType: getFileType(internalDebugFileInfo) });
        });
        return this.sortCandidates(__spreadArray(__spreadArray([], __read(convertedDebugFileInternalOkCandidates)), __read(debugFileOtherCandidates)), unAppliedCandidates);
    };
    DebugImageDetails.prototype.getDebugFilesSettingsLink = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId, image = _a.image;
        var orgSlug = organization.slug;
        var debugId = image === null || image === void 0 ? void 0 : image.debug_id;
        if (!orgSlug || !projectId || !debugId) {
            return undefined;
        }
        return "/settings/" + orgSlug + "/projects/" + projectId + "/debug-symbols/?query=" + debugId;
    };
    DebugImageDetails.prototype.renderBody = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, Footer = _a.Footer, image = _a.image, organization = _a.organization, projectId = _a.projectId, onReprocessEvent = _a.onReprocessEvent, event = _a.event;
        var _b = this.state, loading = _b.loading, builtinSymbolSources = _b.builtinSymbolSources;
        var _c = image !== null && image !== void 0 ? image : {}, code_file = _c.code_file, status = _c.status;
        var debugFilesSettingsLink = this.getDebugFilesSettingsLink();
        var candidates = this.getCandidates();
        var baseUrl = this.api.baseUrl;
        var fileName = getFileName(code_file);
        var haveCandidatesUnappliedDebugFile = candidates.some(function (candidate) { return candidate.download.status === CandidateDownloadStatus.UNAPPLIED; });
        var hasReprocessWarning = haveCandidatesUnappliedDebugFile &&
            displayReprocessEventAction(organization.features, event) &&
            !!onReprocessEvent;
        return (<React.Fragment>
        <Header closeButton>
          <Title>
            {t('Image')}
            <FileName>{fileName !== null && fileName !== void 0 ? fileName : t('Unknown')}</FileName>
          </Title>
        </Header>
        <Body>
          <Content>
            {hasReprocessWarning && (<AlertLink priority="warning" size="small" onClick={onReprocessEvent} withoutMarginBottom>
                {t('You’ve uploaded new debug files. Reprocess events in this issue to view a better stack trace')}
              </AlertLink>)}
            <GeneralInfo image={image}/>
            <Candidates imageStatus={status} candidates={candidates} organization={organization} projectId={projectId} baseUrl={baseUrl} isLoading={loading} eventDateReceived={event.dateReceived} builtinSymbolSources={builtinSymbolSources} onDelete={this.handleDelete} hasReprocessWarning={hasReprocessWarning}/>
          </Content>
        </Body>
        <Footer>
          <StyledButtonBar gap={1}>
            <Button href="https://docs.sentry.io/platforms/native/data-management/debug-files/" external>
              {t('Read the docs')}
            </Button>
            {debugFilesSettingsLink && (<Button title={t('Search for this debug file in all images for the %s project', projectId)} to={debugFilesSettingsLink}>
                {t('Open in Settings')}
              </Button>)}
          </StyledButtonBar>
        </Footer>
      </React.Fragment>);
    };
    return DebugImageDetails;
}(AsyncComponent));
export default DebugImageDetails;
var Content = styled('div')(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  font-size: ", ";\n"])), space(3), function (p) { return p.theme.fontSizeMedium; });
var Title = styled('div')(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  max-width: calc(100% - 40px);\n  word-break: break-all;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  font-size: ", ";\n  max-width: calc(100% - 40px);\n  word-break: break-all;\n"])), space(1), function (p) { return p.theme.fontSizeExtraLarge; });
var FileName = styled('span')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  font-family: ", ";\n"], ["\n  font-family: ", ";\n"])), function (p) { return p.theme.text.familyMono; });
var StyledButtonBar = styled(ButtonBar)(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
export var modalCss = css(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 90%;\n      margin-left: -45%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 70%;\n      margin-left: -35%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 50%;\n      margin-left: -25%;\n    }\n  }\n"], ["\n  .modal-content {\n    overflow: initial;\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 90%;\n      margin-left: -45%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 70%;\n      margin-left: -35%;\n    }\n  }\n\n  @media (min-width: ", ") {\n    .modal-dialog {\n      width: 50%;\n      margin-left: -25%;\n    }\n  }\n"])), theme.breakpoints[0], theme.breakpoints[3], theme.breakpoints[4]);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map
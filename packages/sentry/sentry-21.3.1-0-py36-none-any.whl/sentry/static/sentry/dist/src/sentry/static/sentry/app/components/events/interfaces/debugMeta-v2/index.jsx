import { __assign, __awaiter, __extends, __generator, __makeTemplateObject, __read, __spreadArray } from "tslib";
import React from 'react';
import { withRouter } from 'react-router';
import { AutoSizer, CellMeasurer, CellMeasurerCache, List, } from 'react-virtualized';
import styled from '@emotion/styled';
import { openModal, openReprocessEventModal } from 'app/actionCreators/modal';
import GuideAnchor from 'app/components/assistant/guideAnchor';
import Button from 'app/components/button';
import EventDataSection from 'app/components/events/eventDataSection';
import { getImageRange, parseAddress } from 'app/components/events/interfaces/utils';
import { PanelTable } from 'app/components/panels';
import QuestionTooltip from 'app/components/questionTooltip';
import SearchBar from 'app/components/searchBar';
import { t } from 'app/locale';
import DebugMetaStore, { DebugMetaActions } from 'app/stores/debugMetaStore';
import overflowEllipsis from 'app/styles/overflowEllipsis';
import space from 'app/styles/space';
import { ImageStatus } from 'app/types/debugImage';
import { defined } from 'app/utils';
import Status from './debugImage/status';
import DebugImage from './debugImage';
import Filter from './filter';
import layout from './layout';
import { combineStatus, getFileName, IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT, normalizeId, shouldSkipSection, } from './utils';
var IMAGE_INFO_UNAVAILABLE = '-1';
var cache = new CellMeasurerCache({
    fixedWidth: true,
    defaultHeight: 81,
});
var DebugMeta = /** @class */ (function (_super) {
    __extends(DebugMeta, _super);
    function DebugMeta() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            scrollbarWidth: 0,
            filterOptions: {},
            filteredImages: [],
            filteredImagesByFilter: [],
            filteredImagesBySearch: [],
        };
        _this.panelTableRef = React.createRef();
        _this.listRef = null;
        _this.onDebugMetaStoreChange = function (store) {
            var searchTerm = _this.state.searchTerm;
            if (store.filter !== searchTerm) {
                _this.setState({ searchTerm: store.filter }, _this.filterImagesBySearchTerm);
            }
        };
        _this.updateGrid = function () {
            if (_this.listRef) {
                cache.clearAll();
                _this.listRef.forceUpdateGrid();
                _this.getScrollbarWidth();
            }
        };
        _this.openImageDetailsModal = function () { return __awaiter(_this, void 0, void 0, function () {
            var filteredImages, _a, location, organization, projectId, groupId, event, query, imageCodeId, imageDebugId, image, mod, Modal, modalCss;
            var _this = this;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        filteredImages = this.state.filteredImages;
                        if (!filteredImages.length) {
                            return [2 /*return*/];
                        }
                        _a = this.props, location = _a.location, organization = _a.organization, projectId = _a.projectId, groupId = _a.groupId, event = _a.event;
                        query = location.query;
                        imageCodeId = query.imageCodeId, imageDebugId = query.imageDebugId;
                        if (!imageCodeId && !imageDebugId) {
                            return [2 /*return*/];
                        }
                        image = imageCodeId !== IMAGE_INFO_UNAVAILABLE || imageDebugId !== IMAGE_INFO_UNAVAILABLE
                            ? filteredImages.find(function (_a) {
                                var code_id = _a.code_id, debug_id = _a.debug_id;
                                return code_id === imageCodeId || debug_id === imageDebugId;
                            })
                            : undefined;
                        return [4 /*yield*/, import(
                            /* webpackChunkName: "DebugImageDetails" */ 'app/components/events/interfaces/debugMeta-v2/debugImageDetails')];
                    case 1:
                        mod = _b.sent();
                        Modal = mod.default, modalCss = mod.modalCss;
                        openModal(function (deps) { return (<Modal {...deps} image={image} organization={organization} projectId={projectId} event={event} onReprocessEvent={defined(groupId) ? _this.handleReprocessEvent(groupId) : undefined}/>); }, {
                            modalCss: modalCss,
                            onClose: this.handleCloseImageDetailsModal,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleChangeFilter = function (filterOptions) {
            var filteredImagesBySearch = _this.state.filteredImagesBySearch;
            var filteredImagesByFilter = _this.getFilteredImagesByFilter(filteredImagesBySearch, filterOptions);
            _this.setState({ filterOptions: filterOptions, filteredImagesByFilter: filteredImagesByFilter }, _this.updateGrid);
        };
        _this.handleChangeSearchTerm = function (searchTerm) {
            if (searchTerm === void 0) { searchTerm = ''; }
            DebugMetaActions.updateFilter(searchTerm);
        };
        _this.handleResetFilter = function () {
            var filterOptions = _this.state.filterOptions;
            _this.setState({
                filterOptions: Object.keys(filterOptions).reduce(function (accumulator, currentValue) {
                    accumulator[currentValue] = filterOptions[currentValue].map(function (filterOption) { return (__assign(__assign({}, filterOption), { isChecked: false })); });
                    return accumulator;
                }, {}),
            }, _this.filterImagesBySearchTerm);
        };
        _this.handleResetSearchBar = function () {
            _this.setState(function (prevState) { return ({
                searchTerm: '',
                filteredImagesByFilter: prevState.filteredImages,
                filteredImagesBySearch: prevState.filteredImages,
            }); });
        };
        _this.handleOpenImageDetailsModal = function (code_id, debug_id) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { imageCodeId: code_id !== null && code_id !== void 0 ? code_id : IMAGE_INFO_UNAVAILABLE, imageDebugId: debug_id !== null && debug_id !== void 0 ? debug_id : IMAGE_INFO_UNAVAILABLE }) }));
        };
        _this.handleCloseImageDetailsModal = function () {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(__assign(__assign({}, location), { query: __assign(__assign({}, location.query), { imageCodeId: undefined, imageDebugId: undefined }) }));
        };
        _this.handleReprocessEvent = function (groupId) { return function () {
            var organization = _this.props.organization;
            openReprocessEventModal({
                organization: organization,
                groupId: groupId,
                onClose: _this.openImageDetailsModal,
            });
        }; };
        _this.renderRow = function (_a) {
            var index = _a.index, key = _a.key, parent = _a.parent, style = _a.style;
            var images = _this.state.filteredImagesByFilter;
            return (<CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        <DebugImage style={style} image={images[index]} onOpenImageDetailsModal={_this.handleOpenImageDetailsModal}/>
      </CellMeasurer>);
        };
        return _this;
    }
    DebugMeta.prototype.componentDidMount = function () {
        this.unsubscribeFromDebugMetaStore = DebugMetaStore.listen(this.onDebugMetaStoreChange, undefined);
        cache.clearAll();
        this.getRelevantImages();
        this.openImageDetailsModal();
    };
    DebugMeta.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.filteredImages.length === 0 && this.state.filteredImages.length > 0) {
            this.getPanelBodyHeight();
        }
        this.openImageDetailsModal();
    };
    DebugMeta.prototype.componentWillUnmount = function () {
        if (this.unsubscribeFromDebugMetaStore) {
            this.unsubscribeFromDebugMetaStore();
        }
    };
    DebugMeta.prototype.getScrollbarWidth = function () {
        var _a, _b, _c, _d, _e, _f, _g;
        var panelTableWidth = (_c = (_b = (_a = this.panelTableRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.clientWidth) !== null && _c !== void 0 ? _c : 0;
        var gridInnerWidth = (_g = (_f = (_e = (_d = this.panelTableRef) === null || _d === void 0 ? void 0 : _d.current) === null || _e === void 0 ? void 0 : _e.querySelector('.ReactVirtualized__Grid__innerScrollContainer')) === null || _f === void 0 ? void 0 : _f.clientWidth) !== null && _g !== void 0 ? _g : 0;
        var scrollbarWidth = panelTableWidth - gridInnerWidth;
        if (scrollbarWidth !== this.state.scrollbarWidth) {
            this.setState({ scrollbarWidth: scrollbarWidth });
        }
    };
    DebugMeta.prototype.isValidImage = function (image) {
        // in particular proguard images do not have a code file, skip them
        if (image === null || image.code_file === null || image.type === 'proguard') {
            return false;
        }
        if (getFileName(image.code_file) === 'dyld_sim') {
            // this is only for simulator builds
            return false;
        }
        return true;
    };
    DebugMeta.prototype.filterImage = function (image, searchTerm) {
        var _a, _b;
        // When searching for an address, check for the address range of the image
        // instead of an exact match.  Note that images cannot be found by index
        // if they are at 0x0.  For those relative addressing has to be used.
        if (searchTerm.indexOf('0x') === 0) {
            var needle = parseAddress(searchTerm);
            if (needle > 0 && image.image_addr !== '0x0') {
                var _c = __read(getImageRange(image), 2), startAddress = _c[0], endAddress = _c[1]; // TODO(PRISCILA): remove any
                return needle >= startAddress && needle < endAddress;
            }
        }
        // the searchTerm ending at "!" is the end of the ID search.
        var relMatch = searchTerm.match(/^\s*(.*?)!/); // debug_id!address
        var idSearchTerm = normalizeId((relMatch === null || relMatch === void 0 ? void 0 : relMatch[1]) || searchTerm);
        return (
        // Prefix match for identifiers
        normalizeId(image.code_id).indexOf(idSearchTerm) === 0 ||
            normalizeId(image.debug_id).indexOf(idSearchTerm) === 0 ||
            // Any match for file paths
            (((_a = image.code_file) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || '').indexOf(searchTerm) >= 0 ||
            (((_b = image.debug_file) === null || _b === void 0 ? void 0 : _b.toLowerCase()) || '').indexOf(searchTerm) >= 0);
    };
    DebugMeta.prototype.filterImagesBySearchTerm = function () {
        var _this = this;
        var _a = this.state, filteredImages = _a.filteredImages, filterOptions = _a.filterOptions, searchTerm = _a.searchTerm;
        var filteredImagesBySearch = filteredImages.filter(function (image) {
            return _this.filterImage(image, searchTerm.toLowerCase());
        });
        var filteredImagesByFilter = this.getFilteredImagesByFilter(filteredImagesBySearch, filterOptions);
        this.setState({
            filteredImagesBySearch: filteredImagesBySearch,
            filteredImagesByFilter: filteredImagesByFilter,
        }, this.updateGrid);
    };
    DebugMeta.prototype.getPanelBodyHeight = function () {
        var _a, _b;
        var panelTableHeight = (_b = (_a = this.panelTableRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetHeight;
        if (!panelTableHeight) {
            return;
        }
        this.setState({ panelTableHeight: panelTableHeight });
    };
    DebugMeta.prototype.getListHeight = function () {
        var panelTableHeight = this.state.panelTableHeight;
        if (!panelTableHeight || panelTableHeight > IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT) {
            return IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT;
        }
        return panelTableHeight;
    };
    DebugMeta.prototype.getRelevantImages = function () {
        var data = this.props.data;
        var images = data.images;
        // There are a bunch of images in debug_meta that are not relevant to this
        // component. Filter those out to reduce the noise. Most importantly, this
        // includes proguard images, which are rendered separately.
        var relevantImages = images.filter(this.isValidImage);
        if (!relevantImages.length) {
            return;
        }
        var formattedRelevantImages = relevantImages.map(function (releventImage) {
            var _a = releventImage, debug_status = _a.debug_status, unwind_status = _a.unwind_status;
            return __assign(__assign({}, releventImage), { status: combineStatus(debug_status, unwind_status) });
        });
        // Sort images by their start address. We assume that images have
        // non-overlapping ranges. Each address is given as hex string (e.g.
        // "0xbeef").
        formattedRelevantImages.sort(function (a, b) { return parseAddress(a.image_addr) - parseAddress(b.image_addr); });
        var unusedImages = [];
        var usedImages = formattedRelevantImages.filter(function (image) {
            if (image.debug_status === ImageStatus.UNUSED) {
                unusedImages.push(image);
                return false;
            }
            return true;
        });
        var filteredImages = __spreadArray(__spreadArray([], __read(usedImages)), __read(unusedImages));
        var filterOptions = this.getFilterOptions(filteredImages);
        this.setState({
            filteredImages: filteredImages,
            filterOptions: filterOptions,
            filteredImagesByFilter: this.getFilteredImagesByFilter(filteredImages, filterOptions),
            filteredImagesBySearch: filteredImages,
        });
    };
    DebugMeta.prototype.getFilterOptions = function (images) {
        var _a;
        return _a = {},
            _a[t('Status')] = __spreadArray([], __read(new Set(images.map(function (image) { return image.status; })))).map(function (status) { return ({
                id: status,
                symbol: <Status status={status}/>,
                isChecked: status !== ImageStatus.UNUSED,
            }); }),
            _a;
    };
    DebugMeta.prototype.getFilteredImagesByFilter = function (filteredImages, filterOptions) {
        var checkedOptions = new Set(Object.values(filterOptions)[0]
            .filter(function (filterOption) { return filterOption.isChecked; })
            .map(function (option) { return option.id; }));
        if (!__spreadArray([], __read(checkedOptions)).length) {
            return filteredImages;
        }
        return filteredImages.filter(function (image) { return checkedOptions.has(image.status); });
    };
    DebugMeta.prototype.renderList = function () {
        var _this = this;
        var _a = this.state, images = _a.filteredImagesByFilter, panelTableHeight = _a.panelTableHeight;
        if (!panelTableHeight) {
            return images.map(function (image, index) { return (<DebugImage key={index} image={image} onOpenImageDetailsModal={_this.handleOpenImageDetailsModal}/>); });
        }
        return (<AutoSizer disableHeight onResize={this.updateGrid}>
        {function (_a) {
                var width = _a.width;
                return (<StyledList ref={function (el) {
                        _this.listRef = el;
                    }} deferredMeasurementCache={cache} height={_this.getListHeight()} overscanRowCount={5} rowCount={images.length} rowHeight={cache.rowHeight} rowRenderer={_this.renderRow} width={width} isScrolling={false}/>);
            }}
      </AutoSizer>);
    };
    DebugMeta.prototype.getEmptyMessage = function () {
        var _a = this.state, searchTerm = _a.searchTerm, images = _a.filteredImagesByFilter, filterOptions = _a.filterOptions;
        if (!!images.length) {
            return {};
        }
        if (searchTerm && !images.length) {
            var hasActiveFilter = Object.values(filterOptions)
                .flatMap(function (filterOption) { return filterOption; })
                .find(function (filterOption) { return filterOption.isChecked; });
            return {
                emptyMessage: t('Sorry, no images match your search query'),
                emptyAction: hasActiveFilter ? (<Button onClick={this.handleResetFilter} priority="primary">
            {t('Reset filter')}
          </Button>) : (<Button onClick={this.handleResetSearchBar} priority="primary">
            {t('Clear search bar')}
          </Button>),
            };
        }
        return {
            emptyMessage: t('There are no images to be displayed'),
        };
    };
    DebugMeta.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.state, searchTerm = _b.searchTerm, filterOptions = _b.filterOptions, scrollbarWidth = _b.scrollbarWidth, filteredImages = _b.filteredImagesByFilter;
        var data = this.props.data;
        var images = data.images;
        if (shouldSkipSection(filteredImages, images)) {
            return null;
        }
        var displayFilter = ((_a = Object.values(filterOptions !== null && filterOptions !== void 0 ? filterOptions : {})[0]) !== null && _a !== void 0 ? _a : []).length > 1;
        return (<StyledEventDataSection type="images-loaded" title={<TitleWrapper>
            <GuideAnchor target="images-loaded" position="bottom">
              <Title>{t('Images Loaded')}</Title>
            </GuideAnchor>
            <QuestionTooltip size="xs" position="top" title={t('A list of dynamic librarys or shared objects loaded into process memory at the time of the crash. Images contribute application code that is referenced in stack traces.')}/>
          </TitleWrapper>} actions={<Search>
            {displayFilter && (<Filter options={filterOptions} onFilter={this.handleChangeFilter}/>)}
            <StyledSearchBar query={searchTerm} onChange={function (value) { return _this.handleChangeSearchTerm(value); }} placeholder={t('Search images')} blendWithFilter={displayFilter}/>
          </Search>} wrapTitle={false} isCentered>
        <StyledPanelTable isEmpty={!filteredImages.length} scrollbarWidth={scrollbarWidth} headers={[t('Status'), t('Image'), t('Processing'), t('Details'), '']} {...this.getEmptyMessage()}>
          <div ref={this.panelTableRef}>{this.renderList()}</div>
        </StyledPanelTable>
      </StyledEventDataSection>);
    };
    DebugMeta.defaultProps = {
        data: { images: [] },
    };
    return DebugMeta;
}(React.PureComponent));
export default withRouter(DebugMeta);
var StyledEventDataSection = styled(EventDataSection)(templateObject_1 || (templateObject_1 = __makeTemplateObject(["\n  padding-bottom: ", ";\n\n  /* to increase specificity */\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n  }\n"], ["\n  padding-bottom: ", ";\n\n  /* to increase specificity */\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n  }\n"])), space(4), function (p) { return p.theme.breakpoints[0]; }, space(2));
var StyledPanelTable = styled(PanelTable)(templateObject_2 || (templateObject_2 = __makeTemplateObject(["\n  overflow: hidden;\n  > * {\n    :nth-child(-n + 5) {\n      ", ";\n      border-bottom: 1px solid ", ";\n      :nth-child(5n) {\n        height: 100%;\n        ", "\n      }\n    }\n\n    :nth-child(n + 6) {\n      grid-column: 1/-1;\n      ", "\n    }\n  }\n\n  ", "\n"], ["\n  overflow: hidden;\n  > * {\n    :nth-child(-n + 5) {\n      ", ";\n      border-bottom: 1px solid ", ";\n      :nth-child(5n) {\n        height: 100%;\n        ", "\n      }\n    }\n\n    :nth-child(n + 6) {\n      grid-column: 1/-1;\n      ",
    "\n    }\n  }\n\n  ", "\n"])), overflowEllipsis, function (p) { return p.theme.border; }, function (p) { return !p.scrollbarWidth && "display: none"; }, function (p) {
    return !p.isEmpty &&
        "\n          display: grid;\n          padding: 0;\n        ";
}, function (p) { return layout(p.theme, p.scrollbarWidth); });
var TitleWrapper = styled('div')(templateObject_3 || (templateObject_3 = __makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  padding: ", " 0;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  padding: ", " 0;\n"])), space(0.5), space(0.75));
var Title = styled('h3')(templateObject_4 || (templateObject_4 = __makeTemplateObject(["\n  margin-bottom: 0;\n  padding: 0 !important;\n  height: 14px;\n"], ["\n  margin-bottom: 0;\n  padding: 0 !important;\n  height: 14px;\n"])));
var StyledList = styled(List)(templateObject_5 || (templateObject_5 = __makeTemplateObject(["\n  height: auto !important;\n  max-height: ", "px;\n  overflow-y: auto !important;\n  outline: none;\n"], ["\n  height: auto !important;\n  max-height: ", "px;\n  overflow-y: auto !important;\n  outline: none;\n"])), function (p) { return p.height; });
var Search = styled('div')(templateObject_6 || (templateObject_6 = __makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  width: 100%;\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n    grid-gap: 0;\n    grid-template-columns: ", ";\n    justify-content: flex-end;\n  }\n\n  @media (min-width: ", ") {\n    width: 400px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  width: 100%;\n  margin-top: ", ";\n\n  @media (min-width: ", ") {\n    margin-top: 0;\n    grid-gap: 0;\n    grid-template-columns: ",
    ";\n    justify-content: flex-end;\n  }\n\n  @media (min-width: ", ") {\n    width: 400px;\n  }\n\n  @media (min-width: ", ") {\n    width: 600px;\n  }\n"])), space(2), space(1), function (props) { return props.theme.breakpoints[0]; }, function (p) {
    return p.children && React.Children.toArray(p.children).length === 1
        ? '1fr'
        : 'max-content 1fr';
}, function (props) { return props.theme.breakpoints[1]; }, function (props) { return props.theme.breakpoints[3]; });
// TODO(matej): remove this once we refactor SearchBar to not use css classes
// - it could accept size as a prop
var StyledSearchBar = styled(SearchBar)(templateObject_7 || (templateObject_7 = __makeTemplateObject(["\n  width: 100%;\n  position: relative;\n  .search-input {\n    height: 32px;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n\n  @media (min-width: ", ") {\n    ", "\n  }\n"], ["\n  width: 100%;\n  position: relative;\n  .search-input {\n    height: 32px;\n  }\n  .search-clear-form,\n  .search-input-icon {\n    height: 32px;\n    display: flex;\n    align-items: center;\n  }\n\n  @media (min-width: ", ") {\n    ",
    "\n  }\n"])), function (props) { return props.theme.breakpoints[0]; }, function (p) {
    return p.blendWithFilter &&
        "\n        .search-input,\n        .search-input:focus {\n          border-top-left-radius: 0;\n          border-bottom-left-radius: 0;\n        }\n      ";
});
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7;
//# sourceMappingURL=index.jsx.map
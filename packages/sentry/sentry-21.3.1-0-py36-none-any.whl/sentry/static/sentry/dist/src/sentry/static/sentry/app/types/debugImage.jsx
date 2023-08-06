// Candidate Processing Info
export var CandidateProcessingStatus;
(function (CandidateProcessingStatus) {
    CandidateProcessingStatus["OK"] = "ok";
    CandidateProcessingStatus["MALFORMED"] = "malformed";
    CandidateProcessingStatus["ERROR"] = "error";
})(CandidateProcessingStatus || (CandidateProcessingStatus = {}));
export var SymbolType;
(function (SymbolType) {
    SymbolType["UNKNOWN"] = "unknown";
    SymbolType["BREAKPAD"] = "breakpad";
    SymbolType["ELF"] = "elf";
    SymbolType["MACHO"] = "macho";
    SymbolType["PDB"] = "pdb";
    SymbolType["PE"] = "pe";
    SymbolType["SOURCEBUNDLE"] = "sourcebundle";
    SymbolType["WASM"] = "wasm";
    SymbolType["PROGUARD"] = "proguard";
})(SymbolType || (SymbolType = {}));
export var ImageFeature;
(function (ImageFeature) {
    ImageFeature["has_sources"] = "has_sources";
    ImageFeature["has_debug_info"] = "has_debug_info";
    ImageFeature["has_unwind_info"] = "has_unwind_info";
    ImageFeature["has_symbols"] = "has_symbols";
})(ImageFeature || (ImageFeature = {}));
// Candidate Download Status
export var CandidateDownloadStatus;
(function (CandidateDownloadStatus) {
    CandidateDownloadStatus["OK"] = "ok";
    CandidateDownloadStatus["MALFORMED"] = "malformed";
    CandidateDownloadStatus["NOT_FOUND"] = "notfound";
    CandidateDownloadStatus["ERROR"] = "error";
    CandidateDownloadStatus["NO_PERMISSION"] = "noperm";
    CandidateDownloadStatus["DELETED"] = "deleted";
    CandidateDownloadStatus["UNAPPLIED"] = "unapplied";
})(CandidateDownloadStatus || (CandidateDownloadStatus = {}));
// Debug Status
export var ImageStatus;
(function (ImageStatus) {
    ImageStatus["FOUND"] = "found";
    ImageStatus["UNUSED"] = "unused";
    ImageStatus["MISSING"] = "missing";
    ImageStatus["MALFORMED"] = "malformed";
    ImageStatus["FETCHING_FAILED"] = "fetching_failed";
    ImageStatus["TIMEOUT"] = "timeout";
    ImageStatus["OTHER"] = "other";
})(ImageStatus || (ImageStatus = {}));
//# sourceMappingURL=debugImage.jsx.map
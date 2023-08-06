import React from 'react';
import { IconFile } from 'app/icons';
import { fileExtensionToPlatform, getFileExtension } from 'app/utils/fileExtension';
import theme from 'app/utils/theme';
var FileIcon = function (_a) {
    var _b;
    var fileName = _a.fileName, _c = _a.size, providedSize = _c === void 0 ? 'sm' : _c, className = _a.className;
    var fileExtension = getFileExtension(fileName);
    var iconName = fileExtension ? fileExtensionToPlatform(fileExtension) : null;
    var size = (_b = theme.iconSizes[providedSize]) !== null && _b !== void 0 ? _b : providedSize;
    if (!iconName) {
        return <IconFile size={size} className={className}/>;
    }
    return (<img src={require("platformicons/svg/" + iconName + ".svg")} width={size} height={size} className={className}/>);
};
export default FileIcon;
//# sourceMappingURL=fileIcon.jsx.map
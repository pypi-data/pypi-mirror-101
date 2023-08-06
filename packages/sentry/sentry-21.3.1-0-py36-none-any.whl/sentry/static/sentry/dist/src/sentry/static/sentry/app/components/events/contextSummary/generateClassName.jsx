import { defined } from 'app/utils';
function generateClassname(name, version) {
    if (!defined(name)) {
        return '';
    }
    var lowerCaseName = name.toLowerCase();
    // amazon fire tv device id changes with version: AFTT, AFTN, AFTS, AFTA, AFTVA (alexa), ...
    if (lowerCaseName.startsWith('aft')) {
        return 'amazon';
    }
    if (lowerCaseName.startsWith('sm-') || lowerCaseName.startsWith('st-')) {
        return 'samsung';
    }
    if (lowerCaseName.startsWith('moto')) {
        return 'motorola';
    }
    if (lowerCaseName.startsWith('pixel')) {
        return 'google';
    }
    var formattedName = name
        .split(/\d/)[0]
        .toLowerCase()
        .replace(/[^a-z0-9\-]+/g, '-')
        .replace(/\-+$/, '')
        .replace(/^\-+/, '');
    if (formattedName === 'edge' && version) {
        var majorVersion = version.split('.')[0];
        var isLegacyEdge = majorVersion >= '12' && majorVersion <= '18';
        if (isLegacyEdge) {
            return 'legacy-edge';
        }
    }
    return formattedName;
}
export default generateClassname;
//# sourceMappingURL=generateClassName.jsx.map
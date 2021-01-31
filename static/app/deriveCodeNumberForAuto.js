function deriveCodeNumberForAuto(codeStr) {
    var codeSegments = codeStr.split('/');
    if (codeSegments.length != 4) {
        return false;
    }
    var lastSegment = codeSegments[codeSegments.length - 1];
    if (isNaN(lastSegment)) {
        return false;
    }
    return lastSegment;
}
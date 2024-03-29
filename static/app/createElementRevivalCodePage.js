var selectedOutageInfo_g = null;
jQuery(document).ready(function($) {
    // populate latest unrevived outages
    loadLatestUnrevivedOutages(outagesFetchFetchUrl_g, "displayTable", onOutageRowSelect);
    loadLatestCode(latestCodeFetchUrl_g, onLatestCodeFetch)
    setupDatetimepicker('datetimepicker');
    loadCodeTags(codeTagsFetchUrl_g, function(codeTags){setupAutocomplete(".autocom", codeTags)});
});

function onLatestCodeRefreshBtnClick() {
    loadLatestCode(latestCodeFetchUrl_g, onLatestCodeFetch)
}

function onOutageRowSelect(rowObjs) {
    if (rowObjs.length > 0) {
        selectedOutageInfo_g = rowObjs[0];
        displaySelectedElemInfo();
        populateSelectedOutageInForm();
    }
}

function onLatestCodeFetch(codeObj) {
    // console.log(codeObj);
    var latestCodeNum = deriveCodeNumberForAuto(codeObj["codeStr"]);
    var message = "";
    if (latestCodeNum === false) {
        message = "Please enter code number manually, since the latest code " + codeObj["codeStr"] + " is not in desired format for auto code generation";
    } else {
        message = "Latest code is " + latestCodeNum;
    }
    document.getElementById("latestCodeInfoSpan").textContent = message;
}

function populateSelectedOutageInForm() {
    if (selectedOutageInfo_g != null) {
        document.getElementById('elementName').value = selectedOutageInfo_g["elName"];
        document.getElementById('elementId').value = selectedOutageInfo_g["elId"];
        document.getElementById('elementType').value = selectedOutageInfo_g["elType"];
        document.getElementById('elementTypeId').value = selectedOutageInfo_g["elTypeId"];
        document.getElementById('rtoId').value = selectedOutageInfo_g["rtoId"];
    } else {
        document.getElementById('elementName').value = "";
        document.getElementById('elementId').value = "";
        document.getElementById('elementType').value = "";
        document.getElementById('elementTypeId').value = "";
        document.getElementById('rtoId').value = "";
    }
}

function displaySelectedElemInfo() {
    var displayElem = document.getElementById("selOutageDisplaySpan");
    if (selectedOutageInfo_g != null) {
        displayElem.innerText = "Selected element is " + selectedOutageInfo_g["elName"];
    } else {
        displayElem.innerText = "";
    }
}
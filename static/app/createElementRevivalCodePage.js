var selectedOutageInfo_g = null;
jQuery(document).ready(function($) {
    // populate latest unrevived outages
    loadLatestUnrevivedOutages(outagesFetchFetchUrl_g, "displayTable", onOutageRowSelect);
    loadLatestCode(latestCodeFetchUrl_g, onLatestCodeFetch)
});

function onOutageRowSelect(rowObjs) {
    if (rowObjs.length > 0) {
        selectedOutageInfo_g = rowObjs[0];
        populateSelectedOutageInForm();
    }
}

function onLatestCodeFetch(codeObj) {
    // console.log(codeObj);
    document.getElementById("latestCodeInfoSpan").textContent = "Latest code is " + codeObj["codeStr"].split('/').pop();
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
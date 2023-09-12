var selectedOutageInfo_g = null;
jQuery(document).ready(function($) {
    loadLatestUnrevivedOutages(outagesFetchFetchUrl_g, "displayTable", onOutageRowSelect);
    // setup datetime picker
    setupDatetimepicker('datetimepicker');
});


function onOutageRowSelect(rowObjs) {
    if (rowObjs.length > 0) {
        selectedOutageInfo_g = rowObjs[0];
        displaySelectedElemInfo();
        populateSelectedOutageInForm();
    }
}

function populateSelectedOutageInForm() {
    if (selectedOutageInfo_g != null) {
        document.getElementById('rtoId').value = selectedOutageInfo_g["rtoId"];
    } else {
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

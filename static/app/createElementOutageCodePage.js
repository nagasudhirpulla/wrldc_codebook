var selectedElemInfo_g = null;
jQuery(document).ready(function($) {
    // populate element types
    loadElementTypes(elTypesFetchUrl_g, "elTypesSelect");
    // setup datetime picker
    setupDatetimepicker('datetimepicker');
    loadLatestCode(latestCodeFetchUrl_g, onLatestCodeFetch)
});

function onLatestCodeRefreshBtnClick() {
    loadLatestCode(latestCodeFetchUrl_g, onLatestCodeFetch)
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

function onElemRowSelect(rowObjs) {
    if (rowObjs.length > 0) {
        selectedElemInfo_g = rowObjs[0];
        displaySelectedElemInfo();
        populateSelectedElemInForm();
    }
}

function populateSelectedElemInForm() {
    if (selectedElemInfo_g != null) {
        document.getElementById('elementName').value = selectedElemInfo_g["elementName"];
        document.getElementById('elementId').value = selectedElemInfo_g["elementId"];
        document.getElementById('elementType').value = selectedElemInfo_g["elementType"];
        document.getElementById('elementTypeId').value = selectedElemInfo_g["elementTypeId"];
    } else {
        document.getElementById('elementName').value = "";
        document.getElementById('elementId').value = "";
        document.getElementById('elementType').value = "";
        document.getElementById('elementTypeId').value = "";
    }
}

function resetElemInfo() {
    // populate element name and element id
    document.getElementById('elementName').value = "";
    document.getElementById('elementId').value = "";
    document.getElementById('elementType').value = "";
    document.getElementById('elementTypeId').value = "";
}

function displaySelectedElemInfo() {
    var displayElem = document.getElementById("selElemDisplaySpan");
    if (selectedElemInfo_g != null) {
        displayElem.innerText = selectedElemInfo_g["elementName"];
    } else {
        displayElem.innerText = "";
    }
}

function onElTypeChange() {
    // clear element info in form
    // populate element type info in form
    selectedElemInfo_g = null;
    populateSelectedElemInForm();
    displaySelectedElemInfo();
    populateOutageTypes();
    loadElements(elsFetchBaseUrl_g, "elTypesSelect", "displayTable", onElemRowSelect);
}

function populateOutageTypes() {
    var oTypeSelEl = document.getElementById("outageTypeSelEl");
    // remove all options from outage Type selection
    $(oTypeSelEl).find('option').remove();
    // clear outage tag and outage type
    $("#outageTypeId").val("");
    $("#outageTagId").val("");
    $("#outageType").val("");
    $("#outageTag").val("");
    // check if selected element type is a generator
    var isElemTypeGen = ($("#elTypesSelect option:selected").text() == "GENERATING_UNIT");
    for (var i = 0; i < oTypes_g.length; i++) {
        var oType = oTypes_g[i];
        if ((oType.id == "") || (oType.isGenerator == 0 && !isElemTypeGen) || (oType.isGenerator == 1 && isElemTypeGen)) {
            var oTypeOpt = new Option(oType.name, oType.id);
            $(oTypeOpt).html(oType.name);
            $(oTypeSelEl).append(oTypeOpt);
        }
    }
}

function onOutageTypeChange() {
    // set outage type form values
    var oTypeId = $("#outageTypeSelEl").val();
    $("#outageTypeId").val(oTypeId);
    $("#outageType").val($("#outageTypeSelEl option:selected").text());
    // set outage tag form values
    $("#outageTagId").val("");
    $("#outageTag").val("");
    // remove all options from outage Tag selection
    var oTagSelEl = document.getElementById("outageTagSelEl");
    $(oTagSelEl).find('option').remove();
    // populate outage tag options
    for (var i = 0; i < oTags_g.length; i++) {
        var oTag = oTags_g[i];
        if ((oTag.outageTypeId == oTypeId) || (oTag.id == "")) {
            var oTagOpt = new Option(oTag.name, oTag.id);
            $(oTagOpt).html(oTag.name);
            $(oTagSelEl).append(oTagOpt);
        }
    }
}

function onOutageTagChange() {
    // set form values
    $("#outageTagId").val($("#outageTagSelEl").val());
    $("#outageTag").val($("#outageTagSelEl option:selected").text());
}
var selOutageInfo_g = null;
jQuery(document).ready(function($) {
    // populate code Request
    loadCodeRequest(codeRequestFetchUrl_g, "displayTable", onOutageRowSelect);
    // setup datetime picker
    setupDatetimepicker('datetimepicker');
    loadLatestCode(latestCodeFetchUrl_g, onLatestCodeFetch);
    loadCodeTags(codeTagsFetchUrl_g, function(codeTags){setupAutocomplete(".autocom", codeTags)});
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

function onOutageRowSelect(rowObjs) {
    if (rowObjs.length > 0) {
        selOutageInfo_g = rowObjs[0];
        displaySelectedElemInfo();
        populateDescriptionInForm();
        populateSelOutageInForm();
        populateOutageTypes();
    }
}

function populateDescriptionInForm() {
    if (selOutageInfo_g != null) {
        document.getElementById('codeDescription').value = selOutageInfo_g["description"];
    }
    else{
        document.getElementById('codeDescription').value ="" ;
    }

}

function populateSelOutageInForm() {
    if (selOutageInfo_g != null) {
        document.getElementById('elementName').value = selOutageInfo_g["elementName"];
        document.getElementById('elementId').value = selOutageInfo_g["elementId"];
        document.getElementById('elementType').value = selOutageInfo_g["elementType"];
        document.getElementById('elementTypeId').value = selOutageInfo_g["elementTypeId"];
        document.getElementById('sdReqId').value = selOutageInfo_g["outageRequestId"];
        document.getElementById('rtoId').value = selOutageInfo_g["outageId"];
        document.getElementById('codeType').value = selOutageInfo_g["codeType"].value;
        document.getElementById('codeReqId').value = selOutageInfo_g["id"];
        // var stakeholders= [];
        // if(selOutageInfo_g["concernedStakeholders"]!= null)
        // {
        //     for(var x = 0; x < selOutageInfo_g["concernedStakeholders"].length; x++)
        //         stakeholders.push(selOutageInfo_g.concernedStakeholders[x].item2);
        // }
        // const requester = selOutageInfo_g["requester"];
        // if(!stakeholders.includes(requester)){
        //     stakeholders.push(requester);
        // }
        // console.log(stakeholders)
        // document.getElementById('codeIssuedTo').value = stakeholders.join(", ");
        document.getElementById('codeIssuedTo').value = selOutageInfo_g["testStakeholders"];
    } else {
        document.getElementById('elementName').value = "";
        document.getElementById('elementId').value = "";
        document.getElementById('elementType').value = "";
        document.getElementById('elementTypeId').value = "";
        document.getElementById('sdReqId').value = "";
        document.getElementById('rtoId').value = "" ;
        document.getElementById('codeType').value ="" ;
        document.getElementById('codeIssuedTo').value = "";
        document.getElementById('codeReqId').value ="" ;
    }
}

function displaySelectedElemInfo() {
    var displayElem = document.getElementById("selApprovalDisplaySpan");
    if (selOutageInfo_g != null) {
        displayElem.innerText = selOutageInfo_g["elementName"];
    } else {
        displayElem.innerText = "";
    }
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
    // check if element of selected outage is a generator
    var isElemTypeGen = (document.getElementById('elementType').value == "GENERATING_UNIT");
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
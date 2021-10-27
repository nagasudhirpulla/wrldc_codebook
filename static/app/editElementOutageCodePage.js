var selectedElemInfo_g = null;
jQuery(document).ready(function($) {
    // setup datetime picker
    setupDatetimepicker('datetimepicker');
    //initialize element name span
    $("#elemNameDisplaySpan").text(code_g.pwcElName);
    // initialize outage types options
    initOutageTypesOptions();
    // set outage type value based on code object
    $("#outageTypeSelEl").val($("#outageTypeId").val());
    var defOutageTagId = $("#outageTagId").val();
    var defOutageTag = $("#outageTag").val();
    // trigger outage type change
    onOutageTypeChange();
    $("#outageTagId").val(defOutageTagId);
    $("#outageTag").val(defOutageTag);
    // set outage tag value as per code object
    $("#outageTagSelEl").val($("#outageTagId").val());
    loadCodeTags(codeTagsFetchUrl_g, function(codeTags){setupAutocomplete(".autocom", codeTags)});
});

function initOutageTypesOptions() {
    var oTypeSelEl = document.getElementById("outageTypeSelEl");
    // remove all options from outage Type selection
    $(oTypeSelEl).find('option').remove();
    // clear outage tag and outage type
    // check if selected element type is a generator
    var isElemTypeGen = (code_g.pwcElType == "GENERATING_UNIT");
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
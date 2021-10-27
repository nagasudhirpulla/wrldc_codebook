var selectedElemInfo_g = null;
jQuery(document).ready(function($) {
    // setup datetime picker
    setupDatetimepicker('datetimepicker');
    //initialize element name span
    $("#elemNameDisplaySpan").text(code_g.pwcElName);
    loadCodeTags(codeTagsFetchUrl_g, function(codeTags){setupAutocomplete(".autocom", codeTags)});
});
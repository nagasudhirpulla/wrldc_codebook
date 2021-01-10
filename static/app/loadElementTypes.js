function loadElementTypes(fetchUrl, selElId) {
    $.ajax({
        url: fetchUrl,
        type: 'get',
        contentType: "application/json",
        success: function(resp) {
            if (resp.hasOwnProperty('elTypes')) {
                var elTypesDropDownEl = document.getElementById(selElId);
                //remove all options from select list
                var elTypesDropDownLen = elTypesDropDownEl.options.length;
                for (i = elTypesDropDownLen - 1; i >= 0; i--) {
                    elTypesDropDownEl.options[i] = null;
                }
                var elTypes = resp['elTypes'];
                elTypes.unshift("Select");
                for (var i = 0; i < elTypes.length; i++) {
                    var option = document.createElement("option");
                    txt = document.createTextNode(elTypes[i]);
                    option.appendChild(txt);
                    option.setAttribute("value", elTypes[i]);
                    elTypesDropDownEl.add(option);
                }
            } else {
                console.log('response not desired for fetching element types');
                console.log(resp);
            }
        },
        error: function(jqXHR, exception) {
            console.log(jqXHR);
            console.log(exception);
        }
    });


}
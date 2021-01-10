function loadElements(fetchUrl, selElId, elTableId) {
    var selElType = document.getElementById(selElId).value;
    $.ajax({
        url: fetchUrl + selElType,
        type: 'get',
        contentType: "application/json",
        success: function(resp) {
            if (resp.hasOwnProperty('elements')) {
                var elemsList = resp["elements"]
                console.log(elemsList);
                if (elemsList.length > 0) {
                    // populate elements table only if number of elements > 0
                    var colNames = Object.keys(elemsList[0]);
                    const elNameInd = colNames.indexOf("elementName");
                    if (elNameInd >= 0) {
                        colNames.splice(elNameInd, 1);
                        colNames.unshift("elementName")
                    }
                    var dtColumns = [];
                    for (var i = 0; i < colNames.length; i++) {
                        dtColumns.push({ title: colNames[i], data: colNames[i] });
                    }
                    $('#' + elTableId).DataTable({
                        data: elemsList,
                        columns: dtColumns,
                        select: {
                            style: 'single'
                        }
                    });
                    // $("#displayTable").DataTable().row({selected:true}).data()
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
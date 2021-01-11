function loadElements(fetchUrl, selElId, elTableId, onRowSelect) {
    if ($.fn.DataTable.isDataTable('#' + elTableId)) {
        $('#' + elTableId).DataTable().destroy();
        $('#' + elTableId + ' tbody').empty();
        $('#' + elTableId + ' thead').empty();
    }
    var elTypeSelector = document.getElementById(selElId);
    var selElType = elTypeSelector.options[elTypeSelector.selectedIndex].text;
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

                    for (var i = 0; i < elemsList.length; i++) {
                        elemsList[i]["elementType"] = selElType;
                        elemsList[i]["elementTypeId"] = elTypeSelector.value;
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
                    $('#' + elTableId).on('select.dt', function(e, dt, type, indexes) {
                        // get the array of rows
                        var rowsData = dt.rows(indexes).data();
                        // console.log(data);
                        onRowSelect(rowsData);
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
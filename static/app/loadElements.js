function loadElements(fetchUrl, selElId, elTableId, onRowSelect) {
    if ($.fn.DataTable.isDataTable('#' + elTableId)) {
        $('#' + elTableId).DataTable().destroy();
        $('#' + elTableId + ' tbody').empty();
        $('#' + elTableId + ' thead').empty();
        $('#' + elTableId + ' tfoot').remove();
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
                    // move element name column to first
                    var elNameInd = colNames.indexOf("elementName");
                    if (elNameInd >= 0) {
                        colNames.splice(elNameInd, 1);
                        colNames.unshift("elementName")
                    }
                    // remove element id column
                    var elIdInd = colNames.indexOf("elementId");
                    if (elIdInd >= 0) {
                        colNames.splice(elIdInd, 1);
                    }
                    for (var i = 0; i < elemsList.length; i++) {
                        elemsList[i]["elementType"] = selElType;
                        elemsList[i]["elementTypeId"] = elTypeSelector.value;
                    }

                    var dtColumns = [];
                    for (var i = 0; i < colNames.length; i++) {
                        dtColumns.push({ title: colNames[i], data: colNames[i] });
                    }

                    // create footer th elements
                    var footerHtml = "<tfoot><tr>";
                    for (var i = 0; i < dtColumns.length; i++) {
                        footerHtml += '<th>' + dtColumns[i].title + '</th>';
                    }
                    footerHtml += "</tr></tfoot>";
                    $("#" + elTableId).append(footerHtml);

                    // Setup - add a text input to each footer cell
                    $('#' + elTableId + ' tfoot th').each(function() {
                        //var title = $(this).text();
                        $(this).html('<input type="text" placeholder="Search" />');
                    });

                    var dataTable = $('#' + elTableId).DataTable({
                        data: elemsList,
                        columns: dtColumns,
                        lengthMenu: [
                            [10, 20, 50, 100, -1],
                            [10, 20, 50, 100, "All"]
                        ],
                        select: {
                            style: 'single'
                        },
                        order: [
                            [0, "desc"]
                        ],
                        dom: 'Bfrtip',
                        fixedHeader: true,
                        buttons: ['pageLength', 'copy', 'excel', 'pdf', 'csv', 'print']
                    });

                    // setup column based search
                    var r = $('#' + elTableId + ' tfoot tr');
                    r.find('th').each(function() {
                        $(this).css('padding', '3px');
                    });
                    $('#' + elTableId + ' thead').append(r);
                    $('#' + elTableId + " thead input").on('keyup change', function() {
                        dataTable
                            .column($(this).parent().index() + ':visible')
                            .search(this.value)
                            .draw();
                    });

                    // setup row selection listener
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
function loadCodeRequest(fetchUrl, tableId, onRowSelect) {
    if ($.fn.DataTable.isDataTable('#' + tableId)) {
        $('#' + tableId).DataTable().destroy();
        $('#' + tableId + ' tbody').empty();
        $('#' + tableId + ' thead').empty();
        $('#' + tableId + ' tfoot').remove();
    }
    
    
    $.ajax({
        url: fetchUrl,
        type: 'get',
        contentType: "application/json",
        success: function(resp) {
            if (resp.hasOwnProperty("outages")) {
                var outagesList = resp["outages"]
                console.log(outagesList);
                if (outagesList.length > 0) {
                   
                    // populate code request table only if number of rows > 0
                    var dtColumns = [
                        { title: "desired Execution Start Time", data: "desiredExecutionStartTime" },
                        { title: "desired Execution End Time", data: "desiredExecutionEndTime" },
                        { title: "Element", data: "elementName" },
                        { title: "Element Type", data: "elementType" },
                        { title: "Reason", data: "description" },
                        { title: "Outage Type", data: "outageType" },
                        { title: "Requester", data: "requester" },
                        { title: "Requester Remarks", data: "remarks" },
                        { title: "Code Type", data: "codeType.value" }
                    ];

                    // create footer th elements
                    var footerHtml = "<tfoot><tr>";
                    for (var i = 0; i < dtColumns.length; i++) {
                        footerHtml += '<th>' + dtColumns[i].title + '</th>';
                    }
                    footerHtml += "</tr></tfoot>";
                    $("#" + tableId).append(footerHtml);

                    // Setup - add a text input to each footer cell
                    $('#' + tableId + ' tfoot th').each(function() {
                        //var title = $(this).text();
                        $(this).html('<input type="text" placeholder="Search" />');
                    });

                    var dataTable = $('#' + tableId).DataTable({
                        data: outagesList,
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
                    var r = $('#' + tableId + ' tfoot tr');
                    r.find('th').each(function() {
                        $(this).css('padding', '3px');
                    });
                    $('#' + tableId + ' thead').append(r);
                    $('#' + tableId + " thead input").on('keyup change', function() {
                        dataTable
                            .column($(this).parent().index() + ':visible')
                            .search(this.value)
                            .draw();
                    });

                    // setup row selection listener
                    $('#' + tableId).on('select.dt', function(e, dt, type, indexes) {
                        // get the array of rows
                        var rowsData = dt.rows(indexes).data();
                        // console.log(data);
                        onRowSelect(rowsData);
                    });
                    // $("#displayTable").DataTable().row({selected:true}).data()
                }
            } else {
                console.log('response not desired for fetching approved outages');
                console.log(resp);
            }
        },
        error: function(jqXHR, exception) {
            console.log(jqXHR);
            console.log(exception);
        }
    });
}
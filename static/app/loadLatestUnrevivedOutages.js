function loadLatestUnrevivedOutages(fetchUrl, outagesTableId, onRowSelect) {
    if ($.fn.DataTable.isDataTable('#' + outagesTableId)) {
        $('#' + outagesTableId).DataTable().destroy();
        $('#' + outagesTableId + ' tbody').empty();
        $('#' + outagesTableId + ' thead').empty();
        $('#' + outagesTableId + ' tfoot').remove();
    }
    $.ajax({
        url: fetchUrl,
        type: 'get',
        contentType: "application/json",
        success: function(resp) {
            if (resp.hasOwnProperty('outages')) {
                var outagesList = resp["outages"]
                console.log(outagesList);
                if (outagesList.length > 0) {
                    // populate outages table only if number of elements > 0
                    // var colNames = Object.keys(outagesList[0]);
                    var dtColumns = [
                        { title: "Outage Time", data: "outageDt" },
                        { title: "Expected Revival", data: "expectedRevDt" },
                        { title: "Element Name", data: "elName" },
                        { title: "Code", data: "code" },
                        { title: "Outage Type", data: "outageType" },
                        { title: "Outage Tag", data: "outageTag" },
                        { title: "Reason", data: "reason" },
                        { title: "Remarks", data: "outageRemarks" },
                        { title: "Element Type", data: "elType" }
                    ];

                    // create footer th elements
                    var footerHtml = "<tfoot><tr>";
                    for (var i = 0; i < dtColumns.length; i++) {
                        footerHtml += '<th>' + dtColumns[i].title + '</th>';
                    }
                    footerHtml += "</tr></tfoot>";
                    $("#" + outagesTableId).append(footerHtml);

                    // Setup - add a text input to each footer cell
                    $('#' + outagesTableId + ' tfoot th').each(function() {
                        //var title = $(this).text();
                        $(this).html('<input type="text" placeholder="Search" />');
                    });

                    var dataTable = $('#' + outagesTableId).DataTable({
                        data: outagesList,
                        columns: dtColumns,
                        lengthMenu: [
                            [10, 20, 50, 100, -1],
                            [10, 20, 50, 100, "All"]
                        ],
                        order: [
                            [0, "desc"]
                        ],
                        select: {
                            style: 'single'
                        },
                        dom: 'Bfrtip',
                        fixedHeader: true,
                        buttons: ['pageLength', 'copy', 'excel', 'pdf', 'csv', 'print']
                    });

                    // setup column based search
                    var r = $('#' + outagesTableId + ' tfoot tr');
                    r.find('th').each(function() {
                        $(this).css('padding', '3px');
                    });
                    $('#' + outagesTableId + ' thead').append(r);
                    $('#' + outagesTableId + " thead input").on('keyup change', function() {
                        dataTable
                            .column($(this).parent().index() + ':visible')
                            .search(this.value)
                            .draw();
                    });

                    // setup row selection listener
                    $('#' + outagesTableId).on('select.dt', function(e, dt, type, indexes) {
                        // get the array of rows
                        var rowsData = dt.rows(indexes).data();
                        onRowSelect(rowsData);
                    });
                }
            } else {
                console.log('response not desired for fetching latest unrevived outages');
                console.log(resp);
            }
        },
        error: function(jqXHR, exception) {
            console.log(jqXHR);
            console.log(exception);
        }
    });
}
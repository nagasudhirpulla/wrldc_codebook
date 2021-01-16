function loadLatestUnrevivedOutages(fetchUrl, outagesTableId, onRowSelect) {
    if ($.fn.DataTable.isDataTable('#' + outagesTableId)) {
        $('#' + outagesTableId).DataTable().destroy();
        $('#' + outagesTableId + ' tbody').empty();
        $('#' + outagesTableId + ' thead').empty();
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
                        { title: "Element Name", data: "elName" },
                        { title: "Outage Type", data: "outageType" },
                        { title: "Outage Tag", data: "outageTag" },
                        { title: "Reason", data: "reason" },
                        { title: "Remarks", data: "outageRemarks" },
                        { title: "Element Type", data: "elType" }
                    ];
                    $('#' + outagesTableId).DataTable({
                        data: outagesList,
                        columns: dtColumns,
                        select: {
                            style: 'single'
                        }
                    });
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
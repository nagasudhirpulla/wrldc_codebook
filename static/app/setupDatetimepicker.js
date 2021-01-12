function setupDatetimepicker(pickerClass) {
    if (window.jQuery().datetimepicker) {
        $('.' + pickerClass).datetimepicker({
            // https://github.com/technovistalimited/bootstrap4-datetimepicker#user-content-installation
            // MomentJS Formats: https://momentjs.com/docs/#/displaying/format/
            format: 'YYYY-MM-DD HH:mm',
            // as Bootstrap 4 is not using Glyphicons anymore
            icons: {
                time: 'fa fa-clock',
                date: 'fa fa-calendar',
                up: 'fa fa-chevron-up',
                down: 'fa fa-chevron-down',
                previous: 'fa fa-chevron-left',
                next: 'fa fa-chevron-right',
                today: 'fa fa-check',
                clear: 'fa fa-trash',
                close: 'fa fa-times'
            }
        });
    };
}
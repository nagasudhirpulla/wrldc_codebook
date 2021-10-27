function loadCodeTags(fetchUrl, onCodeTagsFetch) {
    $.ajax({
        url: fetchUrl,
        type: 'get',
        contentType: "application/json",
        success: function (resp) {
            if (resp.hasOwnProperty('codeTags')) {
                var codeTags = resp['codeTags'];
                onCodeTagsFetch(codeTags);
            } else {
                console.log('response not desired for fetching code tags');
                console.log(resp);
            }
        },
        error: function (jqXHR, exception) {
            console.log(jqXHR);
            console.log(exception);
        }
    });
}
function loadLatestCode(fetchUrl, onLatestCodeFetch) {
    $.ajax({
        url: fetchUrl,
        type: 'get',
        contentType: "application/json",
        success: function(resp) {
            if (resp.hasOwnProperty('code')) {
                var code = resp['code'];
                onLatestCodeFetch(code);
            } else {
                console.log('response not desired for fetching latest code');
                console.log(resp);
            }
        },
        error: function(jqXHR, exception) {
            console.log(jqXHR);
            console.log(exception);
        }
    });
}
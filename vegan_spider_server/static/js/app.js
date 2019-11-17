$(function() {

    const $ajax = function(url, type, data) {
        return $.ajax({
            url: url,
            type: type,
            data: data,
            dataType: "json"
        }).fail(
            function (xhr, status, error) {
                console.error(error);
            }
        )
    };

    $('.js-example-basic-single').select2({
        ajax: {
            delay: 250,
            url: 'http://127.0.0.1:8000/ingredients/',
            dataType: 'json',
            data: function(params) {
                return {search: params.term}
            },
            processResults: function (data) {
                return {results: data}
            }
        }
    });
});
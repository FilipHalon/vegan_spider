$(function () {
    const $btn = $('button');

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

    $btn.on("click", e => {
        e.preventDefault();
        const $data = $('form').serialize();
        $ajax('http://127.0.0.1:8000/user', 'POST', $data)
    })
});
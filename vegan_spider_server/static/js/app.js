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

    const $select2Ingredients = $('#select2-ingredients');

    const addNewIngredientRow = function(id, name, photo) {
        return $(`<ul>
                    <input type="hidden" value="${id}">
                    <li><img src="${photo}" alt="${name}"></li>
                    <li>${name}</li>
                    <li>
                        <input name="quantity" type="number">
                    </li>
                    <li>
                        <select name="unit">
                            <option value="gram" selected>gram</option>
                            <option value="kilogramow" selected>kilogramów</option>
                            <option value="mililitrow">mililitrów</option>
                            <option value="litrow">litrów</option>
                            <option value="sztuk">sztuk</option>
                        </select>
                    </li>
                    <li>
                        <button class="ingredient delete">Usuń</button>
                    </li>
                </ul>`)
    };

    let displayedIngredients;

    $('.ingredient.add').on("click", () => {
        const choices = $select2Ingredients.select2('data');
        console.log(choices);
        $select2Ingredients.val(null).trigger('change');

    });

    $select2Ingredients.select2({
        dropdownParent: $('#ingredient-search-form'),
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
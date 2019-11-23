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
        return $(`<li class="ingredient box">
                        <ul>
                            <li class="hidden">
                                <input class="ingredient id" type="hidden" name="ingredients" value="${id}">
                            </li>
                            <li><img src="${photo}" alt="${name}"></li>
                            <li>${name}</li>
                            <li>
                                <input name="quantity" type="number">
                            </li>
                            <li>
                                <select name="unit">
                                    <option value="gram" selected>gram</option>
                                    <option value="kilogram">kilogramów</option>
                                    <option value="millilitre">mililitrów</option>
                                    <option value="litre">litrów</option>
                                    <option value="number">sztuk</option>
                                </select>
                            </li>
                            <li>
                                <button class="ingredient delete">Usuń</button>
                            </li>
                        </ul>
                    </li>`)
    };

    const displayedIngredients = [];
    const $ingredientListDisplay = $(".ingredient.list.display");

    $('.ingredient.add').on("click", () => {
        const choices = $select2Ingredients.select2('data');
        $select2Ingredients.val(null).trigger('change');
        for (let ing of choices) {
            if (!displayedIngredients.includes(ing.id)) {
                displayedIngredients.push(ing.id);
                $ingredientListDisplay.append(addNewIngredientRow(ing.id, ing.text, ing.photo))
            }
        }
    });

    const $recipeDisplayRow = function (name, photo, desc, url, match) {
        return $(`<li>
                    <ul>
                        <li><img src="${photo}" alt="${name}"></li>
                        <li><a href="${url}">${name}</a></li>
                        <li>${desc}</li>
                        <li><a href="${url}">Przejdź do strony</a></li>
                        <li>
                            <ul class="ingredient display"></ul>
                        </li>
                        <li>Dopasowanie: ${match}</li>
                    </ul>
                </li>`)
    };

    const $ingredientListForm = $(".ingredient.list.form");
    const $recipeDisplayList = $(".recipe.list.display");

    $ingredientListForm.on("click", (e) => {
        e.preventDefault();
        const $target = $(e.target);
        if ($target.hasClass("delete")) {
            const ingredientBox = $target.closest('.ingredient.box');
            const ingredientId = ingredientBox.find('.ingredient.id').val();
            if (displayedIngredients.includes(ingredientId)) {
                displayedIngredients.splice(displayedIngredients.indexOf(ingredientId), 1);
            }
            ingredientBox.remove();
        }
        else if ($target.hasClass("search")) {
            const $ingredientList = $ingredientListForm.serialize();
            console.log($ingredientList);
            $ajax('http://127.0.0.1:8000/recipe_details/', 'GET', $ingredientList).done(resp => {
                resp.forEach(el => {
                    // const recipe = JSON.parse(el);
                    const recipe = el;
                    const match = recipe.ingredients_included/recipe.ingredient_count;
                    $recipeDisplayList.append($recipeDisplayRow(recipe.name, recipe.photo, recipe.desc, recipe.url, match));
                    const $ingredientDisplayList = $(".ingredient.display");
                    for (let ingredient of recipe.ingredients) {
                        $ingredientDisplayList.append($(`<li>${ingredient.name}</li>`))
                    }
                });
            })
        }
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
$(function() {

    /* to be added later:   <li>
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
                            </li> */


    const $ajax = function(url, type="GET", data) {
        return $.ajax({
            url: url,
            type: type,
            data: data,
            dataType: "json",
            headers: {'X-CSRFToken': window.CSRF_TOKEN}
        }).fail(
            function (xhr, status, error) {
                console.error(error);
            }
        )
    };

    const dataRequest = async (url) => {
        try {
            const res = await fetch(url);
            if (res.ok) {
                const jsonRes = await res.json();
                // console.log(jsonRes);
                // return jsonRes
            }
            throw Error("The data could not be collected")
        }
        catch (err) {
            console.log(err.message);
        }
    };

    // dataRequest('http://127.0.0.1:8000/user/current/')
    //     .then();

    /* User Profile Section */

    // Upload user data on page loading

    const displayedIngredients = [];

    const addOwnIngredientRow = function(id, name, photo) {
        return $(`<li class="ingredient instance box">
                        <form class="own list form">
                            <ul>
                                <div>
                                    <li class="hidden">
                                        <input class="ingredient id" type="hidden" name="ingredient" value="${id}">
                                    </li>
                                    <li><img src="${photo}" alt="${name}"></li>
                                    <li>${name}</li>
                                </div>
                                <div>
                                    <li>
                                        <button class="ingredient delete btn btn-outline-secondary">Usuń</button>
                                    </li>
                                </div>
                            </ul>
                        </form>
                    </li>`)
    };

    const $profilePhoto = $('.profile.photo');
    const $profileUsername = $('.profile.username');
    const $profileEmail = $('.profile.e-mail');
    const $profileFirstName = $('.profile.first_name');
    const $profileLastName = $('.profile.last_name');
    const $userIngredientList = $('.own.list.display');

    $ajax('http://127.0.0.1:8000/user/current/')
        .done(res => {

            $profilePhoto.html(`<img src="${res.photo}" alt="Zdjęcie profilowe">`);
            $profileUsername.text(res.username);
            $profileEmail.text(res.email);
            $profileFirstName.text(res.first_name);
            $profileLastName.text(res.last_name);

            const userIngredients = res.ingredients;
            for (let ing of userIngredients) {
                $userIngredientList.append(addOwnIngredientRow(ing.id, ing.text, ing.photo));
                displayedIngredients.push(`${ing.id}`);
                console.log(displayedIngredients);
            }
        });

    // Change user data on demand

    const profileDataForm = $('.profile-data.form');
    const profileDataChangeBtn = $('.profile-data.edit');
    const profileDataChangeCancelBtn = $('.profile-data.cancel');
    const userDataInputs = $('.profile.input');

    profileDataForm.on("click", e => {
        e.preventDefault();
        const $target = $(e.target);
        if ($target.hasClass("edit") || $target.hasClass("cancel")) {
            profileDataChangeBtn.toggleClass("save");
            profileDataChangeBtn.toggleClass("change");
            profileDataChangeCancelBtn.toggleClass("hidden");
            if (profileDataChangeBtn.hasClass("change")) {
                profileDataChangeBtn.text("Zmień dane");
            }
            else if (profileDataChangeBtn.hasClass("save")) {
                $target.text("Zatwierdź");
            }
            if ($target.hasClass("change")) {
                userDataInputs.each((i, input) => {
                input.innerHTML = `<input name="${input.id}" value=${input.innerText}>`
                })
            }
            else if ($target.hasClass("save")) {
                $ajax('http://127.0.0.1:8000/user/current/')
                    .done(res => {
                        const userId = res.id;
                        const detailsChanged = profileDataForm.serialize();
                        $ajax(`http://127.0.0.1:8000/user/${userId}/`, 'PATCH', detailsChanged)
                            .done(res => {
                                $profileEmail.text(res.email);
                                $profileFirstName.text(res.first_name);
                                $profileLastName.text(res.last_name);
                        })
                });
            }
            else if ($target.hasClass("cancel")) {
                $ajax('http://127.0.0.1:8000/user/current/')
                    .done(res => {
                        $profileEmail.text(res.email);
                        $profileFirstName.text(res.first_name);
                        $profileLastName.text(res.last_name);
                })
            }
        }
    });

    // User's ingredient list item delete on demand

    $userIngredientList.on("click", e => {
        const $target = $(e.target);
        if ($target.hasClass("delete")) {
            e.preventDefault();
            const $ownListSerialized = $target.closest(".own.list.form").serialize();
            const ingredientId = $ownListSerialized.split('=')[1];
            $ajax(`http://127.0.0.1:8000/user_ingredient_search/?${$ownListSerialized}`)
                .done(res => {
                    const idToDelete = res[0].id;
                    $ajax(`http://127.0.0.1:8000/user_ingredients/${idToDelete}/`, "DELETE");
                    $target.closest(".ingredient.instance.box").remove();
                    displayedIngredients.splice(displayedIngredients.indexOf(idToDelete), 1);
                    console.log(displayedIngredients);
            })
        }
    });

    // Ingredient select

    const $select2Ingredients = $('#select2-ingredients');

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

    // Ingredient add on the current list

    const addNewIngredientRow = function(id, name, photo) {
        return $(`<li class="ingredient instance box">
                        <ul>
                            <div>
                                <li class="hidden">
                                    <input class="ingredient id" type="hidden" name="ingredients" value="${id}">
                                </li>
                                <li><img src="${photo}" alt="${name}"></li>
                                <li>${name}</li>
                            </div>
                            <div>
                                <li>
                                    <button class="ingredient delete btn btn-outline-secondary">Usuń</button>
                                </li>
                            </div>
                        </ul>
                    </li>`)
    };

    const $ingredientListDisplay = $(".ingredient.list.display");

    $('.ingredient.add').on("click", () => {
        const choices = $select2Ingredients.select2('data');
        $select2Ingredients.val(null).trigger('change');
        for (let ing of choices) {
            if (!displayedIngredients.includes(ing.id)) {
                displayedIngredients.push(ing.id);
                console.log(displayedIngredients);
                $ingredientListDisplay.append(addNewIngredientRow(ing.id, ing.text, ing.photo))
            }
        }
    });

    // Recipe search / user ingredient list update

    const $recipeDisplayRow = function (id, name, photo, desc, url, match) {
        return $(`<li class="recipe instance box">
                    <ul class="row">
                        <div class="col-3">
                            <li><img src="${photo}" alt="${name}"></li>
                            <li><a href="${url}">${name}</a></li>
                        </div>
                        <div class="col-3">
                            <li>${desc}</li>
                            <li><a href="${url}">Przejdź do strony</a></li>
                        </div>
                        <div class="col-2">
                            <li>
                                <ul class="recipe ${id} ingredient list display"></ul>
                            </li>
                        </div>
                        <div class="col-2">
                            <li>Dopasowanie: ${match}</li>
                        </div>
                    </ul>
                </li>`)
    };

    const $ingredientListForm = $(".ingredient.list.form");
    const $recipeSection = $("section.recipe.list");
    const $recipeDisplayList = $(".recipe.list.display");

    $ingredientListForm.on("click", (e) => {
        e.preventDefault();
        const $target = $(e.target);
        if ($target.hasClass("delete")) {
            const ingredientBox = $target.closest('.ingredient.box');
            const ingredientId = ingredientBox.find('.ingredient.id').val();
            if (displayedIngredients.includes(ingredientId)) {
                displayedIngredients.splice(displayedIngredients.indexOf(ingredientId), 1);
                console.log(displayedIngredients);
            }
            ingredientBox.remove();
        }
        else if ($target.hasClass("search")) {
            $recipeSection.removeClass("hidden");
            // const $ingredientList = $ingredientListForm.serialize();
            let ingredientList = '';
            displayedIngredients.forEach((ingr, i) => {
               ingredientList += `ingredients=${ingr}`;
               if (i < displayedIngredients.length-1) {
                   ingredientList += '&';
               }
            });
            $recipeDisplayList.children().remove();
            $ajax('http://127.0.0.1:8000/recipe_details/', 'GET', ingredientList).done(resp => {
                resp.forEach(recipe => {
                    const ingredientsIncluded = recipe.ingredients_included ? recipe.ingredients_included : 0;
                    const match = Math.round(parseFloat(ingredientsIncluded)/parseFloat(recipe.ingredients_count)*100)/100;
                    $recipeDisplayList.append($recipeDisplayRow(recipe.id, recipe.name, recipe.photo, recipe.desc, recipe.url, match));
                    const $ingredientDisplayList = $(`.recipe.${recipe.id}.ingredient.list.display`);
                    for (let ingredient of recipe.ingredients) {
                        $ingredientDisplayList.append($(`<li>${ingredient.text}</li>`))
                    }
                });
            })
        }
        else if ($target.hasClass("own")) {
            const $ingredientList = $ingredientListForm.serialize();
            $ajax('/', "POST", $ingredientList)
                .done(() => {
                    $ingredientListDisplay.children().remove();
                    $ajax('http://127.0.0.1:8000/user/current/')
                        .done(res => {
                            $userIngredientList.children().remove();
                            const userIngredients = res.ingredients;
                            for (let ing of userIngredients) {
                                $userIngredientList.append(addOwnIngredientRow(ing.id, ing.text, ing.photo));
                    }
                })
            })
        }
    });
});
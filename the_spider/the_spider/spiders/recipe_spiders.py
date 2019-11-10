import scrapy


class LidlRecipeSpider(scrapy.Spider):
    name = "lidl"
    start_urls = [
        'https://kuchnialidla.pl/przepisy/weganskie',
    ]

    def parse(self, response):

        # if response:
        #     for ingredient in response.css('.skladniki li::text').getall():
        #         ingredient = ingredient.split(' – ')
        #         if len(ingredient) == 2:
        #             yield {
        #                 f'{ingredient[0]}': ingredient[1],
        #             }

        # for a in response.css('.recipe_box .description'):
        #     yield response.follow(a, callback=self.parse)
        recipes = response.css('.recipe_box .description::attr(href)').getall()
        for recipe in recipes:
            yield response.follow(recipe,
                                  self.parse_recipe)
                                  # cb_kwargs={'recipe_name': ' '.join(recipe.split('-'))[1:]})

        # next_url = response.css('.pager a').re('/przepisy/weganskie/\d+#lista')
        next_page = response.css('.pager .nextPage::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
        # for a in response.css('.pager a').re('/przepisy/weganskie/\d+#lista'):
        #     yield response.follow(a, callback=self.parse)

    def parse_recipe(self, response):
        # recipe_name = response.css('h1::text').get()
        # ingredient_list = response.css('.skladniki li::text').getall()
        ingredient_list = response.css('li::text').getall()
        ingredients = {}
        for ingredient in ingredient_list:
            ingredient = ingredient.split(' – ')
            if len(ingredient) == 2:
                ingredients[f'{ingredient[0]}'] = ingredient[1]
            else:
                if isinstance(ingredients, dict):
                    ingredients = list(ingredients)
                ingredients += ingredient

        yield {
            'recipe_name': response.css('h1::text').get(),
            'ingredients': ingredients,
        }

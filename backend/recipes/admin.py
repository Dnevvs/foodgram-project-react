from django.contrib import admin

from .models import (Favorites, Ingredient, Recipe, RecipeIngredient,
                     Shopping_Cart, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'pub_date',
        'author',
    )
    readonly_fields = ('show_count',)
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    ordering = ('-pub_date', )
    empty_value_display = '-пусто-'

    def show_count(self, obj):
        count = Favorites.objects.filter(recipe=obj).count()
        return count

    show_count.short_description = 'В избранном'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter = ('name', )


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Favorites)
admin.site.register(Shopping_Cart)

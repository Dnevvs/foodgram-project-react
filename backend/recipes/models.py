from datetime import datetime

from colorfield.fields import ColorField
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import Sum, UniqueConstraint
from django.http import HttpResponse
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название тэга',
        max_length=200,
        unique=True)
    color = ColorField(
        verbose_name='Цвет тега',
        unique=True,
        default='#FF0000',
        validators=[
            RegexValidator(
                regex="^#([A-Fa-f0-9]{6})$",
                message='Должен быть формат HEX!',
            )
        ],
    )
    slug = models.SlugField(
        verbose_name='Слаг тэга',
        max_length=200,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='Набор символов неверный',
            ),
        ]
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэг рецепта'
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200
    )
    measurement_unit = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_cart',
        verbose_name='Ингредиенты рецепта',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=[MinValueValidator(1, 'Количество < 1')],
        default=1)

    class Meta:
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        default_related_name = 'ingridients_recipe'
        constraints = [
            models.UniqueConstraint(
                fields=('ingredient', 'amount'),
                name='Unique_Ingredient_Amount')]

    def __str__(self):
        return f'{self.ingredient.name} ' \
               f'{self.amount} {self.ingredient.measurement_unit},'


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    name = models.CharField(max_length=200,
                            verbose_name='Название рецепта',
                            unique=True,
                            db_index=True)
    image = models.ImageField(upload_to='recipes/images/',
                              blank=True,
                              default=None)
    text = models.TextField('Описание рецепта')
    cooking_time = models.PositiveSmallIntegerField(
        null=False,
        validators=([
            MinValueValidator(
                1,
                message='Время приготовления должно больше или равно 1 минуте')
        ]),
        default=1)
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)
    ingredients = models.ManyToManyField(
        RecipeIngredient,
        verbose_name='Ингредиенты рецепта',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes',
    )

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class Shopping_Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт',
    )

    def __str__(self):
        return f'Список покупок пользовтеля {self.user}'

    def shopping_cart_to_txt(self, request):
        user = request.user
        shopping_cart = f'{user.get_full_name()}:\n\nСписок покупок:\n\n'
        if not user.shopping_cart.exists():
            shopping_cart += 'Нет покупок'
        else:
            ingredients = RecipeIngredient.objects.filter(
                recipes__shopping_cart__user=request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit'
            ).annotate(amount=Sum('amount'))
            shopping_cart += '\n'.join([
                f'- {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]})'
                f' - {ingredient["amount"]}'
                for ingredient in ingredients
            ])
        shopping_cart += f'\n\n{datetime.today():%Y-%m-%d}\n'
        filename = f'{user.username}_shopping_cart.txt'
        response = HttpResponse(
            shopping_cart, content_type='text.txt; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'
            )
        ]


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        default=None,
    )

    def __str__(self):
        return f'Избранное пользователя {self.user}'

    class Meta:
        ordering = ('user',)
        verbose_name = 'Избранное пользователя'
        verbose_name_plural = 'Избранное пользователя'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favourites',
            )
        ]

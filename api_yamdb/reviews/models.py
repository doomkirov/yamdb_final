from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year


class User(AbstractUser):
    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'
    MODERATOR_ROLE = 'moderator'
    ROLES = [
        (USER_ROLE, 'User'),
        (ADMIN_ROLE, 'Administrator'),
        (MODERATOR_ROLE, 'Moderator'),

    ]
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(
        'Код подтверждения', blank=True, max_length=50
    )
    role = models.CharField(
        'Роль', max_length=50, choices=ROLES, default='user'
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user_email'),
        ]
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True, max_length=50
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True, max_length=50
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256
    )
    year = models.IntegerField(
        verbose_name='Дата выхода',
        validators=[validate_year],
        db_index=True
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория',
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        db_index=True
    )
    description = models.TextField(
        'Описание произведения',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        verbose_name='Жанр',
        db_index=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.SET_NULL,
        verbose_name='Произведение',
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        verbose_name='Жанр',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.genre.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Название произведения'
    )
    text = models.TextField(max_length=500, verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(limit_value=1, message='Минимальная оценка 1'),
            MaxValueValidator(limit_value=10, message='Максимальная оценка 10')
        ],
        verbose_name='Оценка произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review_author'
            )
        ]

    def __str__(self):
        return self.text[:10]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Комментарий к отзыву'
    )
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария к отзыву'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации комментария'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Комментарий к отзывам'
        verbose_name_plural = 'Комментарии к отзывам'

    def __str__(self):
        return self.text[:10]

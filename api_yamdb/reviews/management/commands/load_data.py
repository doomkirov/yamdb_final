from csv import DictReader

from django.core.management import BaseCommand

from reviews.models import (
    User, Title, Category, Genre, GenreTitle, Review, Comment
)


CSV_MODELS = [
    [User, 'users.csv'],
    [Category, 'category.csv'],
    [Genre, 'genre.csv'],
    [Title, 'titles.csv'],
    [GenreTitle, 'genre_title.csv'],
    [Review, 'review.csv'],
    [Comment, 'comments.csv'],
]


class Command(BaseCommand):
    help = "Loads data from static/data/*.csv files"

    def handle(self, *args, **options):
        self.stdout.write('Удаляем старые данные...')
        for model, file in CSV_MODELS:
            model.objects.all().delete()
        self.stdout.write(self.style.NOTICE('Заполняем базу данных...'))

        for model, file in CSV_MODELS:
            for row in DictReader(
                open('static/data/' + file, mode='r', encoding='utf-8')
            ):
                model.objects.get_or_create(**row)
        self.stdout.write(self.style.SUCCESS('Успешно!'))

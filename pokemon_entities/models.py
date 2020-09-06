from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField('Имя (RU)', max_length=200)
    title_en = models.CharField('Имя (EN)', max_length=200, blank=True)
    title_jp = models.CharField('Имя (JP)', max_length=200, blank=True)
    picture = models.ImageField('Изображение', upload_to='pokemons', null=True, blank=True)
    description = models.TextField('Описание', default='', blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next_evolution',
        verbose_name='Эволюционирует из'
    )

    def __str__(self):
        return f'{self.title_ru}'


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='Покемон'
    )
    latitude = models.FloatField('Широта')
    longitude = models.FloatField('Долгота')
    appeared_at = models.DateTimeField('Время появления', null=True, blank=True)
    disappeared_at = models.DateTimeField('Время исчезновения', null=True, blank=True)
    level = models.IntegerField('Уровень', null=True, blank=True)
    health = models.IntegerField('Здоровье', null=True, blank=True)
    strength = models.IntegerField('Сила', null=True, blank=True)
    defence = models.IntegerField('Защита', null=True, blank=True)
    stamina = models.IntegerField('Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title_ru} {self.latitude} {self.longitude}'

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Notre classe nommée Band, hérite de models.Model, qui est la classe de base du modèle de Django.


class Band(models.Model):
    """Affiche le nom dans l'admin de Django au lieu de 'Band object (1)' """
    def __str__(self):
        return f'{self.name}'

    class Genre(models.TextChoices):
        HIP_HOP = 'HH'
        SYNTH_POP = 'SP'
        ALTERNATIVE_ROCK = 'AR'

    name = models.fields.CharField(max_length=100)
    genre = models.fields.CharField(choices=Genre.choices, max_length=2)
    biography = models.fields.CharField(max_length=1000)
    year_formed = models.fields.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2024)]
    )
    active = models.fields.BooleanField(default=True)
    official_homepage = models.fields.URLField(null=True, blank=True)


class Listing(models.Model):
    def __str__(self):
        return f'{self.title}'

    class Type(models.TextChoices):
        RECORDS = 'RECORDS'
        CLOTHING = 'CLOTHING'
        POSTERS = 'POSTERS'
        MISCELLANEOUS = 'MISCELLANEOUS'

    title = models.fields.CharField(max_length=100)
    description = models.fields.CharField(max_length=500)
    sold = models.fields.BooleanField(default=False)
    year = models.fields.IntegerField()
    type = models.fields.CharField(choices=Type.choices, max_length=25)
    band = models.ForeignKey(Band, null=True, on_delete=models.SET_NULL)
    # like_new = models.fields.BooleanField(default=False)

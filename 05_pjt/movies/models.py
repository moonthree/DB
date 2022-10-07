from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_genre = (
        (None, None),
        ('comedy', '코미디'),
        ('horor', '호러'),
        ('fantasy', '판타지'),
    )

    title = models.CharField(max_length=20)
    audience = models.IntegerField()
    release_date = models.DateTimeField()
    genre = models.CharField(max_length=30, choices=movie_genre)
    score = models.FloatField()
    poster_url = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.title
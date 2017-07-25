from django.db import models

class Album(models.Model):
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    logo = models.CharField(max_length=1000)
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title + ' by ' + self.artist

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title
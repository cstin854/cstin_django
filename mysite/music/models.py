from django.db import models
from django.core.urlresolvers import reverse

class Album(models.Model):
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    logo = models.CharField(max_length=1000)
    genre = models.CharField(max_length=100)

    #After the user creates a new Album object using album_form,
    #Re-direct the user to music:detail, giving album_id = pk of the newly created album.
    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + ' by ' + self.artist

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    title = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # After the user creates a new Song object using song_form,
    # Re-direct the user to music:detail, giving album_id = pk of the parent album
    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'pk': self.album.pk})
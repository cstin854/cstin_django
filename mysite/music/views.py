from django.shortcuts import render, get_object_or_404
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView


def index(request):
    all_albums = Album.objects.all()
    context = {
        'all_albums' : all_albums
        }
    return render(request, 'music/index.html', context)


def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album' : album})

# class used to create new instances of Album
# Naming convention: Object_NameCreate
# Note that this inherits from django.views.generic.edit.CreateView
class AlbumCreate(CreateView):
    #Specify the model
    model = Album
    #Specify which fields the user should be able to control in the model form.
    fields = ['artist', 'title', 'genre', 'logo']

#Generic views implementation -- this didn't work for me!
'''
from django.views import generic
from .models import Album

class IndexView(generic.ListView):
    template = 'music/templates/music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    template = 'music/templates/music/detail.html'
    model = Album
'''

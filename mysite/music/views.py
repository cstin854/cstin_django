from django.shortcuts import render, get_object_or_404
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


def index(request):
    all_albums = Album.objects.all()
    context = {
        'all_albums' : all_albums
        }
    return render(request, 'music/index.html', context)


def detail(request, pk, error_message=''):
    album = get_object_or_404(Album, pk=pk)
    return render(request, 'music/detail.html', {'album' : album, 'error_message': error_message})

# class used to create new instances of Album
# Naming convention: Object_NameCreate
# Note that this inherits from django.views.generic.edit.CreateView
class AlbumCreate(CreateView):
    #Specify the model
    model = Album
    #Specify which fields the user should be able to control in the model form.
    fields = ['artist', 'title', 'genre', 'logo']

class AlbumUpdate(UpdateView):
    #Specify the model
    model = Album
    #Specify which fields the user should be able to control in the model form.
    fields = ['artist', 'title', 'genre', 'logo']

class AlbumDelete(DeleteView):
    #Specify the model
    model = Album
    #Specify which fields the user should be able to control in the model form.
    success_url = reverse_lazy('music:index')

def create_song(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return render(request, 'music/song_add.html', {'album' : album})

def song_created(request, pk):
    album = get_object_or_404(Album, pk=pk)
    song_list = []
    for s in album.song_set.all():
        if request.POST['songTitle'] == s.title:
            return detail(request,pk,error_message="A song with that name already exists.")
    song = Song()
    song.title = request.POST['songTitle']
    song.file_type = '.mp3'
    song.album = album
    song.is_favorite = False
    song.save()
    return detail(request, pk)

def post_test(request):
    return render(request, 'music/post_test.html')


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

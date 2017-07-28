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


def detail(request, pk, error_message='',template='music/detail.html'):
    album = get_object_or_404(Album, pk=pk)
    #If POST data is received, handle it:
    if request.POST:
        #If 'song-add' is passed in POST, use a template that just adds a field to
        #input the song name.
        if 'song-add' in request.POST.keys():
            template='music/song_add.html'
        #If 'songTitle' is passed by POST, create a song tied to the appropriate album.
        if 'songTitle' in request.POST.keys():
            #Attempt to create a song. If an error occurs, create_song will return
            #an error message. Assign this to error_message for display in the modal.
            error_message = create_song(pk, request.POST['songTitle'])
    return render(request, template, {'album' : album, 'error_message': error_message})

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

def create_song(album_id, song_title):
    album = get_object_or_404(Album, pk=album_id)
    for s in album.song_set.all():
        if song_title == s.title:
            return "A song with that name already exists."
    song = Song()
    song.title = song_title
    song.file_type = '.mp3'
    song.album = album
    song.is_favorite = False
    song.save()
    return '' #Error message null

def post_test(request):
    return render(request, 'music/post_test.html')

from django.shortcuts import render, get_object_or_404
from .models import Album, Song
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm, UserLogin
from django.contrib.auth import logout


def index(request, context={}):
    all_albums = Album.objects.all()
    context['all_albums'] = all_albums
    return render(request, 'music/index.html', context)

def logout_view(request):
    username = request.user.username
    if not username:
        username = 'Logout'
    context = {}
    context['error_title'] = username
    context['error_message'] = 'You have been logged out.'
    logout(request)
    return index(request,context)


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

class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # Displays a blank form for a user that isn't signed up
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Process form data:
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            #normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns User object if credentials are valid
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')

        return render(request, self.template_name, {'form':form, 'error_message':self.get_errors(form)})

    def get_errors(self, form):
        message = ''
        for key, value in form.errors.items():
            print(key, ":", value)
            message += value
        return message

class LoginView(View):

    form_class = UserLogin
    template_name = 'music/registration_form.html'

    # Displays a blank form for a user that isn't logged in
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # Process form data:
    def post(self, request):
        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('music:index')

        return render(request, self.template_name, {'form':form, 'error_message':self.get_errors(form)})

    def get_errors(self, form):
        message = ''
        for key, value in form.errors.items():
            print(key, ":", value)
            message += value
        return message

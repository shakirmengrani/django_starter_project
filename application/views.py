from django.shortcuts import render
from django.middleware import csrf
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms.CategoryForm import Form as CategoryForm
from .forms.ArtistForm import Form as ArtistForm
from .forms.AlbumForm import Form as AlbumForm
from .forms.TrackForm import Form as TrackForm
from .forms.videoForm import Form as videoForm
from .forms.CarouselForm import Form as CarouselForm
import json

@login_required
def welcome(request):
    context = {}
    return render(request, 'application/Welcome/index.html', context)

@login_required
def category_page(request):
    category = CategoryForm()
    context = {}
    http_status = 200
    if request.is_ajax():
        if request.method == "GET":
            context = category.getData(request)
        elif request.method == "POST":
            context = category.postData(request)
            http_status = context["status"]
        elif request.method == "PUT":
            context = category.putData(request)
            http_status = context["status"]
        elif request.method == "DELETE":
            context = category.deleteData(request)
            http_status = context["status"]
        else:
            http_status = 402
            context = {'message': 'Invalid operation'}
        return HttpResponse(json.dumps(context), status=http_status, content_type="application/json")        
    else:
        context = category.getData(request)
        context['form'] = category
        return render(request, 'application/Master/Category/index.html', context) 

@login_required
def artist_page(request):
    artist = ArtistForm()
    context = {}
    http_status = 200

    if request.is_ajax():
        if request.method == "GET":
            context = artist.getData(request)
        elif request.method == "POST":
            context = artist.postData(request)
            http_status = context["status"]
        elif request.method == "PUT":
            context = artist.putData(request)
            http_status = context["status"]
        elif request.method == "DELETE":
            context = artist.deleteData(request)
            http_status = context["status"]
        else:
            http_status = 402
            context = {'message': 'Invalid operation'}
        return HttpResponse(json.dumps(context), status=http_status, content_type="application/json")        
    else:
        context = artist.getData(request)
        context['form'] = artist
        return render(request, 'application/Master/Artist/index.html', context)

@login_required
def album_page(request):
    album = AlbumForm()
    context = {}
    http_status = 200

    if request.is_ajax():
        if request.method == "GET":
            context = album.getData(request)
        elif request.method == "POST" and request.FILES:
            context = album.uploadFile(request)
        elif request.method == "POST" and 'video_id' in request.POST:
            context = album.addVideo(request)
            http_status = context["status"]
        elif request.method == "POST":
            context = album.postData(request)
            http_status = context["status"]
        elif request.method == "PUT":
            context = album.putData(request)
            http_status = context["status"]
        elif request.method == "DELETE":
            context = album.deleteData(request)
            http_status = context["status"]
        elif request.method == "REMOVE":
            context = album.removeVideo(request)
            http_status = context["status"]
        elif request.method == "DELETE":
            context = album.deleteData(request)
            http_status = context["status"]
        else:
            http_status = 402
            context = {'message': 'Invalid operation'}
        return HttpResponse(json.dumps(context), status=http_status, content_type="application/json")        
    else:
        context = album.getData(request)
        context['form'] = album
    return render(request, 'application/Album/index.html', context)

@login_required
def album_search_page(request):
    return render(request, 'application/Album/search.html', {})  

@login_required
def track_page(request):
    track = TrackForm()
    context = {}
    http_status = 200
    if request.is_ajax():
        if request.method == "GET":
            context = track.getData(request)
        elif request.method == "POST" and request.FILES:
            context = track.uploadFile(request)
        elif request.method == "POST" and 'video_id' in request.POST:
            context = track.addVideo(request)
            http_status = context["status"]
        elif request.method == "POST":
            context = track.postData(request)
            http_status = context["status"]
        elif request.method == "PUT":
            context = track.putData(request)
            http_status = context["status"]
        elif request.method == "DELETE":
            context = track.deleteData(request)
            http_status = context["status"]
        elif request.method == "REMOVE":
            context = track.removeVideo(request)
            http_status = context["status"]
        else:
            http_status = 402
            context = {'message': 'Invalid operation'}
        return HttpResponse(json.dumps(context), status=http_status, content_type="application/json")        
    else:
        context = track.getData(request)
        context['form'] = track
    return render(request, 'application/Track/index.html', context)

@login_required
def video_page(request):
    videoTrack = videoForm()
    context = {}
    http_status = 200
    if request.is_ajax():
        if request.method == "GET":
            context = videoTrack.getData(request)
        elif request.method == "POST" and request.FILES:
            context = videoTrack.uploadFile(request)
        elif request.method == "POST":
            context = videoTrack.postData(request)
            http_status = context["status"]
        elif request.method == "PUT":
            context = videoTrack.putData(request)
            http_status = context["status"]
        elif request.method == "DELETE":
            context = videoTrack.deleteData(request)
            http_status = context["status"]
        else:
            http_status = 402
            context = {'message': 'Invalid operation'}
        return HttpResponse(json.dumps(context), status=http_status, content_type="application/json")        
    else:
        context = videoTrack.getData(request)
        context['form'] = videoTrack
    return render(request, 'application/Video/index.html', context)

@login_required
def carousel_page(request):
    carousel = CarouselForm()
    context = {}
    http_status = 200
    if request.is_ajax():
        if request.method == "GET":
            context = carousel.getData(request)
        elif request.method == "POST":
            context = carousel.postData(request)
            http_status = context["status"]
        elif request.method == "PUT":
            context = carousel.putData(request)
            http_status = context["status"]
        elif request.method == "DELETE":
            context = carousel.deleteData(request)
            http_status = context["status"]
        else:
            http_status = 402
            context = {'message': 'Invalid operation'}
        return HttpResponse(json.dumps(context), status=http_status, content_type="application/json")  
    else:
        context = carousel.getData(request)
        context['form'] = carousel
    return render(request, 'application/Carousal/index.html', context)


def firebase_user(request):
    context = {'user': request.user}
    return render(request, 'registration/firebaseui.html', context)


@login_required
def user_profile(request):
    context = {'user': request.user}
    return render(request, 'application/User/profile.html', context)
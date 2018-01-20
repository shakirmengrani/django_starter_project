import re
from django import forms
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from ..models import track, album
import datetime
from django.conf import settings
from application.library.viewer import * 

class Form(forms.Form):
    mp3_url = forms.FileField(required=True, widget=forms.FileInput(attrs=dict({})))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs=dict({"class":"form-control"})),label=_("Title: "))
    # album = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs=dict({"class":"form-control selectpicker"})), label=_("Album: "))
    album = forms.CharField(widget=forms.TextInput(attrs=dict({"class":"form-control"})),label=_("Album: "))
    cover_image = forms.ImageField(required=False,widget=forms.FileInput(attrs=dict({})))

    def clean(self):
        error_lst = []
        if 'name' in self.cleaned_data:
            if self.cleaned_data["name"] == "" or self.cleaned_data["name"] == None:
                error_lst.append("Please enter Track name")
        return error_lst

    def getData(self,request):
        data = request.GET
        if 'id' in data and request.is_ajax():
            d = {}
            trackData = track.objects.filter(activeyn=1, id = data['id'])
            if len(trackData) == 1 and 'id' in data:
                d = {'id': trackData[0].id, 'name': trackData[0].name , 'cover_url': trackData[0].cover_image, 'mp3_url': trackData[0].mp3_url, 'album': [{ 'id': x.id, 'name': x.name } for x in trackData[0].album_set.all()], 'video': [{ 'id': x.id, 'name': x.name } for x in trackData[0].video.all()]}
            else:
                d = [{'id':item.id, 'name': item.name, 'cover_url': item.cover_image, 'mp3_url': item.mp3_url, 'album': [{ 'id': x.id, 'name': x.name } for x in trackData[0].album_set.all()]} for item in trackData]
            context = {'data': d}
        else:
            if 'search' in data:
                track_list = page(track.objects.filter(activeyn=1, name__startswith=data['search']).order_by("updated_at"), data['page'] if 'page' in data else 1)  
            else:
                track_list = page(track.objects.filter(activeyn=1).order_by("-updated_at"), data['page'] if 'page' in data else 1)  
            context = {'data': track_list}
        return context


    def postData(self,request):
        data = request.POST
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            newTrack = track(name=str(data["name"]), activeyn=1, updated_at=str(datetime.datetime.now()))
            newTrack.save()
            latest = track.objects.latest('id')
            if data["album"] != "":
                albumId = data["album"].split(",")
                for item in albumId:
                    album.add_track(int(item), latest.id)
            context = {'data': str(latest.id), 'message': 'Record added', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context

    def putData(self,request):
        data = QueryDict(request.body)
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            myTrack = track.objects.filter(id=data["id"])
            myTrack.update(name=str(data["name"]), activeyn=1)
            for album_id in myTrack[0].album_set.all():
                album.remove_track(album_id.id, myTrack[0].id)
            if data["album"] != "":
                albumId = data["album"].split(",")
                for item in albumId:
                    album.add_track(int(item), myTrack[0].id)
            context = {'data': str(myTrack[0].id), 'message': 'track has been updated', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context

    def deleteData(self,request):
        data = QueryDict(request.body)
        myTrack = track.objects.filter(id=data["id"])
        myTrack.update(activeyn=0)
        context = {'message': 'Selected track has been deleted !', 'status': 200}
        return context

    def addVideo(self, request):
        data = request.POST
        myTrack = track.objects.filter(id=data["id"])[0]
        track.add_video(myTrack, data["video_id"])
        context = {'message': 'Video has been added in this track !', 'status': 200}
        return context
    
    def removeVideo(self, request):
        data = QueryDict(request.body)
        myTrack = track.objects.filter(id=data["id"])[0]
        track.remove_video(myTrack, data["video_id"])
        context = {'message': 'Video has been removed in this track !', 'status': 200}
        return context


    def uploadFile(self, request):
        data = request.POST
        files = request.FILES
        if 'cover_image' in files:
            with open(settings.MEDIA_URL + "track_cover/" + str(request.FILES['cover_image']), 'wb+') as destination:
                for chunk in request.FILES['cover_image'].chunks():
                    destination.write(chunk)
            destination.close()
            myTrack = track.objects.filter(id=data["id"])
            myTrack.update(cover_image=str(request.FILES['cover_image']))
        if 'mp3_url' in files:
            with open(settings.MEDIA_URL + "mp3/" + str(request.FILES['mp3_url']), 'wb+') as destination:
                for chunk in request.FILES['mp3_url'].chunks():
                    destination.write(chunk)
            destination.close()
            myTrack = track.objects.filter(id=data["id"])
            myTrack.update(mp3_url=str(request.FILES['mp3_url']))
        return { "message": 'Upload successfully !', 'status': 200 } 
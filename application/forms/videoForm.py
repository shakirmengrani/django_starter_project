import re
from django import forms
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from ..models import video
import datetime
from django.conf import settings

class Form(forms.Form):
    name = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({"class":"form-control"})),label=_("Video Name: "))
    isMpd = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=dict({"checked": True})), label=_("Make MPD: "))
    cover_image = forms.FileField(required=True, widget=forms.FileInput(attrs=dict({})),label=_("Cover Image: "))
    mp4_url = forms.FileField(required=True, widget=forms.FileInput(attrs=dict({})),label=_("MP4 File: "))

    def clean(self):
        error_lst = []
        if 'name' in self.cleaned_data:
            if self.cleaned_data["name"] == "" or self.cleaned_data["name"] == None:
                error_lst.append("Please enter video name")
        return error_lst


    def getData(self,request):
        data = request.GET
        if 'id' in data or request.is_ajax():
            d = {}
            videoData = None
            if 'id' in data:
                videoData = video.objects.filter(activeyn=1, id = data['id'])
            else:
                videoData = video.objects.filter(activeyn=1)
            if len(videoData) == 1 and 'id' in data:
                d = {'id': videoData[0].id,'name': videoData[0].name}
            else:
                d = [{'id':item.id, 'name': item.name} for item in videoData]
            context = {'data': d}
        else:    
            context = {'data': video.objects.filter(activeyn=1)}
        return context

    def postData(self,request):
        data = request.POST
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            newVideo = video(name=data["name"], activeyn=1, updated_at=str(datetime.datetime.now()))
            newVideo.save()
            latest = video.objects.latest('id')
            context = {'data': str(latest.id), 'message': 'Record added', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context
       
    def putData(self,request):
        data = QueryDict(request.body)
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            myVideo = video.objects.filter(id=data["id"])
            myVideo.update(name=data["name"], updated_at=str(datetime.datetime.now()))
            context = {'data': str(myVideo), 'message': 'Data has been updated', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context

    def deleteData(self,request):
        data = QueryDict(request.body)
        myVideo = video.objects.filter(id=data["id"])
        myVideo.update(activeyn=0)
        context = {'message': 'Selected category has been deleted !', 'status': 200}
        return context

    def uploadFile(self, request):
        data = request.POST
        files = request.FILES
        if 'cover_image' in files:
            with open(settings.MEDIA_URL + "track_cover/" + str(request.FILES['cover_image']), 'wb+') as destination:
                for chunk in request.FILES['cover_image'].chunks():
                    destination.write(chunk)
            destination.close()
            myVideo = video.objects.filter(id=data["id"])
            myVideo.update(cover_image=str(request.FILES['cover_image']))
        if 'mp4_url' in files and 'isMpd' in data and data['isMpd'] == "true":
            with open(settings.MEDIA_URL + "mp4/" + str(request.FILES['mp4_url']), 'wb+') as destination:
                    for chunk in request.FILES['mp4_url'].chunks():
                        destination.write(chunk)
            destination.close()
            myVideo = video.objects.filter(id=data["id"])
            myVideo.update(mp4_url=str(request.FILES['mp4_url']))
            with open(settings.MEDIA_URL + "mpd/" + str(request.FILES['mp4_url']), 'wb+') as destination:
                for chunk in request.FILES['mp4_url'].chunks():
                    destination.write(chunk)
            destination.close()
            myVideo = video.objects.filter(id=data["id"])
            myVideo.update(mpd_url=str(request.FILES['mp4_url']))
        else:
            if 'mp4_url' in files:
                with open(settings.MEDIA_URL + "mp4/" + str(request.FILES['mp4_url']), 'wb+') as destination:
                    for chunk in request.FILES['mp4_url'].chunks():
                        destination.write(chunk)
                destination.close()
                myVideo = video.objects.filter(id=data["id"])
                myVideo.update(mp4_url=str(request.FILES['mp4_url']))
        return { "message": 'Upload successfully !', 'status': 200 } 
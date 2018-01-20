import re
from django import forms
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from application.models import album
import datetime
from django.conf import settings
from application.library.viewer import * 


class Form(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs=dict({"class":"form-control"})),label=_("Title: "))
    release_date = forms.DateField(required=True, widget=forms.DateInput(attrs=dict({"class":"form-control datepicker"})), label=_("Release Date: "))
    category = forms.ChoiceField(widget=forms.Select(attrs=dict({"class":"form-control"})), label=_("Category: "))
    carousal = forms.ChoiceField(widget=forms.Select(attrs=dict({"class":"form-control"})), label=_("Carousal: "))
    #artist = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs=dict({"class":"form-control selectpicker"})), label=_("Artists: "))
    artist = forms.CharField(widget=forms.TextInput(attrs=dict({"class":"form-control"})),label=_("Artist: "))
    # cover_image = forms.FileField(widget=forms.FileInput(attrs=dict({})))
    cover_image = forms.ImageField(required=False,widget=forms.FileInput(attrs=dict({})))
    feature = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs=dict({})), label=_("Checked: "))

    def clean(self):
            error_lst = []
            if 'name' in self.cleaned_data:
                if self.cleaned_data["name"] == "" or self.cleaned_data["name"] == None:
                    error_lst.append("Please enter Album name")
            return error_lst

    def getData(self,request):
        data = request.GET
        context = {}
        if 'id' in data or request.is_ajax():
            d = {}
            if 'id' in data:
                albumData = album.objects.filter(activeyn=1, id = data['id'])
            elif 'term' in data:
                albumData = album.objects.filter(activeyn=1, name__startswith = data['term'])
            else:
                albumData = album.objects.filter(activeyn=1)
            if len(albumData) == 1 and 'id' in data:
                d = {'id': int(albumData[0].id), 'name': albumData[0].name, 'release_date': albumData[0].release_date.strftime("%d-%b-%Y"), 'category': [{'id': x.id, 'name': x.name, 'carousal': x.feature} for x in albumData[0].category.all()], 'artist': [{'id': x.id, 'name': x.name} for x in albumData[0].artist.all()], 'video': [{'id': x.id, 'name': x.name} for x in albumData[0].video.all()]}
            elif 'term' in data:
                d = [{'id': qx.id, 'label': qx.name, 'value': qx.name} for qx in albumData]
            else:
                album_list = albumData
                d = [{'id': int(item.id), 'name': item.name, 'release_date': item.release_date.strftime("%d-%b-%Y"), 'category': [{'id': x.id, 'name': x.name} for x in item.category.all()], 'artist': [{'id': x.id, 'name': x.name} for x in item.artist.all()], 'video': [{'id': x.id, 'name': x.name} for x in albumData[0].video.all()]} for item in album_list]
            context['data'] = d
        else:
            # album_list = album.objects.filter(activeyn=1).order_by("-id")
            album_list = None
            album_list = page(album.objects.filter(activeyn=1).order_by("-id"), data['page'] if 'page' in data else 1)
            context = {'data': album_list}
        return context

    def postData(self,request):
        data = request.POST
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            newAlbum = album(name=str(data["name"]), release_date=str(data["release_date"]), activeyn=1, updated_at=str(datetime.datetime.now()))
            newAlbum.save()
            latest = album.objects.latest('id')
            album.add_category(latest,int(data["category"]))
            if int(data["carousal"]) > 0:
                album.add_category(latest,int(data["carousal"]))
            if data["artist"] != "":
                artistId = data["artist"].split(",")
                for item in artistId:
                    album.add_artist(latest, int(item))
            context = {'data': str(latest.id), 'message': 'Record added', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context
    
    def putData(self,request):
        data = QueryDict(request.body)
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            myAlbum = album.objects.filter(id=data["id"])
            myAlbum.update(name=str(data["name"]), release_date=str(datetime.datetime.strptime(str(data["release_date"]),'%d-%b-%Y')), activeyn=1)
            for cat_id in myAlbum[0].category.all():
               album.remove_category(myAlbum[0], int(cat_id.id))
            for art_id in myAlbum[0].artist.all():
               album.remove_artist(myAlbum[0], int(art_id.id))

            album.add_category(myAlbum[0],int(data["category"]))
            if int(data["carousal"]) > 0:
                album.add_category(myAlbum[0],int(data["carousal"]))
            if data["artist"] != "":
                artistId = data["artist"].split(",")
                print(artistId) 
                for item in artistId:
                    album.add_artist(myAlbum[0], int(item))
            context = {'data': str(myAlbum[0].id), 'message': 'Data has been updated', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context
        
    def deleteData(self,request):
        data = QueryDict(request.body)
        myAlbum = album.objects.filter(id=data["id"])
        myAlbum.update(activeyn=0)
        context = {'message': 'Selected album has been deleted !', 'status': 200}
        return context

    def addVideo(self,request):
        data = request.POST
        myAlbum = album.objects.filter(id=data["id"])[0]
        album.add_video(myAlbum, data["video_id"])
        context = {'message': 'Trailer has been added in this album !', 'status': 200}
        return context

    def removeVideo(self,request):
        data = QueryDict(request.body)
        myAlbum = album.objects.filter(id=data["id"])[0]
        album.remove_video(myAlbum, data["video_id"])
        context = {'message': 'Trailer has been removed from this album !', 'status': 200}
        return context

    def uploadFile(self, request):
        data = request.POST
        with open(settings.MEDIA_URL + "album_cover/" + str(request.FILES['cover_image']), 'wb+') as destination:
            for chunk in request.FILES['cover_image'].chunks():
                destination.write(chunk)
            destination.close()
        myAlbum = album.objects.filter(id=data["id"])
        myAlbum.update(cover_image=str(request.FILES['cover_image']))
        return { "message": 'Upload successfully !', 'status': 200 } 
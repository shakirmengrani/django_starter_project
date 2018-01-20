import re
from django import forms
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from ..models import artist
import datetime
from django.conf import settings
from application.library.viewer import * 

class Form(forms.Form):
    name = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({"class":"form-control"})),label=_("Artist Name: "))

    def clean(self):
            error_lst = []
            if 'name' in self.cleaned_data:
                if self.cleaned_data["name"] == "" or self.cleaned_data["name"] == None:
                    error_lst.append("Please enter Artist name")
            return error_lst

    def getData(self,request):
        data = request.GET
        if 'id' in data or request.is_ajax():
            d = {}
            artistData = None
            if 'id' in data:
                artistData = artist.objects.filter(activeyn=1, id = data['id'])
            elif 'term' in data:
                artistData = artist.objects.filter(activeyn=1, name__startswith=data['term'])
            else:
                artistData = artist.objects.filter(activeyn=1)    
            
            if len(artistData) == 1 and 'id' in data:
                d = {'id': int(artistData[0].id),'name': artistData[0].name}
            elif 'term' in data:
                d = [{'id': qx.id, 'label': qx.name, 'value': qx.name} for qx in artistData]
            else:
                d = [{'id':int(item.id), 'name': item.name} for item in artistData]       
            context = {'data': d}
        else:    
            artist_list = None
            artist_list = page(artist.objects.filter(activeyn=1).order_by("-id"), data['page'] if 'page' in data else 1)
            context = {'data': artist_list}
        return context

    def postData(self,request):
        data = request.POST
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            newArtist = artist(name=data["name"], activeyn=1, cover_image='', updated_at=str(datetime.datetime.now()))
            newArtist.save()
            context = {'data': str(newArtist), 'message': 'Record added', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context
    
    def putData(self,request):
        data = QueryDict(request.body)
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            myArtist = artist.objects.filter(id=data["id"])
            myArtist.update(name=data["name"], cover_image='')
            context = {'data': str(myArtist), 'message': 'Data has been updated', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context

    def deleteData(self,request):
        data = QueryDict(request.body)
        myArtist = artist.objects.filter(id=data["id"])
        myArtist.update(activeyn=0)
        context = {'message': 'Selected artist has been deleted !', 'status': 200}
        return context
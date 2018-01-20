import re
from django import forms
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from ..models import category, album
import datetime
from django.conf import settings

class Form(forms.Form):
    # album = forms.ChoiceField(widget=forms.Select(attrs=dict({"class":"form-control"})), label=_("Albums: "))
    # carousel = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs=dict({"class":"form-control selectpicker"})), label=_("Carousels: "))

    def getData(self,request):
        data = request.GET
        if request.is_ajax():
            context = {'data': []}
        else:
            context = {'data': [{'id': x.id, 'name': x.name, 'album':[{'id': x1.id, 'name': x1.name, 'm_order': x1.m_order} for x1 in x.album_set.filter(activeyn=1).order_by("m_order")]} for x in category.objects.filter(activeyn=1, feature=1)]}
        return context

    def postData(self,request):
        data = request.POST
        self.cleaned_data = data
        myAlbum = album.objects.filter(id=data['album_id'])
        if data["carousel"] != "":
            carouselId = data["carousel"].split(",")
            for item in carouselId:
                album.add_category(myAlbum[0],int(item))
            
        context = {'data': str(myAlbum[0].id), 'message': 'Record added', 'status': 200}
        return context

    def putData(self,request):
        data = QueryDict(request.body)
        self.cleaned_data = data
        myAlbum = album.objects.filter(id=data['album_id'])
        myAlbum.update(m_order=data['m_order'])
        context = {'data': str(myAlbum[0].id), 'message': 'Data has been updated', 'status': 200}
        return context

    def deleteData(self,request):
        data = QueryDict(request.body)
        self.cleaned_data = data
        myAlbum = album.objects.filter(id=data['album_id'])
        album.remove_category(myAlbum[0], int(data["carousel"]))
        context = {'message': 'Selected album has been deleted from selected category !', 'status': 200}
        return context
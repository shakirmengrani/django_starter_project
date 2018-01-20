import re
from django import forms
from django.http import QueryDict
from django.utils.translation import ugettext_lazy as _
from ..models import category
import datetime

class Form(forms.Form):
    name = forms.CharField(required=True,widget=forms.TextInput(attrs=dict({"class":"form-control"})),label=_("Category Name: "))
    type = forms.ChoiceField(widget=forms.Select(attrs=dict({"class":"form-control"})), label=_("Category Type: "))
    feature = forms.BooleanField(required=False,widget=forms.CheckboxInput(attrs=dict()),label=_("Carousal: "))
    
    def clean(self):
        error_lst = []
        if 'name' in self.cleaned_data:
            if self.cleaned_data["name"] == "" or self.cleaned_data["name"] == None:
                error_lst.append("Please enter category name")
        return error_lst


    def getData(self,request):
        data = request.GET
        if 'id' in data or request.is_ajax():
            d = {}
            categoryData = None
            if 'id' in data:
                categoryData = category.objects.filter(activeyn=1, id = data['id'])
            elif 'carousal' in data:
                categoryData = category.objects.filter(activeyn=1, feature = data['carousal'], type=data['type'])
            else:
                categoryData = category.objects.filter(activeyn=1, type=data['type'])
            if len(categoryData) == 1 and 'id' in data:
                d = {'id': categoryData[0].id,'name': categoryData[0].name, 'feature': categoryData[0].feature}
            else:
                d = [{'id':item.id, 'name': item.name} for item in categoryData]
            context = {'data': d}
        else:    
            context = {'data': category.objects.filter(activeyn=1)}
        return context

    def postData(self,request):
        data = request.POST
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            newCategory = category(name=data["name"], feature=data["feature"], activeyn=1, type=data["type"], updated_at=str(datetime.datetime.now()))
            newCategory.save()
            context = {'data': str(newCategory), 'message': 'Record added', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context
       
    def putData(self,request):
        data = QueryDict(request.body)
        self.cleaned_data = data
        if len(self.clean()) <= 0:
            myCategory = category.objects.filter(id=data["id"])
            myCategory.update(name=data["name"], feature=data["feature"], type=data["type"])
            context = {'data': str(myCategory), 'message': 'Data has been updated', 'status': 200}
        else:
            context = {'invalid': self.clean(), 'message': 'Record not saved', 'status': 422}
        return context

    def deleteData(self,request):
        data = QueryDict(request.body)
        myCategory = category.objects.filter(id=data["id"])
        myCategory.update(activeyn=0)
        context = {'message': 'Selected category has been deleted !', 'status': 200}
        return context
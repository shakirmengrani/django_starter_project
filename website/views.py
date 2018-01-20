from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def welcome(request):
    context = {}
    return render(request, 'website/index.html', context)

def firebase_sw(request):
    file_content = ""
    f = open("static/firebase-messaging-sw.js")
    file_content = f.read()
    return HttpResponse(str(file_content), status=200, content_type="text/javascript")  
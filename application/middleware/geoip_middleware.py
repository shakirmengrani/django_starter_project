import requests
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
class Middleware(MiddlewareMixin):
    
    def process_response(self, request, response):
        try:
            r = requests.get("http://freegeoip.net/json/")
            if str(r.json()["country_code"]) == "PK":
                return response
            else:
                return HttpResponseForbidden()
        except:
            return HttpResponseForbidden()
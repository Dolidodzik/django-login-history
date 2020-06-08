from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import models
import json
import requests
import ipaddress
from django.conf import settings as conf_settings
from django.contrib.auth.models import User



'''

Models

'''

class Login(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.CharField(max_length=15)
    user_agent = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)



def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip

def get_location_data__from_ip(ip):

    # if ip is local (so it's impossible to find lat/long coords and location) project will use random google ip as placeholder]
    print(ipaddress.ip_address('192.168.0.1').is_private)
    if ipaddress.ip_address('192.168.0.1').is_private:
        if hasattr(conf_settings, 'IP_PLACEHOLDER'):
            ip = conf_settings.IP_PLACEHOLDER
        else:
            ip = "216.58.201.110"
    else:
        pass

    url = "http://ip-api.com/json/"+ip

    locationInfo = requests.get(url).text
    locationInfo = json.loads(locationInfo)
    return locationInfo




@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):

    ip = get_client_ip(request)
    locationInfo = get_location_data__from_ip(ip)

    print(type(locationInfo))
    print(locationInfo["country"])

    login = Login.objects.create(
        user=user,
        ip=ip,
        user_agent=request.META['HTTP_USER_AGENT'],
        country=locationInfo["country"],
        region=locationInfo["region"],
        city=locationInfo["city"],
        lon=locationInfo["lon"],
        lat=locationInfo["lat"],
    )
    print(login)

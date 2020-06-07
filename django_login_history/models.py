from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import models
import json
import requests
import ipaddress
from django.conf import settings as conf_settings


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
        if conf_settings.IP_PLACEHOLDER:
            ip = conf_settings.IP_PLACEHOLDER
        else:
            ip = "216.58.201.110"
    else:
        pass

    print(ip)
    url = "http://ip-api.com/json/"+ip

    locationInfo = requests.get(url)
    print("locationInfo below:")
    print(locationInfo.text)
    return locationInfo




@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):

    ip = get_client_ip(request)
    locationInfo = get_location_data__from_ip(ip)

    print(ip)
    print(request.META['HTTP_USER_AGENT'])

    return 0



'''

Models

'''

class Login(models.Model):
    ip = models.CharField(max_length=15)

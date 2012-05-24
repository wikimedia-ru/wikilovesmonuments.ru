from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from house.models import *


def index_page(request):
    h_list = House.objects.all()
    p_list = HousePhoto.objects.all()[:30]

    return render_to_response('house/index.html', {
        'house_list': h_list,
        'photo_list': p_list,
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


def upload(request):
    h_list = House.objects.all()

    return render_to_response('house/upload.html', {
        'house_list': h_list,
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


def add(request):
    h_list = House.objects.all()
    p_list = HousePhoto.objects.all()[:30]

    return render_to_response('house/add.html', {
        'house_list': h_list,
        'photo_list': p_list,
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))



def house(request, id):
    h = House.objects.get(pk=id)
    photo = HousePhoto.objects.filter(house=h)[:30]

    return render_to_response('house/house.html', {
        'house': h,
        'photo': photo,
        'is_admin': True,
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


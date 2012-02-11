from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings

from house.models import Street, House



def street_list(request):
    s_list = Street.objects.order_by('name')

    return render_to_response('house/street_list.html', {
        'list': s_list,
        }, context_instance=RequestContext(request))


def street(request, id):
    s = Street.objects.get(pk=id)
    h_list = House.objects.filter(street=id).order_by('number')

    return render_to_response('house/street.html', {
        'street': s,
        'list': h_list,
        }, context_instance=RequestContext(request))


def house(request, id):
    h = House.objects.get(pk=id)

    return render_to_response('house/house.html', {
        'house': h,
        'YMAPS_KEY': settings.YMAPS_KEY,
        }, context_instance=RequestContext(request))


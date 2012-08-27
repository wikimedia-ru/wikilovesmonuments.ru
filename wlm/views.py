from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.conf import settings
from wlm.models import Region, City, Monument, HousePhoto
from wlm.forms import MonumentForm
from wlm.utils import get_region
from django.contrib.auth.decorators import permission_required

def index_page(request):
    h_list = Monument.objects.exclude(coord_lon=None).select_related()
    h_list = h_list.filter(city_id=34)
    p_list = HousePhoto.objects.all()[:30]
    ip_region = get_region(request.META['REMOTE_ADDR'])
    if not ip_region:
        ip_region = "47"

    return render_to_response('house/index.html', {
        'house_list': h_list,
        'photo_list': p_list,
        'region': Region.objects.values('id').get(iso_code=ip_region),
        'regions': Region.objects.values('id', 'name', "latitude", "longitude", "scale").exclude(id=77),
        'cities': City.objects.values('id', 'name').all(),
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


def upload(request):
    h_list = Monument.objects.all()

    return render_to_response('house/upload.html', {
        'house_list': h_list,
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


def add(request):
    h_list = Monument.objects.all()
    p_list = HousePhoto.objects.all()[:30]

    return render_to_response('house/add.html', {
        'house_list': h_list,
        'photo_list': p_list,
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))

@permission_required('wlm.can_moderate')
def monument_edit_form(request, m_id):
    monument = Monument.objects.select_related().get(id=m_id)
    form = MonumentForm(instance=monument)
    print request.user.has_perm('monuments.can_moderate')
    return render_to_response( "edit_monument.html", {
        'id': m_id,
        'form': form,
        }, context_instance = RequestContext(request))


def house(request, id):
    h = Monument.objects.get(pk=id)
    photo = HousePhoto.objects.filter(house=h)[:30]

    return render_to_response('house/house.html', {
        'house': h,
        'photo': photo,
        'is_admin': True,
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))

def coordinates_doubled(request):
    query = '''select count(id), coord_lat, coord_lon from wlm_monument
        group by coord_lat, coord_lon
        having count(id) > 1;'''
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_to_response('coord_doubles.html', {'doubles':rows,})

def monuments_double_coordinates(request):
    if request.GET['lat']:
        lat = float(request.GET.get('lat'))
    else:
        lat = None
    if request.GET['lon']:
        lon = float(request.GET.get('lon'))
    else:
        lon = None
    monuments = Monument.objects.filter(coord_lat=lat, coord_lon=lon)
    return render_to_response('monuments_double.html', {'monuments': monuments,})

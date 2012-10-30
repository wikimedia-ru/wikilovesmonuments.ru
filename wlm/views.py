from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from wlm.models import Region, City, Monument, MonumentPhoto, MonumentPhotoRating
from wlm.forms import MonumentForm
from wlm.utils import get_region
from django.contrib.auth.decorators import permission_required

def index_page(request):
    ip_region = get_region(request.META['REMOTE_ADDR'])
    if not ip_region:
        ip_region = "47"

    return render_to_response('house/index.html', {
        'region': Region.objects.values('id').get(iso_code=ip_region),
        'regions': Region.objects.values('id', 'name', "latitude", "longitude", "scale").exclude(id=77),
        'cities': City.objects.values('id', 'name').all(),
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


def list_page(request):
    h_list = Monument.objects.exclude(coord_lon=None).select_related()
    h_list = h_list.filter(city_id=34)
    p_list = MonumentPhoto.objects.all()[:30]
    ip_region = get_region(request.META['REMOTE_ADDR'])
    if not ip_region:
        ip_region = "47"

    return render_to_response('house/list_index.html', {
        'region': Region.objects.values('id').get(iso_code=ip_region),
        'regions': Region.objects.values('id', 'name', "latitude", "longitude", "scale").exclude(id=77),
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


def list_region(request, id):
    return render_to_response('house/list_region.html', {
        'region': Region.objects.get(id=id),
        'cities': City.objects.values('id', 'name').filter(region_id=id),
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


def list_city(request, id):
    return render_to_response('house/list_city.html', {
        'monuments': Monument.objects.filter(city_id=id).exclude(coord_lon=None).exclude(kult_id=None).select_related(),
        'city': City.objects.get(id=id),
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
    p_list = MonumentPhoto.objects.all()[:30]

    return render_to_response('house/add.html', {
        'house_list': h_list,
        'photo_list': p_list,
        'CMADE_KEY': settings.CMADE_KEY,
        }, context_instance=RequestContext(request))


@permission_required('wlm.can_change')
def monument_edit_form(request, m_id):
    monument = Monument.objects.select_related().get(id=m_id)
    form = MonumentForm(request.POST or None, instance=monument)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('/house/%s' % m_id)
    return render_to_response( "edit_monument.html", {
        'id': m_id,
        'form': form,
        }, context_instance = RequestContext(request))


def house(request, id):
    m = Monument.objects.get(pk=id)
    photo = MonumentPhoto.objects.filter(monument=m)[:30]

    return render_to_response('house/house.html', {
        'house': m,
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

def voting(request):
    if request.user is None or not request.user.is_active:
        return HttpResponseRedirect('/admin/')

    cnt = {}

    pr = MonumentPhotoRating.objects.all()
    #pr = MonumentPhotoRating.objects.filter(user_id=request.user.id)
    pr2 = []
    for i in pr:
        pr2.append(i.photo_id)
    cnt = {
        'all': len(MonumentPhoto.objects.all()),
        'done': len(pr2),
    }

    p = MonumentPhoto.objects.exclude(id__in=pr2)
    if (len(p)):
        p = p.order_by('?')[0]
    else:
        return render_to_response('voting_over.html', {
            'cnt': cnt,
            'user': request.user,
            }, context_instance=RequestContext(request))
    
    p.url_name = p.name.replace(' ', '_')
    return render_to_response('voting.html', {
        'photo': p,
        'cnt': cnt,
        'user': request.user,
        }, context_instance=RequestContext(request))

def vote_for_photo(request, photo_id, vote):
    vote = int(vote)
    if vote >= 1 and vote <= 5:
        r, created = MonumentPhotoRating.objects.get_or_create(user=request.user, 
            photo=MonumentPhoto.objects.get(id=photo_id))
        r.vote = vote
        r.save()
    return HttpResponseRedirect('/voting')


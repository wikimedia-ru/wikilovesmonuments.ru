from django.db import connection
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import permission_required

from wlm.models import Region, City
from wlm.models import Monument, MonumentPhoto, MonumentPhotoRating
from wlm.forms import MonumentForm
from wlm.utils import get_region


MOSCOW_REGION_ID = '47'
MOSCOW_ID = '77'


def index_page(request):
    ip_region = get_region(request.META['REMOTE_ADDR'])
    if not ip_region:
        ip_region = MOSCOW_REGION_ID

    return render_to_response('wlm/index.html', {
        'region': Region.objects.values('id').get(iso_code=ip_region),
        'regions': Region.objects.values('id', 'name', 'latitude',
                    'longitude', 'scale').exclude(pk=MOSCOW_ID),
        'cities': City.objects.values('id', 'name').all(),
        'CMADE_KEY': settings.CMADE_KEY,
    }, context_instance=RequestContext(request))


def list_page(request):
    ip_region = get_region(request.META['REMOTE_ADDR'])
    if not ip_region:
        ip_region = MOSCOW_REGION_ID

    return render_to_response('wlm/list_index.html', {
        'region': Region.objects.values('id').get(iso_code=ip_region),
        'regions': Region.objects.values('id', 'name', 'latitude',
                    'longitude', 'scale').exclude(pk=MOSCOW_ID),
    }, context_instance=RequestContext(request))


def list_region(request, id):
    return render_to_response('wlm/list_region.html', {
        'region': Region.objects.get(pk=id),
        'cities': City.objects.values('id', 'name').filter(region_id=id),
    }, context_instance=RequestContext(request))


def list_city(request, id):
    monuments = Monument.objects.filter(city_id=id, coord_lon__isnull=False,
                kult_id__isnull=False)
    return render_to_response('wlm/list_city.html', {
        'monuments': monuments,
        'city': City.objects.get(pk=id),
    }, context_instance=RequestContext(request))


def upload(request):
    m_list = Monument.objects.all()

    return render_to_response('wlm/upload.html', {
        'monuments_list': m_list,
        'CMADE_KEY': settings.CMADE_KEY,
    }, context_instance=RequestContext(request))


def add(request):
    m_list = Monument.objects.all()

    return render_to_response('wlm/add_monument.html', {
        'monuments_list': m_list,
        'CMADE_KEY': settings.CMADE_KEY,
    }, context_instance=RequestContext(request))


@permission_required('wlm.can_change')
def monument_edit_form(request, id):
    monument = Monument.objects.select_related().get(pk=id)
    form = MonumentForm(request.POST or None, instance=monument)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect('/monument/%s' % id)
    return render_to_response("wlm/edit_monument.html", {
        'id': id,
        'form': form,
    }, context_instance=RequestContext(request))


def monument(request, id):
    return render_to_response('wlm/monument.html', {
        'monument': get_object_or_404(Monument, pk=id),
        'CMADE_KEY': settings.CMADE_KEY,
    }, context_instance=RequestContext(request))


def monument_photo(request, id):
    return render_to_response('wlm/monument_photo.html', {
        'monument': get_object_or_404(Monument, pk=id),
    }, context_instance=RequestContext(request))


def redirect_by_kult_id(request, kult_id):
    m = get_object_or_404(Monument, kult_id=kult_id)
    return HttpResponseRedirect('/monument/%d' % m.id)


def coordinates_doubled(request):
    query = '''select count(id), coord_lat, coord_lon from wlm_monument
        group by coord_lat, coord_lon
        having count(id) > 1;'''
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return render_to_response('coord_doubles.html', {'doubles': rows})


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
    return render_to_response('wlm/monuments_double.html', {
        'monuments': monuments,
    })


def voting(request):
    if request.user is None or not request.user.is_active:
        return HttpResponseRedirect('/admin/')

    cnt = {}

    pr = MonumentPhotoRating.objects.all()
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
        return render_to_response('wlm/voting_over.html', {
            'cnt': cnt,
        }, context_instance=RequestContext(request))

    return render_to_response('wlm/voting.html', {
        'photo': p,
        'cnt': cnt,
    }, context_instance=RequestContext(request))


def vote_for_photo(request, photo_id, vote):
    vote = int(vote)
    if vote >= 1 and vote <= 5:
        r, created = MonumentPhotoRating.objects.get_or_create(
            user=request.user,
            photo=MonumentPhoto.objects.get(pk=photo_id))
        r.vote = vote
        r.save()
    return HttpResponseRedirect('/voting')

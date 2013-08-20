# -*- encoding: utf-8 -*-
import urllib
import json
import re

from datetime import datetime
from dateutil.parser import parse
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from wlm.models import Region, Monument, MonumentPhoto


class Command(BaseCommand):
    help = u'Export cultural heritage into Wikipedia'

    def handle(self, *args, **options):
        regions = Region.objects.all()
        for region in regions:
            print '%s (%s): ' % (region.name, region.id)
            monuments = Monument.objects.filter(region_id=region.id)
            if self.update_page(region.name, monuments):
                print 'OK\n'
            else:
                print 'fail!\n'

        self.stdout.write(u'Successfully exported all cultural heritage objects\n')


    def update_page(self, title, monuments):
        if not len(monuments) or len(monuments) > 500:
            return False
        text = u'{{WLM/заголовок}}\n'
        for m in monuments:
            text += u'{{WLM/строка\n'
            text += u'| id = %s\n' % m.kult_id
            text += u'| название = %s\n' % m.name
            text += u'| нп = %s\n' % m.city
            text += u'| адрес = %s\n' % m.address
            text += u'| регион = %s\n' % m.region
            text += u'| lat = %s\n' % m.coord_lat
            text += u'| lon = %s\n' % m.coord_lon
            text += u'| фото = \n'
            text += u'}}\n'
        text += u'|}'

        page = u'Проект:Вики любит памятники/Списки/%s' % title
        api_params = {
            'action': 'query',
            'prop': 'info',
            'intoken': 'edit',
            'titles': page.encode('utf8'),
        }
        answer = self.api_request(api_params)
        pages = answer['query']['pages']
        for page_id in pages:
            token = pages[page_id]['edittoken']
            break
        print 'token: %s\n' % token

        api_params = {
            'action': 'edit',
            'summary': u'автоматическое обновление списка'.encode('utf8'),
            'bot': 1,
            'title': page.encode('utf8'),
            'text': text.encode('utf8'),
            'token': token,
        }
        answer = self.api_request(api_params, True)
        
        return True


    def api_request(self, ext_params, post=False):
        params = {
            'format': 'json',
        }
        params.update(ext_params)
        get_string = urllib.urlencode(params)

        server = 'http://ru.wikipedia.org'
        if post:
            f = urllib.urlopen('%s/w/api.php' % server, get_string)
        else:
            f = urllib.urlopen('%s/w/api.php?%s' % (server, get_string))

        return json.load(f)


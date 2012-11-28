# -*- encoding: utf-8 -*-
import urllib
import json
import re

from datetime import datetime
from dateutil.parser import parse
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from wlm.models import Monument, MonumentPhoto


class Command(BaseCommand):
    help = 'Update cultural heritage images'

    def handle(self, *args, **options):
        api_server = 'http://commons.wikimedia.org'
        api_token = ''

        re_kult = re.compile(r'\{\{Cultural Heritage Russia\s*\|\s*id\s*=\s*([0-9]+)\D')

        while True:
            api_params = {
                'format': 'json',
                'action': 'query',
                'list': 'embeddedin',
                'eititle': 'Template:Cultural Heritage Russia',
                'einamespace':  6, # file
                'eilimit': 50,
            }
            if api_token:
                api_params['eicontinue'] = api_token
            api_get_str = urllib.urlencode(api_params)
            f = urllib.urlopen('%s/w/api.php?%s' % (api_server, api_get_str))
            answer = json.load(f)

            for photo in answer['query']['embeddedin']:
                try:
                    MonumentPhoto.objects.get(commons_id=photo['pageid'])
                except ObjectDoesNotExist:
                    print "%s ..." % photo['title'],
                    api_params = {
                        'format': 'json',
                        'action': 'query',
                        'prop': 'imageinfo|revisions',
                        'iiprop': 'timestamp|user|url|size',
                        'iilimit': 1,
                        'rvprop': 'content',
                        'rvlimit': 1,
                        'titles': photo['title'].encode('utf8'),
                    }
                    api_get_str = urllib.urlencode(api_params)
                    f = urllib.urlopen('%s/w/api.php?%s' % (api_server, api_get_str))
                    p_answer = json.load(f)
                    p_info = p_answer['query']['pages'][str(photo['pageid'])]
                    p_url_parts = p_info['imageinfo'][0]['url'].split('/', 7)
                    m = re.search(re_kult, p_info['revisions'][0]['*'])
                    try:
                        kult_id = int(m.group(1))
                        monument = Monument.objects.get(kult_id=kult_id)
                    except:
                        print "ERROR"
                        continue
                    MonumentPhoto.objects.create(
                        monument=monument,
                        commons_id=photo['pageid'],
                        name=photo['title'][5:],  # without 'File:'
                        folder='%s/%s' % (p_url_parts[5], p_url_parts[6]),
                        width=p_info['imageinfo'][0]['width'],
                        height=p_info['imageinfo'][0]['height'],
                        size=p_info['imageinfo'][0]['size'],
                        author=p_info['imageinfo'][0]['user'],
                        datetime=parse(p_info['imageinfo'][0]['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                    )
                    print "OK"
            if not 'query-continue' in answer:
                break
            api_token = answer['query-continue']['embeddedin']['eicontinue']

        self.stdout.write('Successfully updated photos of cultural heritage\n')

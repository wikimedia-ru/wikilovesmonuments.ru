# -*- encoding: utf-8 -*-
import urllib, json, re
from datetime import datetime
from dateutil.parser import parse
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from wlm.models import Monument, MonumentPhoto


class Command(BaseCommand):
    help = 'Update cultural heritage images'
    
    def handle(self, *args, **options):
        query_server = 'http://commons.wikimedia.org'
        continue_token = ''

        re_kult = re.compile(r'\{\{Cultural Heritage Russia\|id\s*=\s*([0-9]+)\}\}')
        
        while True:
            query_params = {
                'format':       'json',
                'action':       'query',
                'list':         'embeddedin',
                'eititle':      'Template:Cultural Heritage Russia',
                'einamespace':  6, # file
                'eilimit':      50,
            }
            if continue_token:
                query_params['eicontinue'] = continue_token
            f = urllib.urlopen('%s/w/api.php?%s' % (query_server, urllib.urlencode(query_params)))
            answer = json.load(f)

            for photo in answer['query']['embeddedin']:
                try:
                    photo_record = MonumentPhoto.objects.get(commons_id = photo['pageid'])
                except ObjectDoesNotExist:
                    query_params = urllib.urlencode({
                        'format':       'json',
                        'action':       'query',
                        'prop':         'imageinfo|revisions',
                        'iiprop':       'timestamp|user|url|size',
                        'iilimit':      1,
                        'rvprop':       'content',
                        'rvlimit':      1,
                        'titles':       photo['title'].encode('utf8'),
                    })
                    #print '%s/w/api.php?%s' % (query_server, query_params)
                    f = urllib.urlopen('%s/w/api.php?%s' % (query_server, query_params))
                    photo_answer = json.load(f)
                    photo_info = photo_answer['query']['pages'][str(photo['pageid'])]
                    photo_url_parts = photo_info['imageinfo'][0]['url'].split('/', 7)
                    m = re.search(re_kult, photo_info['revisions'][0]['*'])
                    try:
                        kult_id = int(m.group(1))
                        monument = Monument.objects.get(kult_id = kult_id)
                    except:
                        continue
                    MonumentPhoto.objects.create(
                        monument = monument,
                        commons_id = photo['pageid'],
                        name = photo['title'][5:], # without 'File:'
                        folder = '%s/%s' % (photo_url_parts[5], photo_url_parts[6]),
                        width = photo_info['imageinfo'][0]['width'],
                        height = photo_info['imageinfo'][0]['height'],
                        size = photo_info['imageinfo'][0]['size'],
                        author = photo_info['imageinfo'][0]['user'],
                        datetime = parse(photo_info['imageinfo'][0]['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                    )
            if not 'query-continue' in answer:
                break
            continue_token = answer['query-continue']['embeddedin']['eicontinue']

        self.stdout.write('Successfully updated photos of cultural heritage\n')


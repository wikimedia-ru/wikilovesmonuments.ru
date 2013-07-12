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
        api_token = ''
        file_errors = []
        re_kult = re.compile(r'\{\{Cultural Heritage Russia\s*\|\s*id\s*=\s*([0-9]+)\D')

        while True:
            api_params = {
                'action': 'query',
                'list': 'embeddedin',
                'eititle': 'Template:Cultural Heritage Russia',
                'einamespace': 6, # file
                'eilimit': 50,
            }
            if api_token:
                api_params['eicontinue'] = api_token
            answer = self.api_request(api_params)

            for photo in answer['query']['embeddedin']:
                try:
                    MonumentPhoto.objects.get(commons_id=photo['pageid'])
                except ObjectDoesNotExist:
                    print "%s ..." % photo['title'],
                    api_params = {
                        'action': 'query',
                        'prop': 'imageinfo|revisions',
                        'iiprop': 'timestamp|user|url|size',
                        'iilimit': 1,
                        'rvprop': 'content',
                        'rvlimit': 1,
                        'titles': photo['title'].encode('utf8'),
                    }
                    p_answer = self.api_request(api_params)
                    p_info = p_answer['query']['pages'][str(photo['pageid'])]
                    p_url_parts = p_info['imageinfo'][0]['url'].split('/', 7)
                    m = re.search(re_kult, p_info['revisions'][0]['*'])
                    try:
                        kult_id = int(m.group(1))
                        monument = Monument.objects.get(kult_id=kult_id)
                    except:
                        file_errors.append({
                            'filename': photo['title'][5:],
                            'kult_id': kult_id,
                        })
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

        self.update_errors_page(file_errors)

        self.stdout.write('Successfully updated photos of cultural heritage\n')


    def update_errors_page(self, errors):
        text = u'{| class="wikitable sortable"\n'
        text += u'! File !! ID\n'
        for error in errors:
            text += u'|-\n'
            text += u'| [[:File:%s]] ' % error['filename']
            text += u'|| %s\n' % error['kult_id']
        text += u'|}'

        error_page = u'Commons:Wiki Loves Monuments 2012 in Russia/Errors'
        api_params = {
            'action': 'query',
            'prop': 'info',
            'intoken': 'edit',
            'titles': error_page,
        }
        answer = self.api_request(api_params)
        pages = answer['query']['pages']
        for page_id in pages:
            token = pages[page_id]['edittoken']
            break

        api_params = {
            'action': 'edit',
            'summary': u'Bot: Updating list',
            'bot': 1,
            'title': error_page,
            'text': text.encode('utf-8'),
            'token': token,
        }
        answer = self.api_request(api_params, True)


    def api_request(self, ext_params, post=False):
        params = {
            'format': 'json',
        }
        params.update(ext_params)
        get_string = urllib.urlencode(params)

        server = 'http://commons.wikimedia.org'
        if post:
            f = urllib.urlopen('%s/w/api.php' % server, get_string)
        else:
            f = urllib.urlopen('%s/w/api.php?%s' % (server, get_string))

        return json.load(f)


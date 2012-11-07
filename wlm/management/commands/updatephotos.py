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
    args = '<contest_year>'
    help = 'Update contest images'

    def handle(self, *args, **options):
        contest_year = 0
        for a in args:
            contest_year = a
            break
        if not contest_year:
            today = datetime.today()
            contest_year = today.year

        api_server = 'http://commons.wikimedia.org'
        api_token = ''

        re_kult = re.compile(r'\{\{Cultural Heritage Russia\|id\s*=\s*([0-9]+)\}\}')

        while True:
            api_params = {
                'format': 'json',
                'action': 'query',
                'list': 'categorymembers',
                'cmtitle': 'Category:Images from Wiki Loves Monuments %s in Russia' % contest_year,
                'cmtype': 'file',
                'cmprop': 'ids|title',
                'cmlimit': 50,
            }
            if api_token:
                api_params['cmcontinue'] = api_token
            api_get_str = urllib.urlencode(api_params)
            f = urllib.urlopen('%s/w/api.php?%s' % (api_server, api_get_str))
            answer = json.load(f)

            for photo in answer['query']['categorymembers']:
                try:
                    p_record = MonumentPhoto.objects.get(commons_id=photo['pageid'])
                except ObjectDoesNotExist:
                    api_params = urllib.urlencode({
                        'format': 'json',
                        'action': 'query',
                        'prop': 'imageinfo|revisions',
                        'iiprop': 'timestamp|user|url|size',
                        'iilimit': 1,
                        'rvprop': 'content',
                        'rvlimit': 1,
                        'titles': photo['title'].encode('utf8'),
                    })
                    f = urllib.urlopen('%s/w/api.php?%s' % (api_server, api_params))
                    p_answer = json.load(f)
                    p_info = p_answer['query']['pages'][str(photo['pageid'])]
                    p_url_parts = p_info['imageinfo'][0]['url'].split('/', 7)
                    m = re.search(re_kult, p_info['revisions'][0]['*'])
                    try:
                        kult_id = int(m.group(1))
                        monument = Monument.objects.get(kult_id=kult_id)
                    except:
                        continue
                    MonumentPhoto.objects.create(
                        contest_year=contest_year,
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
            if not 'query-continue' in answer:
                break
            api_token = answer['query-continue']['categorymembers']['cmcontinue']

        self.stdout.write('Successfully updated photos of WLM %s\n' % contest_year)

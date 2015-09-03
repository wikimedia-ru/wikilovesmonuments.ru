# -*- encoding: utf-8 -*-
import cookielib, urllib, urllib2
import json
import re
import sys

from datetime import datetime
from dateutil.parser import parse
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from wlm.models import Region, City, Monument, MonumentPhoto
from settings import WIKI_NAME, WIKI_PASSWORD


class Command(BaseCommand):
    help = u'Import cultural heritage from Russian Wikivoyage'


    def handle(self, *args, **options):
        regions = Region.objects.all()

        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

        self.login()
        self.run_pagegenerator()

        self.stdout.write(u'Successfully imported all cultural heritage objects\n')


    def process_text(self, text, page = ''):
        tpl_matches = re.findall(u'\{\{\s*monument((?:[\n\s]*\|[\n\s]*[^\|\{\}]+?)+)\}\}', text)
        for tpl in tpl_matches:
            tpl_params = re.split(u'[\n\s]*\|[\n\s]*', tpl)
            monument_data = {}
            for param in tpl_params:
                if param.find(u'=') == -1:
                    continue
                (param_key, param_val) = re.split(u'[\n\s]*=[\n\s]*', param, 1)
                monument_data[param_key] = param_val
                
            if u'knid' not in monument_data:
                continue
                
            try:
                monument = Monument.objects.get(kult_id=int(monument_data[u'knid']))
            except:
                monument = Monument(kult_id=int(monument_data[u'knid']))
            print monument_data[u'knid']
            
            if u'name' in monument_data and monument_data[u'name'] != '':
                monument.name = monument_data[u'name']
                
            if u'address' in monument_data and monument_data[u'address'] != '':
                monument.address = monument_data[u'address']
                
            if u'wikipedia' in monument_data and monument_data[u'wikipedia'] != '':
                monument.ruwiki = monument_data[u'wikipedia']
                
            if u'commonscat' in monument_data and monument_data[u'commonscat'] != '':
                monument.commons = monument_data[u'commonscat']
                
            if (u'lat' in monument_data and monument_data[u'lat'] != '' and \
                u'long' in monument_data and monument_data[u'long'] != ''):
                try:
                    coord_lat = float(monument_data[u'lat'])
                    coord_lon = float(monument_data[u'long'])
                    monument.coord_lat = coord_lat
                    monument.coord_lon = coord_lon
                except:
                    print u'ERROR: lat/log; Page: ' + page


            if u'region' in monument_data and monument_data[u'region'] != '':
                iso_code = monument_data[u'region'].upper()
                if iso_code == u'RU-MOW':
                    iso_code = u'RU-MOS'
                if iso_code == u'RU-SEV':
                    iso_code = u'RU-KM'
                regions = Region.objects.filter(iso_code=iso_code)
                if regions.count():
                    region = regions[0]
                    monument.region = region
                    if u'municipality' in monument_data and monument_data[u'municipality'] != '':
                        cities = City.objects.filter(region=region, name=monument_data[u'municipality'])
                        if cities.count():
                            monument.city = cities[0]
                            
            monument.save()
            

    def run_pagegenerator(self):
        api_params = {
            'action': 'query',
            'generator': 'allpages',
            'gapprefix': u'Культурное наследие России/'.encode('utf8'),
            'gapnamespace': 0,
            'gapcontinue': '',
            'gaplimit': 100, # 500
            'prop': 'revisions',
            'rvprop': 'content',
        }
        self.run_pagegenerator_loop(api_params)
        
        api_params['gapprefix'] = u'Культурное наследие/Крым'.encode('utf8')
        self.run_pagegenerator_loop(api_params)
        
        api_params['gapprefix'] = u'Культурное наследие/Севастополь'.encode('utf8')
        self.run_pagegenerator_loop(api_params)


    def run_pagegenerator_loop(self, api_params):
        while True:
            answer = self.api_request(api_params, True)
            for page_id in answer['query']['pages']:
                page = answer['query']['pages'][page_id]
                if 'revisions' in page:
                    for rev in page['revisions']:
                        self.process_text(rev['*'], page['title'])
                    
            if ('query-continue' not in answer or \
                'allpages' not in answer['query-continue'] or \
                'gapcontinue' not in answer['query-continue']['allpages'] or \
                answer['query-continue']['allpages']['gapcontinue'] == ''):
                break
            api_params.gapcontinue = answer['query-continue']['allpages']['gapcontinue'].encode('utf8')
                
            
    def login(self):
        api_params = {
            'action': 'login',
            'lgname': WIKI_NAME.encode('utf8'),
            'lgpassword': WIKI_PASSWORD.encode('utf8'),
        }   
        answer = self.api_request(api_params, True)
        
        api_params['lgtoken'] = answer['login']['token']
        answer = self.api_request(api_params, True)
        
        return True


    def api_request(self, ext_params, post=False):
        params = {
            'format': 'json',
        }
        params.update(ext_params)
        get_string = urllib.urlencode(params)

        server = 'http://ru.wikivoyage.org'

        if post:
            f = self.opener.open('%s/w/api.php' % server, get_string)
        else:
            f = self.opener.open('%s/w/api.php?%s' % (server, get_string))

        return json.load(f)

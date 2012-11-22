## Install

    git clone git@github.com:putnik/WLM.git
    cd WLM
    cp settings_local.default.py settings_local.py

Create database for project. Than put settings to your settings\_local.py file.

Install django-tynymce application.

    python2 manage.py syncdb
    wget http://wikilovesmonuments.ru/dumps/wlm.sql.bz2
    bzip2 -d wlm.sql.bz2
    mysql -u<db_user> -p <db_name> < wlm.sql

Now you may remove dump file and start django server:

    rm wlm.sql
    python2 manage.py runserver


## Daily dumps

* [Region] (http://wikilovesmonuments.ru/dumps/region.sql)
* [City] (http://wikilovesmonuments.ru/dumps/city.sql)
* [Monument] (http://wikilovesmonuments.ru/dumps/monument.sql)
* [MonumentPhoto] (http://wikilovesmonuments.ru/dumps/monumentphoto.sql)

All in one archive:
[wlm.sql.bz2] (http://wikilovesmonuments.ru/dumps/wlm.sql.bz2)

If something wron with latest dump, you can download more old (since
2012-11-10) using direct link with date:

    http://wikilovesmonuments.ru/dumps/wlm_<yyyy-mm-dd>.sql.bz2


## License

(The MIT License)

Copyright (c) 2012 [Sergey Leschina] (http://putnik.ws)  
Copyright (c) 2012 [Valery Ilychev] (http://sarutobi.me)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

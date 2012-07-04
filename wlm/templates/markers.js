{%spaceless%}
{ "markers":[
{%for m in monuments%}
{"lat":{{m.coord_lat|stringformat:'f'}}, "lon":{{m.coord_lon|stringformat:'f'}},"name":"{{m.name|default:"Неизвестно"|truncatewords:5}}"}{%if forloop.last%}{%else%},{%endif%}
{%endfor%}
]}
{%endspaceless%}

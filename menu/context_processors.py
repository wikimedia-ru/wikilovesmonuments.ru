from menu.models import MenuItem


def menu_items(request):
    items = MenuItem.objects.all()
    for item in items:
        if (request.path[:len(item.url)] == item.url):
            item.active = True
    return { 'menu': items }

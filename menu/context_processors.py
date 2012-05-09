from menu.models import MenuItem


def menu_items(request):
    items = MenuItem.objects.order_by('order')
    for item in items:
        if item.url == '/':
            if request.path == '/':
                item.active = True
        elif request.path[:len(item.url)] == item.url:
            item.active = True
    return { 'menu': items }

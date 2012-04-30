from menu.models import MenuItem


def menu_items(request):
    return { 'menu': MenuItem.objects.all() }

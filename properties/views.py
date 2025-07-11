from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Property

@cache_page(60 * 15)  # Cache for 15 minutes (60 seconds * 15)
def property_list(request):
    properties = Property.objects.all().values('id', 'title', 'price', 'description')
    return JsonResponse(list(properties), safe=False)
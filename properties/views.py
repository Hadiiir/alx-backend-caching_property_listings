from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .models import Property  # Assuming you have a Property model


@cache_page(60 * 15)  # Cache for 15 minutes (60 seconds * 15)
def property_list(request):
    properties = Property.objects.all()
    properties = get_all_properties()  # Use our cached queryset function

    return render(request, 'properties/list.html', {'properties': properties})
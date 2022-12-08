import django_filters
from .models import Request

#Request filter form
# "exact" requires a correct value
# "icontains" allows you to search for queries that contain this value
class RequestFilter(django_filters.FilterSet):

    class Meta:
        model = Request
        fields = {
            'id': ['exact'],
            'customer' : ['icontains'],
            'status' : ['exact'],
            'faction' : ['exact'],
            'priority' : ['exact'],
        }
        



        
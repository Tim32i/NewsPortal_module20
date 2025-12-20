from django_filters import FilterSet, DateTimeFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Post, Category


class NewsFilter(FilterSet):
    created_after = DateTimeFilter(
            field_name='time_create',
            lookup_expr='gt',
            widget=DateTimeInput(format='%Y-%m-%dT%H:%M',
                                 attrs={'type': 'datetime-local'})
        )
    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'author': ['exact'],
            'time_create': [],
        }


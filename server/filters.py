from .models import *
import django_filters


class UserFilterForm(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = {'first_name', 'is_katchy', 'is_zam', 'is_tor_aga', 'region'}


class NewsFilterForm(django_filters.FilterSet):
    class Meta:
        model = News
        fields = {'rubric', }


class ChatFilterForm(django_filters.FilterSet):
    # title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Chat
        fields = {'title', }

import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post



NEWS = 'NW'
ARTICLE = 'AR'
CATEGORY_CHOCE = [
    (NEWS, 'Новость'),
    (ARTICLE, 'Статья')
]


class PostFilter(FilterSet):
    CategoryType = django_filters.ChoiceFilter(label='Тип',choices=CATEGORY_CHOCE)
    heading = django_filters.CharFilter(label='Заголовок',lookup_expr='icontains',)
    date_time = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}),lookup_expr='gt',label='Даты поста')
    postCategory = django_filters.ChoiceFilter(label='Категория')
    class Meta:
        model = Post
        fields = ['heading','CategoryType','date_time','postCategory',]


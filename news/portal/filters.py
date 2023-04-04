from django_filters import FilterSet, DateFilter # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
from django import forms


# создаём фильтр
class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться
    # (т. е. подбираться) информация о постах
    date = DateFilter(field_name='post_date', widget=forms.DateInput(attrs={'type': 'date'}),
                      label='поиск по дате начиная с', lookup_expr='date__gte')

    class Meta:
        model = Post

        fields = {
            'post_title': ['icontains'],
            'post_date': ['lte'],
            'post_text': ['icontains']
        }
    # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)
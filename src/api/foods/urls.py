from django.urls import path

from api.foods.views import FoodsListView

app_name = 'foods'

urlpatterns = [
    path('', FoodsListView.as_view(), name='list'),
]

from django.db.models import Exists, OuterRef, Prefetch
from rest_framework.generics import ListAPIView

from api.foods.serializers import FoodListSerializer
from apps.foods.models import FoodCategory, Food


class FoodsListView(ListAPIView):
    """
    Возвращает список блюд по категориям
    """
    serializer_class = FoodListSerializer

    def get_queryset(self):
        """
        Необходимо вывести только категории, у которых есть блюда, доступные к
        публикации (is_publish=True).
        """
        published_foods = Food.objects.filter(
            category_id=OuterRef('pk'), is_publish=True
        )
        prefetch_foods = Prefetch(
            'food', Food.objects.filter(is_publish=True), to_attr='foods'
        )
        queryset = FoodCategory.objects.prefetch_related(
            prefetch_foods, 'foods__additional'
        ).filter(
            Exists(published_foods)
        )
        return queryset

from .models import *
from django.db.models import Count
from django.core.cache import cache


menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class DataMixin:
    """Класс добавления функционала для модели данных.
    """
    paginate_by = 3

    def get_user_context(self, **kwargs):
        """Получение контекста пользователя."""
        context = kwargs
        cats = Category.objects.annotate(Count('women'))

    # def get_user_context(self, **kwargs):
    #     context = kwargs
    #     # берем из кэша данные коллекции БД, если есть
    #     cats = cache.get('cats')
    #     if not cats:  # если нет, то читаем из БД
    #         cats = Category.objects.annotate(Count('women'))
    #         cache.set('cats', cats, 60)  # добавляем в кэш данные коллекции

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

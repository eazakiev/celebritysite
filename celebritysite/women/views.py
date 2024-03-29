from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from .serializers import WomenSerializer
from .forms import RegisterUserForm, ContactForm, AddPostForm, LoginUserForm
from .utils import DataMixin
from django.core.paginator import Paginator
from .models import Category, Women
from .utils import *
from rest_framework import generics


class WomenHome(DataMixin, ListView):
    """Класс для получения главной страницы сайта
    Args:
        DataMixin (class): _description_
        ListView (class): _description_
    """
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для главной страницы сайта"""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        # dict(list(context.items()) + list(c_def.items()))
        return context | c_def

    def get_queryset(self):
        """Получение объектов для постов"""
        return Women.objects.filter(is_published=True).select_related('cat')


# def index(request):
#     posts = Women.objects.filter(is_published=True)
#     # posts = Women.objects.all()
#     context = {
#         "posts": posts,
#         "menu": menu,
#         "title": "Главная страница",
#         "cat_selected": 0,
#     }
#     return render(request, "women/index.html", context=context)

def about(request):
    """О сайте"""
    contact_list = Women.objects.all()
    # paginator = Paginator(contact_list, 3)  # Show 3 contacts per page.

    page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number) 'page_obj': page_obj,
    return render(request, 'women/about.html', {"title": "О сайте", "menu": menu})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """Класс для добавления статьи
    Args:
        LoginRequiredMixin (class): _description_
        DataMixin (class): _description_
        CreateView (class): _description_
    """
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для добавления статьи"""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return context | c_def


class ContactFormView(DataMixin, FormView):
    """Класс для представления формы контактов
    Args:
        DataMixin (class): _description_
        FormView (class): Стандартный базовый класс для форм,
        не привязанных к моделям, не работает с БД
    """
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для шаблона, формы контактов"""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return context | c_def

    def form_valid(self, form):
        """
        Обработка формы контактов, вызывается если пользователь
        корректно заполнил все поля контактной формы
        """
        print(form.cleaned_data)
        return redirect('home')


def pageNotFound(request, exception):
    """Получение сообщения страница не найдена"""
    return HttpResponseNotFound("<h1>Страница не найдена (Боевой сервер!)</h1>")


class ShowPost(DataMixin, DetailView):
    """Класс для представления статьи
    Args:
        DataMixin (class): _description_
        DetailView (class): _description_
    """
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для представления статьи"""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context | c_def


class WomenCategory(DataMixin, ListView):
    """Класс для получения списка категорий сайта
    Args:
        DataMixin (class): _description_
        ListView (class): _description_
    """
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        """Получение объектов для списка категорий"""
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для списка категорий"""
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(
            title='Категория - ' + str(c.name), cat_selected=c.pk)
        return context | c_def


class RegisterUser(DataMixin, CreateView):
    """Класс для регистрации пользователя
    Args:
        DataMixin (class): _description_
        CreateView (class): _description_
    """
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для регистрации пользователя"""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return context | c_def

    def form_valid(self, form):
        """
        Обработка формы регистрации пользователя, вызывается если
        пользователь корректно заполнил все поля контактной формы
        """
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    """Класс для авторизации пользователя
    Args:
        DataMixin (class): _description_
        LoginView (class): _description_
    """
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """Получение контекста для авторизации пользователя"""
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return context | c_def

    def get_success_url(self):
        """Получение страницы после авторизации пользователя"""
        return reverse_lazy('home')


def logout_user(request):
    """Получение перенаправления после авторизации пользователя"""
    logout(request)
    return redirect('login')


class WomenAPIView(generics.ListAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer

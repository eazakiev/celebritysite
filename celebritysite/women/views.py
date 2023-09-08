from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Women

menu = [{'title': "О сайте", 'url_name': "about"},
        {'title': "Добавить статью", 'url_name': "add_page"},
        {'title': "Обратная связь", 'url_name': "contact"},
        {'title': "Войти", 'url_name': "login"},
        ]


def index(request):
    posts = Women.objects.filter(is_published=True)
    # posts = Women.objects.all()
    context = {
        "posts": posts,
        "menu": menu,
        "title": "Главная страница",
        "cat_selected": 0,
    }
    return render(request, "women/index.html", context=context)


def about(request):
    context = {
        "title": "О сайте",
        "menu": menu,
    }
    return render(request, "women/about.html", context=context)


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена (Боевой сервер!)</h1>")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    context = {
        "post": post,
        "menu": menu,
        "title": post.title,
        "cat_selected": post.cat_id,
    }
    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    posts = Women.objects.filter(cat__slug=cat_slug)

    if len(posts) == 0:
        raise Http404()

    context = {
        "posts": posts,
        "menu": menu,
        "title": "Отображение по рубрикам",
        "cat_selected": cat_slug
    }
    return render(request, "women/index.html", context=context)

from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import re_path

from .models import Women

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


def index(request):
    context = {
        "title": "Главная страница",
        "menu": menu,
        "posts": Women.objects.all(),
    }
    return render(request, "women/index.html", context=context)


def about(request):
    context = {
        "title": "О сайте",
        "menu": menu,
    }
    return render(request, "women/about.html", context=context)


def categories(request, catid: int):
    print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>{catid}</p>")


def archive(request, year: re_path):
    if int(year) > 2023:
        # raise Http404()
        return redirect("/", permanent=False)
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

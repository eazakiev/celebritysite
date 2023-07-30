from django.urls import path

from .views import about, addpage, contact, index, login

app_name = "women"
urlpatterns = [
    path("", index, name="home"),
    path("about/", about, name="about"),
    path("addpage/", addpage, name="add_page"),
    path("contact/", contact, name="contact"),
    path("login/", login, name="login"),
]

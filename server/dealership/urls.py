from django.contrib import admin
from django.urls import path
from frontend import views
urlpatterns=[
    path("admin/",admin.site.urls),
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("djangoapp/login",views.login_user,name="login_user"),
    path("djangoapp/logout",views.logout_user,name="logout_user"),
]

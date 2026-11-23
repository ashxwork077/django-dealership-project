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
    path("djangoapp/get_dealer_reviews/<int:dealer_id>",views.get_dealer_reviews,name="get_dealer_reviews"),
    path("djangoapp/get_dealers",views.get_all_dealers,name="get_all_dealers"),
]

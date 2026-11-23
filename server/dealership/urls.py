from django.contrib import admin
from django.urls import path
from frontend import views
urlpatterns=[
    path("admin/",admin.site.urls),
    path("dealers/",views.dealers_page,name="dealers_page"),
    path("",views.home,name="home"),
    path("about/",views.about,name="about"),
    path("contact/",views.contact,name="contact"),
    path("djangoapp/login",views.login_user,name="login_user"),
    path("djangoapp/logout",views.logout_user,name="logout_user"),
    path("djangoapp/get_dealer_reviews/<int:dealer_id>",views.get_dealer_reviews,name="get_dealer_reviews"),
    path("djangoapp/get_dealers",views.get_all_dealers,name="get_all_dealers"),
    path("djangoapp/get_dealer_by_id/<int:dealer_id>",views.get_dealer_by_id,name="get_dealer_by_id"),
    path("djangoapp/get_dealers/<str:state>",views.get_dealers_by_state,name="get_dealers_by_state"),
]

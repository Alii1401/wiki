from django.urls import path
from . import views


app_name="entries"
urlpatterns = [
    path("", views.index, name="index"),
    path("newpage/", views.newpage.as_view(), name="newpage"),
    path("randpage",views.randpage, name="randpage"),
    path("edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("error", views.error, name="error"),
    path('page/<slugtitle>/', views.page, name='page')

]
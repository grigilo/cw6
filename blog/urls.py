from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogUpdateView, BlogDeleteView, \
    BlogDetailView

app_name = BlogConfig.name
urlpatterns = [

    path("detail/<int:pk>/", cache_page(60)(BlogDetailView.as_view()),
         name="detail"),
    path("create/", BlogCreateView.as_view(), name="create"),
    path("update/<int:pk>/", BlogUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", BlogDeleteView.as_view(), name="delete"),

]

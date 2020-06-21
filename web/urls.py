from django.urls import path, re_path
from .views import Articlelist, ArticleDetail,Categorylist

app_name = 'web'

urlpatterns = [
    path('', Articlelist.as_view(), name='home'),
    path('page/<int:page>', Articlelist.as_view(), name='home'),
    path('article/<slug:slug>', ArticleDetail.as_view(), name='detail'),
    path('category/<slug:slug>', Categorylist.as_view(), name='category'),
    path('category/<slug:slug>/page/<int:page>', Categorylist.as_view(), name='category'),
]

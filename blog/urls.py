from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home_page, name='home_page'),
    path('', views.HomePageView.as_view(), name='home_page'),
    path('posts', views.PostsView.as_view(), name='posts_page'),
    path('posts/<slug:slug>', views.PostDetail.as_view(), name='posts_detail_page'),
    path('read-later',views.ReadLaterView.as_view(),name="read-later"),
]

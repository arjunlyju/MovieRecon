from django.urls import path
from . import views

app_name = 'movieapp'
urlpatterns = [
    path('', views.allmovies, name='allmovies'),
    path('search/', views.SearchResult, name='searchresult'),
    path('mylist/', views.mylist, name='mylist'),
    path('<slug:c_slug>/', views.allmovies, name='movies_by_category'),
    path('<slug:c_slug>/<slug:m_slug>/', views.moviedetails, name='moviedetails'),
    path('category/<slug:category_slug>/', views.allmovies, name='movies_by_category'),
    path('category/<slug:m_slug>/submit_review/', views.submit_review, name='submit_review')
]

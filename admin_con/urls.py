from django.urls import path
from . import views

app_name='admin_con'

urlpatterns=[
path('',views.movielist,name='all_list'),
path('cat/',views.catlist,name='cat_list'),
path('user/',views.userlist,name='user_list')
]

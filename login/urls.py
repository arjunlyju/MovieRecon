from django.urls import path
from . import views
app_name='login'
urlpatterns=[
    path('',views.login_user,name='login'),
    path('registration/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('user/',views.userprofile,name='user'),
    path('update/',views.update,name='update'),
    path('admin/',views.admin,name='admin')
]
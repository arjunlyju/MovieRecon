from django.urls import path
from. import views
app_name='edit'
urlpatterns=[
    path('add/',views.addlist,name='add'),
    path('addcat/',views.addcategory,name='addcat'),
    path('delete/<slug:d_slug>/',views.delete,name='delete'),
    path('delete/user/<int:user_id>/',views.deleteuser,name='deleteuser'),
    path('delete/category/<slug:c_slug>/',views.delete_cat,name='delete_cat'),
    path('<slug:m_slug>/',views.updatelist,name='update'),
]
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from movieapp.models import Movie,Category
# Create your views here.
@login_required(login_url='login:admin')
def movielist(request):
    movies=Movie.objects.all()
    return render(request,'movie_list.html',dict(movies=movies))

@login_required(login_url='login:admin')
def catlist(request):
    category=Category.objects.all()
    return render(request, 'cat_list.html', dict(category=category))

@login_required(login_url='login:admin')
def userlist(request):
    users=get_user_model().objects.all()
    return render(request, 'user_list.html', dict(users=users))

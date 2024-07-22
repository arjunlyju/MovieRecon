from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from movieapp.models import Movie,Category
from. forms import MovieForm
# Create your views here.
@login_required(login_url='login:login')
def addlist(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        actor = request.POST.get('actor')
        rdate = request.POST.get('rdate')
        desc = request.POST.get('desc')
        category = request.POST.get('category')
        category_instance = Category.objects.get(id=category)
        poster = request.FILES.get('poster')
        link=request.POST.get('link')
        user = request.user
        movie = Movie(title=title, actor=actor, release=rdate, desc=desc, category=category_instance, poster=poster, link=link,added_by=user)
        movie.save()
        return redirect('movieapp:allmovies')
    return render(request, 'add.html')

@login_required(login_url='login:login')
def updatelist(request, m_slug):
    movie = get_object_or_404(Movie, slug=m_slug)
    form=MovieForm(request.POST or None,instance=movie)
    if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('movieapp:allmovies')
    return render(request,'update2.html',dict(form=form))

@login_required(login_url='login:login')
def delete(request,d_slug):
    print(d_slug)
    movie = get_object_or_404(Movie, slug=d_slug)
    movie.delete()
    return redirect('/')

@login_required(login_url='login:admin')
def delete_cat(request,c_slug):
    category=get_object_or_404(Category, slug=c_slug)
    category.delete()
    return redirect('admin_con:cat_list')
@login_required(login_url='login:admin_con')
def addcategory(request):
    if request.method=='POST':
        name=request.POST.get('name')
        if Category.objects.filter(name=name).exists():
            messages.info(request, 'category exists')
            return redirect('edit:addcat')
        else:
            category=Category(name=name)
            category.save()
        return redirect('movieapp:allmovies')
    return render(request,'add_category.html')

def deleteuser(request,user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    user.delete()
    return redirect('admin_con:user_list')
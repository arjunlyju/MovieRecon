from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category,Movie
# Create your views here.
def allmovies(request,c_slug=None):
    c_page = None
    movie_list = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movie_list = Movie.objects.all().filter(category=c_page)
    else:
        movie_list = Movie.objects.all()
    paginator = Paginator(movie_list, 6)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)
    new_registration = request.session.pop('new_registration', False)
    return render(request,  'home.html', {'category': c_page, 'movies': movies,'new_registration':new_registration})
@login_required(login_url='login:login')
def moviedetails(request,m_slug,c_slug):
    try:
        movie = Movie.objects.get(slug=m_slug)
    except Exception as e:
        raise e
    return render(request, 'movie.html', {'movie': movie})

def SearchResult(request):
    movies=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        movies=Movie.objects.all().filter(Q(title__contains=query))
    return render(request,'search.html',{'query':query,'movies':movies})

@login_required
def mylist(request):
    user=request.user
    movie_list = Movie.objects.all().filter(added_by=user)
    return render(request,'mymovies.html',dict(movies=movie_list))




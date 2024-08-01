from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ReviewForm
from .models import Category, Movie, ReviewRating


# Create your views here.
def allmovies(request, c_slug=None):
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
    return render(request, 'home.html', {'category': c_page, 'movies': movies,
                                         'new_registration': new_registration})


@login_required(login_url='login:login')
def moviedetails(request, m_slug, c_slug):
    try:
        movie = Movie.objects.get(slug=m_slug)
    except Exception as e:
        raise e
    return render(request, 'movie.html', {'movie': movie})


def SearchResult(request):
    movies = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        movies = Movie.objects.filter(Q(title__contains=query))
    return render(request, 'search.html', {'query': query, 'movies': movies})


@login_required
def mylist(request):
    user = request.user
    movie_list = Movie.objects.all().filter(added_by=user)
    return render(request, 'mymovies.html', dict(movies=movie_list))


# def submit_review(request, m_slug):
#     global data
#     url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             movie = get_object_or_404(Movie, slug=m_slug)
#             review = ReviewRating.objects.get(user_id=request.user, movie=movie)
#             form = ReviewForm(request.POST or None, instance=review)
#             form.save()
#             messages.success(request, 'thank you your review as been updated')
#             return redirect(url)
#         except ReviewRating.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = ReviewRating()
#                 data.movie = m_slug
#                 data.user = request.user
#                 data.subject = form.cleaned_data['subject']
#                 data.review = form.cleaned_data['review']
#                 data.rating = form.cleaned_data['rating']
#                 data.ip = form.cleaned_data['REMOTE_ADDR']
#
#             data = ReviewRating(subject=data.subject, review=data.review, rating=data.rating)
#             data.save()
#             messages.success(request, 'thank you your review as been updated')
#             return redirect(url)

def submit_review(request, m_slug):
    url = request.META.get('HTTP_REFERER')
    movie = get_object_or_404(Movie, slug=m_slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review, created = ReviewRating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={
                    'subject': form.cleaned_data['subject'],
                    'review': form.cleaned_data['review'],
                    'rating': form.cleaned_data['rating'],
                    'ip': request.META.get('REMOTE_ADDR')
                }
            )
            if created:
                messages.success(request, 'Thank you, your review has been submitted.')
            else:
                messages.success(request, 'Thank you, your review has been updated.')

            return redirect(url)

    return redirect(url)
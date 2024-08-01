from django.contrib import admin
from .models import Category, Movie, ReviewRating


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'desc', 'release', 'actor']
    prepopulated_fields = {'slug': ('title',)}


class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ['movie', 'user', 'subject', 'rating', 'created_at']
    list_filter = ['movie', 'user', 'rating']
    search_fields = ['subject', 'review']
    readonly_fields = ['created_at']  # If you want to make `created_at` read-only


admin.site.register(Category, CategoryAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)

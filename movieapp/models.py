from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        # Automatically generate a slug when saving the instance
        if not self.slug or self.slug != self.name:
            generated_slug = slugify(self.name)
            print(f"Generated Slug: {generated_slug}")
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('movieapp:movies_by_category', args=[str(self.slug)])


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200)
    poster = models.ImageField(upload_to='poster', blank=True)
    desc = models.TextField()
    release = models.DateField()
    actor = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    link = models.URLField()
    added_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return '{}'.format(self.title)

    def save(self, *args, **kwargs):
        # Automatically generate a slug when saving the instance
        if not self.slug or self.slug != self.title:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('movieapp:moviedetails', args=[self.category.slug, self.slug])


class ReviewRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subject = models.CharField(max_length=100,blank=True)
    review = models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

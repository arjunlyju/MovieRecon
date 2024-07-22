from django.contrib import admin
from.models import Category,Movie

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,CategoryAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ['title','category','desc','release','actor']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Movie,MovieAdmin)
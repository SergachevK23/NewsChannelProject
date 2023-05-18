from django.contrib import admin
from .models import Category, Author, Post, Comment, PostCategory

class CategoryInline(admin.TabularInline):
    # указываем в качестве модели промежуточный класс
    model = PostCategory
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = (CategoryInline,)


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'role',
        'date_joined',
    )
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'role',
        'date_joined',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'slug',
    )
    search_fields = ('name',)


class GenreTitleInline(admin.TabularInline):
    model = Title.genre.through


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'description')
    search_fields = ('name',)
    list_filter = (
        'year',
        'category',
        'genre',
    )
    inlines = [GenreTitleInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'text', 'score', 'pub_date')
    search_fields = ('title',)
    list_filter = ('author', 'title', 'pub_date')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'review', 'text', 'pub_date')
    search_fields = ('author', 'review')
    list_filter = ('author', 'review', 'pub_date')


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)

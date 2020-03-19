from django.contrib import admin
from .models import Post, Profile, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status')
    list_filter = ('status', 'created', 'update')
    prepopulated_fields = {'slug': ('title',)}  # автозаполнение
    list_editable = ('status',)  # что можно менять сразу


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment)

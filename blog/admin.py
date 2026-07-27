from django.contrib import admin
from django.utils.html import format_html
from .models import AuthorProfile, Category, Tag, Post, Comment, Like


@admin.register(AuthorProfile)
class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_author', 'bio')
    list_editable = ('is_author',)
    search_fields = ('user__username', 'user__email', 'bio')
    list_filter = ('is_author',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview', 'author', 'category', 'status', 'view_count', 'created_at')
    list_filter = ('status', 'category', 'tags', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Main Info', {
            'fields': ('title', 'slug', 'author', 'category', 'tags', 'content', 'status')
        }),
        ('Featured Image Upload', {
            'fields': ('featured_image',),
            'description': 'Local file upload (takes top priority over external images).'
        }),
        ('External Sample Image & Attribution', {
            'fields': ('external_image_url', 'image_credit_name', 'image_credit_url'),
            'classes': ('collapse',),
            'description': 'Optional direct stock photo URL and photographer credits.'
        }),
    )

    def image_preview(self, obj):
        url = obj.display_image_url
        return format_html('<img src="{}" style="height: 40px; width: 60px; object-fit: cover; border-radius: 4px;" />', url)
    image_preview.short_description = 'Image'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content_snippet', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username', 'post__title')

    def content_snippet(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_snippet.short_description = 'Content'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__title')

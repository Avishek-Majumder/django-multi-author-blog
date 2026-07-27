from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home_view, name='home'),

    # Auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Author Dashboard
    path('dashboard/', views.author_dashboard_view, name='author_dashboard'),

    # Post Management
    path('post/create/', views.post_create_view, name='post_create'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),

    # Comments & Likes
    path('post/<slug:slug>/comment/', views.comment_create_view, name='comment_create'),
    path('comment/<int:pk>/delete/', views.comment_delete_view, name='comment_delete'),
    path('post/<slug:slug>/like/', views.like_toggle_view, name='like_toggle'),

    # Taxonomies & Search
    path('category/<slug:slug>/', views.category_posts_view, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts_view, name='tag_posts'),
    path('search/', views.search_view, name='search'),

    # Public Author Profile
    path('author/<str:username>/', views.author_profile_view, name='author_profile'),
]

from django.urls import path

from . import views


urlpatterns = [

    path('', views.home_view, name='home'),

    path('create/', views.create_post, name='create_post'),
    path('update/<int:post_id>/', views.update_post, name='update_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('api/posts/', views.posts_api),
    path('api/comments/', views.comments_api),

]
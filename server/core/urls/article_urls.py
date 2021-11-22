from django.urls import path
from core.views import article_views as views

urlpatterns = [
    path('', views.getArticles, name='articles'),

    path('create/', views.createArticle, name="article-create"),
    path('upload/', views.uploadImage, name='image-upload'),

    path('top/', views.getTopArticle, name='top-articles'),
    path('hot/', views.getHotArticle, name='hot-articles'),
    path('news/', views.getNewsArticle, name='news-articles'),

    path('<str:pk>/comments/', views.createComment, name="create-comment"),
    path('<str:pk>/', views.getArticleById, name="article"),

    path('update/<str:pk>/', views.updateArticle, name="article-update"),
    path('delete/<str:pk>/', views.deleteArticle, name="article-delete"),
]

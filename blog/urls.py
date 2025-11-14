# blog/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views    
from .views import * # our view class definition 

urlpatterns = [
    path('', RandomArticleView.as_view(), name='random'), 
    path('show_all', ShowAllView.as_view(), name='show_all'), 
    path('article/create', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article'),    
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), #New
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name='update_article'),    
    path('comment/<int:pk>/delete', DeleteCommentView.as_view(), name='delete_comment'),    
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'), 
	path('logout/', auth_views.LogoutView.as_view(next_page='show_all'), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),

    ## API Views:
    path(r'api/', ArticleListAPIView.as_view(), name='article_list_api'),
    path(r'api/random', ArticleListAPIView.as_view(), name='article_list_api'),
    path(r'api/jokes', ArticleListAPIView.as_view(), name='article_list_api'),
    path(r'api/joke/<int:pk>', ArticleListAPIView.as_view(), name='article_list_api'),
    path(r'api/pictures', ArticleListAPIView.as_view(), name='article_list_api'),
    path(r'api/picture/<int:pk>', ArticleListAPIView.as_view(), name='article_list_api'),
    path(r'api/random_picture', ArticleListAPIView.as_view(), name='article_list_api'),
]
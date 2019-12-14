from django.urls import path
from . import views

urlpatterns = [
    #Default page (i.e '' or no info) is the post_list page: See VIEWS.PY for furhter documentation
    path('', views.post_list, name='post_list'),

    #Says that when you click on a blog post, the URL should:
        #1.Start with /post/
        #2.take an integer value and set it equal to var pk
        #3 close out the URL with a /
        #ex: post/5/ would tell Django to get the 5th blog post and display it as a page (using the View you created)
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    #Let's you create a new post
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]

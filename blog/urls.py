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

    #Path to create a new post by htting the glyphicon-plus span (button)
    path('post/new/', views.post_new, name='post_new'),
    #Path to edit a post
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    #Path to view all unpublished posts i.e drafts
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    #Path to publish drafts
    path('post/<pk>/publish/', views.post_publish, name='post_publish'),
    #Path to remove posts
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    #Path to add a comment while looking at a blog post
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    #Path to approve of comments
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    #Path to remove comments
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),

]

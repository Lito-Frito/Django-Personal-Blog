from django import forms

from .models import Post, Comment

#Creates a form to let authorized users create posts
class PostForm(forms.ModelForm):

    class Meta:
        #Use Post to create this model
        model = Post
        fields = ('title', 'text',)

#this creates a form to let users comment on a post
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

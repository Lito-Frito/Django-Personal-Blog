from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        #Use Post to create this model
        model = Post
        fields = ('title', 'text',)

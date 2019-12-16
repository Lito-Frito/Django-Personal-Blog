#This is the /admin page
from django.contrib import admin

#This goes to models.py and gets the Post and Comment objects
from .models import Post, Comment

#Shows the models Post and Comment in the admin page
admin.site.register(Post)
admin.site.register(Comment)

from django.shortcuts import redirect
from django.shortcuts import render

#This is needed for Class Post, which uses dates
from django.utils import timezone

#Import the Post class from models.py (in the current directory)
from .models import Post

#This is so that a 404 error comes up if I type in /post/9/ but there's no ninth post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm

#This function (view) tells URLS.PY what post_list is (in that file, it's the default page for the blog) and renders it.
#See blog/template/blog/post_detail.html to see the file that's being rendered
def post_list(request):
    #Uses QuerySets to sort blog posts by date (oldest first)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

    #go to blog/post_list file and get the variable posts (as defined in the line above)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

from django.shortcuts import redirect
from django.shortcuts import render

#This is needed for Class Post, which uses dates
from django.utils import timezone

#Import the Post class from models.py (in the current directory) and Comment class
from .models import Post, Comment

#This is so that a 404 error comes up if I type in /post/9/ but there's no ninth post
from django.shortcuts import render, get_object_or_404

#imports PostForm (which has .ModelForm) and CommentForm
from .forms import PostForm, CommentForm

#decorator used to see if someone is logged in; @login_required will make pages only accessible by logged in users
from django.contrib.auth.decorators import login_required

#This function (view) tells URLS.PY what post_list is (in that file, it's the default page for the blog) and renders it.
#See blog/template/blog/post_detail.html to see the file that's being rendered
def post_list(request):
    #Uses QuerySets to sort blog posts by date (oldest first)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    #go to blog/post_list file and get the variable posts (as defined in the line above)
    return render(request, 'blog/post_list.html', {'posts': posts})

#renders the specific blog post that you clicked on
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})



#POST/.POST means you posted data, not a blog post
@login_required
def post_new(request):
    #This means, "if you have already submited (or POSTed) data, save the content and call post_detail to create a new blog post"
    #Finally, go back to the post_new page, but after submiting the data
    #.method == POST comes from post_edit.html. It's saying if the form method is POST (which it is), trigger the conditional
    if request.method == "POST":
        #See line 34. This generates the form to create a post
        form = PostForm(request.POST)
        #This checks that you're not submiting a blank post (which is invalid) or no incorrect values were entered
        if form.is_valid():
            #Create a var 'post' so it can be saved. commit=False means don't submit post just yet (because more info is added later)
            post = form.save(commit=False)
            #The next lines just add the data typically associated with a blog post
            post.author = request.user
            #Preserve changes to post from added data; save that bad boy!
            post.save()
            #Redirects to post_detail while also generating a new pk for the URL
            return redirect('post_detail', pk=post.pk)
    #Else, if you haven't POSTed data, then just generate the regular post_new page
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})



#Let's  user edit posts, only if authenticated and valid data is passed through in the text form
@login_required
def post_edit(request, pk):
    #if page doesn't exist, return 404; take parameters Post and pk
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})



#view to display only draft posts
@login_required
def post_draft_list(request):
    #using a QuerySet, filters for posts without a publish date (i.e drafts) and orders them by create date
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})



#Publishes the post or returns a 404 error if the pk is wrong
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

#Takes parameter pk, finds the post, deletes it, and then returns you to post_list
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

#Takes parameter pk. If user is looking at post, show comment form. If form is valid (has data), save comment when clicking save and update page
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

#Takes parameter pk, and lets superuser approve of comment, then refresh post_detail page
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


#Takes parameter pk, and lets superuser delete comment, then refresh post_detail page
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

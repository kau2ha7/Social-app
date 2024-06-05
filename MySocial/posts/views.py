from django.shortcuts import render,redirect
from .forms import PostCreateForm,CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(data=request.POST,files=request.FILES)
        if form.is_valid():
         new_user = form.save(commit=False)
         new_user.user = request.user
         new_user.save()
    else:
       form = PostCreateForm()     
    return render(request,'posts/create.html',{'form':form})  

def feed(request):
   logged_user = request.user
   posts = Post.objects.all()
   if request.method == 'POST':
      comment_form = CommentForm(data=request.POST)
      if comment_form.is_valid():
         new_comment = comment_form.save(commit=False)
         post_id = request.POST.get('post_id')
         post = get_object_or_404(Post,id=post_id)
         new_comment.post = post
         new_comment.save()
   else:
     comment_form = CommentForm()   
     posts = Post.objects.all()
   return render(request,'posts/feed.html',{'posts':posts,'comment_form':comment_form,'logged_user':logged_user})

def like_post(request):
   post_id = request.POST.get('post_id')
   post = get_object_or_404(Post, id=post_id)
   if post.liked_by.filter(id=request.user.id).exists():
       post.liked_by.remove(request.user)
   else:
      post.liked_by.add(request.user)
   return redirect('feed')   
      

       



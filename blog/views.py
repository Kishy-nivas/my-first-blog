from django.shortcuts import render,get_object_or_404,redirect
from blog .models import Post
from django.utils import timezone
from .forms import PostForm

# Create your views here.
# To display all list 
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts' : posts})

# To display a particular post, based on url provided 

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'blog/post_detail.html',{'post':post})

# To create a new post
def post_new(request):
    if (request.method =='POST'):
        form = PostForm(request.POST)
        if (form.is_valid()):
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request,'blog/post_new.html',{'form':form})


# To edit an existing post 

def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if(request.method =='POST'):
        form = PostForm(request.POST,instance =post)
        if(form.is_valid()):
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('post_detail',pk= post.pk)
    else :
        form = PostForm(instance = post)

    return render(request,'blog/post_new.html',{'form':form})

# To publish posts in draft (unpublished post)

def post_draft(request):
    posts = Post.objects.filter(published_date__isnull = True).order_by('created_date')
    return render(request,'blog/post_draft.html',{'posts':posts});



def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=post.pk)




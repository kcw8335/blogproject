from django.shortcuts import render, get_object_or_404, redirect ,HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog, Comment
from django.contrib.auth.decorators import login_required
from .forms import BlogForm

def home(request):
    blogs = Blog.objects
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'home.html',{'blogs':blogs, 'posts':posts})

def detail(request, blog_id):
    details = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html',{'details':details})

def new(request):
    form = BlogForm()
    return render(request, 'new.html',{'form':form})

def create(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.save()
            return redirect('/blog/' + str(blog.id))
    else:
        form = BlogForm()
    return render(request, 'new.html', {'form':form})

def edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit = False)
            blog.save()
            return redirect('/blog/' + str(blog.id))
    else:
        form = BlogForm(instance=blog)
    return render(request, 'edit.html', {'form':form})

def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('/')

@login_required
def comment_add(request, blog_id):
    if request.method == "POST":
        post = Blog.objects.get(pk=blog_id)
        comment = Comment()
        comment.user = request.user
        comment.body = request.POST['body']
        comment.post = post
        comment.save()
        return redirect('/blog/' + str(blog_id))
    else:
        return HttpResponse("잘못된 접근입니다.")

@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        comment.body = request.POST['body']
        comment.save()
        return redirect('/blog/' + str(comment.post.id))
    elif request.method == "GET":
        context = {
            'comment' : comment
        }
        return render(request, 'comment_edit.html', context)

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.user:
        if request.method == "POST":
            post_id = comment.post.id
            comment.delete()
            return redirect('/blog/'+ str(post_id))
    return HttpResponse('잘못된 접근입니다.')
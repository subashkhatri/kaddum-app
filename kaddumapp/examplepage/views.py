from django.shortcuts import render
from examplepage.models import Post

def hello(request):
    return render(request, 'pages/hello.html')

def post_index(request):
    posts = Post.objects.all()
    context = {
        "posts" : posts
    }
    return render(request, 'pages/post_index.html', context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        "post": post
    }
    return render(request, "pages/post_detail.html", context)
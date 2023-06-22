# from django.core.paginator import _SupportsPagination
from typing import Any
from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from datetime import date
from .forms import CommentForm
from django.urls import reverse

from django.views.generic import ListView,DetailView
from django.views import View

from .models import Post

# Create your views here.

# all_posts = [
    
# ]


# def get_list(post):
#     return post['date']
 
# def home_page(request):
#     latest_posts=Post.objects.all().order_by("-date")[:3]
#     # sorted_list=sorted(all_posts,key=get_list)
#     # latest_posts=sorted_list[-3:]
#     return render(request,"blog/index.html",{
#         "posts":latest_posts
#     })
#     # return HttpResponse("Hi there")


class HomePageView(ListView):
    model = Post
    template_name="blog/index.html"
    ordering=["-date"]
    context_object_name="posts"

    def get_queryset(self):
        query= super().get_queryset()
        data=query[:3]
        return data

# def posts(request):
#     # all_posts=Post.objects.filter()
#     all_posts=Post.objects.all().order_by("-date")
#     return render(request,"blog/all-posts.html",{
#         "all_posts":all_posts
#     })

class PostsView(ListView):
    model = Post
    template_name="blog/all-posts.html"
    context_object_name='all_posts'
    ordering=['-date']


# def post_detail(request,slug):
#     # identified_post=next(post for post in all_posts if post['slug']==slug)
#     try:
#         identified_post=Post.objects.get(slug=slug)
#     except:
#         raise Http404('No such blog')
    
#     return render(request,"blog/post-detail.html",{
#         "post":identified_post,
#         "post_tags":identified_post.tags.all()
#     })


######## This was used when post detail had to handle only get request##########

# class PostDetail(DetailView):
#     model = Post
#     template_name="blog/post-detail.html"
#     # context_object_name="post"

#     def get_context_data(self, **kwargs):
#         context= super().get_context_data(**kwargs)
#         context["post_tags"]=self.object.tags.all()
#         context["comment_form"]=CommentForm()
        
#         return context


######### Now we need to handle get and post request both when we added the comment section ##########

class PostDetail(View):

    def is_stored_post(self,request,post_id):
        stored_posts=request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later=False

        return is_saved_for_later


    def get(self,request,slug):
        post=Post.objects.get(slug=slug)

        # stored_posts=request.session.get("stored-posts")
        # if stored_posts is not None:
        #     is_saved_for_later = post.id in stored_posts
        # else:
        #     is_saved_for_later=False

        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
            # "saved_for_later":is_saved_for_later
            "saved_for_later":self.is_stored_post(request,post.id)
        }

        return render(request,"blog/post-detail.html",context)
    

    def post(self,request,slug):
        comment_form=CommentForm(request.POST)
        post=Post.objects.get(slug=slug)

        if comment_form.is_valid():
            #Before the data is saved in the database we as a developer need to provide the correct post to which this comment is linked (as we excluded post field in our model )
            comment=comment_form.save(commit=False)
            #commit=False will not directly save comment_form in database but instead create a new model instance
            comment.post=post
            comment.save()

            return HttpResponseRedirect(reverse("posts_detail_page",args=[slug]))
        
        context={
            "post":post,
            "post_tags":post.tags.all(),
            #This time the comment form from the user enetered data
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id"),
            "saved_for_later":self.is_stored_post(request,post.id)

        }

        return render(request,"blog/post-detail.html",context)
    


class ReadLaterView(View):

    def get(self,request):
        stored_posts=request.session.get("stored_posts")
        context={}
        if stored_posts is None or len(stored_posts)==0:
            context["posts"]=[]
            context["has_posts"]=False

        else:
            post=Post.objects.filter(id__in=stored_posts)
            context["posts"]=post
            context["has_posts"]=True

        return render(request,"blog/stored-posts.html",context)

    def post(self,request):
        stored_posts=request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts=[]

        post_id=int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)

        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"]=stored_posts
        return HttpResponseRedirect('/')
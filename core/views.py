from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView
from .models import Post,Category,Comment,CommentVote,APIKey
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch,Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from .forms import SearchForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView




class SwaggerView(LoginRequiredMixin,SpectacularSwaggerView):

	template_name = 'core/swagger_ui.html'
	login_url = '/signin/'
	redirect_field_name = 'next'



# @method_decorator(cache_page(60 * 15),name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'core/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 8

    def get_queryset(self):
        queryset = Post.objects.select_related('author')
        self.form = SearchForm(self.request.GET or None)
        self.query = ""

        if self.form.is_valid():
            self.query = self.form.cleaned_data.get('search') or ""
            if self.query:
                queryset = queryset.filter(
                    Q(title__icontains=self.query) |
                    Q(content__icontains=self.query) |
                    Q(author__username__icontains=self.query)
                )
        self.full_queryset = queryset        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context["query"] = self.query
        context['queryset'] = self.full_queryset
        
        #Separate query for featured
        featured_post = self.full_queryset.filter(is_featured=True).first()

        if featured_post:
        	context['posts'] = [post for post in context['posts'] if post.pk != featured_post.pk]
        
        context['featured_post'] = featured_post

        context["results_count"] = len(context['posts']) + (1 if featured_post else 0)
        return context




class AllUsersPostListView(PermissionRequiredMixin,PostListView):
	template_name='userprofiles/posts_related/all_users_post_list.html'
	paginate_by = None
	permission_required = 'core.can_delete_post'
	raise_exception = True

# @method_decorator(cache_page(60 * 15), name='dispatch')
class PostDetailView(DetailView):
	model = Post
	template_name = 'core/post_detail.html'
	context_object_name = 'post'

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		post = self.object
		context['categories'] = post.categories.all()

		comments = (
			post.comments
			.filter(parent__isnull=True)
			.select_related('user')
			.prefetch_related(

				Prefetch(

					"replies",
					queryset=Comment.objects.select_related("user").all()
                    )
				)
			.order_by('-created_at')
			)


		context["comments"] = comments

		return context


	def post(self,request, *args,**kwargs):
		self.object = self.get_object() #get current post


		content = request.POST.get('content')

		if request.user.is_authenticated:


		   if content and content.strip():
			    Comment.objects.create(
				post=self.object,
				user=request.user,
				content=content
				)
			    messages.success(request,"Comment posted successfully")
		   else:
		   	messages.error(request,"Comment cannot be empty")

		else:
			messages.error(request,"You have to sign in to comment")
			return redirect('signin')

		return redirect('post-detail',slug=self.object.slug)

# fetching all posts from a single user

def single_user_posts(request,username):
	author = get_object_or_404(User,username=username)
	posts = Post.objects.published().filter(author=author).order_by('-published_date')
	return render(request,'core/single_user_posts.html',
		{'posts':posts,
		'author':author,
		}
		)

def display_tags(request):
	tags = Category.objects.all()
	return render(request,'core/post_detail.html',{'tags':tags})



#---------------------------Comment Section----------------------------------------
#Edit Comment

@login_required
def edit_comment(request,slug,comment_pk):
	post = get_object_or_404(Post,slug=slug)
	comment = get_object_or_404(Comment,post=post,pk=comment_pk)

	#only author of the comment can edit it
	if comment.user != request.user:
		messages.error(request,"You are not allowed to edit this comment.")
		return redirect('post-detail',slug=post.slug)

	if request.method == 'POST':
		new_content = request.POST.get('content')

		if new_content and new_content.strip():
			comment.content = new_content.strip()
			comment.save()
			return redirect('post-detail',slug=post.slug)
		else:
			messages.error(request,"Comment cannot be empty.")

	return render(request,'core/edit_comment.html',{'comment':comment,'post':post})

# Delete Comment
@login_required
def delete_comment(request,slug,comment_pk):
	post = get_object_or_404(Post,slug=slug)
	comment = get_object_or_404(Comment,post=post,pk=comment_pk)

	#only author of the comment can delete it

	if comment.user != request.user:
		messages.error(request,"You are not allowed to delete this comment")
		return redirect('post-detail',slug=post.slug)

	if request.method == 'POST':
		comment.delete()
		messages.success(request,"Comment successfully deleted.")
		return redirect('post-detail',slug=post.slug)

	else:
		messages.error(request,"Invalid request method to delete a comment.")

	return redirect('post-detail',slug=post.slug)

# Reply to a Comment
@login_required
def reply_comment(request,slug,comment_pk):
	post = get_object_or_404(Post, slug=slug)
	parent_comment = get_object_or_404(Comment,pk=comment_pk,post=post)

	if request.method == 'POST':
		content = request.POST.get('content')
		if content and content.strip():
			Comment.objects.create(
				post=post,
				user=request.user,
				content=content.strip(),
				parent=parent_comment)

			messages.success(request,"comment posted successfully")
			return redirect('post-detail',slug=post.slug)
		else:
			messages.error(request,"reply cannot be empty")


	# return render(request,'core/reply_comment.html',{'post':post,'parent_comment':parent_comment})
	return redirect('post-detail',slug=post.slug)

# Liking/Disliking Comment

from django.http import JsonResponse

class CommentVoteView(LoginRequiredMixin, View):
    def post(self, request, slug, comment_pk, value):
        comment = get_object_or_404(Comment, id=comment_pk, post__slug=slug)

        vote, created = CommentVote.objects.get_or_create(
            user=request.user,
            comment=comment,
            defaults={"value": value},
        )

        if not created:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "like_count": comment.like_count,
                "dislike_count": comment.dislike_count,
            })

        return redirect("post-detail", slug=slug)










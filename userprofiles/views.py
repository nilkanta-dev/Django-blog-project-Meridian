from django.shortcuts import render, redirect,get_object_or_404
from .forms import SignUpForm, SignInForm
from django.contrib.auth import login,logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib import messages
from core.models import Profile,Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from core.models import APIKey



@login_required
def api_keys(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        APIKey.objects.create(user=request.user,name=name)
        return redirect('api_keys')

    keys = APIKey.objects.filter(user = request.user)
    return render(request,'userprofiles/api_keys.html',{'keys':keys})


@login_required
def publish_post(request,slug):
    post = get_object_or_404(Post,slug=slug)

    if request.method == 'POST':
        post.is_published = True
        post.save()

        return redirect('post-detail',slug=post.slug)

    return redirect('post-detail',slug=post.slug)





@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title, allow_unicode=True)
            if post.is_published:
                post.published_date = timezone.now()
            post.save()
            messages.success(request,"Post created")
            return redirect('dashboard')  # Redirect to dashboard or another page
    else:
        form = PostForm()
    return render(request, 'userprofiles/posts_related/create_post.html', {'form': form})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,"You have successfully Registered! You can log in now.")
            Profile.objects.create(user=user,avatar='avatars/default.png')
            return redirect("signin")
        
        

    else:
        form = SignUpForm()

    

    return render(request, "userprofiles/signup.html", {"form": form})

class UserLoginView(LoginView):
    template_name = 'userprofiles/signin.html'
    authentication_form = SignInForm



class DashboardView(LoginRequiredMixin,TemplateView):

    template_name = 'userprofiles/dashboard_home.html'

    def get_context_data(self,**kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context["recent_posts"] = user.posts.all()[:5] 
        return context

@login_required
def profile_view(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.profile.bio = request.POST.get("bio")

        #Handle avatar

        if "avatar" in request.FILES:
            user.profile.avatar = request.FILES["avatar"]

        user.save()
        user.profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("dashboard")

    return render(request, "userprofiles/user_profile.html")


@login_required
def edit_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)

    #Ensure only the author of the post can edit it

    if post.author != request.user:
        messages.error(request,"You are not allowed to edit this post.")
        return redirect('post-detail',post_id=post.id)

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Post Updated!")
            return redirect('dashboard')

    else:
        form = PostForm(instance=post)

    return render(request,'userprofiles/posts_related/edit_post.html',{'form':form,'post':post})

@login_required

def users_list(request):
    users = User.objects.all()

    return render(request,'userprofiles/users_list.html',{'users':users})

@login_required

def view_user_profile(request,pk):
    user_profile = get_object_or_404(User,pk=pk)

    return render(request,'userprofiles/view_user_profile.html',{'user_profile':user_profile})

#Deleting User
#User must be a superuser to delete users

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@login_required
@superuser_required
def delete_user(request,pk):
    user_to_delete = get_object_or_404(User,pk=pk)

    if request.user == user_to_delete:
        messages.error(request,"You cannot delete your own account when logged in.")
        return redirect('users_list')

    username = user_to_delete.username #save for success message
    user_to_delete.delete()
    messages.success(request,f"User {username} was deleted successfully.")
    return redirect('users_list')


@login_required
def delete_post(request,post_id):
    post_to_delete = get_object_or_404(Post,id=post_id)
    post_to_delete.delete()
    messages.success(request,"Post successfully deleted.")
    return redirect('dashboard')



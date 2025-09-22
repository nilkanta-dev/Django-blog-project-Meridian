from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
from django_bleach.models import BleachField
from datetime import timedelta
from django.db.models import Q


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	bio = models.TextField(blank=True)
	avatar = models.ImageField(upload_to="avatars/", blank=True,null=True)
	phone_number = models.CharField(max_length=20,blank=True,null=True)


	def __str__(self):
		return f"{self.user.username}'s profile"


class PostManager(models.Manager):

	def published(self):
		return self.filter(is_published=True)

	def draft(self):
		return self.filter(is_published=False)

	def recent(self):
		last_30_days = timezone.now() - timedelta(days=30)
		return self.filter(created_at__gte=last_30_days)



class Post(models.Model):
	title = models.CharField(max_length=200)
	# content = HTMLField()
	content = BleachField()
	image = models.ImageField(upload_to="posts_images/",blank=True,null=True)
	published_date = models.DateTimeField(blank=True,null=True)
	is_featured = models.BooleanField(default=False)
	is_published = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posts')
	slug = models.SlugField(max_length=200,blank=True,null=True,unique=True)

	objects = PostManager()


	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug = slugify(self.title)

		if self.is_published and not self.published_date:
			self.published_date = timezone.now()

		super().save(*args,**kwargs)

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'slug':self.slug})


	class Meta:
		permissions = [('can_delete_post',"Can delete post")]

		constraints = [

		 models.UniqueConstraint(
		 	fields = ['is_featured'],
		 	condition = Q(is_featured=True),
		 	name = 'unique_featured_post')
           ]

	def __str__(self):
		return self.title


class Category(models.Model):
	name = models.CharField(max_length=100,unique=True)
	posts =models.ManyToManyField(Post, related_name='categories')

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.name


class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	content = models.TextField()
	parent = models.ForeignKey('self',null=True,blank=True,related_name='replies',on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.user} - {self.content[:20]}"

	@property
	def like_count(self):
		return self.votes.filter(value=1).count()

	@property
	def dislike_count(self):
		return self.votes.filter(value=-1).count()	

COMMENT_VOTES = [(1,"Like"),(-1,"Dislike")]

class CommentVote(models.Model):
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="votes")
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	value = models.SmallIntegerField(choices=COMMENT_VOTES)

	class Meta:
		unique_together = ("comment","user")
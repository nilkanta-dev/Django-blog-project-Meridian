from rest_framework import serializers
from core.models import Post, Comment,Profile
from django.contrib.auth.models import User



class UserSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = User
		fields = [

		'id',
		'username',
		'url',
		'email'
		]
		read_only_fields = ['id']
		extra_kwargs = {'url':{'view_name':'user-detail','lookup_field':'pk'}}


class ProfileSerializer(serializers.ModelSerializer):

	user = UserSerializer()

	class Meta:
		model = Profile

		fields = [

		'id',
		'user',
		'bio',
		'avatar',
		'phone_number'

		]


class CommentSerializer(serializers.ModelSerializer):
	user = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Comment
		fields = [
		'id',
		'post',
		'user',
		'content',
		'parent',
		'created_at',
		'like_count',
		'dislike_count'
		]

		read_only_fields = [
		'id',
		'user',
		'created_at',
		'like_count',
		'dislike_count'
		]



class PostSerializer(serializers.ModelSerializer):
	author = serializers.StringRelatedField(read_only=True)
	comments = CommentSerializer(many=True,read_only=True)
	post_url = serializers.HyperlinkedIdentityField(view_name='post-detail', lookup_field='pk')
	title = serializers.CharField()

	class Meta:
		model = Post
		fields = [
		'id',
		'title',
		'post_url',
		'slug',
		'content',
		'image',
		'published_date',
		'is_featured',
		'is_published',
		'created_at',
		'updated_at',
		'author',
		'comments'


		]

		read_only_fields = [
		'id',
		'slug',
		'author',
		'created_at',
		'updated_at',
		'published_date'
		
		]





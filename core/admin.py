from django.contrib import admin
from core.models import Profile,Post,Comment,Category
from userprofiles.forms import PostForm

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ['title', 'author', 'published_date', 'slug']  # Optional: Customize list view
    list_filter = ['published_date', 'author']  # Optional: Add filters
    search_fields = ['title', 'content']  # Optional: Enable search
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate slug from title


# Register your models here.

admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Category)







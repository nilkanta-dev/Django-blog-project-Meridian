from rest_framework.routers import DefaultRouter
from core.api.views import PostViewSet, CommentViewSet,UserViewSet,ProfileViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('comments', CommentViewSet, basename='comment')
router.register('users',UserViewSet,basename='user')
router.register('profiles',ProfileViewSet,basename='profile')

urlpatterns = router.urls

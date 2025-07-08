from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from raterapi.views import UploadedImageViewSet
from raterapi.views import login_user, register_user, GamesView, CategoriesView, RatingsView, ReviewsViewSet



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'uploads', UploadedImageViewSet , 'upload')
router.register(r'games', GamesView, 'game')
router.register(r'categories', CategoriesView, 'category')
router.register(r'ratings', RatingsView, 'rating')
router.register(r'reviews', ReviewsViewSet, 'review')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]


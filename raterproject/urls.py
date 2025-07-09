from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from rest_framework import routers
from raterapi.views import login_user, register_user, GamesView, CategoriesView, RatingsView, ReviewsViewSet
from raterapi.views.current_user_view import current_user_view


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GamesView, 'game')
router.register(r'categories', CategoriesView, 'category')
router.register(r'ratings', RatingsView, 'rating')
router.register(r'reviews', ReviewsViewSet, 'review')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('me', current_user_view),  # ✅ Add /me route here
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


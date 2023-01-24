from django.conf.urls.static import static
from django.conf.urls import url, include
from django.urls import path
from . import views
from taskmanager import settings
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('admin/', views.admin, name='admin'),
    path('create/', views.create.as_view(), name='create'),
    url('', include('social_django.urls', namespace='social')),
    path('auth/', views.auth, name='auth'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
router.register(r'api', views.VueApi, basename='api')
router.register(r'TaskSubTask/api', views.SubTaskTaskView, basename='TaskSubTask')
urlpatterns += router.urls




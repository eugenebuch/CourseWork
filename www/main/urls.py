from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('',views.home, name='home'),
    path('auth/', views.auth, name='auth'),
    path('exit/', views.exit, name='exit'),
    path('achiev/', views.achiev, name='achiev'),
    path('manage/', views.manage, name='manage')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
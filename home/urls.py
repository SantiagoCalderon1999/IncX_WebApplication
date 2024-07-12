from django.urls import path
from . import views

urlpatterns = [
    path('', views.video_stream, name='home'),
    path('process_frame/', views.process_frame, name='process_frame'),
]

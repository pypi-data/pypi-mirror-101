from django.urls import path

from . import views

app_name = "stats"
urlpatterns = [
    path('user-tracking-dashboard/', views.TrackingDashboard.as_view(), name='user-tracking-dashboard'),
]

from django.urls import path
from .import views

urlpatterns = [
    path("redis-test/", views.RedisTestView.as_view()),
    path("health/",views.HealthCheck.as_view()),
    path("admin-test/",views.AdminView.as_view()),
    path("healthview/",views.HealthView.as_view()),
    path("backend1/", views.Backend1View.as_view()),
    path("backend2/", views.Backend2View.as_view()),
    path("backend3/", views.Backend3View.as_view()),
    path("gateway/", views.GatewayView.as_view()),
    path("metrics/", views.MetricsView.as_view()),
]
from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'registration-rules', views.RegistrationRuleViewSet, basename='registrationrule')
router.register(r'pax-movements', views.PaxMovementViewSet, basename='paxmovement')

app_name = "universal"

urlpatterns = [
    path("register", views.UniversalRegisterView.as_view(), name="register"),
    path("list", views.UniversalListView.as_view(), name="list"),
    path("<str:id>", views.UniversalDetailView.as_view(), name="detail"),
    path("update/<str:id>", views.UniversalUpdateView.as_view(), name="update"),
    path("delete/<str:id>", views.UniversalDeleteView.as_view(), name="delete"),
]

# Add router URLs
urlpatterns += router.urls

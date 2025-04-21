from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import include, path
from django.views.generic.edit import UpdateView

urlpatterns = [
    path("", include("account_management.urls")),
    path(
        "profile/<pk>/",
        UpdateView.as_view(model=get_user_model(), fields=["username", "first_name", "last_name"]),
        name="profile-edit",
    ),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
] + debug_toolbar_urls()

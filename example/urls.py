from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("layout/", views.StandardLayout.as_view(), name="standard"),
    path("sidebars/hide-secondary/", views.SecondarySidebarEmpty.as_view(), name="secondary_empty"),
    path("sidebars/hide-primary/", views.PrimarySidebarEmpty.as_view(), name="primary_empty"),
    path("sidebars/remove-secondary/", views.SecondarySidebarRemoved.as_view(), name="secondary_removed"),
    path("sidebars/remove-primary/", views.PrimarySidebarRemoved.as_view(), name="primary_removed"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
